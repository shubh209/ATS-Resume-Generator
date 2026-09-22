from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PREFLIGHT = Path(".agents/skills/resume-tailor/scripts/preflight.py")
FIXTURE_PATHS = (
    PREFLIGHT,
    Path(".agents/skills/resume-tailor/SKILL.md"),
    Path(".agents/skills/resume-tailor/references/tailoring-report-schema.md"),
    Path("resume-system/governance/auditor-prompt.md"),
    Path("resume-system/governance/FACT_RULES.md"),
    Path("resume-system/facts/work-experience.md"),
    Path("resume-system/facts/per-project-keywords.md"),
    Path("resume-system/facts/projects"),
    Path("resume-system/reference/jd-red-flags.md"),
    Path("resume-system/reference/hiring-reality.md"),
    Path("resume-system/reference/qualification-taxonomy.md"),
    Path("resume-system/templates/variants/fullstack-engineer.tex"),
    Path("resume-system/templates/variants/backend-engineer.tex"),
    Path("resume-system/templates/variants/ai-engineer.tex"),
)


class ResumePreflightTest(unittest.TestCase):
    def make_fixture(self) -> Path:
        fixture = Path(tempfile.mkdtemp(prefix="resume-preflight-"))
        self.addCleanup(shutil.rmtree, fixture)
        for relative in FIXTURE_PATHS:
            source = REPO / relative
            target = fixture / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, target, dirs_exist_ok=True)
            else:
                shutil.copy2(source, target)
        return fixture

    def run_preflight(self, fixture: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(fixture / PREFLIGHT), "--repo", str(fixture)],
            check=False,
            capture_output=True,
            text=True,
        )

    def assert_rejected(self, result: subprocess.CompletedProcess[str], reason: str) -> None:
        self.assertNotEqual(
            result.returncode,
            0,
            f"preflight accepted {reason}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_rejects_project_without_locked_bank_or_nonselectable_boundary(self) -> None:
        fixture = self.make_fixture()
        path = fixture / "resume-system/facts/projects/crypto-market-simulator.md"
        content = path.read_text(encoding="utf-8")
        content = content.replace(
            "**Selection status:** NOT SELECTABLE — no current locked resume bullet bank.",
            "",
        )
        path.write_text(content, encoding="utf-8")

        result = self.run_preflight(fixture)

        self.assert_rejected(result, "a project with neither a locked bank nor a nonselectable boundary")

    def test_rejects_two_current_versions_in_one_locked_lane(self) -> None:
        fixture = self.make_fixture()
        path = fixture / "resume-system/facts/projects/hearloop.md"
        content = path.read_text(encoding="utf-8")
        content = content.replace(
            "### Version 1 (superseded — discard; replaced by Version 2 after user confirmation)",
            "### Version 1 (current — use this)",
            1,
        )
        path.write_text(content, encoding="utf-8")

        result = self.run_preflight(fixture)

        self.assert_rejected(result, "two current versions in one locked lane")

    def test_rejects_stale_current_employment_title(self) -> None:
        fixture = self.make_fixture()
        path = fixture / "resume-system/templates/variants/fullstack-engineer.tex"
        content = path.read_text(encoding="utf-8").replace(
            "Data Management Intern, ASU, AZ",
            "Academic Records Operations, ASU, AZ",
        )
        path.write_text(content, encoding="utf-8")

        result = self.run_preflight(fixture)

        self.assert_rejected(result, "the retired ASU title in a live lane template")

    def test_rejects_unsupported_realized_side_project_outcome(self) -> None:
        fixture = self.make_fixture()
        path = fixture / "resume-system/templates/variants/ai-engineer.tex"
        content = path.read_text(encoding="utf-8").replace(
            r"\section{Projects}",
            "\\section{Projects}\n% reducing manual review effort for suspicious content",
            1,
        )
        path.write_text(content, encoding="utf-8")

        result = self.run_preflight(fixture)

        self.assert_rejected(result, "unsupported realized side-project impact in a live template")

    def test_rejects_live_project_bullet_that_drifted_from_locked_master(self) -> None:
        fixture = self.make_fixture()
        path = fixture / "resume-system/templates/variants/fullstack-engineer.tex"
        content = path.read_text(encoding="utf-8").replace(
            "one slow site could not block the remaining batch",
            "one slow site could not block the remaining client batch",
            1,
        )
        path.write_text(content, encoding="utf-8")

        result = self.run_preflight(fixture)

        self.assert_rejected(result, "a live project bullet whose wording drifted from its locked master")

    def test_rejects_missing_hiring_reality_reference(self) -> None:
        fixture = self.make_fixture()
        (fixture / "resume-system/reference/hiring-reality.md").unlink()
        result = self.run_preflight(fixture)
        self.assert_rejected(result, "a missing hiring-reality reference")

    def test_rejects_missing_qualification_profile(self) -> None:
        fixture = self.make_fixture()
        path = fixture / "resume-system/reference/qualification-taxonomy.md"
        content = path.read_text(encoding="utf-8").replace(
            "## Go / Node.js Engineer",
            "## Backend Profile Removed",
        )
        path.write_text(content, encoding="utf-8")
        result = self.run_preflight(fixture)
        self.assert_rejected(result, "a taxonomy missing the Go / Node.js profile")

    def test_rejects_skill_without_hiring_reality_read_set(self) -> None:
        fixture = self.make_fixture()
        path = fixture / ".agents/skills/resume-tailor/SKILL.md"
        content = path.read_text(encoding="utf-8").replace(
            "5. `resume-system/reference/hiring-reality.md`\n",
            "",
        )
        path.write_text(content, encoding="utf-8")
        result = self.run_preflight(fixture)
        self.assert_rejected(result, "a live skill missing hiring reality from its read set")

    def test_rejects_skill_without_report_opt_in_contract(self) -> None:
        fixture = self.make_fixture()
        path = fixture / ".agents/skills/resume-tailor/SKILL.md"
        content = path.read_text(encoding="utf-8").replace(
            "Do not produce a tailoring report unless the user explicitly requests one.",
            "Always produce a tailoring report.",
        )
        path.write_text(content, encoding="utf-8")
        result = self.run_preflight(fixture)
        self.assert_rejected(result, "a live skill without report opt-in")

    def test_rejects_report_schema_without_opt_in_boundary(self) -> None:
        fixture = self.make_fixture()
        path = fixture / ".agents/skills/resume-tailor/references/tailoring-report-schema.md"
        content = path.read_text(encoding="utf-8").replace(
            "Use this schema only when the user explicitly requests a tailoring report.",
            "Use this schema for every tailoring run.",
        )
        path.write_text(content, encoding="utf-8")
        result = self.run_preflight(fixture)
        self.assert_rejected(result, "a report schema without its opt-in boundary")

    def test_rejects_fixed_keyword_percentage_in_auditor(self) -> None:
        fixture = self.make_fixture()
        path = fixture / "resume-system/governance/auditor-prompt.md"
        content = path.read_text(encoding="utf-8").replace(
            "The three JD priorities must appear in the earliest available truthful evidence allowed by the lane's locked structure.",
            "<75% JD keywords likely in first half of page 1",
        )
        path.write_text(content, encoding="utf-8")
        result = self.run_preflight(fixture)
        self.assert_rejected(result, "the retired fixed placement percentage")

    def test_rejects_keyword_map_that_authorizes_facts(self) -> None:
        fixture = self.make_fixture()
        path = fixture / "resume-system/facts/per-project-keywords.md"
        content = path.read_text(encoding="utf-8").replace(
            "This file does not authorize facts, metrics, skills, project counts, or selection",
            "This file authorizes facts, metrics, skills, project counts, and selection",
        )
        path.write_text(content, encoding="utf-8")
        result = self.run_preflight(fixture)
        self.assert_rejected(result, "a keyword map claiming fact authority")


if __name__ == "__main__":
    unittest.main()
