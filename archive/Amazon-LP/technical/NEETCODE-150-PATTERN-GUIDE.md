# NeetCode 150: Pattern-Based Study Guide

## The Goal

Do not memorize 150 exact solutions. Learn to look at a new problem and quickly recognize its underlying family:

> “This smells like sliding window.”  
> “This is a graph dependency problem.”  
> “The constraints suggest binary search on the answer.”  
> “This is backtracking with pruning.”

NeetCode organizes its 150 problems into 18 topic buckets. For interview recognition, those buckets can be compressed into **8 mental patterns**.

---

## 1. Scan + Remember Something

Use this when scanning an array or string and needing information about what came before: frequencies, duplicates, complements, prefix information, counts, or earliest occurrences.

### Think of

- Hash map
- Hash set
- Frequency array
- Prefix sum

### Recognition signals

- Duplicate, frequency, pair, complement
- Seen before, anagram, unique, count
- Subarray sum, consecutive values

### NeetCode examples

- Contains Duplicate
- Valid Anagram
- Two Sum
- Group Anagrams
- Top K Frequent Elements
- Longest Consecutive Sequence
- Product of Array Except Self

### Recognition example: Two Sum

If `current + x = target`, then `x = target - current`. The real question is:

> Have I already seen `target - current`?

That makes it a hash-map problem.

```python
seen = {}

for x in nums:
    if condition_using_seen:
        return answer
    seen[x] = ...
```

Amazon may replace integers with products, employees, servers, transactions, or timestamps. The story changes; the pattern does not.

---

## 2. Maintain a Moving Range

This family includes two pointers, sliding windows, monotonic stacks, and monotonic deques. The shared idea is:

> Can I process an ordered sequence once while maintaining only the useful candidates?

### 2A. Two pointers

Use two pointers when one side can move according to whether the current result is too small, too large, or invalid. Sorting often creates the needed monotonic behavior.

Examples:

- Two Sum II
- 3Sum
- Container With Most Water
- Valid Palindrome

If a sorted pair sum is below the target, move `left` rightward; moving `right` inward would only make the sum smaller.

### 2B. Sliding window

Strongest signal:

> **Contiguous subarray/substring + longest or shortest + a constraint**

Examples:

- Longest Substring Without Repeating Characters
- Longest Repeating Character Replacement
- Permutation in String
- Minimum Window Substring
- Best Time to Buy and Sell Stock-style scans

```python
left = 0

for right in range(len(nums)):
    # Add nums[right].

    while window_is_invalid:
        # Remove nums[left].
        left += 1

    answer = max(answer, right - left + 1)
```

### 2C. Monotonic stack or deque

Use one when you need:

- The nearest next greater or smaller element
- A maximum or minimum while elements enter and expire
- A collection of unresolved earlier candidates

Examples:

- Daily Temperatures
- Largest Rectangle in Histogram
- Car Fleet
- Sliding Window Maximum

In Daily Temperatures, the stack holds days still waiting for a warmer temperature. The current day resolves earlier days.

---

## 3. Exploit Sorted or Monotonic Behavior

This is the binary-search family.

### Type A: Search for a value

Examples:

- Binary Search
- Search in Rotated Sorted Array
- Find Minimum in Rotated Sorted Array

Ask:

> Which half can I safely eliminate?

### Type B: Binary search on the answer

This is especially important in interviews. You search a range of possible answers, not the input itself.

Examples:

- Koko Eating Bananas
- Minimum speed, capacity, rate, or time variants

For a candidate answer, define a feasibility check:

```python
can_do_it(candidate)
```

If feasibility changes monotonically, such as:

```text
False False False True True True
```

binary search can locate the first feasible value.

### Recognition signals

- Minimum speed or capacity
- Smallest maximum
- Maximum minimum
- Minimum feasible value

Ask:

> If I guess the answer, can I quickly check whether it works—and is that feasibility monotonic?

If both answers are yes, strongly consider binary search on the answer.

---

## 4. Traverse Connected Things

This family includes DFS, BFS, trees, graphs, grids, dependencies, shortest paths, and connectivity.

Core question:

> Can I model the objects as nodes and their relationships as edges?

### Type A: Connected components

Examples:

- Number of Islands
- Max Area of Island
- Surrounded Regions

```python
for every_node_or_cell:
    if unvisited:
        component_count += 1
        dfs(...)
```

### Type B: Shortest path in an unweighted graph

Use BFS when every edge has equal cost. BFS explores distance `0`, then `1`, then `2`, and so on.

Examples:

- Rotting Oranges
- Islands and Treasure
- Word Ladder-style problems

### Type C: Multiple starting points

Use multi-source BFS when many sources spread simultaneously.

Examples:

- Rotting Oranges
- Islands and Treasure

Instead of making every empty cell search for its nearest treasure, let all treasures expand together. Reversing the direction often removes repeated work.

### Type D: Dependencies and cycles

Think directed graph plus either:

- DFS states `0, 1, 2`
- Topological sort / Kahn's algorithm

```text
0 = unvisited
1 = currently visiting
2 = completely processed
```

Reaching state `1` again means the current DFS path contains a cycle.

Examples:

- Course Schedule
- Course Schedule II
- Alien Dictionary-style dependency problems

### Type E: Weighted graphs

Ordinary BFS is no longer enough when edge costs differ. Consider:

- Dijkstra for nonnegative shortest paths
- Prim or Kruskal for minimum spanning trees
- Union-Find for dynamic connectivity and cycle detection

---

## 5. Make Choices, Undo Them, Try Again

This is backtracking. Use it when the problem asks for all possible valid constructions.

### Recognition signals

- All combinations, permutations, subsets, or arrangements
- Construct every valid string
- Choose `k` items
- Find a path through a board with branching choices

Examples:

- Subsets
- Permutations
- Combination Sum
- Generate Parentheses
- Word Search
- N-Queens-style problems

Core pattern:

```text
choose -> explore -> undo
```

```python
def backtrack(...):
    if valid_answer:
        result.append(...)

    for choice in choices:
        path.append(choice)   # Choose
        backtrack(...)        # Explore
        path.pop()            # Undo
```

The improvement over raw brute force is usually **pruning**. Generate Parentheses should place `)` only when `close < open`, rather than generating every string and validating afterward.

Ask:

> At each position, do I have several choices, after which I can recursively solve the remainder?

---

## 6. The Same Problem Keeps Appearing Again

This is dynamic programming. Start with recursion, then notice that identical states are being solved repeatedly.

### Type A: One-variable state

Examples:

- Climbing Stairs
- House Robber
- Decode Ways
- Coin Change

`dp[i]` often means the best answer using the first `i` elements or the answer starting at index `i`.

For House Robber:

```text
dp[i] = max(dp[i - 1], nums[i] + dp[i - 2])
```

### Type B: Two-variable state

Examples:

- Longest Common Subsequence
- Edit Distance
- Unique Paths
- Interleaving String

`dp[i][j]` usually represents an answer involving position `i` in one object and position `j` in another.

### Type C: Decision DP

The transition asks “take or skip?”

Examples include 0/1 knapsack, partition, subset sum, and House Robber.

### Type D: Unlimited-choice DP

The same choice can be used repeatedly, as in Coin Change.

### Best DP recognition question

Do not ask only, “Is this DP?” Ask:

> If I solve this recursively, which parameters uniquely describe the remaining problem?

Those parameters form the DP state.

---

## 7. Always Keep the Best Available Choice

This family combines heaps, greedy algorithms, intervals, and scheduling.

### Heap signal

Use a heap when candidates change and you repeatedly need the:

- Smallest or largest
- Top `k`
- Next best
- Most frequent
- Earliest ending
- Running median

Examples:

- Kth Largest Element
- Top K Frequent Elements
- Find Median from Data Stream
- Task Scheduler
- Merge K Sorted Lists

### Greedy signal

Ask:

> Can I make the best local choice and prove I will never need to undo it?

Examples:

- Jump Game
- Jump Game II
- Gas Station
- Maximum Subarray / Kadane's algorithm
- Partition Labels

Jump Game does not need the exact history—only the farthest reachable index. That is compressed state.

### Interval signal

When input consists of `[start, end]`, first consider sorting. Then ask:

- Do these overlap?
- Which interval ends first?
- Which interval starts next?

Examples:

- Merge Intervals
- Insert Interval
- Non-overlapping Intervals
- Meeting Rooms
- Minimum Interval to Include Each Query

To maximize the number of non-overlapping intervals, preferring the interval that ends earliest leaves the most room for the future.

---

## 8. Maintain a Data-Structure Invariant

Some questions test whether you can preserve the rules of a structure while manipulating it.

### Linked lists

Core tools:

- Dummy node
- Slow and fast pointers
- `prev`, `current`, and `next`
- Reverse, split, merge, and reconnect operations

Examples:

- Reverse Linked List
- Linked List Cycle
- Reorder List
- Remove Nth Node From End
- Merge K Sorted Lists
- LRU Cache

### Stack parsers

Use a stack when unfinished information from earlier must be restored later.

Examples:

- Valid Parentheses
- Decode String
- Evaluate Reverse Polish Notation

In `3[a2[c]]`, `[` saves the earlier context; `]` completes the current level and returns to that context.

### Tries

Use a trie when the problem is fundamentally about prefixes and shared character paths.

Examples:

- Implement Trie
- Design Add and Search Words
- Word Search II

### Bit manipulation

Consider bit operations when constraints mention:

- Fixed integer ranges
- Every number appears twice except one
- Counting bits
- Powers of two
- No extra memory
- XOR relationships

Key identities:

```text
x ^ x = 0
x ^ 0 = x
```

Therefore XOR-ing `[4, 1, 2, 1, 2]` leaves `4`.

---

## Mapping the 18 NeetCode Buckets to 8 Mental Patterns

| Official NeetCode bucket | Mental pattern |
|---|---|
| Arrays & Hashing | Scan + remember |
| Two Pointers | Maintain a moving range |
| Sliding Window | Maintain a moving range |
| Stack | Moving range / structure invariant |
| Binary Search | Exploit monotonicity |
| Linked List | Structure invariant |
| Trees | Traverse connected things |
| Heap / Priority Queue | Best available choice |
| Backtracking | Choose, explore, undo |
| Tries | Structure invariant / DFS |
| Graphs | Traverse connected things |
| Advanced Graphs | Traverse connected things |
| 1D DP | Repeated subproblems |
| 2D DP | Repeated subproblems |
| Greedy | Best local choice |
| Intervals | Sort + best choice |
| Math & Geometry | Specialized math/invariant |
| Bit Manipulation | Specialized invariant |

---

## Amazon Interview Recognition Checklist

Before coding, ask these questions in order.

1. **Is it a contiguous subarray or substring?**  
   Test sliding window, prefix sum, or Kadane.

2. **Is the data sorted, or is feasibility monotonic?**  
   Test two pointers, binary search, or binary search on the answer.

3. **Are there connections, dependencies, neighbors, grids, or trees?**  
   Test DFS, BFS, multi-source BFS, topological sort, Union-Find, or Dijkstra.

4. **Does it ask for all possible combinations or arrangements?**  
   Test backtracking.

5. **Does recursion repeatedly solve the same state?**  
   Test dynamic programming.

6. **Do I repeatedly need the smallest, largest, top `k`, or next-best candidate?**  
   Test a heap.

7. **Do I need only compressed information from the past?**  
   Test greedy—for example, farthest position, current maximum, or earliest ending interval.

8. **Do I need frequency, lookup, “seen before,” or a complement?**  
   Test a hash map or hash set.

This checklist identifies the solution family for a large fraction of interview questions.

---

## Let the Constraints Guide You

| Input size | Algorithms that may be acceptable |
|---:|---|
| `N <= 20` | Exponential search such as `O(2^N)` or backtracking may be fine |
| `N <= 1,000` | `O(N^2)` may be acceptable |
| `N <= 100,000` | Usually aim for `O(N)` or `O(N log N)` |
| `N <= 1,000,000` | Usually aim for close to `O(N)` |

At `N = 100,000`, be suspicious of nested loops. Think about hashing, sorting, sliding windows, binary search, heaps, or linear graph traversal.

Constraints are often an indirect hint to the intended pattern.

---

## Eight High-Value Transformation Tricks

### 1. Brute-force every pair -> hash map

Example: Two Sum.

### 2. Recalculate every range -> sliding window

Examples: Permutation in String and Longest Repeating Character Replacement.

### 3. Search separately from every target -> reverse the search

Examples: Islands and Treasure and Pacific Atlantic Water Flow.

Instead of every cell searching for an ocean or treasure, start from all destinations and find what they can reach.

### 4. Try every possible answer -> binary-search the answer

Example: Koko Eating Bananas.

### 5. Generate everything, then validate -> prune during generation

Example: Generate Parentheses.

### 6. Recursive brute force -> memoize the state

Examples: Coin Change, Decode Ways, and House Robber.

### 7. Repeatedly scan the future -> maintain unresolved candidates

Example: Daily Temperatures with a monotonic stack.

### 8. Repeatedly search for a minimum or maximum -> heap

Examples: Kth Largest Element, Task Scheduler, and Merge K Sorted Lists.

---

## The Whole Cheat Sheet in Eight Lines

```text
1. Remember something
2. Maintain a range
3. Exploit ordering
4. Traverse connections
5. Explore choices
6. Reuse previous answers
7. Pick the best available option
8. Manipulate a structure
```

The data structures are implementation tools:

| Tool | What it helps you do |
|---|---|
| Hash map | Remember and look up |
| Two pointers | Maintain a range |
| Stack | Preserve unresolved earlier state |
| Queue | Run BFS |
| Heap | Retrieve the best candidate |
| DFS | Explore connections or choices |
| DP table | Reuse solved states |
| Linked list pointers | Restructure nodes |
| Trie | Represent shared prefixes |
| Union-Find | Maintain connectivity |

---

## Recommended Practice Grouping

Since you already know the problems reasonably well, stop reviewing only in NeetCode's category order. Mix related categories and practice by mental pattern.

### Session 1: Sliding window and moving range

- Longest Substring Without Repeating Characters
- Longest Repeating Character Replacement
- Permutation in String
- Minimum Window Substring
- Sliding Window Maximum

### Session 2: Graph traversal

- Number of Islands
- Max Area of Island
- Rotting Oranges
- Islands and Treasure
- Surrounded Regions
- Pacific Atlantic Water Flow
- Course Schedule

### Session 3: Greedy and compressed state

- Jump Game
- Jump Game II
- Gas Station
- Partition Labels
- Maximum Subarray

### Session 4: Hashing and scan-and-remember

- Two Sum
- Group Anagrams
- Top K Frequent Elements
- Longest Consecutive Sequence
- Product of Array Except Self

### Session 5: Binary search and monotonicity

- Binary Search
- Search in Rotated Sorted Array
- Find Minimum in Rotated Sorted Array
- Koko Eating Bananas
- Time Based Key-Value Store

### Session 6: Backtracking

- Subsets
- Permutations
- Combination Sum
- Generate Parentheses
- Word Search

### Session 7: Dynamic programming

- Climbing Stairs
- House Robber
- Coin Change
- Decode Ways
- Longest Common Subsequence
- Unique Paths

### Session 8: Heaps, intervals, and scheduling

- Kth Largest Element
- Find Median from Data Stream
- Task Scheduler
- Merge Intervals
- Non-overlapping Intervals
- Meeting Rooms

The purpose is to train one skill:

> **Recognize the family before recalling the exact solution.**

For Amazon preparation, emphasize hashing and arrays, sliding windows and two pointers, trees, graphs, heaps, greedy algorithms, and straightforward DP.

Your target should be to identify the likely pattern for an unseen variant in **30–60 seconds**, justify it from the problem's wording and constraints, and then customize the standard pattern to the exact requirements.

