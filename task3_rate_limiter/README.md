# Task 3 - Rate Limiter (Python)

Simple in-memory rate limiter. Default: 5 requests per 60 seconds per user.

## Usage

from rate_limiter import RateLimiter

limiter = RateLimiter(limit=5, window=60)

allowed, info = limiter.allow_request("user_123")
if allowed:
    # do the thing
    print(info["remaining"], "requests left")
else:
    print("blocked, retry in", info["retry_after_seconds"], "sec")

Check status without using a request:

status = limiter.get_user_status("user_123")

Run demo

python3 rate_limiter.py

Shows some examples + runs basic tests.

More info
See DOCUMENTATION.md for algorithm choice, searches, edge cases etc

