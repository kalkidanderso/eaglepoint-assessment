# Task 3 - Rate Limiter (Python) - Process Notes

Notes on how I built this - what I looked up, why I went with sliding window, etc



## 1. What the task asked for

- Enforce 5 requests per 60 seconds per user
- Identify users by ID
- Block requests once limit is hit
- Auto-reset after window passes
- Include working examples



## 2. Search log

Main searches I used:

1. **Rate limiting algorithms**  
   Search: `rate limiting sliding window token bucket fixed window`  
   URL: https://www.geeksforgeeks.org/system-design/rate-limiting-algorithms-system-design/
   - good overview of the different approaches

2. **Python deque**  
Search: `python collections deque example`  
   - needed efficient append/pop from both ends

3. **Time handling**  
   Search: `python time.time vs datetime.now for timestamps`  
   URL: https://stackoverflow.com/questions/55603536/python-time-time-and-datetime-datetime-utcnow-timestamp-returning-differ
   - went with time.time(), simpler math

4. **HTTP 429 stuff**  
Search: `http 429 retry-after header meaning`  
   - wanted to return retry_after like real APIs do



## 3. Algorithm choice

Compared a few options:

- **Fixed window** - easy but has the boundary problem where users can double up at edges
- **Sliding window log** - store timestamps, look at "now minus window". accurate
- **Token bucket** - good for bursts but more complex than needed here

Went with **sliding window log** because:
- Matches "5 requests in last 60 seconds" exactly
- Easy to implement with deque
- We're not at huge scale so storing timestamps is fine



## 4. Implementation

**Data structure:**
- `self.limit` - requests allowed per window (default 5)
- `self.window` - window size in seconds (default 60)
- `self.user_requests` - dict mapping user_id to deque of timestamps

Used deque because append right + pop left are both O(1)

**Main logic:**

1. `_clean_old_requests()` - remove timestamps older than window. called before every check so memory stays bounded

2. `allow_request(user_id)` - clean old requests, count whats left, if >= limit return False with retry_after, otherwise append timestamp and return True

3. `get_user_status()` - check count without incrementing

4. `reset_user()` - clear deque for a user, mainly for testing

**Demo/tests:**
- `run_demo()` shows different scenarios with output
- `run_tests()` has some basic assertions



## 5. Issues I ran into

1. **Off by one on limit** - had to decide if 5th request allowed or not. went with 5 allowed, 6th blocked (`if count >= limit`)

2. **retry_after rounding** - float math sometimes gave 0 when there was still a fraction of a second. fixed by doing `int(...) + 1` to always round up

3. **Memory** - without cleanup the timestamp list could grow forever. calling `_clean_old_requests` on every check means at most `limit` timestamps per user

4. **Time-based tests** - cant wait 60 seconds in tests. used shorter windows (1-3 sec) for demos



## 6. Why this works

- Actually enforces "N requests per M seconds" not an approximation
- Simple enough to explain
- Returns useful info (remaining, retry_after)
- Easy to extend - could add per-tier limits, swap to Redis, etc.

For this assignment sliding window in memory felt like right balance

