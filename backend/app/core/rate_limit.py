from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Callable, Dict, Optional
import time
from datetime import datetime
import asyncio
from functools import wraps

# In-memory store for rate limiting
# In production, use Redis or similar distributed cache
rate_limit_store: Dict[str, Dict[str, int]] = {}

class RateLimiter:
    def __init__(
        self,
        times: int = 5,  # Number of requests allowed
        seconds: int = 60,  # Time window in seconds
        prefix: str = "rate_limit"  # Prefix for rate limit key
    ):
        self.times = times
        self.seconds = seconds
        self.prefix = prefix

    def _generate_key(self, request: Request) -> str:
        """Generate a unique key for the rate limit."""
        # Get the client's IP address
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0]
        else:
            ip = request.client.host
        
        # Include the endpoint path in the key
        path = request.url.path
        
        return f"{self.prefix}:{ip}:{path}"

    async def is_rate_limited(self, key: str) -> bool:
        """Check if the request should be rate limited."""
        now = int(time.time())
        
        if key not in rate_limit_store:
            rate_limit_store[key] = {"count": 1, "reset_time": now + self.seconds}
            return False
            
        # Get the current count and reset time
        info = rate_limit_store[key]
        
        # If the reset time has passed, reset the counter
        if now > info["reset_time"]:
            info["count"] = 1
            info["reset_time"] = now + self.seconds
            return False
            
        # Increment the counter and check if it exceeds the limit
        info["count"] += 1
        if info["count"] > self.times:
            return True
            
        return False

    def __call__(self, func: Callable) -> Callable:
        """Decorator for rate limiting endpoints."""
        @wraps(func)
        async def wrapper(*args, request: Request, **kwargs):
            key = self._generate_key(request)
            
            # Check rate limit
            is_limited = await self.is_rate_limited(key)
            if is_limited:
                reset_time = rate_limit_store[key]["reset_time"]
                wait_time = reset_time - int(time.time())
                
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "message": "Too many requests",
                        "wait_seconds": wait_time
                    }
                )
                
            # Add rate limit headers
            headers = {
                "X-RateLimit-Limit": str(self.times),
                "X-RateLimit-Remaining": str(
                    self.times - rate_limit_store[key]["count"]
                ),
                "X-RateLimit-Reset": str(rate_limit_store[key]["reset_time"])
            }
            
            # Execute the endpoint function
            response = await func(*args, request=request, **kwargs)
            
            # If the response is a JSONResponse, add the headers
            if isinstance(response, JSONResponse):
                response.headers.update(headers)
                
            return response
            
        return wrapper

# Create rate limiters with different configurations
aggressive_limiter = RateLimiter(times=3, seconds=60, prefix="aggressive")  # 3 requests per minute
normal_limiter = RateLimiter(times=10, seconds=60, prefix="normal")  # 10 requests per minute
relaxed_limiter = RateLimiter(times=30, seconds=60, prefix="relaxed")  # 30 requests per minute
