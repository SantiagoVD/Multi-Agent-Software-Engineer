"""Exceptions raised by application tools."""


class ToolError(RuntimeError):
    """Base error for a failed tool operation."""


class PathSecurityError(ToolError):
    """Raised when a filesystem path escapes its authorized root."""
