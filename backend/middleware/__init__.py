"""
Middleware package for EduBob API.
Contains rate limiting, security headers, and authentication middleware.
"""

# Note: Auth and rate limiter temporarily disabled until dependencies are installed
# Uncomment after running: pip install -r requirements.txt
# from .rate_limiter import limiter, RateLimitMiddleware
# from .auth import get_current_user, create_access_token, verify_password, get_password_hash

from .security_headers import SecurityHeadersMiddleware

__all__ = [
    # 'limiter',
    # 'RateLimitMiddleware',
    'SecurityHeadersMiddleware',
    # 'get_current_user',
    # 'create_access_token',
    # 'verify_password',
    # 'get_password_hash'
]

# Made with Bob