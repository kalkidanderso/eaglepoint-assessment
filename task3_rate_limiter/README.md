# Task 3 – Rate Limiter (Python)

Simple in-memory rate limiter. Default: 5 requests per 60 seconds per user.

## Usage

```python
from rate_limiter import RateLimiter

limiter = RateLimiter(limit=5, window=60)

allowed, info = limiter.allow_request("user_123")
if allowed:
    # do the thing
    print(info["remaining"], "requests left")
else:
    print("blocked, retry in", info["retry_after_seconds"], "sec")

status = limiter.get_user_status("user_123")
print(status)
```

## Run demo

```bash
python3 rate_limiter.py
```

This shows some examples and runs basic tests.

## More info

See `DOCUMENTATION.md` for algorithm choice, searches, edge cases, etc.

