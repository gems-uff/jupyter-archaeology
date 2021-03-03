"""Utility functions for jupat"""

import sys

def to_unicode(text):
    """Convert text to unicode"""
    if sys.version_info < (3, 0):
        if isinstance(text, unicode):
            return text
        return str(text).decode("utf-8")
    if isinstance(text, str):
        return text
    return bytes(text).decode("utf-8")
