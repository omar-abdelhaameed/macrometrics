"""
Rate Limiting Configuration for MacroMetrics
=============================================
Provides centralized rate limiting for all endpoints.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse


# Use client IP for rate limiting (can be customized for auth users)
def get_rate_limit_key(request: Request) -> str:
    """Get rate limit key - use IP for public routes, user ID for authenticated routes."""
    # For authenticated routes, you could use: request.state.user.id
    return get_remote_address(request)


# Create limiter instance
limiter = Limiter(key_func=get_rate_limit_key)


# Custom rate limit exceeded handler
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Handle rate limit exceeded with proper error response."""
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "message": "Too many requests. Please slow down.",
            "detail": f"Limit: {exc.detail}",
            "retry_after": getattr(exc, "retry_after", None)
        }
    )


# Rate limit configurations for different endpoint types
RATE_LIMITS = {
    # Auth endpoints - strict (prevent brute force)
    "auth": "5/minute",
    
    # Search endpoints - moderate
    "search": "30/minute",
    
    # AI/Chat - moderate to prevent abuse
    "chat": "10/minute",
    
    # General API - generous
    "default": "60/minute",
}


def get_rate_limit_for_endpoint(endpoint: str) -> str:
    """Get rate limit string for an endpoint based on its path."""
    if "/auth/" in endpoint:
        return RATE_LIMITS["auth"]
    elif "/search" in endpoint or "/ingredients" in endpoint:
        return RATE_LIMITS["search"]
    elif "/chat" in endpoint:
        return RATE_LIMITS["chat"]
    else:
        return RATE_LIMITS["default"]