import time
from collections import deque
from typing import Dict, Tuple


class RateLimiter:
    """
    Sliding window rate limiter - tracks requests per user using deque of timestamps.
    """
    
    def __init__(self, limit: int = 5, window: int = 60):
        if limit <= 0:
            raise ValueError("Limit must be positive")
        if window <= 0:
            raise ValueError("Window must be positive")
            
        self.limit = limit
        self.window = window
        self.user_requests: Dict[str, deque] = {}
    
    def _clean_old_requests(self, user_id: str, current_time: float) -> None:
        """Remove timestamps outside current window."""
        if user_id not in self.user_requests:
            return
        
        cutoff_time = current_time - self.window
        
        # pop from left while outside window
        while (self.user_requests[user_id] and 
               self.user_requests[user_id][0] <= cutoff_time):
            self.user_requests[user_id].popleft()
    
    def allow_request(self, user_id: str) -> Tuple[bool, dict]:
        """
        Check if request allowed for user.
        Returns (allowed, info_dict)
        """
        if not user_id:
            raise ValueError("user_id cannot be empty")
        
        current_time = time.time()
        
        if user_id not in self.user_requests:
            self.user_requests[user_id] = deque()
        
        self._clean_old_requests(user_id, current_time)
        
        request_count = len(self.user_requests[user_id])
        
        if request_count >= self.limit:
            oldest = self.user_requests[user_id][0]
            retry_after = int(oldest + self.window - current_time) + 1
            
            return False, {
                "allowed": False,
                "user_id": user_id,
                "limit": self.limit,
                "window": self.window,
                "current_count": request_count,
                "retry_after_seconds": retry_after,
                "message": f"Rate limit exceeded. Try again in {retry_after} seconds."
            }
        
        self.user_requests[user_id].append(current_time)
        remaining = self.limit - request_count - 1
        
        return True, {
            "allowed": True,
            "user_id": user_id,
            "limit": self.limit,
            "window": self.window,
            "current_count": request_count + 1,
            "remaining": remaining,
            "message": f"Request allowed. {remaining} requests remaining."
        }
    
    def get_user_status(self, user_id: str) -> dict:
        """Get rate limit status without making a request."""
        current_time = time.time()
        
        if user_id not in self.user_requests:
            return {
                "user_id": user_id,
                "current_count": 0,
                "limit": self.limit,
                "remaining": self.limit
            }
        
        self._clean_old_requests(user_id, current_time)
        request_count = len(self.user_requests[user_id])
        
        return {
            "user_id": user_id,
            "current_count": request_count,
            "limit": self.limit,
            "remaining": max(0, self.limit - request_count)
        }
    
    def reset_user(self, user_id: str) -> None:
        """Reset limit for a user. Mainly for testing."""
        if user_id in self.user_requests:
            self.user_requests[user_id].clear()


def simulate_api_endpoint(limiter: RateLimiter, user_id: str, action: str) -> dict:
    """Fake API endpoint that uses rate limiting."""
    allowed, info = limiter.allow_request(user_id)
    
    if allowed:
        return {"status": "success", "data": f"'{action}' completed", "rate_limit": info}
    else:
        return {"status": "error", "error": "Rate limit exceeded", "rate_limit": info}


# === DEMO & TESTS ===

def run_demo():
    print("=" * 60)
    print("RATE LIMITER DEMO")
    print("=" * 60)
    
    limiter = RateLimiter(limit=5, window=60)
    
    # Demo 1: Hit the limit
    print("\n--- Demo 1: User hitting limit ---")
    user1 = "user_123"
    for i in range(7):
        allowed, info = limiter.allow_request(user1)
        status = "allowed" if allowed else "blocked"
        print(f"Request {i+1}: {status} - {info['message']}")
    
    # Demo 2: Multiple users
    print("\n--- Demo 2: Multiple users (independent) ---")
    for user in ["alice", "bob", "charlie"]:
        for _ in range(3):
            limiter.allow_request(user)
        status = limiter.get_user_status(user)
        print(f"{user}: {status['current_count']}/{status['limit']} used")
    
    # Demo 3: Window reset
    print("\n--- Demo 3: Auto-reset (3 sec window) ---")
    short_limiter = RateLimiter(limit=2, window=3)
    user2 = "user_456"
    
    short_limiter.allow_request(user2)
    short_limiter.allow_request(user2)
    print("Made 2 requests, at limit")
    
    allowed, _ = short_limiter.allow_request(user2)
    print(f"3rd request: {'allowed' if allowed else 'blocked'}")
    
    print("Waiting 3 seconds...")
    time.sleep(3)
    
    allowed, info = short_limiter.allow_request(user2)
    print(f"After wait: {'allowed' if allowed else 'still blocked'}")
    
    # Demo 4: API simulation
    print("\n--- Demo 4: Fake API endpoint ---")
    api_limiter = RateLimiter(limit=2, window=60)
    
    for action in ["get_profile", "update_settings", "send_message"]:
        resp = simulate_api_endpoint(api_limiter, "api_user", action)
        print(f"{action}: {resp['status']}")
    
    print("\n" + "=" * 60)


def run_tests():
    print("\n=== TESTS ===\n")
    
    passed = 0
    
    # Test 1: Basic limiting
    print("Test 1: Basic limiting...")
    limiter = RateLimiter(limit=3, window=60)
    results = [limiter.allow_request("test")[0] for _ in range(5)]
    assert results == [True, True, True, False, False], "Basic limit failed"
    print("passed")
    passed += 1
    
    # Test 2: Independent users
    print("Test 2: Independent users...")
    limiter = RateLimiter(limit=2, window=60)
    assert limiter.allow_request("user1")[0] == True
    assert limiter.allow_request("user2")[0] == True
    print("passed")
    passed += 1
    
    # Test 3: Window reset
    print("Test 3: Window reset...")
    limiter = RateLimiter(limit=1, window=1)
    limiter.allow_request("test")
    assert limiter.allow_request("test")[0] == False
    time.sleep(1.1)
    assert limiter.allow_request("test")[0] == True
    print("passed")
    passed += 1
    
    # Test 4: Status check
    print("Test 4: Status check...")
    limiter = RateLimiter(limit=5, window=60)
    limiter.allow_request("test")
    limiter.allow_request("test")
    status = limiter.get_user_status("test")
    assert status['current_count'] == 2 and status['remaining'] == 3
    print("passed")
    passed += 1
    
    # Test 5: Reset
    print("Test 5: Reset user...")
    limiter = RateLimiter(limit=1, window=60)
    limiter.allow_request("test")
    limiter.reset_user("test")
    assert limiter.allow_request("test")[0] == True
    print("passed")
    passed += 1
    
    print(f"\n{passed}/5 tests passed")


if __name__ == "__main__":
    run_demo()
    run_tests()