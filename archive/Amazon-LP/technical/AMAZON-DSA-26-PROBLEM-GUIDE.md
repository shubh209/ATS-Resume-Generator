# Amazon DSA Interview Prep — 26 Problem Guide in C++

# Clickable Problem Index

| # | Problem | Type / Main Pattern |
|---:|---|---|
| 1 | [Currency Converter](#q01) | Graph — DFS/BFS + memoization |
| 2 | [All Downhill Paths in a Terrain](#q02) | Grid — DFS / backtracking |
| 3 | [Find Files by Name in a Directory](#q03) | Tree — DFS / indexing |
| 4 | [Server Load Assignment](#q04) | Heap — Min-heap / priority queue |
| 5 | [Streaming Top-K](#q05) | Heap — Min-heap of size K |
| 6 | [Customer Log Analysis / Loyal Customers](#q06) | Hashing — unordered_map + unordered_set |
| 7 | [Task Dependencies](#q07) | Graph — DFS/BFS |
| 8 | [Longest Chain of Cascading Task Delays](#q08) | Graph / DAG — Memoized DFS / DP |
| 9 | [Shuffle an Array In Place](#q09) | Array — Fisher-Yates |
| 10 | [Schedule Items Using Three Priority Attributes](#q10) | Heap — Custom comparator / priority queue |
| 11 | [Tree Path Sum Variation](#q11) | Tree — DFS |
| 12 | [Nodes at Distance K from Target](#q12) | Tree / Graph — BFS + parent mapping |
| 13 | [Number of Islands Variation](#q13) | Grid — DFS/BFS |
| 14 | [Rotting Oranges](#q14) | Grid — Multi-source BFS |
| 15 | [Course Schedule II](#q15) | Graph — Topological DFS + cycle detection |
| 16 | [Domino and Tromino Tiling](#q16) | Dynamic Programming — 1D DP |
| 17 | [Next Permutation](#q17) | Array — Pivot + successor + suffix reversal |
| 18 | [House Robber I](#q18) | Dynamic Programming — 1D DP |
| 19 | [House Robber II](#q19) | Dynamic Programming — Circular 1D DP |
| 20 | [Jump / Reachability Problem](#q20) | Array — Greedy reachability |
| 21 | [Median of Two Sorted Arrays Style Problem](#q21) | Array — Binary search partition |
| 22 | [Open the Lock](#q22) | Graph / State Space — BFS |
| 23 | [Merge Two / K Sorted Arrays](#q23) | Array / Heap — Two pointers or min-heap |
| 24 | [Celebrity Problem Variation](#q24) | Graph / Greedy — Candidate elimination |
| 25 | [Robot Route to Collect Required Items from a Matrix](#q25) | Grid / State Space — BFS + bitmask |
| 26 | [Two Sum Sliding Window Variation](#q26) | Array — Sliding window + unordered_map |

---


This guide uses simple, readable C++17 and the interview format you requested:

1. Simple, repeatable problem statement
2. Clarifying questions
3. Brute force: approach, data structure, time, space, code
4. Optimized: approach, data structure, time, space, code

No dry runs.

> Note: For incomplete prompts such as Jump/Reachability, Robot Route, and Two Sum Sliding Window, I state the exact assumption being solved.

---

<a id="q01"></a>

## 1. Currency Converter

### Problem statement
We are given conversion rates between currency pairs. Find the conversion rate from one currency to another, possibly through intermediate currencies.

### Clarifying questions
- Can conversion require multiple hops?
- Should reverse conversion use the reciprocal rate?
- Can the graph contain cycles?
- What should we return if no path exists?

### Brute force
**Approach:** Build a graph and DFS from source to target for every query.  
**Data structure:** Adjacency list + DFS + visited set  
**Time:** `O(V + E)` per query, where `V` = currencies and `E` = conversion edges.  
**Space:** `O(V + E)`

```cpp
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <functional>
#include <utility>
#include <vector>

using Graph = unordered_map<string,vector<pair<string, double>>>;

bool findRate(const Graph& graph, const std::string& current,
              const std::string& target,
              std::unordered_set<std::string>& visited,
              double currentRate, double& answer) {
    if (current == target) {
        answer = currentRate;
        return true;
    }

    visited.insert(current);

    auto neighbors = graph.find(current);
    if (neighbors == graph.end()) {
        return false;
    }

    for (const auto& [nextCurrency, rate] : neighbors->second) {
        if (!visited.count(nextCurrency) &&
            findRate(graph, nextCurrency, target, visited,
                     currentRate * rate, answer)) {
            return true;
        }
    }
    return false;
}

double convertCurrency(
    const vector<tuple<string, string, double>>& rates,
    const string& source, const string& target) {
    Graph graph;
    for (const auto& [from, to, rate] : rates) {
        graph[from].push_back({to, rate});
        graph[to].push_back({from, 1.0 / rate});
    }

    std::unordered_set<std::string> visited;
    double answer = -1.0;
    findRate(graph, source, target, visited, 1.0, answer);
    return answer;
}
```

### Optimized
**Approach:** For a single query DFS/BFS is already optimal. For repeated queries, cache completed source-target results.  
**Data structure:** Graph + memoization  
**Time:** First query `O(V + E)`, cached query `O(1)`.  
**Space:** `O(V + E + Q)`, where `Q` = cached query pairs.

```cpp
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

class CurrencyConverter {
private:
    using Graph = std::unordered_map<std::string,
        std::vector<std::pair<std::string, double>>>;

    Graph graph;
    std::unordered_map<std::string, double> cache;

    std::string cacheKey(const std::string& source,
                         const std::string& target) const {
        return source + "->" + target;
    }

    bool search(const std::string& current, const std::string& target,
                double rate, std::unordered_set<std::string>& visited,
                double& answer) const {
        if (current == target) {
            answer = rate;
            return true;
        }

        visited.insert(current);
        auto neighbors = graph.find(current);
        if (neighbors == graph.end()) {
            return false;
        }

        for (const auto& [nextCurrency, edgeRate] : neighbors->second) {
            if (!visited.count(nextCurrency) &&
                search(nextCurrency, target, rate * edgeRate,
                       visited, answer)) {
                return true;
            }
        }
        return false;
    }

public:
    explicit CurrencyConverter(
        const std::vector<std::tuple<std::string, std::string, double>>& rates) {
        for (const auto& [from, to, rate] : rates) {
            graph[from].push_back({to, rate});
            graph[to].push_back({from, 1.0 / rate});
        }
    }

    double convert(const std::string& source, const std::string& target) {
        const std::string key = cacheKey(source, target);
        if (cache.count(key)) {
            return cache[key];
        }

        std::unordered_set<std::string> visited;
        double answer = -1.0;
        search(source, target, 1.0, visited, answer);
        cache[key] = answer;
        return answer;
    }
};
```

---

<a id="q02"></a>

## 2. All Downhill Paths in a Terrain

### Problem statement
We are given a grid of heights. Starting from a cell, return all paths that move only to strictly lower neighboring cells.

### Clarifying questions
- Can we move in 4 or 8 directions?
- What makes a path complete?
- Are equal-height moves allowed?
- Do we need all paths or only their count?

### Brute force
**Approach:** DFS every valid downhill choice and save a path when no lower neighbor remains.  
**Data structure:** DFS + path list  
**Time:** Exponential in path length in the worst case because all valid paths must be generated.  
**Space:** `O(M * N)` worst-case recursion/path depth, where `M` = rows and `N` = columns.

```cpp
#include <functional>
#include <utility>
#include <vector>

using Cell = std::pair<int, int>;
using Path = std::vector<Cell>;

std::vector<Path> downhillPaths(const std::vector<std::vector<int>>& grid,
                                int startRow, int startCol) {
    const int rows = static_cast<int>(grid.size());
    const int cols = static_cast<int>(grid[0].size());
    const std::vector<Cell> directions = {
        {1, 0}, {-1, 0}, {0, 1}, {0, -1}
    };

    std::vector<Path> result;
    Path currentPath;

    std::function<void(int, int)> dfs = [&](int row, int col) {
        currentPath.push_back({row, col});
        bool moved = false;

        for (const auto& [rowChange, colChange] : directions) {
            int nextRow = row + rowChange;
            int nextCol = col + colChange;

            if (nextRow >= 0 && nextRow < rows &&
                nextCol >= 0 && nextCol < cols &&
                grid[nextRow][nextCol] < grid[row][col]) {
                moved = true;
                dfs(nextRow, nextCol);
            }
        }

        if (!moved) {
            result.push_back(currentPath);
        }
        currentPath.pop_back();
    };

    dfs(startRow, startCol);
    return result;
}
```

### Optimized
**Approach:** Backtracking is already output-optimal when all paths are required. Strict decrease prevents cycles. If the rule becomes `<=`, add path-level visited tracking.  
**Data structure:** DFS + backtracking  
**Time:** `O(total output size)`  
**Space:** `O(M * N)` worst-case recursion depth.

```cpp
#include <functional>
#include <utility>
#include <vector>

using Cell = std::pair<int, int>;
using Path = std::vector<Cell>;

std::vector<Path> downhillPaths(const std::vector<std::vector<int>>& grid,
                                int startRow, int startCol) {
    const int rows = static_cast<int>(grid.size());
    const int cols = static_cast<int>(grid[0].size());
    const std::vector<Cell> directions = {
        {1, 0}, {-1, 0}, {0, 1}, {0, -1}
    };

    std::vector<Path> result;
    Path currentPath;

    std::function<void(int, int)> backtrack = [&](int row, int col) {
        currentPath.push_back({row, col});
        std::vector<Cell> nextCells;

        for (const auto& [rowChange, colChange] : directions) {
            int nextRow = row + rowChange;
            int nextCol = col + colChange;

            if (nextRow >= 0 && nextRow < rows &&
                nextCol >= 0 && nextCol < cols &&
                grid[nextRow][nextCol] < grid[row][col]) {
                nextCells.push_back({nextRow, nextCol});
            }
        }

        if (nextCells.empty()) {
            result.push_back(currentPath);
        }

        for (const auto& [nextRow, nextCol] : nextCells) {
            backtrack(nextRow, nextCol);
        }
        currentPath.pop_back();
    };

    backtrack(startRow, startCol);
    return result;
}
```

---

<a id="q03"></a>

## 3. Find Files by Name in a Directory

### Problem statement
We are given a directory tree. Recursively return files whose name matches a target.

### Clarifying questions
- Exact or partial name match?
- Return first match or all?
- Can links create cycles?
- Can directories contain both files and folders?

### Brute force
**Approach:** DFS through every file and subdirectory.  
**Data structure:** Tree DFS  
**Time:** `O(N)`, where `N` = total files and directories.  
**Space:** `O(H)`, where `H` = maximum directory depth.

```cpp
#include <string>
#include <vector>

struct FileNode {
    std::string name;
    bool isFile;
    std::vector<FileNode*> children;
};

void searchFiles(FileNode* node, string& target, vector<FileNode*>& result) {
    if (node == nullptr) {
        return;
    }

    if (node->isFile) {
        if (node->name == target) {
            result.push_back(node);
        }
        return;
    }

    for (FileNode* child : node->children) {
        searchFiles(child, target, result);
    }
}

vector<FileNode*> findFiles(FileNode* root, string& target) {
    vector<FileNode*> result;
    searchFiles(root, target, result);
    return result;
}
```

### Optimized
**Approach:** For one search, DFS is already optimal. For repeated searches, build a filename index once.  
**Data structure:** Hash map + DFS  
**Time:** Build `O(N)`, query `O(1 + K)`, where `K` = matches.  
**Space:** `O(N)`

```cpp
#include <string>
#include <unordered_map>
#include <vector>

struct FileNode {
    std::string name;
    bool isFile;
    std::vector<FileNode*> children;
};

using FileIndex =
    std::unordered_map<std::string, std::vector<FileNode*>>;

void addToIndex(FileNode* node, FileIndex& index) {
    if (node == nullptr) {
        return;
    }

    if (node->isFile) {
        index[node->name].push_back(node);
        return;
    }

    for (FileNode* child : node->children) {
        addToIndex(child, index);
    }
}

FileIndex buildFileIndex(FileNode* root) {
    FileIndex index;
    addToIndex(root, index);
    return index;
}
```

---

<a id="q04"></a>

## 4. Server Load Assignment

### Problem statement
Each incoming partition must be assigned to the server with the smallest current load, then that server's load increases.

### Clarifying questions
- Does each partition have a load size?
- How are ties broken?
- Do servers join or leave?
- Return assignments or only final loads?

### Brute force
**Approach:** For each partition, scan all servers to find the current minimum.  
**Data structure:** Array  
**Time:** `O(P * S)`, where `P` = partitions and `S` = servers.  
**Space:** `O(S)`

```cpp
#include <vector>

vector<int> assignServersBruteForce( vector<int> serverLoads, vector<int>& partitionLoads) {

    vector<int> assignments;

    for (int partitionLoad : partitionLoads) {
        int bestServer = 0;

        for (int server = 1; server < serverLoads.size(); ++server) {
            if (serverLoads[server] < serverLoads[bestServer]) {
                bestServer = server;
            }
        }

        assignments.push_back(bestServer);
        serverLoads[bestServer] += partitionLoad;
    }

    return assignments;
}
```

### Optimized
**Approach:** Keep servers in a min-heap by `(load, server_id)`.  
**Data structure:** Min-heap  
**Time:** `O(S + P log S)`  
**Space:** `O(S)`

```cpp
#include <functional>
#include <queue>
#include <utility>
#include <vector>

vector<int> assignServers( vector<int>& serverLoads, vector<int>& partitionLoads) {
    Server = pair<int, int>;  // load, server index
    priority_queue<Server, vector<Server>, greater<Server>> minHeap;

    for (int server = 0; server < serverLoads.size(); ++server) {
        minHeap.push({serverLoads[server], server});
    }

    vector<int> assignments;

    for (int partitionLoad : partitionLoads) {
        auto [load, server] = minHeap.top();
        minHeap.pop();

        assignments.push_back(server);
        minHeap.push({load + partitionLoad, server});
    }

    return assignments;
}
```

---

<a id="q05"></a>

## 5. Streaming Top-K

### Problem statement
Values arrive in a stream. Maintain the largest `K` values seen so far.

### Clarifying questions
- Do we need top K after every insertion?
- Are duplicates allowed?
- Is K fixed?
- Must output be sorted?

### Brute force
**Approach:** Store all values and sort when top K is needed.  
**Data structure:** Array  
**Time:** `O(N log N)`  
**Space:** `O(N)`

```cpp
#include <algorithm>
#include <functional>
#include <vector>

std::vector<int> topKBruteForce(std::vector<int> values, int k) {
    std::sort(values.begin(), values.end(), std::greater<int>());

    if (k < static_cast<int>(values.size())) {
        values.resize(k);
    }
    return values;
}
```

### Optimized
**Approach:** Maintain a min-heap of size at most K.  
**Data structure:** Min-heap  
**Time:** `O(N log K)`  
**Space:** `O(K)`

```cpp
#include <algorithm>
#include <functional>
#include <queue>
#include <vector>

std::vector<int> topK(const std::vector<int>& stream, int k) {
    if (k <= 0) {
        return {};
    }

    std::priority_queue<int, std::vector<int>, std::greater<int>> minHeap;

    for (int value : stream) {
        if (static_cast<int>(minHeap.size()) < k) {
            minHeap.push(value);
        } else if (value > minHeap.top()) {
            minHeap.pop();
            minHeap.push(value);
        }
    }

    std::vector<int> result;
    while (!minHeap.empty()) {
        result.push_back(minHeap.top());
        minHeap.pop();
    }

    std::sort(result.rbegin(), result.rend());
    return result;
}
```

---

<a id="q06"></a>

## 6. Customer Log Analysis / Loyal Customers

### Problem statement
Return customers who appeared on both days and interacted with at least two distinct products overall.

### Clarifying questions
- Can the same customer-product pair repeat?
- Is distinct-product count across both days?
- Must the customer appear on both days?
- What output format is needed?

### Brute force
**Approach:** For each customer, rescan both logs and collect products.  
**Data structure:** Sets  
**Time:** `O(C * N)`, where `C` = customers and `N` = total log entries.  
**Space:** `O(P)` temporary, where `P` = products for one customer.

```cpp
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

using Purchase = std::pair<std::string, std::string>;

std::vector<std::string> loyalCustomersBruteForce(
    const std::vector<Purchase>& dayOne,
    const std::vector<Purchase>& dayTwo) {
    std::unordered_set<std::string> allCustomers;
    for (const auto& [customer, product] : dayOne) {
        allCustomers.insert(customer);
    }
    for (const auto& [customer, product] : dayTwo) {
        allCustomers.insert(customer);
    }

    std::vector<std::string> result;

    for (const std::string& customer : allCustomers) {
        bool seenOnDayOne = false;
        bool seenOnDayTwo = false;
        std::unordered_set<std::string> products;

        for (const auto& [name, product] : dayOne) {
            if (name == customer) {
                seenOnDayOne = true;
                products.insert(product);
            }
        }
        for (const auto& [name, product] : dayTwo) {
            if (name == customer) {
                seenOnDayTwo = true;
                products.insert(product);
            }
        }

        if (seenOnDayOne && seenOnDayTwo && products.size() >= 2) {
            result.push_back(customer);
        }
    }
    return result;
}
```

### Optimized
**Approach:** Build day-presence sets and a product set per customer in one pass.  
**Data structure:** Hash maps + sets  
**Time:** `O(N)`  
**Space:** `O(N)`

```cpp
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

using Purchase = std::pair<std::string, std::string>;

std::vector<std::string> loyalCustomers(
    const std::vector<Purchase>& dayOne,
    const std::vector<Purchase>& dayTwo) {
    std::unordered_set<std::string> firstDayCustomers;
    std::unordered_set<std::string> secondDayCustomers;
    std::unordered_map<std::string,
        std::unordered_set<std::string>> productsByCustomer;

    for (const auto& [customer, product] : dayOne) {
        firstDayCustomers.insert(customer);
        productsByCustomer[customer].insert(product);
    }
    for (const auto& [customer, product] : dayTwo) {
        secondDayCustomers.insert(customer);
        productsByCustomer[customer].insert(product);
    }

    std::vector<std::string> result;
    for (const std::string& customer : firstDayCustomers) {
        if (secondDayCustomers.count(customer) &&
            productsByCustomer[customer].size() >= 2) {
            result.push_back(customer);
        }
    }
    return result;
}
```

---

<a id="q07"></a>

## 7. Task Dependencies

### Problem statement
Given one delayed task, return every downstream task that can also be affected.

### Clarifying questions
- Does `A -> B` mean B depends on A?
- Can the graph contain cycles?
- Include the delayed task itself?
- Does output order matter?

### Brute force
**Approach:** For each task, independently search whether it depends on the delayed task.  
**Data structure:** Graph + DFS  
**Time:** `O(V * (V + E))`  
**Space:** `O(V + E)`

```cpp
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

bool dependsOn(const std::string& task, const std::string& delayedTask,
               const std::unordered_map<std::string,
                   std::vector<std::string>>& prerequisites,
               std::unordered_set<std::string>& visited) {
    if (task == delayedTask) {
        return true;
    }

    visited.insert(task);
    auto entry = prerequisites.find(task);
    if (entry == prerequisites.end()) {
        return false;
    }

    for (const std::string& prerequisite : entry->second) {
        if (!visited.count(prerequisite) &&
            dependsOn(prerequisite, delayedTask, prerequisites, visited)) {
            return true;
        }
    }
    return false;
}

std::vector<std::string> affectedTasksBruteForce(
    const std::vector<std::string>& tasks,
    const std::vector<std::pair<std::string, std::string>>& edges,
    const std::string& delayedTask) {
    std::unordered_map<std::string, std::vector<std::string>> prerequisites;
    for (const auto& [parent, child] : edges) {
        prerequisites[child].push_back(parent);
    }

    std::vector<std::string> result;
    for (const std::string& task : tasks) {
        if (task == delayedTask) {
            continue;
        }
        std::unordered_set<std::string> visited;
        if (dependsOn(task, delayedTask, prerequisites, visited)) {
            result.push_back(task);
        }
    }
    return result;
}
```

### Optimized
**Approach:** Build prerequisite-to-dependent edges and traverse once from the delayed task.  
**Data structure:** Adjacency list + DFS/BFS  
**Time:** `O(V + E)`  
**Space:** `O(V + E)`

```cpp
#include <stack>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

std::vector<std::string> affectedTasks(
    const std::vector<std::string>& tasks,
    const std::vector<std::pair<std::string, std::string>>& edges,
    const std::string& delayedTask) {
    std::unordered_map<std::string, std::vector<std::string>> graph;
    for (const std::string& task : tasks) {
        graph[task] = {};
    }
    for (const auto& [parent, child] : edges) {
        graph[parent].push_back(child);
    }

    std::stack<std::string> pending;
    std::unordered_set<std::string> visited = {delayedTask};
    std::vector<std::string> result;
    pending.push(delayedTask);

    while (!pending.empty()) {
        std::string task = pending.top();
        pending.pop();

        for (const std::string& nextTask : graph[task]) {
            if (visited.insert(nextTask).second) {
                result.push_back(nextTask);
                pending.push(nextTask);
            }
        }
    }
    return result;
}
```

---

<a id="q08"></a>

## 8. Longest Chain of Cascading Task Delays

### Problem statement
Tasks form a DAG. Return the length of the longest downstream dependency chain.

### Clarifying questions
- Is the graph guaranteed acyclic?
- Count nodes or edges?
- Need the chain or only length?
- Are edges unweighted?

### Brute force
**Approach:** Run a fresh DFS from every task and recompute downstream paths.  
**Data structure:** DAG + DFS  
**Time:** `O(V * (V + E))`  
**Space:** `O(V + E)`

```cpp
#include <algorithm>
#include <functional>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

int longestChainBruteForce(
    const std::vector<std::string>& tasks,
    const std::vector<std::pair<std::string, std::string>>& edges) {
    std::unordered_map<std::string, std::vector<std::string>> graph;
    for (const auto& [from, to] : edges) {
        graph[from].push_back(to);
    }

    std::function<int(const std::string&)> dfs =
        [&](const std::string& task) {
            int best = 1;
            for (const std::string& nextTask : graph[task]) {
                best = std::max(best, 1 + dfs(nextTask));
            }
            return best;
        };

    int answer = 0;
    for (const std::string& task : tasks) {
        answer = std::max(answer, dfs(task));
    }
    return answer;
}
```

### Optimized
**Approach:** Memoize the longest path starting from each node.  
**Data structure:** DAG + memoized DFS  
**Time:** `O(V + E)`  
**Space:** `O(V + E)`

```cpp
#include <algorithm>
#include <functional>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

int longestChain(
    const std::vector<std::string>& tasks,
    const std::vector<std::pair<std::string, std::string>>& edges) {
    std::unordered_map<std::string, std::vector<std::string>> graph;
    std::unordered_map<std::string, int> memo;

    for (const auto& [from, to] : edges) {
        graph[from].push_back(to);
    }

    std::function<int(const std::string&)> dfs =
        [&](const std::string& task) {
            if (memo.count(task)) {
                return memo[task];
            }

            int best = 1;
            for (const std::string& nextTask : graph[task]) {
                best = std::max(best, 1 + dfs(nextTask));
            }

            memo[task] = best;
            return best;
        };

    int answer = 0;
    for (const std::string& task : tasks) {
        answer = std::max(answer, dfs(task));
    }
    return answer;
}
```

---

<a id="q09"></a>

## 9. Shuffle an Array In Place

### Problem statement
Randomly shuffle an array in place so every permutation is equally likely.

### Clarifying questions
- Must every permutation be equally likely?
- Can we use a random generator?
- Must it be in place?
- Return the same array?

### Brute force
**Approach:** Repeatedly choose random unused output positions. Correct but may retry many times.  
**Data structure:** Array + set  
**Time:** Worse than `O(N)` due to retries.  
**Space:** `O(N)`

```cpp
#include <random>
#include <unordered_set>
#include <vector>

void shuffleBruteForce(std::vector<int>& numbers) {
    std::vector<int> shuffled(numbers.size());
    std::unordered_set<int> usedPositions;
    std::mt19937 generator(std::random_device{}());
    std::uniform_int_distribution<int> position(
        0, static_cast<int>(numbers.size()) - 1);

    for (int value : numbers) {
        int index = position(generator);
        while (usedPositions.count(index)) {
            index = position(generator);
        }

        usedPositions.insert(index);
        shuffled[index] = value;
    }

    numbers = shuffled;
}
```

### Optimized
**Approach:** Use Fisher-Yates: for each position from right to left, swap with a uniformly random position in the remaining prefix.  
**Data structure:** Array  
**Time:** `O(N)`  
**Space:** `O(1)`

```cpp
#include <random>
#include <utility>
#include <vector>

void shuffleArray(std::vector<int>& numbers) {
    std::mt19937 generator(std::random_device{}());

    for (int index = static_cast<int>(numbers.size()) - 1;
         index > 0; --index) {
        std::uniform_int_distribution<int> pick(0, index);
        int randomIndex = pick(generator);
        std::swap(numbers[index], numbers[randomIndex]);
    }
}
```

---

<a id="q10"></a>

## 10. Schedule Items Using Three Priority Attributes

### Problem statement
Items have three priority attributes. Always process the highest-priority item using a defined tie-breaking order.

### Clarifying questions
- Which attribute has highest precedence?
- Does larger or smaller mean higher priority?
- What is the final tie-breaker?
- Can priorities age over time?

### Brute force
**Approach:** Keep items in a list and scan for the best one on every extraction.  
**Data structure:** Array  
**Time:** `O(N^2)` for processing all N items.  
**Space:** `O(N)`

```cpp
#include <vector>

struct WorkItem {
    int firstPriority;
    int secondPriority;
    int thirdPriority;
    int id;

    bool operator<(const WorkItem& other) const {
        if (firstPriority != other.firstPriority) {
            return firstPriority < other.firstPriority;
        }
        if (secondPriority != other.secondPriority) {
            return secondPriority < other.secondPriority;
        }
        if (thirdPriority != other.thirdPriority) {
            return thirdPriority < other.thirdPriority;
        }
        return id < other.id;
    }
};

std::vector<WorkItem> scheduleBruteForce(
    std::vector<WorkItem> items) {
    std::vector<WorkItem> result;

    while (!items.empty()) {
        int best = 0;
        for (int index = 1;
             index < static_cast<int>(items.size()); ++index) {
            if (items[index] < items[best]) {
                best = index;
            }
        }

        result.push_back(items[best]);
        items.erase(items.begin() + best);
    }
    return result;
}
```

### Optimized
**Approach:** Use a priority queue with tuple ordering such as `(p1, p2, p3, id)`.  
**Data structure:** Min-heap  
**Time:** `O(N log N)`  
**Space:** `O(N)`

```cpp
#include <queue>
#include <vector>

struct WorkItem {
    int firstPriority;
    int secondPriority;
    int thirdPriority;
    int id;
};

struct HigherPriority {
    bool operator()(const WorkItem& left,
                    const WorkItem& right) const {
        if (left.firstPriority != right.firstPriority) {
            return left.firstPriority > right.firstPriority;
        }
        if (left.secondPriority != right.secondPriority) {
            return left.secondPriority > right.secondPriority;
        }
        if (left.thirdPriority != right.thirdPriority) {
            return left.thirdPriority > right.thirdPriority;
        }
        return left.id > right.id;
    }
};

std::vector<WorkItem> scheduleItems(
    const std::vector<WorkItem>& items) {
    std::priority_queue<WorkItem, std::vector<WorkItem>,
                        HigherPriority> queue;

    for (const WorkItem& item : items) {
        queue.push(item);
    }

    std::vector<WorkItem> result;
    while (!queue.empty()) {
        result.push_back(queue.top());
        queue.pop();
    }
    return result;
}
```

---

<a id="q11"></a>

## 11. Tree Path Sum Variation

### Problem statement
Given a binary tree and target sum, determine whether a root-to-leaf path adds up to the target.

### Clarifying questions
- Must the path start at root?
- Must it end at a leaf?
- Can values be negative?
- Boolean, count, or actual path?

### Brute force
**Approach:** Generate all root-to-leaf paths, then sum each one.  
**Data structure:** DFS + path list  
**Time:** `O(N * H)` worst case, where `N` = nodes and `H` = height.  
**Space:** `O(H)` auxiliary plus stored paths.

```cpp
#include <numeric>
#include <vector>

struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
};

void collectRootToLeafPaths(TreeNode* node,
                            std::vector<int>& currentPath,
                            std::vector<std::vector<int>>& allPaths) {
    if (node == nullptr) {
        return;
    }

    currentPath.push_back(node->value);

    if (node->left == nullptr && node->right == nullptr) {
        allPaths.push_back(currentPath);
    } else {
        collectRootToLeafPaths(node->left, currentPath, allPaths);
        collectRootToLeafPaths(node->right, currentPath, allPaths);
    }

    currentPath.pop_back();
}

bool hasPathSumBruteForce(TreeNode* root, int target) {
    std::vector<std::vector<int>> paths;
    std::vector<int> currentPath;
    collectRootToLeafPaths(root, currentPath, paths);

    for (const std::vector<int>& path : paths) {
        int sum = std::accumulate(path.begin(), path.end(), 0);
        if (sum == target) {
            return true;
        }
    }
    return false;
}
```

### Optimized
**Approach:** Carry the remaining target down the tree instead of storing paths.  
**Data structure:** Tree DFS  
**Time:** `O(N)`  
**Space:** `O(H)`

```cpp
struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
};

bool hasPathSum(TreeNode* node, int remainingSum) {
    if (node == nullptr) {
        return false;
    }

    remainingSum -= node->value;

    if (node->left == nullptr && node->right == nullptr) {
        return remainingSum == 0;
    }

    return hasPathSum(node->left, remainingSum) ||
           hasPathSum(node->right, remainingSum);
}
```

---

<a id="q12"></a>

## 12. Nodes at Distance K from Target

### Problem statement
Given a binary tree, a target node, and K, return all nodes exactly K edges away from the target.

### Clarifying questions
- Are node values unique?
- Do we receive the target node reference?
- Does output order matter?
- Can we build parent pointers?

### Brute force
**Approach:** For every node, independently compute its distance to the target.  
**Data structure:** Tree DFS  
**Time:** `O(N^2)`  
**Space:** `O(H)`

```cpp
#include <vector>

struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
};

int distanceFrom(TreeNode* node, TreeNode* target) {
    if (node == nullptr) {
        return -1;
    }
    if (node == target) {
        return 0;
    }

    int leftDistance = distanceFrom(node->left, target);
    if (leftDistance != -1) {
        return leftDistance + 1;
    }

    int rightDistance = distanceFrom(node->right, target);
    return rightDistance == -1 ? -1 : rightDistance + 1;
}

void collectNodes(TreeNode* node, std::vector<TreeNode*>& nodes) {
    if (node == nullptr) {
        return;
    }

    nodes.push_back(node);
    collectNodes(node->left, nodes);
    collectNodes(node->right, nodes);
}

std::vector<int> nodesAtDistanceKBruteForce(
    TreeNode* root, TreeNode* target, int k) {
    std::vector<TreeNode*> nodes;
    collectNodes(root, nodes);

    std::vector<int> result;
    for (TreeNode* node : nodes) {
        if (distanceFrom(node, target) == k) {
            result.push_back(node->value);
        }
    }
    return result;
}
```

### Optimized
**Approach:** Build parent pointers, then BFS outward from the target as if the tree were an undirected graph.  
**Data structure:** Parent map + queue + visited  
**Time:** `O(N)`  
**Space:** `O(N)`

```cpp
#include <queue>
#include <unordered_map>
#include <unordered_set>
#include <vector>

struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
};

void buildParentMap(TreeNode* node, TreeNode* parent,
                    std::unordered_map<TreeNode*, TreeNode*>& parents) {
    if (node == nullptr) {
        return;
    }

    parents[node] = parent;
    buildParentMap(node->left, node, parents);
    buildParentMap(node->right, node, parents);
}

std::vector<int> nodesAtDistanceK(
    TreeNode* root, TreeNode* target, int k) {
    std::unordered_map<TreeNode*, TreeNode*> parents;
    buildParentMap(root, nullptr, parents);

    std::queue<std::pair<TreeNode*, int>> queue;
    std::unordered_set<TreeNode*> visited;
    queue.push({target, 0});
    visited.insert(target);

    std::vector<int> result;

    while (!queue.empty()) {
        auto [node, distance] = queue.front();
        queue.pop();

        if (distance == k) {
            result.push_back(node->value);
            continue;
        }

        for (TreeNode* next : {node->left, node->right, parents[node]}) {
            if (next != nullptr && visited.insert(next).second) {
                queue.push({next, distance + 1});
            }
        }
    }
    return result;
}
```

---

<a id="q13"></a>

## 13. Number of Islands Variation

### Problem statement
Given a grid of land and water, return the number of separate connected islands.

### Clarifying questions
- 4-direction or 8-direction connectivity?
- Can I modify the grid?
- Can the grid be empty?
- What values represent land/water?

### Brute force
**Approach:** DFS each new land cell and keep an explicit visited set.  
**Data structure:** Grid DFS + visited set  
**Time:** `O(M * N)`  
**Space:** `O(M * N)`

```cpp
#include <functional>
#include <vector>

int numberOfIslandsBruteForce(
    const std::vector<std::vector<char>>& grid) {
    if (grid.empty()) {
        return 0;
    }

    const int rows = static_cast<int>(grid.size());
    const int cols = static_cast<int>(grid[0].size());
    std::vector<std::vector<bool>> visited(
        rows, std::vector<bool>(cols, false));

    std::function<void(int, int)> visit = [&](int row, int col) {
        if (row < 0 || row >= rows || col < 0 || col >= cols ||
            grid[row][col] == '0' || visited[row][col]) {
            return;
        }

        visited[row][col] = true;
        visit(row + 1, col);
        visit(row - 1, col);
        visit(row, col + 1);
        visit(row, col - 1);
    };

    int islands = 0;
    for (int row = 0; row < rows; ++row) {
        for (int col = 0; col < cols; ++col) {
            if (grid[row][col] == '1' && !visited[row][col]) {
                ++islands;
                visit(row, col);
            }
        }
    }
    return islands;
}
```

### Optimized
**Approach:** Mark visited land directly in the grid to avoid an explicit visited set.  
**Data structure:** Grid DFS  
**Time:** `O(M * N)`  
**Space:** `O(M * N)` recursion worst case.

```cpp
#include <functional>
#include <vector>

int numberOfIslands(std::vector<std::vector<char>>& grid) {
    if (grid.empty()) {
        return 0;
    }

    const int rows = static_cast<int>(grid.size());
    const int cols = static_cast<int>(grid[0].size());

    std::function<void(int, int)> sink = [&](int row, int col) {
        if (row < 0 || row >= rows || col < 0 || col >= cols ||
            grid[row][col] == '0') {
            return;
        }

        grid[row][col] = '0';
        sink(row + 1, col);
        sink(row - 1, col);
        sink(row, col + 1);
        sink(row, col - 1);
    };

    int islands = 0;
    for (int row = 0; row < rows; ++row) {
        for (int col = 0; col < cols; ++col) {
            if (grid[row][col] == '1') {
                ++islands;
                sink(row, col);
            }
        }
    }
    return islands;
}
```

---

<a id="q14"></a>

## 14. Rotting Oranges

### Problem statement
Rotten oranges spread to adjacent fresh oranges each minute. Return the minimum minutes until all fresh oranges rot, or `-1` if impossible.

### Clarifying questions
- Only 4 directions?
- Do rotten oranges spread simultaneously?
- What if no fresh oranges exist?
- What if fresh oranges are unreachable?

### Brute force
**Approach:** Simulate minute by minute by rescanning the entire grid.  
**Data structure:** Grid + temporary list  
**Time:** `O((M * N)^2)`  
**Space:** `O(M * N)`

```cpp
#include <utility>
#include <vector>

int orangesRottingBruteForce(std::vector<std::vector<int>> grid) {
    const int rows = static_cast<int>(grid.size());
    const int cols = static_cast<int>(grid[0].size());
    const std::vector<std::pair<int, int>> directions = {
        {1, 0}, {-1, 0}, {0, 1}, {0, -1}
    };

    int minutes = 0;

    while (true) {
        std::vector<std::pair<int, int>> orangesToRot;
        int freshOranges = 0;

        for (int row = 0; row < rows; ++row) {
            for (int col = 0; col < cols; ++col) {
                if (grid[row][col] != 1) {
                    continue;
                }

                ++freshOranges;
                for (const auto& [rowChange, colChange] : directions) {
                    int nextRow = row + rowChange;
                    int nextCol = col + colChange;

                    if (nextRow >= 0 && nextRow < rows &&
                        nextCol >= 0 && nextCol < cols &&
                        grid[nextRow][nextCol] == 2) {
                        orangesToRot.push_back({row, col});
                        break;
                    }
                }
            }
        }

        if (freshOranges == 0) {
            return minutes;
        }
        if (orangesToRot.empty()) {
            return -1;
        }

        for (const auto& [row, col] : orangesToRot) {
            grid[row][col] = 2;
        }
        ++minutes;
    }
}
```

### Optimized
**Approach:** Use multi-source BFS from all initially rotten oranges. Each BFS level is one minute.  
**Data structure:** Queue  
**Time:** `O(M * N)`  
**Space:** `O(M * N)`

```cpp
#include <queue>
#include <utility>
#include <vector>

int orangesRotting(std::vector<std::vector<int>> grid) {
    const int rows = static_cast<int>(grid.size());
    const int cols = static_cast<int>(grid[0].size());
    const std::vector<std::pair<int, int>> directions = {
        {1, 0}, {-1, 0}, {0, 1}, {0, -1}
    };

    std::queue<std::pair<int, int>> queue;
    int freshOranges = 0;

    for (int row = 0; row < rows; ++row) {
        for (int col = 0; col < cols; ++col) {
            if (grid[row][col] == 2) {
                queue.push({row, col});
            } else if (grid[row][col] == 1) {
                ++freshOranges;
            }
        }
    }

    int minutes = 0;

    while (!queue.empty() && freshOranges > 0) {
        int levelSize = static_cast<int>(queue.size());

        while (levelSize-- > 0) {
            auto [row, col] = queue.front();
            queue.pop();

            for (const auto& [rowChange, colChange] : directions) {
                int nextRow = row + rowChange;
                int nextCol = col + colChange;

                if (nextRow >= 0 && nextRow < rows &&
                    nextCol >= 0 && nextCol < cols &&
                    grid[nextRow][nextCol] == 1) {
                    grid[nextRow][nextCol] = 2;
                    --freshOranges;
                    queue.push({nextRow, nextCol});
                }
            }
        }
        ++minutes;
    }

    return freshOranges == 0 ? minutes : -1;
}
```

---

<a id="q15"></a>

## 15. Course Schedule II

### Problem statement
Given courses and prerequisites, return one valid order to complete all courses, or an empty list if a cycle exists.

### Clarifying questions
- Does `[course, prereq]` mean prereq first?
- Can there be multiple valid orders?
- Return any valid order?
- What should happen on a cycle?

### Brute force
**Approach:** Run DFS from each course with a fresh path set, causing repeated work.  
**Data structure:** Directed graph + DFS  
**Time:** `O(V * (V + E))`  
**Space:** `O(V + E)`

```cpp
#include <functional>
#include <unordered_set>
#include <vector>

std::vector<int> findCourseOrderBruteForce(
    int courseCount,
    const std::vector<std::vector<int>>& prerequisites) {
    std::vector<std::vector<int>> graph(courseCount);
    for (const auto& relation : prerequisites) {
        graph[relation[0]].push_back(relation[1]);
    }

    std::vector<int> order;
    std::unordered_set<int> added;

    std::function<bool(int, std::unordered_set<int>&)> visit =
        [&](int course, std::unordered_set<int>& path) {
            if (path.count(course)) {
                return false;
            }

            path.insert(course);
            for (int prerequisite : graph[course]) {
                if (!visit(prerequisite, path)) {
                    return false;
                }
            }
            path.erase(course);

            if (added.insert(course).second) {
                order.push_back(course);
            }
            return true;
        };

    for (int course = 0; course < courseCount; ++course) {
        std::unordered_set<int> path;
        if (!visit(course, path)) {
            return {};
        }
    }
    return order;
}
```

### Optimized
**Approach:** Use DFS states `0 = unvisited`, `1 = visiting`, `2 = complete`; append in postorder.  
**Data structure:** Directed graph + DFS states  
**Time:** `O(V + E)`  
**Space:** `O(V + E)`

```cpp
#include <functional>
#include <vector>

std::vector<int> findCourseOrder(
    int courseCount,
    const std::vector<std::vector<int>>& prerequisites) {
    std::vector<std::vector<int>> graph(courseCount);
    for (const auto& relation : prerequisites) {
        graph[relation[0]].push_back(relation[1]);
    }

    std::vector<int> state(courseCount, 0);
    std::vector<int> order;

    std::function<bool(int)> visit = [&](int course) {
        if (state[course] == 1) {
            return false;
        }
        if (state[course] == 2) {
            return true;
        }

        state[course] = 1;
        for (int prerequisite : graph[course]) {
            if (!visit(prerequisite)) {
                return false;
            }
        }

        state[course] = 2;
        order.push_back(course);
        return true;
    };

    for (int course = 0; course < courseCount; ++course) {
        if (!visit(course)) {
            return {};
        }
    }
    return order;
}
```

---

<a id="q16"></a>

## 16. Domino and Tromino Tiling

### Problem statement
Count the number of ways to tile a `2 x N` board using dominoes and L-shaped trominoes.

### Clarifying questions
- Are rotations allowed?
- Return modulo `10^9+7`?
- Is `N >= 1`?
- Only the count needed?

### Brute force
**Approach:** Use the recurrence recursively without memoization.  
**Data structure:** Recursion  
**Time:** Exponential  
**Space:** `O(N)`

```cpp
long long countTilingsBruteForce(int width) {
    if (width == 0 || width == 1) {
        return 1;
    }
    if (width == 2) {
        return 2;
    }

    return 2 * countTilingsBruteForce(width - 1) +
           countTilingsBruteForce(width - 3);
}
```

### Optimized
**Approach:** Compute the standard recurrence bottom-up: `dp[i] = 2*dp[i-1] + dp[i-3]`.  
**Data structure:** 1D DP  
**Time:** `O(N)`  
**Space:** `O(N)`

```cpp
#include <vector>

int countTilings(int width) {
    const int modulo = 1'000'000'007;

    if (width == 0 || width == 1) {
        return 1;
    }
    if (width == 2) {
        return 2;
    }

    std::vector<long long> ways(width + 1, 0);
    ways[0] = 1;
    ways[1] = 1;
    ways[2] = 2;

    for (int currentWidth = 3;
         currentWidth <= width; ++currentWidth) {
        ways[currentWidth] =
            (2 * ways[currentWidth - 1] +
             ways[currentWidth - 3]) % modulo;
    }

    return static_cast<int>(ways[width]);
}
```

---

<a id="q17"></a>

## 17. Next Permutation

### Problem statement
Rearrange an array in place into the next lexicographically larger permutation. If none exists, make it the smallest permutation.

### Clarifying questions
- Must be in place?
- Can values repeat?
- What for descending order?
- Need `O(1)` extra space?

### Brute force
**Approach:** Generate all permutations, sort them, find the current one, and take the next.  
**Data structure:** Backtracking + list  
**Time:** `O(N! * N)` or worse with sorting.  
**Space:** `O(N! * N)`

```cpp
#include <algorithm>
#include <map>
#include <set>
#include <vector>

void nextPermutationBruteForce(std::vector<int>& numbers) {
    std::vector<int> current = numbers;
    std::sort(current.begin(), current.end());

    std::set<std::vector<int>> uniquePermutations;
    do {
        uniquePermutations.insert(current);
    } while (std::next_permutation(current.begin(), current.end()));

    auto position = uniquePermutations.find(numbers);
    ++position;

    if (position == uniquePermutations.end()) {
        position = uniquePermutations.begin();
    }
    numbers = *position;
}
```

### Optimized
**Approach:** Find the rightmost pivot that can increase, swap with the smallest larger suffix value, then reverse the suffix.  
**Data structure:** Array  
**Time:** `O(N)`  
**Space:** `O(1)`

```cpp
#include <algorithm>
#include <utility>
#include <vector>

void nextPermutation(vector<int>& numbers) {
    int pivot = numbers.size() - 2;

    while (pivot >= 0 && numbers[pivot] >= numbers[pivot + 1]) {
        --pivot;
    }

    if (pivot >= 0) {
        int successor = numbers.size() - 1;
        while (numbers[successor] <= numbers[pivot]) {
            --successor;
        }
        swap(numbers[pivot], numbers[successor]);
    }

    reverse(numbers.begin() + pivot + 1, numbers.end());
}
```

---

<a id="q18"></a>

## 18. House Robber I

### Problem statement
Each house has money, but adjacent houses cannot both be robbed. Return the maximum amount.

### Clarifying questions
- Are values nonnegative?
- Can we rob no houses?
- Need only the max amount?
- Is the street linear?

### Brute force
**Approach:** At each index, recursively choose rob or skip.  
**Data structure:** Recursion  
**Time:** `O(2^N)`  
**Space:** `O(N)`

```cpp
#include <algorithm>
#include <vector>

int robFromBruteForce(const std::vector<int>& money, int house) {
    if (house >= static_cast<int>(money.size())) {
        return 0;
    }

    int takeCurrent = money[house] +
                      robFromBruteForce(money, house + 2);
    int skipCurrent = robFromBruteForce(money, house + 1);
    return std::max(takeCurrent, skipCurrent);
}

int robHousesBruteForce(const std::vector<int>& money) {
    return robFromBruteForce(money, 0);
}
```

### Optimized
**Approach:** Keep only the previous two DP states.  
**Data structure:** Two variables  
**Time:** `O(N)`  
**Space:** `O(1)`

```cpp
#include <algorithm>
#include <vector>

int robHouses(const std::vector<int>& money) {
    int bestBeforePrevious = 0;
    int bestThroughPrevious = 0;

    for (int currentMoney : money) {
        int bestThroughCurrent = std::max(
            bestThroughPrevious,
            bestBeforePrevious + currentMoney);

        bestBeforePrevious = bestThroughPrevious;
        bestThroughPrevious = bestThroughCurrent;
    }

    return bestThroughPrevious;
}
```

---

<a id="q19"></a>

## 19. House Robber II

### Problem statement
Same as House Robber I, but houses form a circle, so the first and last houses are adjacent.

### Clarifying questions
- Can there be one house?
- Values nonnegative?
- Need only max amount?
- Is the circular restriction the only difference?

### Brute force
**Approach:** Recursively explore rob/skip choices while tracking whether the first house was robbed.  
**Data structure:** Recursion  
**Time:** Exponential  
**Space:** `O(N)`

```cpp
#include <algorithm>
#include <functional>
#include <vector>

int robCircularHousesBruteForce(const std::vector<int>& money) {
    const int houseCount = static_cast<int>(money.size());

    std::function<int(int, bool)> search =
        [&](int house, bool firstHouseWasRobbed) {
            if (house >= houseCount) {
                return 0;
            }

            int skipCurrent = search(house + 1, firstHouseWasRobbed);
            int takeCurrent = 0;

            bool isLastHouse = house == houseCount - 1;
            if (!(isLastHouse && firstHouseWasRobbed)) {
                bool firstIsNowRobbed =
                    firstHouseWasRobbed || house == 0;
                takeCurrent = money[house] +
                              search(house + 2, firstIsNowRobbed);
            }

            return std::max(takeCurrent, skipCurrent);
        };

    return search(0, false);
}
```

### Optimized
**Approach:** Solve two linear cases: exclude last house, or exclude first house.  
**Data structure:** 1D DP with two variables  
**Time:** `O(N)`  
**Space:** `O(1)`

```cpp
#include <algorithm>
#include <vector>

int robLinearRange(const std::vector<int>& money,
                   int start, int end) {
    int bestBeforePrevious = 0;
    int bestThroughPrevious = 0;

    for (int house = start; house <= end; ++house) {
        int bestThroughCurrent = std::max(
            bestThroughPrevious,
            bestBeforePrevious + money[house]);

        bestBeforePrevious = bestThroughPrevious;
        bestThroughPrevious = bestThroughCurrent;
    }
    return bestThroughPrevious;
}

int robCircularHouses(const std::vector<int>& money) {
    if (money.empty()) {
        return 0;
    }
    if (money.size() == 1) {
        return money[0];
    }

    int skipLast = robLinearRange(
        money, 0, static_cast<int>(money.size()) - 2);
    int skipFirst = robLinearRange(
        money, 1, static_cast<int>(money.size()) - 1);

    return std::max(skipLast, skipFirst);
}
```

---

<a id="q20"></a>

## 20. Jump / Reachability Problem

### Problem statement
Assumption: standard Jump Game. Each value is the maximum jump length from that index. Return whether the last index is reachable.

### Clarifying questions
- Are smaller jumps allowed?
- Can values be zero?
- Need boolean only?
- Is input nonempty?

### Brute force
**Approach:** Recursively try every allowed jump from each index.  
**Data structure:** Recursion  
**Time:** Exponential  
**Space:** `O(N)`

```cpp
#include <vector>

bool canReachEndBruteForce(const std::vector<int>& jumps,
                           int position = 0) {
    if (position >= static_cast<int>(jumps.size()) - 1) {
        return true;
    }

    for (int distance = 1;
         distance <= jumps[position]; ++distance) {
        if (canReachEndBruteForce(jumps, position + distance)) {
            return true;
        }
    }
    return false;
}
```

### Optimized
**Approach:** Greedily track the farthest index reachable so far.  
**Data structure:** Greedy variable  
**Time:** `O(N)`  
**Space:** `O(1)`

```cpp
#include <algorithm>
#include <vector>

bool canReachEnd(const std::vector<int>& jumps) {
    int farthestReachable = 0;

    for (int position = 0;
         position < static_cast<int>(jumps.size()); ++position) {
        if (position > farthestReachable) {
            return false;
        }

        farthestReachable = std::max(
            farthestReachable, position + jumps[position]);

        if (farthestReachable >=
            static_cast<int>(jumps.size()) - 1) {
            return true;
        }
    }
    return true;
}
```

---

<a id="q21"></a>

## 21. Median of Two Sorted Arrays Style Problem

### Problem statement
Given two sorted arrays, return the median of all values without fully merging them.

### Clarifying questions
- Can either array be empty?
- Can values repeat?
- Need exact float median?
- Both sorted ascending?

### Brute force
**Approach:** Merge both sorted arrays and read the middle.  
**Data structure:** Two pointers + array  
**Time:** `O(M + N)`  
**Space:** `O(M + N)`

```cpp
#include <vector>

double medianByMerging(const std::vector<int>& first,
                       const std::vector<int>& second) {
    std::vector<int> merged;
    merged.reserve(first.size() + second.size());

    int firstIndex = 0;
    int secondIndex = 0;

    while (firstIndex < static_cast<int>(first.size()) &&
           secondIndex < static_cast<int>(second.size())) {
        if (first[firstIndex] <= second[secondIndex]) {
            merged.push_back(first[firstIndex++]);
        } else {
            merged.push_back(second[secondIndex++]);
        }
    }

    while (firstIndex < static_cast<int>(first.size())) {
        merged.push_back(first[firstIndex++]);
    }
    while (secondIndex < static_cast<int>(second.size())) {
        merged.push_back(second[secondIndex++]);
    }

    int middle = static_cast<int>(merged.size()) / 2;
    if (merged.size() % 2 == 1) {
        return merged[middle];
    }

    return (merged[middle - 1] + merged[middle]) / 2.0;
}
```

### Optimized
**Approach:** Binary search the partition position in the smaller array until left-side values are all `<=` right-side values.  
**Data structure:** Binary search  
**Time:** `O(log(min(M, N)))`  
**Space:** `O(1)`

```cpp
#include <algorithm>
#include <climits>
#include <stdexcept>
#include <vector>

double medianOfSortedArrays(const std::vector<int>& first,
                            const std::vector<int>& second) {
    if (first.size() > second.size()) {
        return medianOfSortedArrays(second, first);
    }

    int firstSize = static_cast<int>(first.size());
    int secondSize = static_cast<int>(second.size());
    int leftSize = (firstSize + secondSize + 1) / 2;

    int low = 0;
    int high = firstSize;

    while (low <= high) {
        int firstCut = low + (high - low) / 2;
        int secondCut = leftSize - firstCut;

        int firstLeft =
            firstCut == 0 ? INT_MIN : first[firstCut - 1];
        int firstRight =
            firstCut == firstSize ? INT_MAX : first[firstCut];
        int secondLeft =
            secondCut == 0 ? INT_MIN : second[secondCut - 1];
        int secondRight =
            secondCut == secondSize ? INT_MAX : second[secondCut];

        if (firstLeft <= secondRight &&
            secondLeft <= firstRight) {
            if ((firstSize + secondSize) % 2 == 1) {
                return std::max(firstLeft, secondLeft);
            }

            return (std::max(firstLeft, secondLeft) +
                    std::min(firstRight, secondRight)) / 2.0;
        }

        if (firstLeft > secondRight) {
            high = firstCut - 1;
        } else {
            low = firstCut + 1;
        }
    }

    throw std::invalid_argument("Input arrays must be sorted");
}
```

---

<a id="q22"></a>

## 22. Open the Lock

### Problem statement
A four-digit lock starts at `0000`. Each move rotates one wheel up or down. Avoid deadends and return the minimum moves to reach the target.

### Clarifying questions
- Does 9 wrap to 0?
- Can start be a deadend?
- Need minimum moves?
- Return `-1` if unreachable?

### Brute force
**Approach:** DFS all possible state paths while tracking the shortest found.  
**Data structure:** DFS + path set  
**Time:** Potentially exponential in explored paths.  
**Space:** Up to `O(10^4)` states.

```cpp
#include <algorithm>
#include <climits>
#include <string>
#include <unordered_set>

void searchLock(const std::string& state,
                const std::string& target,
                const std::unordered_set<std::string>& deadends,
                std::unordered_set<std::string>& currentPath,
                int moves, int& best) {
    if (deadends.count(state) || currentPath.count(state) ||
        moves >= best) {
        return;
    }

    if (state == target) {
        best = moves;
        return;
    }

    currentPath.insert(state);

    for (int wheel = 0; wheel < 4; ++wheel) {
        for (int change : {-1, 1}) {
            std::string next = state;
            int digit = state[wheel] - '0';
            next[wheel] = static_cast<char>(
                '0' + (digit + change + 10) % 10);

            searchLock(next, target, deadends,
                       currentPath, moves + 1, best);
        }
    }

    currentPath.erase(state);
}

int openLockBruteForce(
    const std::vector<std::string>& blocked,
    const std::string& target) {
    std::unordered_set<std::string> deadends(
        blocked.begin(), blocked.end());
    std::unordered_set<std::string> currentPath;
    int best = INT_MAX;

    searchLock("0000", target, deadends, currentPath, 0, best);
    return best == INT_MAX ? -1 : best;
}
```

### Optimized
**Approach:** All moves cost 1, so BFS gives the shortest path in the state graph.  
**Data structure:** Queue + visited set  
**Time:** `O(10^4)`  
**Space:** `O(10^4)`

```cpp
#include <queue>
#include <string>
#include <unordered_set>
#include <vector>

int openLock(const std::vector<std::string>& blocked,
             const std::string& target) {
    std::unordered_set<std::string> deadends(
        blocked.begin(), blocked.end());

    if (deadends.count("0000")) {
        return -1;
    }

    std::queue<std::pair<std::string, int>> queue;
    std::unordered_set<std::string> visited = {"0000"};
    queue.push({"0000", 0});

    while (!queue.empty()) {
        auto [state, moves] = queue.front();
        queue.pop();

        if (state == target) {
            return moves;
        }

        for (int wheel = 0; wheel < 4; ++wheel) {
            for (int change : {-1, 1}) {
                std::string next = state;
                int digit = state[wheel] - '0';
                next[wheel] = static_cast<char>(
                    '0' + (digit + change + 10) % 10);

                if (!deadends.count(next) &&
                    visited.insert(next).second) {
                    queue.push({next, moves + 1});
                }
            }
        }
    }
    return -1;
}
```

---

<a id="q23"></a>

## 23. Merge Two / K Sorted Arrays

### Problem statement
Merge multiple sorted arrays into one sorted result.

### Clarifying questions
- Exactly two arrays or K arrays?
- Can arrays be empty?
- Are duplicates allowed?
- Return a new array?

### Brute force
**Approach:** Concatenate all values and sort.  
**Data structure:** Array  
**Time:** `O(N log N)`, where `N` = total elements.  
**Space:** `O(N)`

```cpp
#include <algorithm>
#include <vector>

std::vector<int> mergeSortedArraysBruteForce(
    const std::vector<std::vector<int>>& arrays) {
    std::vector<int> merged;

    for (const std::vector<int>& array : arrays) {
        merged.insert(merged.end(), array.begin(), array.end());
    }

    std::sort(merged.begin(), merged.end());
    return merged;
}
```

### Optimized
**Approach:** For K arrays, keep the current smallest candidate from each array in a min-heap.  
**Data structure:** Min-heap  
**Time:** `O(N log K)`, where `K` = number of arrays.  
**Space:** `O(K)` auxiliary.

```cpp
#include <functional>
#include <queue>
#include <tuple>
#include <vector>

std::vector<int> mergeSortedArrays(
    const std::vector<std::vector<int>>& arrays) {
    using Entry = std::tuple<int, int, int>;
    std::priority_queue<Entry, std::vector<Entry>,
                        std::greater<Entry>> minHeap;

    for (int arrayIndex = 0;
         arrayIndex < static_cast<int>(arrays.size()); ++arrayIndex) {
        if (!arrays[arrayIndex].empty()) {
            minHeap.push({arrays[arrayIndex][0], arrayIndex, 0});
        }
    }

    std::vector<int> result;

    while (!minHeap.empty()) {
        auto [value, arrayIndex, valueIndex] = minHeap.top();
        minHeap.pop();
        result.push_back(value);

        int nextIndex = valueIndex + 1;
        if (nextIndex < static_cast<int>(arrays[arrayIndex].size())) {
            minHeap.push({
                arrays[arrayIndex][nextIndex],
                arrayIndex,
                nextIndex
            });
        }
    }
    return result;
}
```

---

<a id="q24"></a>

## 24. Celebrity Problem Variation

### Problem statement
A celebrity is known by everyone but knows nobody. Return the celebrity if one exists.

### Clarifying questions
- At most one celebrity?
- How do we query `knows(a,b)`?
- Return `-1` if none?
- Does self-knowledge matter?

### Brute force
**Approach:** Test every person against every other person.  
**Data structure:** None  
**Time:** `O(N^2)`  
**Space:** `O(1)`

```cpp
#include <functional>

int findCelebrityBruteForce(
    int peopleCount,
    const std::function<bool(int, int)>& knows) {
    for (int candidate = 0; candidate < peopleCount; ++candidate) {
        bool isCelebrity = true;

        for (int person = 0; person < peopleCount; ++person) {
            if (person == candidate) {
                continue;
            }

            if (knows(candidate, person) ||
                !knows(person, candidate)) {
                isCelebrity = false;
                break;
            }
        }

        if (isCelebrity) {
            return candidate;
        }
    }
    return -1;
}
```

### Optimized
**Approach:** Eliminate one impossible candidate per comparison, then verify the remaining candidate.  
**Data structure:** Greedy candidate variable  
**Time:** `O(N)`  
**Space:** `O(1)`

```cpp
#include <functional>

int findCelebrity(
    int peopleCount,
    const std::function<bool(int, int)>& knows) {
    int candidate = 0;

    for (int person = 1; person < peopleCount; ++person) {
        if (knows(candidate, person)) {
            candidate = person;
        }
    }

    for (int person = 0; person < peopleCount; ++person) {
        if (person == candidate) {
            continue;
        }

        if (knows(candidate, person) ||
            !knows(person, candidate)) {
            return -1;
        }
    }
    return candidate;
}
```

---

<a id="q25"></a>

## 25. Robot Route to Collect Required Items from a Matrix

### Problem statement
Assumption: the robot moves in 4 directions through open cells and must collect all required items in the minimum number of moves.

### Clarifying questions
- 4 directions?
- Are there blocked cells?
- Can cells be revisited?
- Need minimum moves?
- How many required items can exist?

### Brute force
**Approach:** DFS all routes while tracking `(row, col, collected_items)` state.  
**Data structure:** DFS + bitmask + path set  
**Time:** Exponential in general.  
**Space:** Potentially large state/path space.

```cpp
#include <algorithm>
#include <climits>
#include <functional>
#include <map>
#include <set>
#include <tuple>
#include <utility>
#include <vector>

int collectItemsBruteForce(
    const std::vector<std::vector<char>>& grid,
    std::pair<int, int> start,
    const std::vector<std::pair<int, int>>& itemPositions) {
    const int rows = static_cast<int>(grid.size());
    const int cols = static_cast<int>(grid[0].size());
    const int allItemsMask =
        (1 << static_cast<int>(itemPositions.size())) - 1;

    std::map<std::pair<int, int>, int> itemIndex;
    for (int index = 0;
         index < static_cast<int>(itemPositions.size()); ++index) {
        itemIndex[itemPositions[index]] = index;
    }

    int best = INT_MAX;
    std::set<std::tuple<int, int, int>> currentPath;
    const std::vector<std::pair<int, int>> directions = {
        {1, 0}, {-1, 0}, {0, 1}, {0, -1}
    };

    std::function<void(int, int, int, int)> search =
        [&](int row, int col, int mask, int steps) {
            if (steps >= best) {
                return;
            }

            auto item = itemIndex.find({row, col});
            if (item != itemIndex.end()) {
                mask |= 1 << item->second;
            }

            if (mask == allItemsMask) {
                best = steps;
                return;
            }

            auto state = std::make_tuple(row, col, mask);
            if (currentPath.count(state)) {
                return;
            }

            currentPath.insert(state);
            for (const auto& [rowChange, colChange] : directions) {
                int nextRow = row + rowChange;
                int nextCol = col + colChange;

                if (nextRow >= 0 && nextRow < rows &&
                    nextCol >= 0 && nextCol < cols &&
                    grid[nextRow][nextCol] != '#') {
                    search(nextRow, nextCol, mask, steps + 1);
                }
            }
            currentPath.erase(state);
        };

    search(start.first, start.second, 0, 0);
    return best == INT_MAX ? -1 : best;
}
```

### Optimized
**Approach:** BFS over `(row, col, collected_mask)` because every move costs 1.  
**Data structure:** Queue + visited states + bitmask  
**Time:** `O(M * N * 2^K)`, where `K` = number of items.  
**Space:** `O(M * N * 2^K)`

```cpp
#include <map>
#include <queue>
#include <set>
#include <tuple>
#include <utility>
#include <vector>

int collectAllItems(
    const std::vector<std::vector<char>>& grid,
    std::pair<int, int> start,
    const std::vector<std::pair<int, int>>& itemPositions) {
    const int rows = static_cast<int>(grid.size());
    const int cols = static_cast<int>(grid[0].size());
    const int allItemsMask =
        (1 << static_cast<int>(itemPositions.size())) - 1;

    std::map<std::pair<int, int>, int> itemIndex;
    for (int index = 0;
         index < static_cast<int>(itemPositions.size()); ++index) {
        itemIndex[itemPositions[index]] = index;
    }

    int startMask = 0;
    if (itemIndex.count(start)) {
        startMask |= 1 << itemIndex[start];
    }

    using State = std::tuple<int, int, int, int>;
    std::queue<State> queue;
    std::set<std::tuple<int, int, int>> visited;

    queue.push({start.first, start.second, startMask, 0});
    visited.insert({start.first, start.second, startMask});

    const std::vector<std::pair<int, int>> directions = {
        {1, 0}, {-1, 0}, {0, 1}, {0, -1}
    };

    while (!queue.empty()) {
        auto [row, col, mask, steps] = queue.front();
        queue.pop();

        if (mask == allItemsMask) {
            return steps;
        }

        for (const auto& [rowChange, colChange] : directions) {
            int nextRow = row + rowChange;
            int nextCol = col + colChange;

            if (nextRow < 0 || nextRow >= rows ||
                nextCol < 0 || nextCol >= cols ||
                grid[nextRow][nextCol] == '#') {
                continue;
            }

            int nextMask = mask;
            auto item = itemIndex.find({nextRow, nextCol});
            if (item != itemIndex.end()) {
                nextMask |= 1 << item->second;
            }

            auto state = std::make_tuple(
                nextRow, nextCol, nextMask);

            if (visited.insert(state).second) {
                queue.push({
                    nextRow, nextCol, nextMask, steps + 1
                });
            }
        }
    }
    return -1;
}
```

---

<a id="q26"></a>

## 26. Two Sum Sliding Window Variation

### Problem statement
Assumption: find whether two numbers sum to a target while their indices differ by at most `K`.

### Clarifying questions
- Is K an index-distance limit?
- Return boolean or pair?
- Can values repeat?
- Is K fixed?

### Brute force
**Approach:** For every index, check at most the next K positions.  
**Data structure:** Nested loops  
**Time:** `O(N * K)`  
**Space:** `O(1)`

```cpp
#include <algorithm>
#include <vector>

bool hasTwoSumInWindowBruteForce(
    const std::vector<int>& numbers, int target,
    int maximumDistance) {
    for (int left = 0;
         left < static_cast<int>(numbers.size()); ++left) {
        int end = std::min(
            static_cast<int>(numbers.size()),
            left + maximumDistance + 1);

        for (int right = left + 1; right < end; ++right) {
            if (numbers[left] + numbers[right] == target) {
                return true;
            }
        }
    }
    return false;
}
```

### Optimized
**Approach:** Maintain only the previous K values in a hashmap and check the complement in O(1) average time.  
**Data structure:** Sliding window + hashmap  
**Time:** `O(N)`  
**Space:** `O(K)`

```cpp
#include <unordered_map>
#include <vector>

bool hasTwoSumInWindow(const std::vector<int>& numbers,
                       int target, int maximumDistance) {
    std::unordered_map<int, int> windowCounts;

    for (int index = 0;
         index < static_cast<int>(numbers.size()); ++index) {
        int value = numbers[index];
        int complement = target - value;

        if (windowCounts[complement] > 0) {
            return true;
        }

        ++windowCounts[value];

        if (index >= maximumDistance) {
            int oldValue = numbers[index - maximumDistance];
            --windowCounts[oldValue];

            if (windowCounts[oldValue] == 0) {
                windowCounts.erase(oldValue);
            }
        }
    }
    return false;
}
```

---

# Quick Pattern Index

| Problem | Optimized Pattern |
|---|---|
| Currency Converter | Graph DFS/BFS + memoization |
| Downhill Paths | DFS / backtracking |
| Find Files | Tree DFS / indexing |
| Server Load | Min-heap |
| Streaming Top-K | Min-heap of size K |
| Loyal Customers | Hash maps + sets |
| Task Dependencies | Graph DFS/BFS |
| Longest Delay Chain | DAG DP / memoized DFS |
| Shuffle Array | Fisher-Yates |
| Priority Scheduler | Priority queue |
| Tree Path Sum | Tree DFS |
| Distance K | Tree to graph + BFS |
| Number of Islands | Grid DFS/BFS |
| Rotting Oranges | Multi-source BFS |
| Course Schedule II | Topological DFS |
| Domino/Tromino | 1D DP |
| Next Permutation | Pivot + swap + reverse |
| House Robber I | 1D DP |
| House Robber II | Circular DP |
| Jump Game | Greedy |
| Median Two Sorted Arrays | Binary-search partition |
| Open the Lock | BFS state space |
| Merge K Sorted Arrays | Min-heap |
| Celebrity | Greedy elimination |
| Robot Collect Items | BFS + bitmask |
| Two Sum Window | Sliding window + hashmap |
