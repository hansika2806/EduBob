"""
Rate limiting middleware using SlowAPI.
Protects against DoS attacks and abuse.
"""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import Request
import logging

logger = logging.getLogger(__name__)

# Create limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["60/minute"],  # Default: 60 requests per minute
    storage_uri="memory://",  # Use in-memory storage (upgrade to Redis for production)
    strategy="fixed-window"
)

class RateLimitMiddleware(SlowAPIMiddleware):
    """
    Custom rate limit middleware with enhanced logging.
    """
    
    def __init__(self, app, limiter):
        super().__init__(app, limiter=limiter)
        self.limiter = limiter
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            client_ip = get_remote_address(request)
            path = request.url.path
            
            # Log rate limit hits
            logger.debug(f"Rate limit check: {client_ip} -> {path}")
        
        return await super().__call__(scope, receive, send)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """
    Custom handler for rate limit exceeded errors.
    """
    client_ip = get_remote_address(request)
    logger.warning(f"Rate limit exceeded for {client_ip} on {request.url.path}")
    
    return _rate_limit_exceeded_handler(request, exc)

# Made with Bob