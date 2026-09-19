#!/usr/bin/env python3
"""Validate deterministic resume-tailoring source invariants."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

REQUIRED_FILES = (
    "resume-system/governance/FACT_RULES.md",
    "resume-system/facts/work-experience.md",
    "resume-system/facts/per-project-keywords.md",
    "resume-system/reference/jd-red-flags.md",
)

LANES = {
    "full-stack": "resume-system/templates/variants/fullstack-engineer.tex",
    "backend": "resume-system/templates/variants/backend-engineer.tex",
    "ai-engineer": "resume-system/templates/variants/ai-engineer.tex",
}

REQUIRED_BANK_HEADINGS = (
    "Locked Resume Bullets — Full Stack",
    "Locked Resume Bullets — Backend",
    "Locked Resume Bullets — AI Engineer Supporting Experience",
)

# Maps the project name shown in a template's \resumeProjectHeading to its
# master file under resume-system/facts/projects. Kept explicit rather than
# auto-derived because
# names like "SEO Audit Engine" -> seo-audit-engine.md and "ClusterOps" ->
# ClusterOps.md do not share one clean transform; an unknown name must fail loud.
PROJECT_NAME_TO_MASTER = {
    "Hearloop": "hearloop.md",
    "SEO Audit Engine": "seo-audit-engine.md",
    "ClusterOps": "ClusterOps.md",
    "Distributed Caching System": "distributed-caching.md",
    "Video Compliance Pipeline": "youtube-ads-compliance-pipeline.md",
    "Fake Review Detector": "fake-review-detector.md",
}

BANNED_EINFOCHIPS_TEXT = (
    "Angular",
    r"\metric{40\%}",
    "May 2023",
    "Aug 2023",
    "Software Intern, eInfochips",
)

NONSELECTABLE_MARKER = (
    "**Selection status:** NOT SELECTABLE — no current locked resume bullet bank."
)

BANNED_ACTIVE_PROJECT_TEXT = (
    "reducing manual review effort",
    "reduces the manual effort",
    "live accounts",
    "improving retention",
    "new accounts each week",
    "customer traffic",
    "$420 saved",
    "under real load",
)


def role_section(text: str, marker: str) -> str:
    marker_at = text.find(marker)
    if marker_at < 0:
        raise ValueError(f"missing experience marker: {marker}")
    start = text.find(r"\resumeItemListStart", marker_at)
    end = text.find(r"\resumeItemListEnd", start)
    if start < 0 or end < 0:
        raise ValueError(f"malformed item list after: {marker}")
    return text[start:end]


def section_body(text: str, name: str) -> str:
    marker = rf"\section{{{name}}}"
    start = text.find(marker)
    if start < 0:
        raise ValueError(f"missing section: {name}")
    next_section = text.find(r"\section{", start + len(marker))
    return text[start : next_section if next_section >= 0 else len(text)]


def item_counts(text: str) -> list[int]:
    counts: list[int] = []
    cursor = 0
    while True:
        heading = text.find(r"\resumeProjectHeading", cursor)
        if heading < 0:
            return counts
        start = text.find(r"\resumeItemListStart", heading)
        end = text.find(r"\resumeItemListEnd", start)
        if start < 0 or end < 0:
            raise ValueError("malformed project item list")
        counts.append(text[start:end].count(r"\resumeItem{"))
        cursor = end + len(r"\resumeItemListEnd")


def resume_items(text: str) -> list[str]:
    items: list[str] = []
    marker = r"\resumeItem{"
    cursor = 0
    while True:
        start = text.find(marker, cursor)
        if start < 0:
            return items
        index = start + len(marker)
        depth = 1
        body_start = index
        while index < len(text) and depth:
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
            index += 1
        if depth:
            raise ValueError("unclosed resume item")
        items.append(text[body_start : index - 1])
        cursor = index


def strip_metric_commands(text: str) -> str:
    marker = r"\metric{"
    while True:
        start = text.find(marker)
        if start < 0:
            return text
        index = start + len(marker)
        body_start = index
        depth = 1
        while index < len(text) and depth:
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
            index += 1
        if depth:
            return text
        text = text[:start] + text[body_start : index - 1] + text[index:]


def normalized_prose(text: str) -> str:
    text = strip_metric_commands(text)
    return " ".join(
        text.replace(r"\&", "&")
        .replace(r"\%", "%")
        .replace("{,}", ",")
        .split()
    )


def markdown_h2_sections(text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    heading = ""
    body: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if heading:
                sections.append((heading, "\n".join(body)))
            heading = line[3:].strip()
            body = []
        elif heading:
            body.append(line)
    if heading:
        sections.append((heading, "\n".join(body)))
    return sections


def selectable_bullet_text(master: str) -> str:
    """Master text with superseded `### ` version subsections removed.

    Splits on `### ` headings and drops any block whose heading marks the
    version superseded, so a template bullet can only match against a bullet
    bank that is still selectable. Text before the first `### ` heading (tech
    stack, impact, etc.) is retained.
    """
    kept: list[str] = []
    heading = ""
    body: list[str] = []
    blocks: list[tuple[str, str]] = []
    for line in master.splitlines():
        if line.startswith("### "):
            blocks.append((heading, "\n".join(body)))
            heading = line[4:].strip()
            body = []
        else:
            body.append(line)
    blocks.append((heading, "\n".join(body)))
    for block_heading, block_body in blocks:
        if "superseded" in block_heading.casefold():
            continue
        kept.append(block_heading)
        kept.append(block_body)
    return normalized_prose("\n".join(kept))


def template_project_blocks(projects: str) -> list[tuple[str, list[str]]]:
    """Return (project name, bullets) per \\resumeProjectHeading in Projects.

    The name is read from the first \\textbf{...} of each heading; bullets are
    the \\resumeItem{...} entries in that heading's item list.
    """
    blocks: list[tuple[str, list[str]]] = []
    cursor = 0
    while True:
        heading = projects.find(r"\resumeProjectHeading", cursor)
        if heading < 0:
            return blocks
        name_marker = projects.find(r"\textbf{", heading)
        list_start = projects.find(r"\resumeItemListStart", heading)
        if name_marker < 0 or list_start < 0 or name_marker > list_start:
            raise ValueError("project heading missing name or item list")
        name_body = name_marker + len(r"\textbf{")
        depth = 1
        index = name_body
        while index < len(projects) and depth:
            if projects[index] == "{":
                depth += 1
            elif projects[index] == "}":
                depth -= 1
            index += 1
        if depth:
            raise ValueError("unclosed project name")
        name = projects[name_body : index - 1]
        list_end = projects.find(r"\resumeItemListEnd", list_start)
        if list_end < 0:
            raise ValueError("malformed project item list")
        bullets = resume_items(projects[list_start:list_end])
        blocks.append((name, bullets))
        cursor = list_end + len(r"\resumeItemListEnd")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.repo.resolve()
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    project_files = sorted((root / "resume-system/facts/projects").glob("*.md"))
    if not project_files:
        errors.append("no project master files found in resume-system/facts/projects")

    for path in project_files:
        content = path.read_text(encoding="utf-8")
        if "locked resume bullets" not in content.casefold() and NONSELECTABLE_MARKER not in content:
            errors.append(
                f"{path.relative_to(root)} has neither a locked bullet bank nor a "
                "NOT SELECTABLE boundary"
            )
        for heading, body in markdown_h2_sections(content):
            if "locked resume bullets" not in heading.casefold():
                continue
            current_versions = sum(
                1
                for line in body.splitlines()
                if line.startswith("### ") and "current" in line.casefold()
            )
            if current_versions > 1:
                errors.append(
                    f"{path.relative_to(root)} has {current_versions} current versions "
                    f"in locked lane: {heading}"
                )

    # Per-master selectable bullet text (superseded version blocks removed),
    # keyed by filename, so each template bullet is checked against its own
    # project's still-selectable bank rather than the whole corpus.
    # ponytail: matches per-project, not per-lane-within-project; a bullet from
    # the wrong lane of the *same* master would still pass. That is a far
    # narrower hole than matching against every master at once, and closes the
    # superseded-bullet and cross-project-leak gaps the audit named.
    selectable_by_master = {
        path.name: selectable_bullet_text(path.read_text(encoding="utf-8"))
        for path in project_files
    }

    work_experience = root / "resume-system/facts/work-experience.md"
    if work_experience.is_file():
        content = work_experience.read_text(encoding="utf-8")
        for heading in REQUIRED_BANK_HEADINGS:
            if heading not in content:
                errors.append(f"missing locked experience bank: {heading}")

    for lane, relative in LANES.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"missing {lane} template: {relative}")
            continue
        content = path.read_text(encoding="utf-8")
        if "Software Engineer, Digital Aid Seattle, Remote" not in content:
            errors.append(f"{lane} template has incorrect Digital Aid Seattle title")
        if "Data Management Intern, ASU, AZ" not in content:
            errors.append(f"{lane} template has incorrect ASU title")
        if "Academic Records Operations, ASU, AZ" in content:
            errors.append(f"{lane} template contains retired ASU title")
        title_at = content.find("Software Engineer Intern, eInfochips, India")
        date_at = content.find("Jan 2024 -- May 2024", title_at)
        if title_at < 0 or date_at < 0 or date_at - title_at > 200:
            errors.append(f"{lane} template has incorrect eInfochips title or dates")
        try:
            section = role_section(content, "eInfochips, India")
        except ValueError as exc:
            errors.append(f"{lane} template: {exc}")
            continue
        count = section.count(r"\resumeItem{")
        expected_einfochips = 2 if lane == "ai-engineer" else 3
        if count != expected_einfochips:
            errors.append(
                f"{lane} template has {count} eInfochips bullets; expected {expected_einfochips}"
            )
        for banned in BANNED_EINFOCHIPS_TEXT:
            if banned in section:
                errors.append(f"{lane} template contains retired eInfochips text: {banned}")

        try:
            projects = section_body(content, "Projects")
        except ValueError as exc:
            errors.append(f"{lane} template: {exc}")
            continue
        projects_folded = projects.casefold()
        for banned in BANNED_ACTIVE_PROJECT_TEXT:
            if banned.casefold() in projects_folded:
                errors.append(
                    f"{lane} template contains unsupported project outcome text: {banned}"
                )
        try:
            project_blocks = template_project_blocks(projects)
        except ValueError as exc:
            errors.append(f"{lane} template projects: {exc}")
            project_blocks = []
        for name, bullets in project_blocks:
            master_file = PROJECT_NAME_TO_MASTER.get(name)
            if master_file is None:
                errors.append(
                    f"{lane} template project '{name}' has no known master mapping"
                )
                continue
            selectable = selectable_by_master.get(master_file)
            if selectable is None:
                errors.append(
                    f"{lane} template project '{name}' maps to missing master {master_file}"
                )
                continue
            for number, bullet in enumerate(bullets, start=1):
                if normalized_prose(bullet) not in selectable:
                    errors.append(
                        f"{lane} template project '{name}' bullet {number} does not match a "
                        f"current locked bullet in {master_file}"
                    )

        if lane == "ai-engineer":
            try:
                das_count = role_section(content, "Digital Aid Seattle, Remote").count(r"\resumeItem{")
                asu_count = role_section(content, "Data Management Intern, ASU, AZ").count(r"\resumeItem{")
                counts = item_counts(projects)
            except ValueError as exc:
                errors.append(f"ai-engineer template: {exc}")
                continue
            if (das_count, asu_count, count) != (3, 2, 2):
                errors.append(
                    "ai-engineer experience counts are "
                    f"{das_count}/{asu_count}/{count}; expected 3/2/2"
                )
            if counts != [3, 2, 2, 2]:
                errors.append(
                    f"ai-engineer project bullet distribution is {counts}; expected [3, 2, 2, 2]"
                )
            project_at = content.find(r"\section{Projects}")
            experience_at = content.find(r"\section{Experience}")
            skills_at = content.find(r"\section{Technical Skills}")
            if not (0 <= project_at < experience_at < skills_at):
                errors.append(
                    "ai-engineer section order must be Projects, Experience, Technical Skills"
                )
        else:
            counts = item_counts(projects)
            if counts != [3, 3, 2]:
                errors.append(
                    f"{lane} project bullet distribution is {counts}; expected [3, 3, 2]"
                )

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: deterministic resume-tailoring sources satisfy preflight invariants")
    print(f"PASS: {len(project_files)} project master files available")
    for lane, relative in LANES.items():
        print(f"PASS: {lane} -> {relative}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
