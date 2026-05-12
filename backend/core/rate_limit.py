"""
Shared rate limiter instance for slowapi.
All routes should import from here instead of creating their own Limiter.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
