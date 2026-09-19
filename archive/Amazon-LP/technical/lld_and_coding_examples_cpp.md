# Amazon SDE-1 LLD / OOD Interview Guide — C++

This guide contains the unique LLD/OOD questions discussed so far, upgraded for a **40–45 minute interview**.

For each problem:

1. Recognize the underlying LLD from the interview story.
2. Clarify scope first.
3. Explain the architecture completely.
4. Use design patterns only when they genuinely fit.
5. Explain entities and relationships in interview-friendly language.
6. State **implementation priority** before coding.
7. Code the highest-value classes first.
8. Finish with verification, edge cases, complexity, and extensibility.

Architecture diagrams are intentionally simple text flows so they render reliably in Markdown.

# Index — Easy to Hard

- [1. Design LRU Cache](#q1) — **Easy–Medium**
- [2. Design Snake and Ladder](#q2) — **Easy–Medium**
- [3. Design Retry Handler](#q3) — **Easy–Medium**
- [4. Design Pub-Sub System](#q4) — **Medium**
- [5. Design API Rate Limiter](#q5) — **Medium**
- [6. Design Logger Rate Limiter](#q6) — **Medium**
- [7. Design Shop in Mall / Checkout System](#q7) — **Medium**
- [8. Design Internal Ticketing System](#q8) — **Medium**
- [9. Design In-Memory File System](#q9) — **Medium**
- [10. Design Linux Find / File Search API](#q10) — **Medium**
- [11. Design Amazon Locker](#q11) — **Medium**
- [12. Design Returns Drop-Off Locker](#q12) — **Medium**
- [13. Design Parking Lot](#q13) — **Medium**
- [14. Design Vending Machine](#q14) — **Medium**
- [15. Design Pizza / Coffee Shop OOD](#q15) — **Medium**
- [16. Design Movie Ticket Booking](#q16) — **Medium–Hard**
- [17. Design Hotel / Restaurant Reservation](#q17) — **Medium–Hard**
- [18. Design Splitwise](#q18) — **Medium–Hard**
- [19. Design Elevator System](#q19) — **Hard**
- [20. Design Library Management System](#q20) — **Hard**
- [21. Design Customer Reviews for Amazon Products](#q21) — **Hard**
- [22. Design Delivery Partner Assignment](#q22) — **Hard**
- [23. Design Chat Messenger with File Download](#q23) — **Hard**
- [24. Design ALB Listener Rule Routing](#q24) — **Hard**
- [25. Design Hierarchical Configuration Service](#q25) — **Hard**
- [26. Design Chess Game](#q26) — **Hard**

---


<a id="q1"></a>
# 1. Design LRU Cache

## 2. How This May Be Asked in an Interview

> You are building a small in-memory cache for a service that repeatedly requests the same data. The cache has a fixed capacity, so when it becomes full you need to discard one existing entry before inserting a new one. Recently accessed entries should stay longer, while entries that have not been used for the longest time should be removed first. Reads and writes are on the hot path, so both operations need to be constant time. Design the component that supports this behavior.

### What I should identify

- fixed-capacity cache
- recently used entries must stay
- least recently used entry must be evicted
- O(1) get and put

### What clues tell me that?

- `"fixed capacity"`
- `"not been used for the longest time"`
- `"constant time reads and writes"`


## 3. Clarifying Questions with Answers
Should the cache support only `get(key)` and `put(key, value)`? **Yes.**  
Should both operations be O(1)? **Yes.**  
Should `get()` make a key most recently used? **Yes.**  
Should `put()` update an existing key and make it most recently used? **Yes.**  
Should a full cache evict the least recently used key? **Yes.**  
Should this be in-memory only? **Yes.**

## 4. Requirements
1. `get(key)` returns value or `-1`.
2. `put(key, value)` inserts or updates.
3. Both operations are O(1).
4. Accessed/updated key becomes MRU.
5. Overflow evicts LRU.

## 5. Design Pattern
Candidate patterns: Composition.  
Final choice: Composition rather than a heavy GoF pattern.  
Where: `LRUCache` combines a hashmap and doubly linked list.  
Why: hashmap gives O(1) lookup; list gives O(1) recency updates.  
Tradeoff: manual pointer management.

## 6. Entities and Relationships
Node: stores key, value, and list pointers.  
DoublyLinkedList: maintains LRU → MRU order.  
LRUCache: coordinates lookup, recency movement, and eviction.

### Architecture
```text
             +------------------+
get/put ---> |     LRUCache     |
             +--------+---------+
                      |
          +-----------+-----------+
          v                       v
 unordered_map<int,Node*>   DoublyLinkedList
        key -> node          LRU <----> MRU
```

### Say It
“The hashmap tells me where the key is. The doubly linked list tells me how recently it was used.”

## 7. Class Design
```cpp
class Node {
public:
    int key;               // cache key
    int value;             // cache value
    Node* prev;            // previous node
    Node* next;            // next node
};

class DoublyLinkedList {
public:
    Node* head;            // dummy before LRU
    Node* tail;            // dummy after MRU

    void addToEnd(Node* node); // make MRU
    void remove(Node* node);   // unlink node
    Node* removeFront();       // remove LRU
};

class LRUCache {
public:
    int capacity;
    unordered_map<int, Node*> cache;
    DoublyLinkedList list;

    int get(int key);
    void put(int key, int value);
};
```

## 8. Implementation

### DSA Used

1. **`unordered_map<string, Topic>`**
   - Purpose: find a topic by name in average O(1).
   - Alternative: `map<string, Topic>`.
   - Advantage: faster average lookup.
   - Tradeoff: no topic ordering.

2. **`vector<Subscriber*>`**
   - Purpose: store subscribers of one topic.
   - Alternative: `unordered_set<Subscriber*>`.
   - Advantage: simple iteration and predictable delivery order.
   - Tradeoff: unsubscribe is O(S) instead of average O(1).

### Implementation Priority

1. `Topic`
2. `PubSubBroker`
3. `Subscriber`

```cpp
#include <bits/stdc++.h>
using namespace std;

class Subscriber {
public:
    virtual void onMessage(const string& message) = 0;

    virtual ~Subscriber() {}
};

class Topic {
private:
    vector<Subscriber*> subscribers;

public:
    void subscribe(Subscriber* subscriber) {
        subscribers.push_back(subscriber);
    }

    void unsubscribe(Subscriber* subscriber) {
        for (int i = 0; i < (int)subscribers.size(); i++) {
            if (subscribers[i] == subscriber) {
                subscribers.erase(subscribers.begin() + i);
                return;
            }
        }
    }

    void publish(const string& message) {
        // Notify every subscriber synchronously.
        for (Subscriber* subscriber : subscribers) {
            try {
                subscriber->onMessage(message);
            } catch (...) {
                // One subscriber failure should not block others.
            }
        }
    }
};

class PubSubBroker {
private:
    unordered_map<string, Topic> topics;

public:
    void createTopic(string topicName) {
        if (!topics.count(topicName)) {
            topics[topicName] = Topic();
        }
    }

    void subscribe(string topicName, Subscriber* subscriber) {
        if (!topics.count(topicName)) {
            return;
        }

        topics[topicName].subscribe(subscriber);
    }

    void publish(string topicName, string message) {
        if (!topics.count(topicName)) {
            return;
        }

        topics[topicName].publish(message);
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    LRUCache cache(2);
    cache.put(1, 10);              // [1]
    cache.put(2, 20);              // [1,2]
    cout << cache.get(1) << endl;  // 10, order [2,1]
    cache.put(3, 30);              // evicts 2
    cout << cache.get(2) << endl;  // -1
}
```

## 10. Edge Cases
Missing key, capacity 1, repeated gets, updating existing key, capacity <= 0.

## 11. Complexity
`get`: O(1).  
`put`: O(1).  
Space: O(n), where `n` = capacity.

## 12. Extensibility Questions
TTL? Add expiry to `Node`.  
LFU? Replace recency list with frequency buckets.  
Thread safety? Lock both structures together.

## 13. Final Summary
Hashmap gives O(1) lookup; doubly linked list gives O(1) recency and eviction.

---

<a id="q2"></a>
# 2. Design Snake and Ladder

## 2. How This May Be Asked in an Interview

> You are implementing the backend logic for a turn-based board game. Several players take turns rolling a die and moving across numbered cells toward the final cell. Some cells immediately move the player forward, while others send the player backward. A player wins only by landing exactly on the final cell. Design the game model and the main turn-processing flow.

### What I should identify

- turn-based board game
- players with positions
- special cells that redirect movement
- winner detection

### What clues tell me that?

- `"move forward or backward from special cells"`
- `"players take turns"`
- `"land exactly on the final cell"`


## 3. Clarifying Questions with Answers
Should the game support multiple players? **Yes.**  
Should the board be 1 to 100, with players starting at 0? **Yes.**  
Should a player need to reach exactly 100 to win? **Yes.**  
Should snakes and ladders be `start -> end` mappings? **Yes.**  
Should dice return 1 to 6? **Yes.**  
Should extra-turn-on-6 be excluded? **Yes.**  
Should this be in-memory only? **Yes.**

## 4. Requirements
Multiple players, board 1–100, exact finish, snakes, ladders, turn rotation.

## 5. Design Pattern
No major pattern required. Simple OOP is sufficient.

## 6. Entities and Relationships
Player: stores identity and position.  
Dice: produces movement value.  
Board: owns snakes, ladders, and position resolution.  
SnakeAndLadderGame: owns turns and winner detection.

### Architecture
```text
Players ---> SnakeAndLadderGame ---> Dice
                     |
                     v
                   Board
              /             \
          snakes           ladders
```

## 7. Class Design
```cpp
class Player {
public:
    string name;
    int position;
};

class Board {
public:
    int size;
    unordered_map<int,int> snakes;
    unordered_map<int,int> ladders;

    int resolvePosition(int position);
};

class SnakeAndLadderGame {
public:
    Board board;
    vector<Player> players;
    int turnIndex;

    bool playTurn(int diceValue);
};
```

## 8. Implementation

### DSA Used

1. **`vector<Player>`**
   - Purpose: store players in turn order.
   - Alternative: `queue<Player>`.
   - Advantage: easy indexed round-robin using `turnIndex`.
   - Tradeoff: changing turn order in the middle is less natural than a queue.

2. **`unordered_map<int,int>`**
   - Purpose: map snake/ladder starting cell to destination.
   - Alternative: `map<int,int>`.
   - Advantage: average O(1) lookup after a move.
   - Tradeoff: no ordering.

### Implementation Priority

1. `SnakeAndLadderGame`
2. `Board`
3. `Player`

```cpp
#include <bits/stdc++.h>
using namespace std;

class Player {
public:
    string name;
    int position;

    Player(string name) {
        this->name = name;
        position = 0;
    }
};

class Board {
public:
    int size;
    unordered_map<int, int> jumps;

    Board(int size = 100) {
        this->size = size;
    }

    void addSnake(int start, int end) {
        jumps[start] = end;
    }

    void addLadder(int start, int end) {
        jumps[start] = end;
    }

    int getFinalPosition(int position) {
        // If this cell starts a snake or ladder, jump once.
        if (jumps.count(position)) {
            return jumps[position];
        }

        return position;
    }
};

class SnakeAndLadderGame {
private:
    Board board;
    vector<Player> players;
    int turnIndex;

public:
    SnakeAndLadderGame(Board board, vector<Player> players) {
        this->board = board;
        this->players = players;
        turnIndex = 0;
    }

    bool playTurn(int diceValue) {
        Player& player = players[turnIndex];

        int nextPosition = player.position + diceValue;

        // Player must land exactly on the last cell.
        if (nextPosition <= board.size) {
            player.position = board.getFinalPosition(nextPosition);
        }

        if (player.position == board.size) {
            return true;
        }

        turnIndex = (turnIndex + 1) % players.size();
        return false;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    Board board;
    board.ladders[4] = 14;
    board.snakes[17] = 7;

    SnakeAndLadderGame game(board, {Player("A"), Player("B")});
    cout << game.playTurn(4) << endl; // false, A lands at 14
}
```

## 10. Edge Cases
Move beyond 100, invalid snake/ladder direction, duplicate starting cell, fewer than two players.

## 11. Complexity
One turn: O(1).  
Space: O(p + s + l).

## 12. Extensibility Questions
Custom board size? Parameterize `Board`.  
Extra turn on 6? Modify turn advancement.  
Special cells? Add a `CellEffect` abstraction.

## 13. Final Summary
Board owns movement rules; game owns turn flow.

---

<a id="q3"></a>
# 3. Design Retry Handler

## 2. How This May Be Asked in an Interview

> A backend service frequently calls external APIs that can occasionally fail because of temporary network issues or overloaded servers. You do not want every caller to write its own retry loop. The system should retry failed operations a configurable number of times and wait between attempts, with the waiting rule potentially changing between fixed, exponential, or jittered delays. Permanent failures should eventually stop retrying. Design a reusable component for this behavior.

### What I should identify

- generic operation execution
- automatic retries
- configurable retry count
- pluggable backoff policy

### What clues tell me that?

- `"temporary failures"`
- `"retry a configurable number of times"`
- `"fixed, exponential, or jittered delays"`


## 3. Clarifying Questions with Answers
Should the API execute one callable? **Yes.**  
Should retries happen only for transient failures? **Yes.**  
Should maximum retries be configurable? **Yes.**  
Should fixed/exponential/jitter backoff be supported? **Yes.**  
Should the interview version skip actual sleeping? **Yes.**

## 4. Requirements
Execute an operation, retry transient failures, configurable retries, pluggable backoff, stop on success.

## 5. Design Pattern
Strategy on `BackoffStrategy`.

## 6. Entities and Relationships
BackoffStrategy: calculates delay.  
ExponentialBackoffStrategy: one concrete policy.  
RetryHandler: owns retry loop.

### Architecture
```text
apiCall ---> RetryHandler ---> BackoffStrategy
                 |
                 +-- success -> return
                 +-- failure -> retry
```

## 7. Class Design
```cpp
class BackoffStrategy {
public:
    virtual int delayMs(int retryNumber) = 0;
};

class RetryHandler {
public:
    int maxRetries;
    BackoffStrategy* strategy;

    bool execute(function<bool()> apiCall);
};
```

## 8. Implementation

### DSA Used

This problem does not need a major container like a heap or hashmap.

1. **Function object: `function<bool()>`**
   - Purpose: lets `RetryHandler` execute any operation that returns success/failure.
   - Alternative: hard-code one API/service method.
   - Advantage: makes the retry handler reusable.
   - Tradeoff: `std::function` has a little runtime/type-erasure overhead.

2. **Strategy interface**
   - Purpose: separate retry timing from retry control flow.
   - Alternative: hard-code exponential backoff inside `RetryHandler`.
   - Advantage: easy to swap fixed, exponential, or jitter strategies.
   - Tradeoff: adds one abstraction.

### Implementation Priority

1. `RetryHandler`
2. `BackoffStrategy`
3. One concrete backoff strategy

```cpp
#include <bits/stdc++.h>
using namespace std;

class BackoffStrategy {
public:
    virtual int getDelay(int retryNumber) = 0;

    virtual ~BackoffStrategy() {}
};

class ExponentialBackoffStrategy : public BackoffStrategy {
private:
    int baseDelay;

public:
    ExponentialBackoffStrategy(int baseDelay) {
        this->baseDelay = baseDelay;
    }

    int getDelay(int retryNumber) override {
        // 100, 200, 400, ...
        return baseDelay * (1 << (retryNumber - 1));
    }
};

class RetryHandler {
private:
    int maxRetries;
    BackoffStrategy* strategy;

public:
    RetryHandler(int maxRetries, BackoffStrategy* strategy) {
        this->maxRetries = maxRetries;
        this->strategy = strategy;
    }

    bool execute(function<bool()> apiCall) {
        // Initial attempt + maxRetries additional attempts.
        for (int attempt = 0; attempt <= maxRetries; attempt++) {
            if (apiCall()) {
                return true;
            }

            // We already used the final allowed attempt.
            if (attempt == maxRetries) {
                break;
            }

            int retryNumber = attempt + 1;
            int delay = strategy->getDelay(retryNumber);

            // In an interview, we only simulate waiting.
            cout << "Retry after " << delay << " ms" << endl;
        }

        return false;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    ExponentialBackoffStrategy strategy(100);
    RetryHandler handler(3, &strategy);

    int attempts = 0;
    cout << handler.execute([&]() {
        attempts++;
        return attempts == 3;
    }) << endl; // true
}
```

## 10. Edge Cases
Success first attempt, zero retries, permanent error, overflow for huge retry counts.

## 11. Complexity
O(r) attempts, O(1) space, where `r` = retries.

## 12. Extensibility Questions
Jitter? Decorate exponential delay.  
Transient classification? Add `RetryPolicy`.  
Async? Schedule retries instead of blocking.

## 13. Final Summary
RetryHandler owns control flow; strategy owns delay calculation.

---

<a id="q4"></a>
# 4. Design Pub-Sub System

## 2. How This May Be Asked in an Interview

> Different components in an application need to react when certain events happen, but the component producing the event should not know all of the consumers. For example, when an order is created, email, inventory, and analytics components may all want to react. Consumers should be able to register interest in different event categories, and a published message should be delivered to everyone currently registered for that category. Design an in-memory version of this communication mechanism.

### What I should identify

- publishers and subscribers
- named event categories/topics
- decoupled event delivery
- one event fan-outs to many consumers

### What clues tell me that?

- `"producer should not know consumers"`
- `"register interest"`
- `"delivered to everyone registered"`


## 3. Clarifying Questions with Answers
Should this be single-process and in-memory? **Yes.**  
Should delivery be synchronous? **Yes.**  
Should subscribers subscribe to multiple topics? **Yes.**  
Should one subscriber failure not block others? **Yes.**  
Should create topic, subscribe, unsubscribe, publish be supported? **Yes.**

## 4. Requirements
Topic management, subscriptions, synchronous publish, failure isolation.

## 5. Design Pattern
Observer.

## 6. Entities and Relationships
Message: payload.  
Subscriber: callback interface.  
Topic: subscriber collection.  
PubSubBroker: coordinator.

### Architecture
```text
Publisher -> Broker -> Topic -> Subscriber A
                         \----> Subscriber B
```

## 7. Class Design
```cpp
class Subscriber {
public:
    virtual void onMessage(const string& message) = 0;
};

class Topic {
public:
    vector<Subscriber*> subscribers;
    void publish(const string& message);
};

class PubSubBroker {
public:
    unordered_map<string, Topic> topics;
    bool publish(string topic, string message);
};
```

## 8. Implementation

### DSA Used

1. **`unordered_map<string, Topic>`**
   - Purpose: find a topic by name in average O(1).
   - Alternative: `map<string, Topic>`.
   - Advantage: faster average lookup.
   - Tradeoff: no topic ordering.

2. **`vector<Subscriber*>`**
   - Purpose: store subscribers of one topic.
   - Alternative: `unordered_set<Subscriber*>`.
   - Advantage: simple iteration and predictable delivery order.
   - Tradeoff: unsubscribe is O(S) instead of average O(1).

### Implementation Priority

1. `Topic`
2. `PubSubBroker`
3. `Subscriber`

```cpp
#include <bits/stdc++.h>
using namespace std;

class Subscriber {
public:
    virtual void onMessage(const string& message) = 0;

    virtual ~Subscriber() {}
};

class Topic {
private:
    vector<Subscriber*> subscribers;

public:
    void subscribe(Subscriber* subscriber) {
        subscribers.push_back(subscriber);
    }

    void unsubscribe(Subscriber* subscriber) {
        for (int i = 0; i < (int)subscribers.size(); i++) {
            if (subscribers[i] == subscriber) {
                subscribers.erase(subscribers.begin() + i);
                return;
            }
        }
    }

    void publish(const string& message) {
        // Notify every subscriber synchronously.
        for (Subscriber* subscriber : subscribers) {
            try {
                subscriber->onMessage(message);
            } catch (...) {
                // One subscriber failure should not block others.
            }
        }
    }
};

class PubSubBroker {
private:
    unordered_map<string, Topic> topics;

public:
    void createTopic(string topicName) {
        if (!topics.count(topicName)) {
            topics[topicName] = Topic();
        }
    }

    void subscribe(
        string topicName,
        Subscriber* subscriber
    ) {
        if (!topics.count(topicName)) {
            return;
        }

        topics[topicName].subscribe(subscriber);
    }

    void publish(
        string topicName,
        string message
    ) {
        if (!topics.count(topicName)) {
            return;
        }

        topics[topicName].publish(message);
    }
};
```


## 9. Dry Run / Verification
```cpp
class PrintSubscriber : public Subscriber {
public:
    void onMessage(const string& message) override {
        cout << message << endl;
    }
};
```

## 10. Edge Cases
Missing topic, duplicate subscription, subscriber throws, unsubscribe missing subscriber.

## 11. Complexity
Publish: O(s), where `s` = subscribers on topic.

## 12. Extensibility Questions
Async delivery? Per-subscriber queues.  
Persistence? Durable log.  
Retries? Delivery policy.

## 13. Final Summary
Topic is the observable; subscribers receive published events.

---

<a id="q5"></a>
# 5. Design API Rate Limiter

## 2. How This May Be Asked in an Interview

> A backend service is receiving bursts of traffic from many clients, and one noisy client can overwhelm the service. Each client should only be allowed a configured number of requests during any recent 60-second period. Every incoming request must be checked before processing, and the decision needs to be fast. Design an in-memory component that tracks this independently for each client.

### What I should identify

- request limiting per client
- rolling/sliding time window
- fast allow/reject decision
- independent state per client

### What clues tell me that?

- `"configured number of requests"`
- `"recent 60-second period"`
- `"allow or reject before processing"`


## 3. Clarifying Questions with Answers
Should this be a single-server in-memory API rate limiter? **Yes.**  
Should the rate limit be based on user ID? **Yes.**  
Should we use a sliding window? **Yes.**  
Should `allowRequest(userId, currentTime)` return only true/false? **Yes.**  
Should every user have the same limit? **Yes.**

## 4. Requirements
Per-user sliding window, same limit for all users, accepted timestamps only, in-memory.

## 5. Design Pattern
No major pattern required for one algorithm.

## 6. Entities and Relationships
UserRequestLog: timestamps for one user.  
RateLimiter: cleans window, checks count, records request.

### Architecture
```text
request(userId,time)
        |
        v
   RateLimiter
        |
        v
logs[userId] ---> deque<timestamps>
```

## 7. Class Design
```cpp
class RateLimiter {
public:
    int maxRequests;
    int windowSeconds;
    unordered_map<string, deque<int>> logs;

    bool allowRequest(string userId, int currentTime);
};
```

## 8. Implementation

### DSA Used

1. **`unordered_map<string, deque<int>>`**
   - Purpose: store request history separately for each `userId`.
   - Alternative: `map<string, deque<int>>`.
   - Advantage: average O(1) user lookup instead of O(log U).
   - Tradeoff: no ordering and slightly higher memory overhead.

2. **`deque<int>`**
   - Purpose: store accepted request timestamps for one user in time order.
   - Alternative: `vector<int>`.
   - Advantage: `push_back()` and `pop_front()` are both O(1).
   - Tradeoff: slightly more memory overhead than a vector.

### Why not use a queue?

A `queue<int>` would also work because we only need:

```text
front
push back
pop front
```

I prefer `deque<int>` because it exposes those operations directly and is a little more flexible for follow-ups.

### Implementation Priority

1. `RateLimiter`
2. No separate request-log class unless the interviewer asks for more abstraction

```cpp
#include <bits/stdc++.h>
using namespace std;

class RateLimiter {
private:
    int maxRequests;
    int windowSize;

    // userId -> timestamps of accepted requests
    unordered_map<string, deque<int>> requests;

public:
    RateLimiter(int maxRequests, int windowSize) {
        this->maxRequests = maxRequests;
        this->windowSize = windowSize;
    }

    bool allowRequest(string userId, int currentTime) {
        // Get this user's current sliding window.
        deque<int>& q = requests[userId];

        // Remove requests that are outside the window.
        while (!q.empty() &&
               q.front() <= currentTime - windowSize) {
            q.pop_front();
        }

        // User already reached the limit.
        if ((int)q.size() >= maxRequests) {
            return false;
        }

        // Accept and record this request.
        q.push_back(currentTime);

        return true;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    RateLimiter limiter(3, 60);
    cout << limiter.allowRequest("U1", 100) << endl; // 1
    cout << limiter.allowRequest("U1", 110) << endl; // 1
    cout << limiter.allowRequest("U1", 120) << endl; // 1
    cout << limiter.allowRequest("U1", 130) << endl; // 0
}
```

## 10. Edge Cases
New user, exact boundary, rejected request not stored, invalid limit/window.

## 11. Complexity
Amortized O(1) per request.  
Space: O(u * r).

## 12. Extensibility Questions
Multiple algorithms? `RateLimitStrategy`.  
Distributed? Redis.  
Different limits? Per-key policy.

## 13. Final Summary
A per-user deque is enough for a clean sliding-window limiter.

---

<a id="q6"></a>
# 6. Design Logger Rate Limiter

## 2. How This May Be Asked in an Interview

> A logging system receives many repeated messages and can flood downstream storage if the same message is printed too frequently. At the same time, the system also has an overall cap on how many log entries may be emitted during a recent time window. A message should only be printed when both the message-specific rule and the global rule allow it. The design should make it easy to add more logging policies later. Build the in-memory component that makes this decision.

### What I should identify

- multiple rate-limit policies
- per-message throttling
- global throttling
- all policies must pass

### What clues tell me that?

- `"same message too frequently"`
- `"overall cap"`
- `"both rules must allow it"`


## 3. Clarifying Questions with Answers
Should there be a per-message limit? **Yes.**  
Should there also be a global message limit? **Yes.**  
Should every policy have to approve before printing? **Yes.**  
Should new policies be easy to add? **Yes.**  
Should this be in-memory and single-process? **Yes.**

## 4. Requirements
Per-message throttling, global throttling, all policies must pass, extensible policy composition.

## 5. Design Pattern
Policy/Strategy composition.

## 6. Entities and Relationships
LogPolicy: interface for one rule.  
PerMessagePolicy: repeated-message limit.  
GlobalRatePolicy: total-message limit.  
LoggerRateLimiter: coordinates policies.

### Architecture
```text
shouldPrint(msg,time)
        |
        v
 LoggerRateLimiter
     /        \
    v          v
PerMessage   Global
 Policy      Policy
```

## 7. Class Design
```cpp
class LogPolicy {
public:
    virtual bool allow(const string& message, int timestamp) = 0;
};

class LoggerRateLimiter {
public:
    bool shouldPrint(string message, int timestamp);
};
```

## 8. Implementation

### DSA Used

1. **`unordered_map<string,int>`**
   - Purpose: store the latest accepted timestamp for each message.
   - Alternative: `map<string,int>`.
   - Advantage: average O(1) message lookup.
   - Tradeoff: no ordering.

2. **`deque<int>`**
   - Purpose: store all globally accepted log timestamps in the active window.
   - Alternative: `vector<int>`.
   - Advantage: expired timestamps can be removed from the front in O(1).
   - Tradeoff: slightly more memory overhead.

### Implementation Priority

1. `LoggerRateLimiter`
2. Split policies into separate classes only if interviewer asks for stronger extensibility

```cpp
#include <bits/stdc++.h>
using namespace std;

class LoggerRateLimiter {
private:
    int repeatInterval;
    int globalLimit;
    int globalWindow;

    // message -> last accepted timestamp
    unordered_map<string, int> lastPrinted;

    // All accepted logs in the active global window
    deque<int> globalLogs;

public:
    LoggerRateLimiter(
        int repeatInterval,
        int globalLimit,
        int globalWindow
    ) {
        this->repeatInterval = repeatInterval;
        this->globalLimit = globalLimit;
        this->globalWindow = globalWindow;
    }

    bool shouldPrint(string message, int currentTime) {
        // Check per-message limit first.
        if (lastPrinted.count(message) &&
            currentTime - lastPrinted[message] < repeatInterval) {
            return false;
        }

        // Remove globally expired timestamps.
        while (!globalLogs.empty() &&
               globalLogs.front() <= currentTime - globalWindow) {
            globalLogs.pop_front();
        }

        // Check global rate limit.
        if ((int)globalLogs.size() >= globalLimit) {
            return false;
        }

        // Commit state only after every rule passes.
        lastPrinted[message] = currentTime;
        globalLogs.push_back(currentTime);

        return true;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    LoggerRateLimiter limiter(10, 3, 60);
    cout << limiter.shouldPrint("A", 1) << endl; // 1
    cout << limiter.shouldPrint("A", 5) << endl; // 0
    cout << limiter.shouldPrint("B", 6) << endl; // 1
}
```

## 10. Edge Cases
Policy rejection must not partially mutate state, exact boundaries, many unique messages.

## 11. Complexity
O(1) average/amortized per message.

## 12. Extensibility Questions
More policies? Introduce `LogPolicy` interface and evaluate vector of policies.  
Distributed? Redis counters/timestamps.  
Thread safety? Lock policy state.

## 13. Final Summary
Keep different policies conceptually separate and commit state only after all checks pass.

---

<a id="q7"></a>
# 7. Design Shop in Mall / Checkout System

## 2. How This May Be Asked in an Interview

> You are building the checkout flow for a small retail shop. Customers can browse products, add quantities to a cart, and then pay for the cart. Inventory must be checked again at checkout because stock could have changed after an item was added to the cart. Stock should only be reduced after payment succeeds, and the system should be able to produce a final bill. Design the core in-memory classes and workflow.

### What I should identify

- product catalog
- inventory
- cart
- checkout/payment
- bill generation

### What clues tell me that?

- `"add quantities to a cart"`
- `"recheck stock at checkout"`
- `"reduce stock only after payment"`


## 3. Clarifying Questions with Answers
Should the shop manage products, inventory, cart, checkout, and billing? **Yes.**  
Should inventory decrease only after successful payment? **Yes.**  
Should payment be simulated? **Yes.**  
Should discounts/coupons stay out of the main implementation? **Yes.**  
Should employees/cashiers be represented simply? **Yes.**

## 4. Requirements
1. Add products and stock.
2. Add items to cart.
3. Validate inventory before checkout.
4. Process payment.
5. Reduce inventory only after payment succeeds.
6. Generate a bill.

## 5. Design Pattern
No major pattern required initially. Strategy becomes useful later for discounts or payment methods.

## 6. Entities and Relationships
Product: stores catalog information and price.  
Inventory: owns stock counts.  
CartItem: product + quantity before checkout.  
Cart: holds selected products.  
Bill: immutable receipt.  
PaymentService: simulates payment.  
ShopService: coordinates inventory, cart, payment, and billing.

### Architecture
```text
Customer ---> Cart
              |
              v
         +-----------+
         |ShopService|
         +-----+-----+
               |
       +-------+--------+
       v                v
   Inventory         Payment
       |                |
       +--------> Bill <-+
```

### Say It
“Cart is temporary customer state. Inventory is authoritative stock state. ShopService revalidates inventory and commits the stock reduction only after payment succeeds.”

## 7. Class Design
```cpp
class Product {
public:
    string id;
    string name;
    double price;
};

class Inventory {
public:
    unordered_map<string,int> stock;

    bool hasStock(string productId, int quantity);
    bool reduceStock(string productId, int quantity);
};

class Cart {
public:
    unordered_map<string,int> quantities;

    bool addItem(string productId, int quantity);
};

class ShopService {
public:
    unordered_map<string,Product> products;
    Inventory inventory;

    bool addToCart(Cart& cart, string productId, int quantity);
    bool checkout(Cart& cart);
};
```

## 8. Implementation

### DSA Used

1. **`unordered_map<string, Product>`**
   - Purpose: find product details by product ID.
   - Alternative: `map`.
   - Advantage: average O(1) lookup.
   - Tradeoff: no ordering.

2. **`unordered_map<string,int>`**
   - Purpose: store inventory quantity and cart quantity by product ID.
   - Alternative: `vector` indexed by product ID.
   - Advantage: works even when product IDs are sparse strings.
   - Tradeoff: hashing overhead.

### Implementation Priority

1. `ShopService`
2. `Inventory`
3. `Cart`
4. Bill/payment details if time remains

```cpp
#include <bits/stdc++.h>
using namespace std;

class Product {
public:
    string id;
    string name;
    double price;

    Product() {}

    Product(string id, string name, double price) {
        this->id = id;
        this->name = name;
        this->price = price;
    }
};

class Inventory {
public:
    unordered_map<string, int> stock;

    bool hasStock(string productId, int quantity) {
        return stock[productId] >= quantity;
    }

    void reduceStock(string productId, int quantity) {
        stock[productId] -= quantity;
    }
};

class Cart {
public:
    unordered_map<string, int> items;

    void add(string productId, int quantity) {
        items[productId] += quantity;
    }
};

class ShopService {
private:
    unordered_map<string, Product> products;
    Inventory inventory;

public:
    void addProduct(Product product, int quantity) {
        products[product.id] = product;
        inventory.stock[product.id] += quantity;
    }

    bool addToCart(Cart& cart, string productId, int quantity) {
        if (!products.count(productId) || quantity <= 0) {
            return false;
        }

        int desiredQuantity = cart.items[productId] + quantity;

        if (!inventory.hasStock(productId, desiredQuantity)) {
            return false;
        }

        cart.add(productId, quantity);
        return true;
    }

    bool checkout(Cart& cart) {
        if (cart.items.empty()) {
            return false;
        }

        double total = 0;

        // Revalidate inventory before payment.
        for (auto& [productId, quantity] : cart.items) {
            if (!inventory.hasStock(productId, quantity)) {
                return false;
            }

            total += products[productId].price * quantity;
        }

        bool paymentSuccessful = total > 0;

        if (!paymentSuccessful) {
            return false;
        }

        // Reduce stock only after payment succeeds.
        for (auto& [productId, quantity] : cart.items) {
            inventory.reduceStock(productId, quantity);
        }

        cart.items.clear();
        return true;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    ShopService shop;

    shop.products["P1"] = Product("P1", "Shirt", 30);
    shop.inventory.stock["P1"] = 5;

    Cart cart;

    cout << shop.addToCart(cart, "P1", 2) << endl; // 1
    cout << shop.checkout(cart) << endl;           // 1
    cout << shop.inventory.stock["P1"] << endl;    // 3
}
```

## 10. Edge Cases
Missing product, insufficient stock, zero quantity, empty cart, payment failure, inventory changes between add-to-cart and checkout.

## 11. Complexity
Let `n` = unique products in the cart.  
Checkout: O(n).  
Space: O(p + c), where `p` = catalog products and `c` = cart entries.

## 12. Extensibility Questions
Discounts? Add `PricingStrategy`.  
Multiple payment methods? Add `PaymentStrategy`.  
Returns? Tie a return workflow to immutable bill items.

## 13. Final Summary
ShopService coordinates the flow, but inventory remains the source of truth and is changed only after payment succeeds.

---

<a id="q8"></a>
# 8. Design Internal Ticketing System

## 2. How This May Be Asked in an Interview

> Employees inside a company need a simple support system for reporting issues such as broken laptops or access problems. Each issue should have a priority and status, can be assigned directly to a support agent, and should keep a discussion history. Agents need to update the status as work progresses and eventually close the issue. Design an in-memory object model and service for this workflow.

### What I should identify

- tickets/issues
- assignment to agents
- priority and status
- comments/history

### What clues tell me that?

- `"reporting issues"`
- `"assigned to a support agent"`
- `"update status and close"`


## 3. Clarifying Questions with Answers
Should internal employees create tickets and support agents resolve them? **Yes.**  
Should the core flow be create, assign, comment, update status, close? **Yes.**  
Should priorities like LOW/MEDIUM/HIGH/URGENT be supported? **Yes.**  
Should statuses like OPEN/IN_PROGRESS/RESOLVED/CLOSED be supported? **Yes.**  
Should teams/queues be excluded from the main implementation? **Yes.**  
Should this be in-memory? **Yes.**

## 4. Requirements
Ticket creation, direct assignment, comments, priority, status updates, close flow, in-memory storage.

## 5. Design Pattern
Facade on `TicketService`.

## 6. Entities and Relationships
User: creates a ticket.  
Agent: resolves a ticket.  
Comment: stores discussion history.  
Ticket: owns ticket state.  
TicketService: coordinates ticket APIs.

### Architecture
```text
User ---> TicketService ---> Ticket <--- Agent
                         |
                         +----> Comments
```

### Say It
“Ticket owns ticket-specific state. TicketService is the facade so callers do not directly manipulate the ticket map, IDs, comments, and assignments.”

## 7. Class Design
```cpp
class Ticket {
public:
    string id;
    string title;
    string status;
    string priority;
    string assignedAgentId;
    vector<string> comments;

    bool assign(string agentId);
    bool addComment(string comment);
    bool updateStatus(string status);
};

class TicketService {
public:
    unordered_map<string,Ticket> tickets;
    int nextId;

    Ticket* createTicket(string title, string priority);
    bool assignTicket(string ticketId, string agentId);
    bool addComment(string ticketId, string comment);
};
```

## 8. Implementation

### DSA Used

1. **`unordered_map<string, Ticket>`**
   - Purpose: find a ticket by ticket ID.
   - Alternative: `map`.
   - Advantage: average O(1) access for assign/comment/status operations.
   - Tradeoff: no ordering by ticket ID.

2. **`vector<string>`**
   - Purpose: keep comments in insertion order.
   - Alternative: `list<string>`.
   - Advantage: simpler and cache-friendly for append/read.
   - Tradeoff: inserting in the middle is expensive, but we do not need that.

### Implementation Priority

1. `TicketManager`
2. `Ticket`
3. User/Agent classes only if interviewer asks

```cpp
#include <bits/stdc++.h>
using namespace std;

class Ticket {
public:
    string id;
    string title;
    string priority;
    string status;
    string assignedAgent;
    vector<string> comments;

    Ticket() {}

    Ticket(string id, string title, string priority) {
        this->id = id;
        this->title = title;
        this->priority = priority;

        status = "OPEN";
        assignedAgent = "";
    }
};

class TicketManager {
private:
    unordered_map<string, Ticket> tickets;
    int nextId;

public:
    TicketManager() {
        nextId = 1;
    }

    string createTicket(string title, string priority) {
        string ticketId = "T" + to_string(nextId++);

        tickets[ticketId] = Ticket(ticketId, title, priority);

        return ticketId;
    }

    bool assignTicket(string ticketId, string agentId) {
        if (!tickets.count(ticketId)) {
            return false;
        }

        Ticket& ticket = tickets[ticketId];

        if (ticket.status == "CLOSED") {
            return false;
        }

        ticket.assignedAgent = agentId;
        ticket.status = "IN_PROGRESS";

        return true;
    }

    bool addComment(string ticketId, string comment) {
        if (!tickets.count(ticketId) || comment.empty()) {
            return false;
        }

        tickets[ticketId].comments.push_back(comment);
        return true;
    }

    bool updateStatus(string ticketId, string newStatus) {
        if (!tickets.count(ticketId)) {
            return false;
        }

        tickets[ticketId].status = newStatus;
        return true;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    TicketService service;

    Ticket* ticket = service.createTicket("Laptop issue", "HIGH");
    service.assignTicket(ticket->id, "A1");
    service.addComment(ticket->id, "Investigating");

    cout << ticket->status << endl; // IN_PROGRESS
}
```

## 10. Edge Cases
Missing ticket, closed-ticket mutation, empty title/comment, reassignment rules, invalid status transition.

## 11. Complexity
Create/get/assign/status: O(1) average.  
Add comment: O(1) amortized.

## 12. Extensibility Questions
Automatic assignment? `AssignmentStrategy`.  
Notifications? `NotificationService`.  
Teams and queues? Add `Team` and queue ownership.

## 13. Final Summary
Ticket owns its local state; TicketService coordinates the workflow.

---

<a id="q9"></a>
# 9. Design In-Memory File System

## 2. How This May Be Asked in an Interview

> You need to build a small in-memory storage hierarchy that behaves like a simplified file system. Users should be able to create folders and files using paths, store text inside files, navigate nested folders, and later support operations such as moving or deleting entries. A folder may contain both files and other folders, and names must be unique within the same folder. Design the core object model and path traversal logic.

### What I should identify

- hierarchical file/folder structure
- path traversal
- files as leaves
- folders containing entries

### What clues tell me that?

- `"nested folders"`
- `"paths"`
- `"folder may contain files and folders"`


## 3. Clarifying Questions with Answers
Should this be an in-memory Unix-like file system? **Yes.**  
Should it support files and folders recursively? **Yes.**  
Should we support create, delete, move, list, read, and write? **Yes.**  
Should names be unique within one folder? **Yes.**  
Should it be single-user and single-threaded? **Yes.**

## 4. Requirements
Hierarchical folders/files, path traversal, create/delete/move/list/read/write, unique sibling names.

## 5. Design Pattern
Composite fits naturally because folders recursively contain file-system entries.

## 6. Entities and Relationships
FileSystemEntry: common abstraction.  
File: leaf with content.  
Folder: composite with child entries.  
FileSystem: path resolver and public API.

### Architecture
```text
FileSystem
   |
   v
 root Folder
   |
   +---- File
   |
   +---- Folder
          |
          +---- File
```

### Say It
“The recursive relationship is the main design. Folder contains generic entries, so folders and files can live in the same children map.”

## 7. Class Design
```cpp
class FileSystemEntry {
public:
    string name;
    virtual bool isFolder() const = 0;
};

class File : public FileSystemEntry {
public:
    string content;
};

class Folder : public FileSystemEntry {
public:
    unordered_map<string,FileSystemEntry*> children;
};

class FileSystem {
public:
    Folder* root;

    bool createFile(string path);
    bool createFolder(string path);
};
```

## 8. Implementation

### DSA Used

1. **`unordered_map<string, Node*>` inside each directory**
   - Purpose: find a child file/folder by name in average O(1).
   - Alternative: `vector<Node*>`.
   - Advantage: faster lookup by child name.
   - Tradeoff: more memory and no sorted listing.

2. **Tree / Composite structure**
   - Purpose: represent nested directories recursively.
   - Alternative: one flat map from full path to entry.
   - Advantage: naturally models folders and supports subtree operations.
   - Tradeoff: path traversal costs O(depth).

### Implementation Priority

1. `FileSystem`
2. `Node`
3. Create/read/write methods
4. Move/delete if time remains

```cpp
#include <bits/stdc++.h>
using namespace std;

class FileSystem {
private:
    class Node {
    public:
        string name;
        bool isFile;
        string content;

        unordered_map<string, Node*> children;

        Node(string name, bool isFile) {
            this->name = name;
            this->isFile = isFile;
        }
    };

    Node* root;

    vector<string> splitPath(string path) {
        vector<string> parts;
        string current;

        for (char ch : path) {
            if (ch == '/') {
                if (!current.empty()) {
                    parts.push_back(current);
                    current.clear();
                }
            } else {
                current += ch;
            }
        }

        if (!current.empty()) {
            parts.push_back(current);
        }

        return parts;
    }

    Node* getNode(string path) {
        vector<string> parts = splitPath(path);
        Node* current = root;

        for (string part : parts) {
            if (!current->children.count(part)) {
                return nullptr;
            }

            current = current->children[part];
        }

        return current;
    }

public:
    FileSystem() {
        root = new Node("/", false);
    }

    bool createFolder(string parentPath, string folderName) {
        Node* parent = getNode(parentPath);

        if (!parent || parent->isFile || parent->children.count(folderName)) {
            return false;
        }

        parent->children[folderName] = new Node(folderName, false);

        return true;
    }

    bool createFile(string parentPath, string fileName) {
        Node* parent = getNode(parentPath);

        if (!parent || parent->isFile || parent->children.count(fileName)) {
            return false;
        }

        parent->children[fileName] = new Node(fileName, true);

        return true;
    }

    bool writeFile(string path, string content) {
        Node* file = getNode(path);

        if (!file || !file->isFile) {
            return false;
        }

        file->content = content;
        return true;
    }

    string readFile(string path) {
        Node* file = getNode(path);

        if (!file || !file->isFile) {
            return "";
        }

        return file->content;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    FileSystem fs;

    cout << fs.createFolder("/docs") << endl;      // 1
    cout << fs.createFile("/docs/a.txt") << endl;  // 1
    cout << fs.createFile("/docs/a.txt") << endl;  // 0
}
```

## 10. Edge Cases
Missing parent, duplicate names, traversing through file, deleting root, moving folder into itself.

## 11. Complexity
Let `d` = path depth.  
Path lookup/create: O(d) average.

## 12. Extensibility Questions
Permissions? Add metadata.  
Symlinks? Add another entry type.  
Persistence? Storage adapter/repository.

## 13. Final Summary
Composite models the hierarchy; FileSystem owns path parsing and traversal.

---

<a id="q10"></a>
# 10. Design Linux Find / File Search API

## 2. How This May Be Asked in an Interview

> You are exposing an API that searches through a directory tree and returns files satisfying user-provided conditions. Today the conditions include things like minimum file size and file extension, but more conditions will be added later. Users may also combine multiple conditions, and the search must include nested subdirectories. Design the API so traversal logic does not need to change whenever a new condition is introduced.

### What I should identify

- recursive directory traversal
- extensible file filters
- filter composition
- search API

### What clues tell me that?

- `"nested subdirectories"`
- `"new conditions later"`
- `"traversal should not change"`


## 3. Clarifying Questions with Answers
Should the search include subdirectories? **Yes.**  
Should filters include size and name/extension? **Yes.**  
Should new filter types be easy to add? **Yes.**  
Should filters be composable? **Yes.**  
Should sorting also be extensible? **Yes.**  
Should this be an API, not a real shell parser? **Yes.**

## 4. Requirements
Recursive traversal, size filter, name/extension filter, filter composition, extensible sorting.

## 5. Design Pattern
Strategy for filters/sorting; Composite-style `AndFilter` for combining conditions.

## 6. Entities and Relationships
FileInfo: file metadata.  
FileFilter: condition interface.  
MinimumSizeFilter: size rule.  
ExtensionFilter: filename/extension rule.  
AndFilter: combines filters.  
FileSearcher: traversal engine.  
SortStrategy: result ordering.

### Architecture
```text
directory ---> FileSearcher
                  |
                  v
              FileFilter
             /    |     \
            v     v      v
         Size   Name    AndFilter
                         /    \
                        v      v
                     Filter  Filter
```

### Say It
“The key separation is traversal versus condition logic. FileSearcher should not know whether the user is filtering by size, extension, owner, or date.”

## 7. Class Design
```cpp
struct FileInfo {
    string name;
    long long sizeBytes;
    bool isDirectory;
    vector<FileInfo> children;
};

class FileFilter {
public:
    virtual bool matches(const FileInfo& file) const = 0;
};

class FileSearcher {
public:
    vector<const FileInfo*> search(const FileInfo& root,
                                   const FileFilter& filter);
};
```

## 8. Implementation

### DSA Used

1. **Tree / DFS**
   - Purpose: recursively traverse all files and subdirectories.
   - Alternative: BFS with a queue.
   - Advantage: DFS is very natural for recursive directory trees and uses only recursion stack.
   - Tradeoff: recursion depth can be large for deeply nested directories.

2. **`vector<File*>`**
   - Purpose: collect matching files.
   - Alternative: `list<File*>`.
   - Advantage: simple append and iteration.
   - Tradeoff: not ideal for frequent middle insertions, which we do not need.

### Implementation Priority

1. `FileSearcher`
2. `FileFilter`
3. Concrete filters like size/name

```cpp
#include <bits/stdc++.h>
using namespace std;

class File {
public:
    string name;
    int size;
    bool isDirectory;
    vector<File*> children;

    File(string name, int size, bool isDirectory) {
        this->name = name;
        this->size = size;
        this->isDirectory = isDirectory;
    }
};

class FileFilter {
public:
    virtual bool matches(File* file) = 0;

    virtual ~FileFilter() {}
};

class SizeFilter : public FileFilter {
private:
    int minSize;

public:
    SizeFilter(int minSize) {
        this->minSize = minSize;
    }

    bool matches(File* file) override {
        return !file->isDirectory && file->size > minSize;
    }
};

class ExtensionFilter : public FileFilter {
private:
    string extension;

public:
    ExtensionFilter(string extension) {
        this->extension = extension;
    }

    bool matches(File* file) override {
        if (file->isDirectory) {
            return false;
        }

        if (file->name.size() < extension.size()) {
            return false;
        }

        string suffix =
            file->name.substr(file->name.size() - extension.size());

        return suffix == extension;
    }
};

class FileSearcher {
private:
    void dfs(
        File* current,
        FileFilter* filter,
        vector<File*>& result
    ) {
        if (!current->isDirectory && filter->matches(current)) {
            result.push_back(current);
        }

        if (!current->isDirectory) {
            return;
        }

        for (File* child : current->children) {
            dfs(child, filter, result);
        }
    }

public:
    vector<File*> search(File* root, FileFilter* filter) {
        vector<File*> result;

        dfs(root, filter, result);

        return result;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    FileInfo root{
        "root", 0, true,
        {
            {"a.xml", 6'000'000, false, {}},
            {"b.txt", 8'000'000, false, {}}
        }
    };

    MinimumSizeFilter size(5'000'000);
    ExtensionFilter xml(".xml");
    AndFilter both({&size, &xml});

    FileSearcher searcher;
    auto result = searcher.search(root, both);

    cout << result[0]->name << endl; // a.xml
}
```

## 10. Edge Cases
Empty directory, no matches, duplicate names in different folders, case sensitivity, symlink cycles in a real filesystem.

## 11. Complexity
Let `n` = entries and `f` = filters.  
Search: O(n * f).  
Space: O(h + k), where `h` = recursion depth and `k` = matches.

## 12. Extensibility Questions
OR conditions? Add `OrFilter`.  
Sorting? Add `SortStrategy`.  
Real filesystem? Replace in-memory traversal with filesystem adapter.

## 13. Final Summary
Traversal is stable; filtering is pluggable.

---

<a id="q11"></a>
# 11. Design Amazon Locker

## 2. How This May Be Asked in an Interview

> Packages arrive at a self-service pickup location containing compartments of different sizes. When a package arrives, the system must choose an available compatible compartment and generate a one-time code for the customer. Later, the customer enters the code, retrieves the package, and the compartment becomes available again. The code must not work a second time. Design the in-memory objects and main workflow.

### What I should identify

- package-to-compartment assignment
- one-time pickup code
- compartment availability
- pickup frees slot

### What clues tell me that?

- `"self-service pickup location"`
- `"one-time code"`
- `"compartment becomes available again"`


## 3. Clarifying Questions with Answers
Should the flow be package arrival, compartment assignment, access code, pickup, release? **Yes.**  
Should package and compartment sizes be SMALL/MEDIUM/LARGE? **Yes.**  
Should size matching be exact only? **Yes.**  
Should access codes be single-use? **Yes.**  
Should this be in-memory? **Yes.**

## 4. Requirements
Assign exact-size free compartment, generate code, pickup using code, free compartment.

## 5. Design Pattern
Facade on `LockerService`. Strategy is a future option for compartment selection.

## 6. Entities and Relationships
Package: delivered item.  
Compartment: physical slot.  
AccessCode: pickup credential.  
Locker: owns compartments.  
LockerService: orchestrates the flow.

### Architecture
```text
Delivery ---> LockerService ---> Locker ---> Compartment
                    |
                    +----> AccessCode ---> Customer Pickup
```

## 7. Class Design
```cpp
class Package {
public:
    string id;
    string size;
};

class Compartment {
public:
    string id;
    string size;
    bool available;
    Package* package;

    bool store(Package* package);
    Package* remove();
};

class LockerService {
public:
    string dropPackage(Package* package);
    Package* pickup(string code);
};
```

## 8. Implementation

### DSA Used

1. **`unordered_map<string, Compartment>`**
   - Purpose: find a compartment by ID in average O(1).
   - Alternative: `vector<Compartment>`.
   - Advantage: direct lookup by string ID.
   - Tradeoff: more memory and no ordering.

2. **`unordered_map<string,string>`**
   - Purpose: map pickup code to compartment ID.
   - Alternative: scan every compartment for a code.
   - Advantage: O(1) average pickup lookup.
   - Tradeoff: extra memory for active codes.

### Implementation Priority

1. `LockerService`
2. `Locker`
3. `Compartment`
4. `Package`

```cpp
#include <bits/stdc++.h>
using namespace std;

class Package {
public:
    string id;
    string size;

    Package(string id, string size) {
        this->id = id;
        this->size = size;
    }
};

class Compartment {
public:
    string id;
    string size;
    bool available;
    Package* package;

    Compartment() {}

    Compartment(string id, string size) {
        this->id = id;
        this->size = size;
        available = true;
        package = nullptr;
    }

    bool canFit(Package* package) {
        return available && size >= package->size;
    }

    void store(Package* package) {
        this->package = package;
        available = false;
    }

    Package* removePackage() {
        Package* result = package;

        package = nullptr;
        available = true;

        return result;
    }
};

class Locker {
public:
    unordered_map<string, Compartment> compartments;

    void addCompartment(string id, string size) {
        compartments[id] = Compartment(id, size);
    }

    Compartment* findAvailableCompartment(Package* package) {
        for (auto& [id, compartment] : compartments) {
            if (compartment.canFit(package)) {
                return &compartment;
            }
        }

        return nullptr;
    }
};

class LockerService {
private:
    Locker locker;
    unordered_map<string, string> codeToCompartment;
    int nextCode;

public:
    LockerService() {
        nextCode = 1000;
    }

    void addCompartment(string id, string size) {
        locker.addCompartment(id, size);
    }

    string dropPackage(Package* package) {
        Compartment* compartment = locker.findAvailableCompartment(package);

        if (compartment == nullptr) {
            return "";
        }

        compartment->store(package);

        string code = to_string(nextCode++);

        codeToCompartment[code] = compartment->id;

        return code;
    }

    Package* pickup(string code) {
        if (!codeToCompartment.count(code)) {
            return nullptr;
        }

        string compartmentId =
            codeToCompartment[code];

        Package* package =
            locker.compartments[compartmentId]
                  .removePackage();

        codeToCompartment.erase(code);

        return package;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    Locker locker;
    locker.compartments["C1"] = Compartment("C1", "SMALL");

    LockerService service(&locker);
    Package package("P1", "SMALL");

    string code = service.dropPackage(&package);
    cout << service.pickup(code)->id << endl;      // P1
    cout << (service.pickup(code) == nullptr) << endl; // 1
}
```

## 10. Edge Cases
No matching compartment, invalid code, reused code, occupied slot, wrong size.

## 11. Complexity
Drop: O(c), where `c` = compartments.  
Pickup: O(1).

## 12. Extensibility Questions
Better selection? Strategy.  
Expiry? Timestamp access codes.  
Notifications? NotificationService.  
Multiple locations? Locker registry.

## 13. Final Summary
LockerService coordinates compartment allocation and single-use-code pickup.

---

<a id="q12"></a>
# 12. Design Returns Drop-Off Locker

## 2. How This May Be Asked in an Interview

> Customers should be able to return packages through self-service compartments. A customer first creates a return and receives a code, then scans that code at the location. The system should choose a compatible free compartment, mark the package as dropped off, and prevent the same return code from being reused. Refund processing and courier pickup are handled elsewhere. Design the core return-dropoff workflow.

### What I should identify

- return request
- single-use return code
- compartment assignment
- drop-off state

### What clues tell me that?

- `"creates a return and receives a code"`
- `"choose a compatible compartment"`
- `"code cannot be reused"`


## 3. Clarifying Questions with Answers
Should the flow be create return request, generate code, scan code, assign compartment, drop package, mark dropped off? **Yes.**  
Should exact size matching be required? **Yes.**  
Should refund and courier pickup be out of scope? **Yes.**  
Should the return code be single-use? **Yes.**

## 4. Requirements
Create return request, generate code, validate code, assign exact-size compartment, mark drop-off complete.

## 5. Design Pattern
Facade on `ReturnDropoffService`.

## 6. Entities and Relationships
ReturnPackage: package being returned.  
ReturnRequest: return code and status.  
Compartment: physical slot.  
Locker: owns compartments.  
ReturnDropoffService: coordinates return flow.

### Architecture
```text
Customer ---> ReturnDropoffService ---> ReturnRequest
                      |
                      v
                    Locker ---> Compartment
```

## 7. Class Design
```cpp
class ReturnRequest {
public:
    string id;
    string code;
    string status;
    ReturnPackage package;
    string compartmentId;
};

class ReturnDropoffService {
public:
    string createReturn(ReturnPackage package);
    bool dropOff(string code);
};
```

## 8. Implementation

### DSA Used

1. **`unordered_map<string, ReturnRequest>`**
   - Purpose: find a return request directly by return code.
   - Alternative: `vector<ReturnRequest>`.
   - Advantage: average O(1) lookup instead of O(N) scan.
   - Tradeoff: hashing/memory overhead.

2. **`unordered_map<string, Compartment>`**
   - Purpose: store locker compartments by ID.
   - Alternative: `vector<Compartment>`.
   - Advantage: direct lookup when needed.
   - Tradeoff: no natural ordering.

### Implementation Priority

1. `ReturnService`
2. `Locker`
3. `Compartment`
4. `ReturnRequest`

```cpp
#include <bits/stdc++.h>
using namespace std;

class ReturnPackage {
public:
    string id;
    string size;

    ReturnPackage() {}

    ReturnPackage(string id, string size) {
        this->id = id;
        this->size = size;
    }
};

class Compartment {
public:
    string id;
    string size;
    bool available;

    Compartment() {}

    Compartment(string id, string size) {
        this->id = id;
        this->size = size;
        available = true;
    }
};

class Locker {
public:
    unordered_map<string, Compartment> compartments;

    Compartment* findAvailable(string size) {
        for (auto& [id, compartment] : compartments) {
            if (compartment.available &&
                compartment.size == size) {
                return &compartment;
            }
        }

        return nullptr;
    }
};

class ReturnRequest {
public:
    string code;
    string status;
    ReturnPackage package;
    string compartmentId;
};

class ReturnService {
private:
    Locker locker;
    unordered_map<string, ReturnRequest> requests;
    int nextCode;

public:
    ReturnService() {
        nextCode = 1000;
    }

    void addCompartment(string id, string size) {
        locker.compartments[id] =
            Compartment(id, size);
    }

    string createReturn(ReturnPackage package) {
        string code = to_string(nextCode++);

        ReturnRequest request;
        request.code = code;
        request.status = "CREATED";
        request.package = package;

        requests[code] = request;

        return code;
    }

    bool dropOff(string code) {
        if (!requests.count(code)) {
            return false;
        }

        ReturnRequest& request = requests[code];

        if (request.status != "CREATED") {
            return false;
        }

        Compartment* compartment =
            locker.findAvailable(request.package.size);

        if (compartment == nullptr) {
            return false;
        }

        compartment->available = false;
        request.compartmentId = compartment->id;
        request.status = "DROPPED_OFF";

        return true;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    Locker locker;
    locker.compartments["C1"] = Compartment("C1", "MEDIUM");

    ReturnDropoffService service(&locker);

    string code = service.createReturn(ReturnPackage("P1", "MEDIUM"));

    cout << service.dropOff(code) << endl; // 1
    cout << service.dropOff(code) << endl; // 0
}
```

## 10. Edge Cases
Invalid code, reused code, no compartment, occupied compartment, repeated drop-off.

## 11. Complexity
Create return: O(1).  
Drop-off: O(c).

## 12. Extensibility Questions
Refund? Trigger `RefundService` after drop-off.  
Courier pickup? Free compartments after collection.  
Expiry? Timestamp return requests.

## 13. Final Summary
ReturnDropoffService validates the request, finds a compartment, and updates both request and locker state.

---

<a id="q13"></a>
# 13. Design Parking Lot

## 2. How This May Be Asked in an Interview

> A multi-level facility receives bikes, cars, and trucks and has parking spaces of different sizes. When a vehicle enters, the system should find a compatible available space and issue a ticket. On exit, the system calculates the fee from the parking duration, processes payment, and makes the space available again. The design should leave room for different allocation or pricing rules later. Build the core in-memory system.

### What I should identify

- vehicle-to-spot allocation
- parking tickets
- entry/exit workflow
- pricing/payment

### What clues tell me that?

- `"compatible available space"`
- `"issue a ticket"`
- `"fee from parking duration"`


## 3. Clarifying Questions with Answers
Should this support multiple floors? **Yes.**  
Should vehicle types include BIKE, CAR, and TRUCK? **Yes.**  
Should spot types include SMALL, MEDIUM, and LARGE? **Yes.**  
Should the core flow be enter, assign spot, ticket, exit, calculate fee, payment, free spot? **Yes.**  
Should payment be simulated? **Yes.**

## 4. Requirements
1. Multiple floors.
2. Compatible spot assignment.
3. Ticket generation.
4. Hourly fee.
5. Payment before freeing spot.
6. In-memory implementation.

## 5. Design Pattern
Facade on `ParkingLotService`. Strategy is useful later for allocation and pricing.

## 6. Entities and Relationships
Vehicle: license and vehicle type.  
ParkingSpot: spot type and occupancy.  
ParkingFloor: owns spots.  
ParkingTicket: represents one parking session.  
PaymentService: processes payment.  
ParkingLotService: coordinates the workflow.

### Architecture
```text
Vehicle ---> ParkingLotService ---> ParkingFloor ---> ParkingSpot
                      |
                      +----> ParkingTicket
                                  |
                                  v
                               Payment
                                  |
                                  v
                              free spot
```

### Say It
“The service owns the entry/exit workflow. Floors own spots. A ticket connects the vehicle, assigned spot, and parking duration.”

## 7. Class Design
```cpp
class ParkingSpot {
public:
    string id;
    string type;
    bool available;

    bool canFit(string vehicleType);
};

class ParkingFloor {
public:
    vector<ParkingSpot> spots;

    ParkingSpot* findSpot(string vehicleType);
};

class ParkingTicket {
public:
    string id;
    string spotId;
    int entryTime;
    bool paid;
};

class ParkingLotService {
public:
    ParkingTicket* enter(Vehicle vehicle, int entryTime);
    bool exit(string ticketId, int exitTime);
};
```

## 8. Implementation

### DSA Used

1. **`vector<ParkingSpot>`**
   - Purpose: store spots on a floor and scan for a compatible one.
   - Alternative: separate queues/sets by spot type.
   - Advantage: simplest interview implementation.
   - Tradeoff: finding a spot is O(S).

2. **`unordered_map<string, ParkingTicket>`**
   - Purpose: find an active ticket by ticket ID.
   - Alternative: `vector<ParkingTicket>`.
   - Advantage: average O(1) lookup on exit.
   - Tradeoff: extra hashing memory.

### Implementation Priority

1. `ParkingLot`
2. `ParkingSpot`
3. `ParkingTicket`
4. Multiple-floor optimization if time remains

```cpp
#include <bits/stdc++.h>
using namespace std;

class Vehicle {
public:
    string plate;
    string type;
};

class ParkingSpot {
public:
    string id;
    string type;
    bool available;

    ParkingSpot(string id, string type) {
        this->id = id;
        this->type = type;
        available = true;
    }

    bool canFit(string vehicleType) {
        if (!available) {
            return false;
        }

        if (vehicleType == "BIKE") {
            return true;
        }

        if (vehicleType == "CAR") {
            return type == "MEDIUM" ||
                   type == "LARGE";
        }

        return type == "LARGE";
    }
};

class ParkingTicket {
public:
    string id;
    string spotId;
    int entryTime;
};

class ParkingLot {
private:
    vector<ParkingSpot> spots;
    unordered_map<string, ParkingTicket> tickets;
    int nextTicketId;

public:
    ParkingLot() {
        nextTicketId = 1;
    }

    void addSpot(string id, string type) {
        spots.push_back(ParkingSpot(id, type));
    }

    string park(Vehicle vehicle, int entryTime) {
        for (ParkingSpot& spot : spots) {
            if (spot.canFit(vehicle.type)) {
                spot.available = false;

                string ticketId = "T" + to_string(nextTicketId++);

                tickets[ticketId] = {ticketId, spot.id, entryTime};

                return ticketId;
            }
        }

        return "";
    }

    bool unpark(string ticketId) {
        if (!tickets.count(ticketId)) {
            return false;
        }

        string spotId = tickets[ticketId].spotId;

        for (ParkingSpot& spot : spots) {
            if (spot.id == spotId) {
                spot.available = true;
                break;
            }
        }

        tickets.erase(ticketId);
        return true;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    ParkingFloor floor;
    floor.spots.push_back({"S1", "MEDIUM", true});

    ParkingLotService lot({floor});

    ParkingTicket* ticket =
        lot.enter({"ABC123", "CAR"}, 10);

    cout << ticket->spotId << endl;         // S1
    cout << lot.exit(ticket->id, 13) << endl; // 1
}
```

## 10. Edge Cases
No compatible spot, invalid ticket, double exit, payment failure, partial-hour pricing, same vehicle entering twice.

## 11. Complexity
Let `s` = total spots.  
Entry: O(s).  
Exit: O(1) with indexed ticket/spot.  
Space: O(s + t).

## 12. Extensibility Questions
Nearest spot? `SpotAllocationStrategy`.  
EV charging? Add spot capability/type.  
Availability counters? Maintain per-floor counts.  
Concurrency? Lock spot assignment.

## 13. Final Summary
ParkingLotService coordinates entry/exit; spot-selection logic can later move behind Strategy.

---

<a id="q14"></a>
# 14. Design Vending Machine

## 2. How This May Be Asked in an Interview

> A machine contains several products with limited stock. A customer selects one product, inserts money, and may only receive the product once enough money has been provided. The valid operations depend on what stage of the transaction the machine is currently in, and cancellation should reset the transaction. Design the object model and main transaction flow.

### What I should identify

- product inventory
- transaction states
- selection/payment/dispense
- state-dependent operations

### What clues tell me that?

- `"selects a product"`
- `"only receive after enough money"`
- `"operations depend on current stage"`


## 3. Clarifying Questions with Answers
Should the machine manage product inventory? **Yes.**  
Should a user select a product before payment? **Yes.**  
Should payment happen before dispensing? **Yes.**  
Should we model states like IDLE, SELECTED, PAID, and DISPENSING? **Yes.**  
Should cancel/refund be supported simply? **Yes.**  
Should this be one in-memory machine? **Yes.**

## 4. Requirements
Select product, validate stock, accept payment, dispense product, reduce inventory, cancel/reset transaction.

## 5. Design Pattern
State pattern is appropriate because legal operations depend strongly on current machine state.

## 6. Entities and Relationships
Product: item ID and price.  
Inventory: stock by product.  
VendingMachineState: current transaction state.  
VendingMachine: coordinates selection, payment, dispense, and reset.

### Architecture
```text
Customer
   |
   v
VendingMachine
   |
   +--> Inventory
   |
   +--> State Flow:
        IDLE -> SELECTED -> PAID -> DISPENSING -> IDLE
```

### Say It
“The interview implementation can keep state as an enum/string, but architecturally this is a State-pattern problem because allowed actions depend on current state.”

## 7. Class Design
```cpp
class Product {
public:
    string id;
    double price;
};

class VendingMachine {
public:
    unordered_map<string,Product> products;
    unordered_map<string,int> inventory;
    string state;
    string selectedProductId;
    double insertedAmount;

    bool selectProduct(string productId);
    bool insertMoney(double amount);
    bool dispense();
    void cancel();
};
```

## 8. Implementation

### DSA Used

1. **`unordered_map<string, Product>`**
   - Purpose: store product details by ID.
   - Alternative: `vector<Product>`.
   - Advantage: average O(1) lookup by product ID.
   - Tradeoff: no ordering.

2. **`unordered_map<string,int>`**
   - Purpose: store inventory count by product ID.
   - Alternative: keep quantity inside `Product`.
   - Advantage: separates product metadata from stock state.
   - Tradeoff: two structures must stay consistent.

### Implementation Priority

1. `VendingMachine`
2. Product/inventory data
3. Full State pattern only if interviewer asks

```cpp
#include <bits/stdc++.h>
using namespace std;

class Product {
public:
    string id;
    int price;

    Product() {}

    Product(string id, int price) {
        this->id = id;
        this->price = price;
    }
};

class VendingMachine {
private:
    unordered_map<string, Product> products;
    unordered_map<string, int> inventory;

    string selectedProduct;
    int insertedMoney;
    string state;

public:
    VendingMachine() {
        selectedProduct = "";
        insertedMoney = 0;
        state = "IDLE";
    }

    void addProduct(string id, int price, int quantity) {
        products[id] = Product(id, price);
        inventory[id] += quantity;
    }

    bool selectProduct(string id) {
        if (state != "IDLE") {
            return false;
        }

        if (!products.count(id) ||
            inventory[id] == 0) {
            return false;
        }

        selectedProduct = id;
        state = "SELECTED";

        return true;
    }

    bool insertMoney(int amount) {
        if (state != "SELECTED" || amount <= 0) {
            return false;
        }

        insertedMoney += amount;

        if (insertedMoney >=
            products[selectedProduct].price) {
            state = "PAID";
        }

        return true;
    }

    bool dispense() {
        if (state != "PAID") {
            return false;
        }

        inventory[selectedProduct]--;

        selectedProduct = "";
        insertedMoney = 0;
        state = "IDLE";

        return true;
    }

    void cancel() {
        selectedProduct = "";
        insertedMoney = 0;
        state = "IDLE";
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    VendingMachine machine;
    machine.addProduct({"P1", 2.0}, 2);

    cout << machine.selectProduct("P1") << endl; // 1
    cout << machine.insertMoney(2.0) << endl;    // 1
    cout << machine.dispense() << endl;          // 1
}
```

## 10. Edge Cases
Out of stock, insufficient money, extra money/change, cancel after payment, invalid state transition, dispense failure.

## 11. Complexity
Product lookup and stock update: O(1).  
Space: O(p), where `p` = products.

## 12. Extensibility Questions
Actual State pattern? One class per machine state.  
Change-making? Add coin inventory and change algorithm.  
Multiple payment types? `PaymentStrategy`.

## 13. Final Summary
The key design challenge is state-dependent behavior and inventory consistency.

---

<a id="q15"></a>
# 15. Design Pizza / Coffee Shop OOD

## 2. How This May Be Asked in an Interview

> A food shop lets customers create configurable items and place several of them into one order. Each item has a base price and optional add-ons that change the final price. The business may start with pizzas but later introduce drinks or other menu items without rewriting the entire order flow. Design the object model so item types and customizations can evolve independently.

### What I should identify

- generic menu items
- configurable add-ons
- order aggregation
- polymorphic pricing

### What clues tell me that?

- `"base price and optional add-ons"`
- `"multiple items in one order"`
- `"new item types later"`


## 3. Clarifying Questions with Answers
Should customers customize items with options/toppings? **Yes.**  
Should pricing be base price plus selected add-ons? **Yes.**  
Should an order contain multiple items? **Yes.**  
Should payment be simulated? **Yes.**  
Should changing requirements, like pizza becoming coffee, be expected? **Yes.**

## 4. Requirements
Configurable menu items, add-ons, dynamic price calculation, order aggregation, payment.

## 5. Design Pattern
Composition first. Decorator is appropriate when add-ons need independent behavior. Strategy can handle pricing rules.

## 6. Entities and Relationships
MenuItem: common purchasable abstraction.  
Pizza/Coffee: concrete item.  
Option/Topping: customization.  
Order: owns multiple items.  
PaymentService: handles payment.

### Architecture
```text
Customer ---> Order
              |
              +--> Pizza + toppings
              |
              +--> Coffee + options
              |
              v
           Payment
```

### Say It
“The important part is not hard-coding pizza everywhere. I want a generic `MenuItem` contract so a coffee-shop variation does not force me to redesign the order flow.”

## 7. Class Design
```cpp
class MenuItem {
public:
    virtual double price() const = 0;
    virtual string name() const = 0;
};

class Pizza : public MenuItem {
public:
    string size;
    vector<string> toppings;

    double price() const override;
};

class Order {
public:
    vector<MenuItem*> items;

    void addItem(MenuItem* item);
    double total() const;
};
```

## 8. Implementation

### DSA Used

1. **`vector<MenuItem*>`**
   - Purpose: store all items in an order.
   - Alternative: `list<MenuItem*>`.
   - Advantage: simple append and iteration.
   - Tradeoff: removing from the middle is O(N).

2. **`vector<string>`**
   - Purpose: store toppings/options on a configurable item.
   - Alternative: `unordered_set<string>`.
   - Advantage: preserves insertion order and allows duplicates if business rules permit.
   - Tradeoff: checking whether a topping already exists is O(T).

### Implementation Priority

1. `Order`
2. `MenuItem`
3. One concrete item like `Pizza`
4. Additional item types only if interviewer changes requirements

```cpp
#include <bits/stdc++.h>
using namespace std;

class MenuItem {
public:
    virtual double getPrice() = 0;

    virtual ~MenuItem() {}
};

class Pizza : public MenuItem {
private:
    string size;
    vector<string> toppings;

public:
    Pizza(string size, vector<string> toppings) {
        this->size = size;
        this->toppings = toppings;
    }

    double getPrice() override {
        double price =
            (size == "LARGE") ? 15.0 : 10.0;

        price += toppings.size() * 1.5;

        return price;
    }
};

class Coffee : public MenuItem {
private:
    string size;
    bool extraShot;

public:
    Coffee(string size, bool extraShot) {
        this->size = size;
        this->extraShot = extraShot;
    }

    double getPrice() override {
        double price =
            (size == "LARGE") ? 6.0 : 4.0;

        if (extraShot) {
            price += 1.0;
        }

        return price;
    }
};

class Order {
private:
    vector<MenuItem*> items;

public:
    void addItem(MenuItem* item) {
        items.push_back(item);
    }

    double getTotal() {
        double total = 0;

        for (MenuItem* item : items) {
            total += item->getPrice();
        }

        return total;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    Pizza pizza("LARGE", {"CHEESE", "OLIVE"});
    Coffee coffee("SMALL", true);

    Order order;
    order.addItem(&pizza);
    order.addItem(&coffee);

    cout << order.total() << endl;
}
```

## 10. Edge Cases
Invalid option, duplicate topping rules, unavailable ingredient, empty order, price changes after order creation.

## 11. Complexity
Let `i` = order items and `t` = total options.  
Total price: O(i + t).

## 12. Extensibility Questions
Discounts? `PricingStrategy`.  
Decorator? Wrap menu items with add-on decorators.  
Inventory? Track ingredient availability separately.

## 13. Final Summary
A generic menu-item abstraction makes the design resilient to changing shop requirements.

---

<a id="q16"></a>
# 16. Design Movie Ticket Booking

## 2. How This May Be Asked in an Interview

> Users of a booking application can choose a movie show and select specific seats. Once selected, those seats should become temporarily unavailable while payment is being attempted so another user cannot take them. Successful payment permanently books the seats, while failure should release them. Seat availability is different for each show even when two shows use the same physical screen. Design the main booking workflow.

### What I should identify

- show-specific seat state
- temporary seat hold
- payment
- booking confirmation/release

### What clues tell me that?

- `"specific seats"`
- `"temporarily unavailable during payment"`
- `"availability is different for each show"`


## 3. Clarifying Questions with Answers
Should users browse movies, shows, and seats? **Yes.**  
Should users select specific seats? **Yes.**  
Should selected seats be held before payment? **Yes.**  
Should successful payment convert held seats to booked? **Yes.**  
Should payment failure release seats? **Yes.**  
Should cancellation be out of scope? **Yes.**

## 4. Requirements
Browse shows, view show-specific seats, hold seats, pay, confirm booking, release seats on payment failure.

## 5. Design Pattern
Facade on `BookingService`. Seat state is simple enough to model with an enum/string instead of a full State hierarchy.

## 6. Entities and Relationships
Movie: movie metadata.  
Show: one movie at one time.  
ShowSeat: seat state for a specific show.  
Booking: selected show/seats and booking status.  
PaymentService: payment.  
BookingService: coordinator.

### Architecture
```text
User ---> BookingService ---> Show ---> ShowSeat
                    |
                    +----> Booking ---> Payment
```

### Say It
“Seat availability belongs to a show, not globally to the physical screen, because the same physical seat can be available for one show and booked for another.”

## 7. Class Design
```cpp
class ShowSeat {
public:
    string seatId;
    string status;          // AVAILABLE / HELD / BOOKED
};

class Show {
public:
    string id;
    unordered_map<string,ShowSeat> seats;

    bool hold(vector<string> seatIds);
    bool book(vector<string> seatIds);
    void release(vector<string> seatIds);
};

class BookingService {
public:
    Booking* createHold(string showId, vector<string> seats);
    bool confirm(string bookingId);
};
```

## 8. Implementation

### DSA Used

1. **`unordered_map<string, SeatStatus>`**
   - Purpose: find seat state by seat ID in average O(1).
   - Alternative: `vector<Seat>`.
   - Advantage: direct lookup for selected seat IDs.
   - Tradeoff: no seat ordering.

2. **`unordered_map<string, Booking>`**
   - Purpose: retrieve booking by booking ID.
   - Alternative: `vector<Booking>`.
   - Advantage: average O(1) lookup for confirmation.
   - Tradeoff: extra hashing memory.

### Implementation Priority

1. `BookingService`
2. `Show`
3. Seat status
4. Booking/payment details

```cpp
#include <bits/stdc++.h>
using namespace std;

class Show {
public:
    string id;

    // seatId -> AVAILABLE / HELD / BOOKED
    unordered_map<string, string> seats;

    bool holdSeats(vector<string> seatIds) {
        // First verify every requested seat.
        for (string seatId : seatIds) {
            if (!seats.count(seatId) ||
                seats[seatId] != "AVAILABLE") {
                return false;
            }
        }

        // Hold only after all seats pass validation.
        for (string seatId : seatIds) {
            seats[seatId] = "HELD";
        }

        return true;
    }

    void bookSeats(vector<string> seatIds) {
        for (string seatId : seatIds) {
            seats[seatId] = "BOOKED";
        }
    }

    void releaseSeats(vector<string> seatIds) {
        for (string seatId : seatIds) {
            if (seats[seatId] == "HELD") {
                seats[seatId] = "AVAILABLE";
            }
        }
    }
};

class Booking {
public:
    string id;
    string showId;
    vector<string> seatIds;
    string status;
};

class BookingService {
private:
    unordered_map<string, Show> shows;
    unordered_map<string, Booking> bookings;
    int nextBookingId;

public:
    BookingService() {
        nextBookingId = 1;
    }

    void addShow(Show show) {
        shows[show.id] = show;
    }

    string createBooking(
        string showId,
        vector<string> seatIds
    ) {
        if (!shows.count(showId)) {
            return "";
        }

        if (!shows[showId].holdSeats(seatIds)) {
            return "";
        }

        string bookingId =
            "B" + to_string(nextBookingId++);

        bookings[bookingId] =
            {bookingId, showId, seatIds, "PENDING"};

        return bookingId;
    }

    bool confirmBooking(string bookingId) {
        if (!bookings.count(bookingId)) {
            return false;
        }

        Booking& booking = bookings[bookingId];

        bool paymentSuccess = true;

        if (!paymentSuccess) {
            shows[booking.showId]
                .releaseSeats(booking.seatIds);

            booking.status = "FAILED";
            return false;
        }

        shows[booking.showId]
            .bookSeats(booking.seatIds);

        booking.status = "CONFIRMED";

        return true;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    Show show;
    show.id = "S1";
    show.seats["A1"] = {"A1", "AVAILABLE"};
    show.seats["A2"] = {"A2", "AVAILABLE"};

    BookingService service;
    service.addShow(show);

    Booking* booking = service.createHold("S1", {"A1", "A2"});
    cout << (booking != nullptr) << endl; // 1
    cout << service.confirm(booking->id) << endl; // 1
}
```

## 10. Edge Cases
Partial hold, duplicate seat IDs, already-held seat, payment failure, hold expiration, concurrent booking.

## 11. Complexity
For `k` selected seats, hold/book/release are O(k).

## 12. Extensibility Questions
Hold expiry? Timestamp held seats.  
Cancellation? Booking transition + release.  
Concurrency? Lock show-seat updates.

## 13. Final Summary
The core invariant is show-specific seat state with an atomic hold → payment → book flow.

---

<a id="q17"></a>
# 17. Design Hotel / Restaurant Reservation

## 2. How This May Be Asked in an Interview

> A reservation platform manages resources that can only be used by one customer during a given time interval. Users should be able to check whether a resource is available, reserve it for a start and end time, and later cancel the reservation. Two active reservations for the same resource must never overlap. The same core design should work for things like hotel rooms or restaurant tables. Design the service.

### What I should identify

- time-based reservations
- resource availability
- overlap prevention
- cancellation

### What clues tell me that?

- `"start and end time"`
- `"must never overlap"`
- `"rooms or tables"`


## 3. Clarifying Questions with Answers
Should a customer reserve one resource for a time range? **Yes.**  
Should double-booking be prevented? **Yes.**  
Should cancellation be supported? **Yes.**  
Should payment be optional/simple? **Yes.**  
Should the same architecture apply to rooms/tables/seats? **Yes.**

## 4. Requirements
Check availability, create reservation, prevent overlaps, cancel, associate reservation with customer/resource.

## 5. Design Pattern
Facade on `ReservationService`. Strategy can later handle pricing or resource selection.

## 6. Entities and Relationships
Customer: reservation owner.  
Resource: hotel room/table/seat.  
Reservation: time range and status.  
ReservationService: availability and booking coordinator.

### Architecture
```text
Customer ---> ReservationService ---> Resource
                      |
                      v
                Reservations
```

### Say It
“The important invariant is no overlapping confirmed reservations for the same resource.”

## 7. Class Design
```cpp
class Reservation {
public:
    string id;
    string resourceId;
    int startTime;
    int endTime;
    string status;
};

class ReservationService {
public:
    unordered_map<string,vector<Reservation>> reservationsByResource;

    bool isAvailable(string resourceId, int start, int end);
    Reservation* reserve(string resourceId, int start, int end);
};
```

## 8. Implementation

### DSA Used

1. **`unordered_map<string, vector<Reservation>>`**
   - Purpose: group reservations by resource ID.
   - Alternative: one global vector of reservations.
   - Advantage: only scan reservations for the requested room/table.
   - Tradeoff: availability check is still O(R) for that resource.

2. **Interval overlap check**
   - Purpose: detect conflicting time ranges.
   - Alternative: interval tree.
   - Advantage: simple and interview-friendly.
   - Tradeoff: slower when a resource has many reservations.

### Implementation Priority

1. `ReservationService`
2. `Reservation`
3. Resource/Customer classes only if needed

```cpp
#include <bits/stdc++.h>
using namespace std;

class Reservation {
public:
    string id;
    string resourceId;
    int startTime;
    int endTime;
    string status;
};

class ReservationService {
private:
    unordered_map<string, vector<Reservation>> reservations;
    int nextId;

public:
    ReservationService() {
        nextId = 1;
    }

    bool isAvailable( string resourceId, int startTime, int endTime ) {
        for (Reservation& reservation : reservations[resourceId]) {
            if (reservation.status != "CONFIRMED") {
                continue;
            }

            bool overlap = max(startTime, reservation.startTime) < min(endTime, reservation.endTime);

            if (overlap) {
                return false;
            }
        }

        return true;
    }

    string reserve( string resourceId, int startTime, int endTime) {
        if (startTime >= endTime) {
            return "";
        }

        if (!isAvailable( resourceId, startTime, endTime)) {
            return "";
        }

        string reservationId = "R" + to_string(nextId++);

        reservations[resourceId].push_back({
            reservationId,
            resourceId,
            startTime,
            endTime,
            "CONFIRMED"
        });

        return reservationId;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    ReservationService service;

    cout << (service.reserve("ROOM1", 10, 12) != nullptr) << endl; // 1
    cout << (service.reserve("ROOM1", 11, 13) == nullptr) << endl; // 1
    cout << (service.reserve("ROOM1", 12, 13) != nullptr) << endl; // 1
}
```

## 10. Edge Cases
Adjacent reservations, invalid time range, cancellation, overlapping requests, missing resource.

## 11. Complexity
Naive availability: O(r), where `r` = reservations for one resource.

## 12. Extensibility Questions
Faster overlap search? Sorted intervals/interval tree.  
Waitlist? Queue per resource/time.  
Different resource types? `ReservableResource` abstraction.

## 13. Final Summary
ReservationService owns the no-overlap invariant.

---

<a id="q18"></a>
# 18. Design Splitwise

## 2. How This May Be Asked in an Interview

> A group of friends frequently pays expenses on behalf of one another. One person may pay the full amount while the cost is divided among several participants using equal, exact, or percentage-based splits. The system should continuously track who owes whom and allow users to settle outstanding balances later. Design the in-memory model and expense-processing flow.

### What I should identify

- shared expenses
- multiple split algorithms
- who-owes-whom balances
- settlement

### What clues tell me that?

- `"one person pays"`
- `"equal, exact, or percentage"`
- `"track who owes whom"`


## 3. Clarifying Questions with Answers
Should we support groups? **Yes.**  
Should one user pay the full expense? **Yes.**  
Should split types be EQUAL, EXACT, and PERCENTAGE? **Yes.**  
Should balances track who owes whom? **Yes.**  
Should settlement reduce balances? **Yes.**  
Should this be in-memory? **Yes.**

## 4. Requirements
Groups, users, expenses, split calculation, balance tracking, settlement.

## 5. Design Pattern
Strategy for split calculation.

## 6. Entities and Relationships
User: participant.  
Group: members.  
Expense: payer + amount + split type.  
Split: user + owed amount.  
SplitStrategy: calculates shares.  
BalanceSheet: stores debts.  
SplitwiseService: coordinator.

### Architecture
```text
User/Group ---> SplitwiseService ---> SplitStrategy
                      |
                      +----> Expense
                      |
                      +----> BalanceSheet
```

### Say It
“SplitStrategy owns the math. BalanceSheet owns who-owes-whom state. SplitwiseService coordinates the expense flow.”

## 7. Class Design
```cpp
class SplitStrategy {
public:
    virtual vector<double> calculate(
        double amount,
        int count,
        const vector<double>& values
    ) = 0;
};

class BalanceSheet {
public:
    unordered_map<string,unordered_map<string,double>> balances;

    void addDebt(string from, string to, double amount);
};

class SplitwiseService {
public:
    bool addExpense(
        string payer,
        vector<string> users,
        double amount,
        SplitStrategy* strategy,
        vector<double> values
    );
};
```

## 8. Implementation

### DSA Used

1. **Nested `unordered_map`**
   - Purpose: store `fromUser -> toUser -> amount owed`.
   - Alternative: graph with explicit edge objects.
   - Advantage: direct average O(1) balance lookup/update.
   - Tradeoff: reciprocal debts may need later simplification.

2. **`vector<string>`**
   - Purpose: store users participating in an expense.
   - Alternative: `unordered_set`.
   - Advantage: keeps participant order aligned with calculated shares.
   - Tradeoff: duplicate-user validation requires extra checking.

### Implementation Priority

1. `Splitwise`
2. Balance map
3. Split strategy
4. Equal split first, then exact/percentage if time remains

```cpp
#include <bits/stdc++.h>
using namespace std;

class SplitStrategy {
public:
    virtual vector<double> split( double amount, int people ) = 0;
    virtual ~SplitStrategy() {}
};

class EqualSplitStrategy : public SplitStrategy {
public:
    vector<double> split( double amount, int people) override {
        return vector<double>( people, amount / people);
    }
};

class Splitwise {
private:
    // balances[A][B] = the total amount user A owes user B
    unordered_map< string, unordered_map<string, double>> balances;

public:
    bool addExpense(
        string payer,
        vector<string> users,
        double amount,
        SplitStrategy* strategy
    ) {
        if (users.empty() || amount <= 0) {
            return false;
        }

        vector<double> shares =
            strategy->split(
                amount,
                users.size()
            );

        for (int i = 0; i < (int)users.size(); i++) {
            if (users[i] == payer) {
                continue;
            }

            balances[users[i]][payer] += shares[i];
        }

        return true;
    }

    double getBalance(string from, string to) {
        return balances[from][to];
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    SplitwiseService service;
    EqualSplitStrategy equal;

    cout << service.addExpense(
        "A",
        {"A", "B", "C"},
        90,
        &equal
    ) << endl; // 1
}
```

## 10. Edge Cases
Invalid total, payer not participant, percentages not 100, over-settlement, floating-point rounding.

## 11. Complexity
For `n` participants, add expense is O(n).

## 12. Extensibility Questions
Simplify debts? Net balances and debtor/creditor matching.  
Currency conversion? Add `CurrencyService`.  
Recurring expenses? Add templates.

## 13. Final Summary
Strategy separates split math from expense orchestration; BalanceSheet owns debt state.

---

<a id="q19"></a>
# 19. Design Elevator System

## 2. How This May Be Asked in an Interview

> A building has several lifts serving the same set of floors. People can request a lift from a floor and specify whether they want to go up or down, then choose a destination after entering. Each lift maintains its current floor and pending stops, and the controller should choose a suitable nearby lift while trying to avoid unnecessary direction changes. Design the core controller and lift behavior.

### What I should identify

- multiple elevators
- hall and internal requests
- pending stops
- elevator selection

### What clues tell me that?

- `"several lifts"`
- `"up or down request"`
- `"choose a suitable nearby lift"`


## 3. Clarifying Questions with Answers
Should there be multiple elevators? **Yes.**  
Should floors be 0 to 9? **Yes.**  
Should we support external floor+direction requests? **Yes.**  
Should we support internal destination selection? **Yes.**  
Should an elevator continue in its current direction and then reverse? **Yes.**  
Should the system choose the nearest suitable elevator? **Yes.**  
Should concurrency and hardware concerns stay in extensibility? **Yes.**

## 4. Requirements
1. Multiple elevators.
2. External hall request with floor and direction.
3. Internal floor selection.
4. Each elevator tracks current floor, direction, door state, and pending stops.
5. Continue current direction before reversing.
6. Choose nearest suitable elevator.

## 5. Design Pattern
Strategy on `ElevatorSelectionStrategy`.

## 6. Entities and Relationships
Direction: UP, DOWN, IDLE.  
DoorState: OPEN, CLOSED.  
Elevator: movement state and pending stops.  
ElevatorSelectionStrategy: assignment policy.  
NearestElevatorStrategy: concrete selector.  
ElevatorSystem: coordinates all requests.

### Architecture
```text
Hall Request ------+
                   v
             ElevatorSystem
             /     |      \
            v      v       v
         Lift1   Lift2   Lift3
             \     |     /
              \    |    /
          ElevatorSelectionStrategy
```

### Say It
“Elevator owns movement. ElevatorSystem owns request routing. Assignment logic is separated because that is the part most likely to change.”

## 7. Class Design
```cpp
class Elevator {
public:
    int id;
    int currentFloor;
    string direction;
    string doorState;
    set<int> upStops;
    set<int,greater<int>> downStops;

    void addStop(int floor);
    void step();
};

class ElevatorSelectionStrategy {
public:
    virtual Elevator* select(
        vector<Elevator>& elevators,
        int floor,
        string direction
    ) = 0;
};

class ElevatorSystem {
public:
    vector<Elevator> elevators;
    ElevatorSelectionStrategy* strategy;

    bool requestElevator(int floor, string direction);
    bool selectFloor(int elevatorId, int floor);
    void step();
};
```

## 8. Implementation

### DSA Used

1. **`set<int>`**
   - Purpose: store pending stops in sorted order.
   - Alternative: `vector<int>`.
   - Advantage: automatic ordering and O(log S) insertion.
   - Tradeoff: more overhead than a vector.

2. **`vector<Elevator>`**
   - Purpose: store all elevators.
   - Alternative: `unordered_map<int, Elevator>`.
   - Advantage: simple iteration when selecting the best elevator.
   - Tradeoff: finding a specific elevator by ID is O(E).

### Implementation Priority

1. `Elevator`
2. `ElevatorSystem`
3. Selection strategy
4. Door/emergency details if time remains

```cpp
#include <bits/stdc++.h>
using namespace std;

class Elevator {
public:
    int id;
    int currentFloor;
    string direction;

    set<int> upStops;
    set<int, greater<int>> downStops;

    Elevator(int id, int currentFloor) {
        this->id = id;
        this->currentFloor = currentFloor;
        direction = "IDLE";
    }

    void addStop(int floor) {
        if (floor > currentFloor) {
            upStops.insert(floor);
        } else if (floor < currentFloor) {
            downStops.insert(floor);
        }

        if (direction == "IDLE") {
            if (!upStops.empty()) {
                direction = "UP";
            } else if (!downStops.empty()) {
                direction = "DOWN";
            }
        }
    }

    void moveOneStep() {
        if (direction == "UP") {
            currentFloor++;

            // Serve this stop if requested.
            upStops.erase(currentFloor);

            if (upStops.empty()) {
                direction = downStops.empty() ? "IDLE" : "DOWN";
            }
        } else if (direction == "DOWN") {
            currentFloor--;

            downStops.erase(currentFloor);

            if (downStops.empty()) {
                direction = upStops.empty() ? "IDLE" : "UP";
            }
        }
    }
};

class ElevatorSystem {
private:
    vector<Elevator> elevators;

public:
    ElevatorSystem(vector<Elevator> elevators) {
        this->elevators = elevators;
    }

    int requestElevator(
        int floor,
        string requestDirection
    ) 
    {
        int bestIndex = -1;
        int bestDistance = INT_MAX;

        for (int i = 0; i < (int)elevators.size(); i++) {
            Elevator& elevator = elevators[i];

            bool suitable =
                elevator.direction == "IDLE" ||
                (elevator.direction == "UP" &&
                 requestDirection == "UP" &&
                 elevator.currentFloor <= floor) ||
                (elevator.direction == "DOWN" &&
                 requestDirection == "DOWN" &&
                 elevator.currentFloor >= floor);

            if (!suitable) {
                continue;
            }

            int distance = abs(elevator.currentFloor - floor);

            if (distance < bestDistance) {
                bestDistance = distance;
                bestIndex = i;
            }
        }

        if (bestIndex == -1) {
            return -1;
        }

        elevators[bestIndex].addStop(floor);

        return elevators[bestIndex].id;
    }

    void moveAll() {
        for (Elevator& elevator : elevators) {
            elevator.moveOneStep();
        }
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    NearestElevatorStrategy strategy;

    ElevatorSystem system(
        {Elevator(1, 0), Elevator(2, 5)},
        &strategy
    );

    cout << system.requestElevator(3, "UP") << endl; // 1
}
```

## 10. Edge Cases
Request at current floor, duplicate stops, no suitable elevator, direction reversal, invalid floor, concurrent hall calls.

## 11. Complexity
Let `e` = elevators and `s` = pending stops.  
Assignment: O(e).  
Add stop: O(log s).  
Step: O(e log s) worst case.

## 12. Extensibility Questions
Least-busy strategy? New selection strategy.  
Capacity? Add weight state.  
Emergency mode? State machine.  
Concurrency? Lock each elevator’s state.

## 13. Final Summary
Elevator owns movement; ElevatorSystem owns requests; Strategy isolates assignment logic.

---

<a id="q20"></a>
# 20. Design Library Management System

## 2. How This May Be Asked in an Interview

> A library maintains titles that may each have several physical copies. Members should be able to borrow an available copy, receive a due date, and return that specific copy later. The system must prevent two members from borrowing the same physical copy at the same time and should leave room for reservations or fines later. Design the core in-memory classes.

### What I should identify

- book metadata vs physical copies
- loans
- availability
- borrow/return

### What clues tell me that?

- `"several physical copies"`
- `"borrow an available copy"`
- `"due date and return"`


## 3. Clarifying Questions with Answers
Should users search books and borrow/return them? **Yes.**  
Should one title have multiple physical copies? **Yes.**  
Should a copy become unavailable when borrowed? **Yes.**  
Should due dates be represented? **Yes.**  
Should fine calculation be a follow-up? **Yes.**

## 4. Requirements
Catalog books, track physical copies, checkout, return, availability, due dates.

## 5. Design Pattern
Facade on `LibraryService`. Strategy can later handle fine calculation.

## 6. Entities and Relationships
Book: title-level metadata.  
BookCopy: one physical copy.  
Member: borrower.  
Loan: active borrowing relationship.  
LibraryService: coordinates checkout/return/search.

### Architecture
```text
Member ---> LibraryService ---> Book
                     |
                     +----> BookCopy
                     |
                     +----> Loan
```

### Say It
“A Book is metadata. A BookCopy is what actually gets borrowed. Loan connects a member to one specific copy.”

## 7. Class Design
```cpp
class BookCopy {
public:
    string copyId;
    string bookId;
    bool available;
};

class Loan {
public:
    string copyId;
    string memberId;
    int dueDate;
    bool returned;
};

class LibraryService {
public:
    unordered_map<string,BookCopy> copies;
    unordered_map<string,Loan> activeLoans;

    bool checkout(string copyId, string memberId, int dueDate);
    bool returnBook(string copyId);
};
```

## 8. Implementation

### DSA Used

1. **`unordered_map<string, BookCopy>`**
   - Purpose: find a physical copy by copy ID.
   - Alternative: `vector<BookCopy>`.
   - Advantage: average O(1) checkout lookup.
   - Tradeoff: no ordering.

2. **`unordered_map<string, Loan>`**
   - Purpose: track active loan by copy ID.
   - Alternative: `vector<Loan>`.
   - Advantage: average O(1) return lookup.
   - Tradeoff: extra memory for indexing.

### Implementation Priority

1. `LibraryManager`
2. `BookCopy`
3. `Loan`
4. Book/member metadata if time remains

```cpp
#include <bits/stdc++.h>
using namespace std;

class BookCopy {
public:
    string copyId;
    string bookId;
    bool available;

    BookCopy() {}

    BookCopy(string copyId, string bookId) {
        this->copyId = copyId;
        this->bookId = bookId;
        available = true;
    }
};

class Loan {
public:
    string copyId;
    string memberId;
    int dueDate;
};

class LibraryManager {
private:

    //copyId -> book details
    unordered_map<string, BookCopy> copies;

    // copyId -> active loan
    unordered_map<string, Loan> activeLoans;

public:
    void addBookCopy(string copyId, string bookId) {
        copies[copyId] = BookCopy(copyId, bookId);
    }

    bool checkout(
        string copyId,
        string memberId,
        int dueDate
    ) {
        if (!copies.count(copyId) || !copies[copyId].available) {
            return false;
        }

        copies[copyId].available = false;

        activeLoans[copyId] = {copyId, memberId, dueDate};

        return true;
    }

    bool returnBook(string copyId) {
        if (!activeLoans.count(copyId)) {
            return false;
        }
        activeLoans.erase(copyId);
        copies[copyId].available = true;
        return true;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    LibraryService library;
    library.addCopy({"C1", "BOOK1", true});

    cout << library.checkout("C1", "M1", 30) << endl; // 1
    cout << library.checkout("C1", "M2", 30) << endl; // 0
    cout << library.returnBook("C1") << endl;         // 1
}
```

## 10. Edge Cases
Unavailable copy, duplicate return, lost book, member borrow limit, overdue loan.

## 11. Complexity
Checkout: O(1).  
Return: O(1).  
Space: O(c + l).

## 12. Extensibility Questions
Reservations? Waitlist per title.  
Fine rules? `FineStrategy`.  
Search? Index books by title/author.

## 13. Final Summary
Separate title metadata from physical copies, and index active loans by copy for constant-time return.

---

<a id="q21"></a>
# 21. Design Customer Reviews for Amazon Products

## 2. How This May Be Asked in an Interview

> An e-commerce marketplace lets customers submit a numeric rating and text feedback for products they purchased. A customer should have at most one active review for a given product, but should be able to update that review later. Product pages need to show the average rating quickly without scanning every review each time. Design the in-memory review component.

### What I should identify

- user-product reviews
- one active review per user/product
- review updates
- fast average rating

### What clues tell me that?

- `"one active review per product"`
- `"update later"`
- `"average quickly without scanning all reviews"`


## 3. Clarifying Questions with Answers
Should users review products? **Yes.**  
Should each review contain rating and text? **Yes.**  
Should products expose average rating? **Yes.**  
Should one user have at most one active review per product? **Yes.**  
Should moderation be out of the main implementation? **Yes.**

## 4. Requirements
Create/update review, one review per user/product, validate rating, retrieve average rating efficiently.

## 5. Design Pattern
Facade on `ReviewService`. Strategy can later support ranking/moderation.

## 6. Entities and Relationships
User: reviewer.  
Product: reviewed item.  
Review: user/product/rating/text.  
ReviewService: stores reviews and aggregates ratings.

### Architecture
```text
User ---> ReviewService ---> Review ---> Product
               |
               +----> rating aggregate
```

### Say It
“I keep the review itself keyed by `(user, product)` and separately maintain rating sum/count so average rating stays O(1).”

## 7. Class Design
```cpp
class Review {
public:
    string userId;
    string productId;
    int rating;
    string text;
};

class ReviewService {
public:
    bool addOrUpdate(Review review);
    double averageRating(string productId);
};
```

## 8. Implementation

### DSA Used

1. **`unordered_map<string, Review>`**
   - Purpose: keep one review per `(userId, productId)`.
   - Alternative: `vector<Review>`.
   - Advantage: average O(1) update of an existing review.
   - Tradeoff: requires building a composite key.

2. **`unordered_map<string, pair<long long,int>>`**
   - Purpose: maintain rating sum and count per product.
   - Alternative: recompute average by scanning all reviews.
   - Advantage: average rating becomes O(1).
   - Tradeoff: aggregate state must stay consistent with reviews.

### Implementation Priority

1. `ReviewManager`
2. `Review`
3. Product/User classes only if interviewer asks

```cpp
#include <bits/stdc++.h>
using namespace std;

class Review {
public:
    string userId;
    string productId;
    int rating;
    string text;
};

class ReviewManager {
private:
    //string here is a key: userId+#+productId
    unordered_map<string, Review> reviews;

    // productId -> {ratingSum, reviewCount}
    unordered_map<string, pair<long long, int>> ratingData;

    string getKey(string userId, string productId) {
        return userId + "#" + productId;
    }

public:
    bool addOrUpdateReview(
        string userId,
        string productId,
        int rating,
        string text
    ) {
        if (rating < 1 || rating > 5) {
            return false;
        }

        string key = getKey(userId, productId);

        if (reviews.count(key)) {
            // Remove old rating before replacing it.
            ratingData[productId].first -=reviews[key].rating;
        } else {
            ratingData[productId].second++;
        }

        reviews[key] = {userId, productId, rating, text};

        ratingData[productId].first += rating;

        return true;
    }

    double getAverageRating(string productId) {
        auto [sum, count] = ratingData[productId];

        if (count == 0) {
            return 0.0;
        }

        return (double)sum / count;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    ReviewService service;

    service.addOrUpdate({"U1", "P1", 5, "Great"});
    service.addOrUpdate({"U2", "P1", 3, "Okay"});

    cout << service.averageRating("P1") << endl; // 4
}
```

## 10. Edge Cases
Invalid rating, update existing review, deleted review, empty product reviews, abusive content.

## 11. Complexity
Add/update: O(1).  
Average: O(1).  
Space: O(r).

## 12. Extensibility Questions
Helpful votes? Add vote aggregate.  
Sort reviews? Strategy for newest/helpful/rating.  
Moderation? `ReviewModerationService`.

## 13. Final Summary
Use a unique user-product key and maintain aggregates incrementally.

---

<a id="q22"></a>
# 22. Design Delivery Partner Assignment

## 2. How This May Be Asked in an Interview

> A delivery platform has a pool of drivers that continuously change availability and workload. When a new order arrives, the system should choose an available driver using factors such as current active orders and distance to pickup. The ranking policy may change later, so assignment logic should not be tightly coupled to one scoring rule. Design the core assignment component.

### What I should identify

- worker/driver assignment
- availability and load
- ranking policy
- replaceable selection logic

### What clues tell me that?

- `"choose an available driver"`
- `"active orders and distance"`
- `"ranking policy may change"`


## 3. Clarifying Questions with Answers
Should orders be assigned to available delivery partners? **Yes.**  
Should assignment consider load/distance? **Yes.**  
Should selection logic be replaceable? **Yes.**  
Should partner state include availability and active load? **Yes.**

## 4. Requirements
Register partners, track availability/load, assign an order using a selection policy, update load.

## 5. Design Pattern
Strategy on `AssignmentStrategy`.

## 6. Entities and Relationships
DeliveryPartner: availability, distance, active load.  
Order: delivery work item.  
AssignmentStrategy: partner selection policy.  
DeliveryService: coordinator.

### Architecture
```text
Order ---> DeliveryService ---> AssignmentStrategy
                   |
                   v
           Available Partners
```

### Say It
“The changing behavior is how we rank partners, so I isolate that behind Strategy.”

## 7. Class Design
```cpp
class DeliveryPartner {
public:
    string id;
    int distance;
    int activeOrders;
    bool available;
};

class AssignmentStrategy {
public:
    virtual DeliveryPartner* select(
        vector<DeliveryPartner>& partners
    ) = 0;
};

class DeliveryService {
public:
    string assignOrder();
};
```

## 8. Implementation

### DSA Used

1. **`vector<DeliveryPartner>`**
   - Purpose: store all delivery partners and scan available ones.
   - Alternative: min-heap ordered by load/distance.
   - Advantage: simple and easy to update partner state.
   - Tradeoff: assignment is O(P).

2. **No heap in the base version**
   - Why: a heap is fast for top lookup, but partner load/distance changes frequently.
   - Advantage of vector: avoids stale-heap-entry complexity.
   - Tradeoff: slower selection for large fleets.

### Implementation Priority

1. `DeliveryManager`
2. `DeliveryPartner`
3. Separate assignment strategy only if interviewer asks

```cpp
#include <bits/stdc++.h>
using namespace std;

class DeliveryPartner {
public:
    string id;
    int distance;
    int activeOrders;
    bool available;
};

class DeliveryManager {
private:
    vector<DeliveryPartner> partners;

public:
    void addPartner(DeliveryPartner partner) {
        partners.push_back(partner);
    }

    string assignOrder() {
        int bestIndex = -1;

        for (int i = 0; i < (int)partners.size(); i++) {
            if (!partners[i].available) {
                continue;
            }

            if (bestIndex == -1) {
                bestIndex = i;
                continue;
            }

            // Prefer lower load, then shorter distance.
            if (partners[i].activeOrders < partners[bestIndex].activeOrders ||
                (partners[i].activeOrders == partners[bestIndex].activeOrders &&
                 partners[i].distance < partners[bestIndex].distance)) 
            {
                bestIndex = i;
            }
        }

        if (bestIndex == -1) {
            return "";
        }

        partners[bestIndex].activeOrders++;

        return partners[bestIndex].id;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    vector<DeliveryPartner> partners = {
        {"A", 5, 2, true},
        {"B", 8, 1, true}
    };

    LeastLoadedStrategy strategy;
    DeliveryService service(partners, &strategy);

    cout << service.assignOrder() << endl; // B
}
```

## 10. Edge Cases
No available partner, tie-breaking, stale distance, partner goes offline during assignment, concurrent assignment.

## 11. Complexity
Naive assignment: O(p), where `p` = partners.

## 12. Extensibility Questions
Faster lookup? Heap/geospatial index.  
Different scoring? New Strategy.  
Concurrency? Atomic partner reservation.

## 13. Final Summary
DeliveryService coordinates assignment while Strategy owns partner ranking.

---

<a id="q23"></a>
# 23. Design Chat Messenger with File Download

## 2. How This May Be Asked in an Interview

> Users of a messaging application can participate in conversations and send text messages to one another. Messages may optionally contain a file attachment, but the chat system should reference stored files rather than embedding the file bytes in every message. Conversations need ordered history, membership checks, and message status that can later support delivery or read receipts. Design the core in-memory model.

### What I should identify

- conversations
- ordered messages
- participant membership
- file references

### What clues tell me that?

- `"conversation history"`
- `"optional file attachment"`
- `"reference stored files instead of bytes"`


## 3. Clarifying Questions with Answers
Should users send direct messages? **Yes.**  
Should messages have delivery/read state? **Yes.**  
Should file attachments be represented? **Yes.**  
Should actual file bytes/network transfer be abstracted? **Yes.**  
Should this be in-memory for the interview implementation? **Yes.**

## 4. Requirements
Create conversation, send text/file message, fetch history, track message state, reference downloadable files.

## 5. Design Pattern
Facade on `ChatService`. Adapter/Strategy can later abstract storage providers.

## 6. Entities and Relationships
User: participant.  
Conversation: participants + ordered messages.  
Message: sender, content, file reference, status.  
FileAttachment: file metadata.  
ChatService: coordinator.

### Architecture
```text
User A ---> ChatService ---> Conversation ---> Message ---> User B
                    |
                    +----> FileStorage abstraction
```

### Say It
“The message stores a file reference, not file bytes. Chat and file storage remain separate concerns.”

## 7. Class Design
```cpp
class Message {
public:
    string id;
    string senderId;
    string content;
    string fileId;
    string status;
};

class Conversation {
public:
    string id;
    unordered_set<string> participants;
    vector<Message> messages;
};

class ChatService {
public:
    Message* sendMessage(
        string conversationId,
        string senderId,
        string content,
        string fileId
    );
};
```

## 8. Implementation

### DSA Used

1. **`unordered_map<string, Conversation>`**
   - Purpose: find a conversation by ID.
   - Alternative: `vector<Conversation>`.
   - Advantage: average O(1) lookup.
   - Tradeoff: no ordering.

2. **`unordered_set<string>`**
   - Purpose: check whether a user belongs to a conversation.
   - Alternative: `vector<string>`.
   - Advantage: average O(1) membership check.
   - Tradeoff: no participant ordering.

3. **`vector<Message>`**
   - Purpose: preserve message history in send order.
   - Alternative: `list<Message>`.
   - Advantage: simple append and cache-friendly iteration.
   - Tradeoff: middle insertions/removals are expensive.

### Implementation Priority

1. `ChatManager`
2. `Conversation`
3. `Message`
4. File storage abstraction if time remains

```cpp
#include <bits/stdc++.h>
using namespace std;

class Message {
public:
    string id;
    string senderId;
    string text;
    string fileId;
    string status;
};

class Conversation {
public:
    string id;
    unordered_set<string> users;
    vector<Message> messages;
};

class ChatManager {
private:
    unordered_map<string, Conversation> conversations;
    int nextMessageId;

public:
    ChatManager() {
        nextMessageId = 1;
    }

    void addConversation(
        string conversationId,
        vector<string> users
    ) {
        Conversation conversation;
        conversation.id = conversationId;

        for (string userId : users) {
            conversation.users.insert(userId);
        }

        conversations[conversationId] = conversation;
    }

    string sendMessage(
        string conversationId,
        string senderId,
        string text,
        string fileId = ""
    ) {
        if (!conversations.count(conversationId)) {
            return "";
        }

        Conversation& conversation = conversations[conversationId];

        if (!conversation.users.count(senderId)) {
            return "";
        }

        if (text.empty() && fileId.empty()) {
            return "";
        }

        string messageId =
            "M" + to_string(nextMessageId++);

        conversation.messages.push_back({
            messageId,
            senderId,
            text,
            fileId,
            "SENT"
        });

        return messageId;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    ChatService chat;

    Conversation c;
    c.id = "C1";
    c.participants = {"U1", "U2"};

    chat.addConversation(c);

    Message* message = chat.sendMessage("C1", "U1", "hello", "");

    cout << message->status << endl; // SENT
}
```

## 10. Edge Cases
Non-member sender, empty message, missing file, duplicate delivery, ordering, large histories.

## 11. Complexity
Send: O(1) amortized.  
Fetch full history: O(m).

## 12. Extensibility Questions
Realtime delivery? WebSockets/event bus.  
File download? Signed URL from storage adapter.  
Read receipts? Per-user message state.  
Group chat? Participant set already supports it.

## 13. Final Summary
ChatService coordinates conversations; files are referenced externally instead of embedded.

---

<a id="q24"></a>
# 24. Design ALB Listener Rule Routing

## 2. How This May Be Asked in an Interview

> You are working on a traffic-routing component in front of a fleet of backend services. Incoming HTTP requests are evaluated against configurable rules, where each rule has a unique priority and can inspect properties such as the request path or headers. The first matching rule should forward the request to its configured backend group, and a default group handles requests that match nothing. New condition types may be added later. Design the routing component.

### What I should identify

- ordered routing rules
- pluggable request conditions
- first match wins
- target-group action

### What clues tell me that?

- `"unique priority"`
- `"path or headers"`
- `"first matching rule forwards"`


## 3. Clarifying Questions with Answers
Should each rule have a unique integer priority where lower means higher priority? **Yes.**  
Should conditions match request path prefix or header? **Yes.**  
Should the action be a target-group name? **Yes.**  
Should the first matching rule by priority win? **Yes.**  
Should there be a default target group when no rule matches? **Yes.**

## 4. Requirements
1. Listener stores routing rules.
2. Rule = priority + condition + target group.
3. Evaluate rules in ascending priority.
4. First match wins.
5. Condition types are extensible.
6. Default route exists.

## 5. Design Pattern
Strategy on `Condition`.

## 6. Entities and Relationships
Request: host, path, headers.  
Condition: match interface.  
PathPrefixCondition: matches path prefix.  
HeaderCondition: matches header value.  
Rule: priority + condition + action.  
Listener: ordered rules and routing API.

### Architecture
```text
Incoming Request
       |
       v
   +--------+
   |Listener|
   +---+----+
       |
   sorted rules
   /    |     \
  v     v      v
 R1    R2      R3
 |      |
 v      v
Condition ---> Target Group
```

### Say It
“The listener owns ordering. Conditions own match logic. First matching rule returns its target group.”

## 7. Class Design
```cpp
struct Request {
    string host;
    string path;
    unordered_map<string,string> headers;
};

class Condition {
public:
    virtual bool matches(const Request& request) const = 0;
};

class Rule {
public:
    int priority;
    shared_ptr<Condition> condition;
    string targetGroup;
};

class Listener {
public:
    vector<Rule> rules;
    string defaultTargetGroup;

    string route(const Request& request) const;
};
```

## 8. Implementation

### DSA Used

1. **`vector<Rule>`**
   - Purpose: store listener rules in priority order.
   - Alternative: `priority_queue<Rule>`.
   - Advantage: after one initial sort, routing can iterate cleanly without destroying/removing rules.
   - Tradeoff: checking a request is O(R).

2. **`unordered_map<string,string>` for headers**
   - Purpose: find a header by name in average O(1).
   - Alternative: vector of header pairs.
   - Advantage: faster exact header lookup.
   - Tradeoff: extra hashing overhead.

### Implementation Priority

1. `LoadBalancer::route()`
2. `Rule`
3. Condition classes
4. More condition types if time remains

```cpp
#include <bits/stdc++.h>
using namespace std;

class Request {
public:
    string host;
    string path;
    unordered_map<string, string> headers;
};

class Condition {
public:
    virtual bool matches(Request& request) = 0;

    virtual ~Condition() {}
};

class PathPrefixCondition : public Condition {
private:
    string prefix;

public:
    PathPrefixCondition(string prefix) {
        this->prefix = prefix;
    }

    bool matches(Request& request) override {
        return request.path.rfind(prefix, 0) == 0;
    }
};

class HeaderCondition : public Condition {
private:
    string key;
    string value;

public:
    HeaderCondition(string key, string value) {
        this->key = key;
        this->value = value;
    }

    bool matches(Request& request) override {
        return request.headers.count(key) &&
               request.headers[key] == value;
    }
};

class Rule {
public:
    int priority;
    Condition* condition;
    string targetGroup;
};

class LoadBalancer {
private:
    vector<Rule> rules;
    string defaultTargetGroup;

public:
    LoadBalancer(
        vector<Rule> rules,
        string defaultTargetGroup
    ) {
        this->rules = rules;
        this->defaultTargetGroup =
            defaultTargetGroup;

        sort(
            this->rules.begin(),
            this->rules.end(),
            [](Rule& a, Rule& b) {
                return a.priority < b.priority;
            }
        );
    }

    string route(Request& request) {
        for (Rule& rule : rules) {
            if (rule.condition->matches(request)) {
                return rule.targetGroup;
            }
        }

        return defaultTargetGroup;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    vector<Rule> rules = {
        {10, make_shared<PathPrefixCondition>("/api"), "api-targets"},
        {20, make_shared<HeaderCondition>("x-beta", "true"), "beta-targets"}
    };

    Listener listener(rules, "default-targets");

    Request request{"example.com", "/api/orders", {}};

    cout << listener.route(request) << endl; // api-targets
}
```

## 10. Edge Cases
Duplicate priorities, overlapping prefixes, no match, missing header, empty path, dynamic rule updates.

## 11. Complexity
Let `r` = rules.  
Initial sort: O(r log r).  
Route: O(r × condition-cost).  
Space: O(r).

## 12. Extensibility Questions
Multiple conditions per rule? Add `AndCondition`/`OrCondition`.  
Faster path matching? Trie.  
Dynamic updates? Build immutable rule snapshot and atomically swap.

## 13. Final Summary
Listener owns priority evaluation; conditions are pluggable; first match wins.

---

<a id="q25"></a>
# 25. Design Hierarchical Configuration Service

## 2. How This May Be Asked in an Interview

> A configuration platform stores values at several levels of scope, such as company, region, and service. A more specific scope can override a value defined by a broader parent scope, while keys that are not overridden should inherit the closest ancestor value. The system needs an API to define a key/value at an exact sequence of scope segments and another API to resolve the effective value for a requested scope. Design the in-memory structure and lookup logic.

### What I should identify

- hierarchical scopes
- ancestor inheritance
- deeper overrides
- set/get by path segments

### What clues tell me that?

- `"several levels of scope"`
- `"more specific overrides parent"`
- `"inherit closest ancestor value"`


## 3. Clarifying Questions with Answers
Should a path be represented as ordered segments? **Yes.**  
Should deeper ancestors override higher-level values? **Yes.**  
Should `set(pathSegments, key, value)` define a value at exactly that scope? **Yes.**  
Should `get(pathSegments, key)` return the deepest applicable ancestor value? **Yes.**  
Should a missing key return an empty result? **Yes.**

## 4. Requirements
1. Store config values at hierarchical scopes.
2. Same key can exist at multiple scopes.
3. `set()` writes to one exact node.
4. `get()` walks ancestors.
5. Deepest matching value wins.
6. Root defaults are supported.

## 5. Design Pattern
Trie/tree data structure. No heavy GoF pattern required.

## 6. Entities and Relationships
ConfigNode: one hierarchy scope with local key/value pairs and children.  
ConfigService: owns root and traversal.

### Architecture
```text
root
 |
 +-- org=A
      |
      +-- region=us
           |
           +-- service=payments

Values may exist at every level.

get(path,key):
root -> org -> region -> service
remember deepest node that defines key
```

### Say It
“`set()` walks or creates nodes. `get()` walks the same path and keeps updating the candidate whenever a deeper ancestor defines the key.”

## 7. Class Design
```cpp
class ConfigNode {
public:
    unordered_map<string,unique_ptr<ConfigNode>> children;
    unordered_map<string,string> values;
};

class ConfigService {
public:
    void set(
        vector<string> pathSegments,
        string key,
        string value
    );

    optional<string> get(
        vector<string> pathSegments,
        string key
    );
};
```

## 8. Implementation

### DSA Used

1. **Trie / Tree**
   - Purpose: represent ordered configuration path segments.
   - Alternative: flat hashmap keyed by the full joined path.
   - Advantage: naturally supports ancestor traversal and inheritance.
   - Tradeoff: more node objects and pointer/map overhead.

2. **`unordered_map<string, Node*>`**
   - Purpose: find a child segment in average O(1).
   - Alternative: `map<string, Node*>`.
   - Advantage: faster average traversal.
   - Tradeoff: no ordering.

3. **`unordered_map<string,string>`**
   - Purpose: store config key/value pairs at each scope.
   - Alternative: vector of pairs.
   - Advantage: average O(1) local key lookup.
   - Tradeoff: hashing overhead.

### Implementation Priority

1. `ConfigService`
2. `Node`
3. `set()`
4. `get()`

```cpp
#include <bits/stdc++.h>
using namespace std;

class ConfigService {
private:
    class Node {
    public:
        unordered_map<string, Node*> children;
        unordered_map<string, string> values;
    };

    Node* root;

public:
    ConfigService() {
        root = new Node();
    }

    void set(
        vector<string> pathSegments,
        string key,
        string value
    ) {
        Node* current = root;

        // Create path nodes as needed.
        for (string segment : pathSegments) {
            if (!current->children.count(segment)) {
                current->children[segment] = new Node();
            }

            current = current->children[segment];
        }

        current->values[key] = value;
    }

    string get(
        vector<string> pathSegments,
        string key
    ) {
        Node* current = root;

        bool found = false;
        string answer = "";

        // Root value is the least specific fallback.
        if (current->values.count(key)) {
            answer = current->values[key];
            found = true;
        }

        for (string segment : pathSegments) {
            if (!current->children.count(segment)) {
                break;
            }

            current = current->children[segment];

            // Deeper value overrides the previous one.
            if (current->values.count(key)) {
                answer = current->values[key];
                found = true;
            }
        }

        return found ? answer : "";
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    ConfigService config;

    config.set({}, "timeout", "30");
    config.set({"orgA"}, "timeout", "20");
    config.set({"orgA", "us"}, "timeout", "10");

    cout << *config.get(
        {"orgA", "us", "payments"},
        "timeout"
    ) << endl; // 10
}
```

## 10. Edge Cases
Missing path, missing key, root default, partial hierarchy, overwrite at same scope, delete/unset.

## 11. Complexity
Let `d` = path depth.  
`set`: O(d).  
`get`: O(d).  
Space: O(nodes + stored values).

## 12. Extensibility Questions
Delete value? Remove key at node and optionally prune empty nodes.  
Dynamic updates? Already O(d).  
Typed values? `variant`.  
Concurrency? Reader/writer lock or immutable snapshots.

## 13. Final Summary
The hierarchy itself is the data structure, and `get()` simply remembers the deepest value seen.

---

<a id="q26"></a>
# 26. Design Chess Game

## 2. How This May Be Asked in an Interview

> You are implementing the core rules engine for a two-player board game played on an 8×8 grid. Different piece types have different legal movement rules, players alternate turns, pieces can capture opposing pieces, and moves must respect the current board state. The initial interview scope focuses on validating and applying moves rather than building an AI opponent. Design the object model so piece-specific behavior stays easy to extend.

### What I should identify

- 8×8 board
- different piece movement rules
- alternating turns
- captures and move validation

### What clues tell me that?

- `"different piece types"`
- `"legal movement rules"`
- `"players alternate turns"`
- `"capture opposing pieces"`


## 3. Clarifying Questions with Answers
Should we model a standard 8×8 chess board? **Yes.**  
Should pieces have type/color and movement rules? **Yes.**  
Should turns alternate between white and black? **Yes.**  
Should we focus on move validation and board updates rather than AI? **Yes.**  
Should castling/en-passant/checkmate details be follow-ups unless asked? **Yes.**

## 4. Requirements
Board setup, pieces, alternating turns, legal movement validation, capture, basic game state.

## 5. Design Pattern
Polymorphism for piece-specific movement. Command can later support move history/undo.

## 6. Entities and Relationships
Position: row and column.  
Piece: base abstraction with color and movement rule.  
ConcretePiece: King/Queen/Rook/Bishop/Knight/Pawn.  
Board: owns pieces by position.  
Move: source, destination, captured piece.  
ChessGame: validates turn and applies moves.

### Architecture
```text
Player Move
    |
    v
ChessGame
    |
    +----> Board ----> Piece at source
                    |
                    v
              piece.canMove(...)
                    |
                    v
              apply/capture
```

### Say It
“Pieces know how they move. ChessGame knows whose turn it is and whether the move can be applied to the board.”

## 7. Class Design
```cpp
struct Position {
    int row;
    int col;
};

class Piece {
public:
    string color;
    virtual bool canMove( Position from, Position to, const vector<vector<Piece*>>& board ) const = 0;
};

class ChessGame {
public:
    vector<vector<Piece*>> board;
    string currentTurn;

    bool move(Position from, Position to);
};
```

## 8. Implementation

### DSA Used

1. **2D `vector<vector<Piece*>>`**
   - Purpose: represent the 8×8 chess board.
   - Alternative: hashmap from coordinate to piece.
   - Advantage: direct O(1) board access and very easy to visualize.
   - Tradeoff: fixed board memory even for empty cells, which is trivial for 8×8.

2. **Polymorphism**
   - Purpose: each piece implements its own movement rule.
   - Alternative: one giant `switch(pieceType)`.
   - Advantage: new/changed piece behavior stays isolated.
   - Tradeoff: more classes.

### Implementation Priority

1. `ChessGame::move()`
2. `Piece`
3. One concrete piece such as `Rook`
4. Other pieces only if time remains
5. Check/checkmate as follow-up

```cpp
#include <bits/stdc++.h>
using namespace std;

class Piece {
public:
    string color;

    Piece(string color) {
        this->color = color;
    }

    virtual bool canMove(
        int fromRow,
        int fromCol,
        int toRow,
        int toCol,
        vector<vector<Piece*>>& board
    ) = 0;

    virtual ~Piece() {}
};

class Rook : public Piece {
public:
    Rook(string color)
        : Piece(color) {}

    bool canMove(
        int fromRow,
        int fromCol,
        int toRow,
        int toCol,
        vector<vector<Piece*>>& board
    ) override {
        if (fromRow != toRow &&
            fromCol != toCol) {
            return false;
        }

        int rowStep =
            (toRow > fromRow) -
            (toRow < fromRow);

        int colStep =
            (toCol > fromCol) -
            (toCol < fromCol);

        int row = fromRow + rowStep;
        int col = fromCol + colStep;

        // Every square before destination must be empty.
        while (row != toRow || col != toCol) {
            if (board[row][col] != nullptr) {
                return false;
            }

            row += rowStep;
            col += colStep;
        }

        return true;
    }
};

class ChessGame {
private:
    vector<vector<Piece*>> board;
    string turn;

public:
    ChessGame() {
        board = vector<vector<Piece*>>( 8,vector<Piece*>(8, nullptr));
        turn = "WHITE";
    }

    void placePiece(
        int row,
        int col,
        Piece* piece
    ) {
        board[row][col] = piece;
    }

    bool move(
        int fromRow,
        int fromCol,
        int toRow,
        int toCol
    ) {
        if (fromRow < 0 || fromRow >= 8 ||
            fromCol < 0 || fromCol >= 8 ||
            toRow < 0 || toRow >= 8 ||
            toCol < 0 || toCol >= 8) {
            return false;
        }

        Piece* piece =
            board[fromRow][fromCol];

        if (piece == nullptr || piece->color != turn) {
            return false;
        }

        Piece* target = board[toRow][toCol];

        if (target != nullptr && target->color == turn) {
            return false;
        }

        if (!piece->canMove(
                fromRow,
                fromCol,
                toRow,
                toCol,
                board)) {
            return false;
        }

        board[toRow][toCol] = piece;
        board[fromRow][fromCol] = nullptr;

        turn =
            (turn == "WHITE") ?
            "BLACK" : "WHITE";

        return true;
    }
};
```


## 9. Dry Run / Verification
```cpp
int main() {
    ChessGame game;
    Rook rook("WHITE");

    game.place({0, 0}, &rook);

    cout << game.move({0, 0}, {0, 5}) << endl; // 1
}
```

## 10. Edge Cases
Out-of-board move, own-piece capture, blocked path, moving opponent piece, king left in check, special chess rules.

## 11. Complexity
On a fixed 8×8 board, sliding-piece validation is O(8) = O(1).  
Space is O(64) = O(1).

## 12. Extensibility Questions
Undo? Command/Move history.  
Check/checkmate? Simulate move and verify king safety.  
Castling/en-passant? Add game-rule state.  
AI? Separate chess engine from game model.

## 13. Final Summary
Pieces own movement rules; ChessGame owns turn and board orchestration.

---
