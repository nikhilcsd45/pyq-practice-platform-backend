"""
Compatibility module to fix bcrypt version issues.
"""

import bcrypt

# Add __about__ module to bcrypt if it doesn't exist
if not hasattr(bcrypt, '__about__'):
    class About:
        __version__ = bcrypt.__version__ if hasattr(bcrypt, '__version__') else "unknown"
    
    bcrypt.__about__ = About
