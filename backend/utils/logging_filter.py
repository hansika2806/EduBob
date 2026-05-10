"""
Logging utilities with sensitive data filtering.
Prevents logging of passwords, API keys, and other sensitive information.
"""

import logging
import re
from typing import Any, Dict
from config import SENSITIVE_FIELDS


class SensitiveDataFilter(logging.Filter):
    """
    Logging filter that redacts sensitive information from log messages.
    """
    
    def __init__(self):
        super().__init__()
        self.sensitive_patterns = self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for sensitive data detection"""
        patterns = []
        
        # Pattern for sensitive field names
        for field in SENSITIVE_FIELDS:
            # Match field="value" or field: "value" or field='value'
            pattern = re.compile(
                rf'{field}["\']?\s*[:=]\s*["\']?([^"\'\s,}}]+)["\']?',
                re.IGNORECASE
            )
            patterns.append(pattern)
        
        # Pattern for Bearer tokens
        patterns.append(re.compile(r'Bearer\s+([A-Za-z0-9\-._~+/]+=*)', re.IGNORECASE))
        
        # Pattern for API keys (common formats)
        patterns.append(re.compile(r'["\']?api[_-]?key["\']?\s*[:=]\s*["\']?([A-Za-z0-9]{20,})["\']?', re.IGNORECASE))
        
        return patterns
    
    def _redact_sensitive_data(self, text: str) -> str:
        """Redact sensitive data from text"""
        if not isinstance(text, str):
            text = str(text)
        
        for pattern in self.sensitive_patterns:
            text = pattern.sub(lambda m: m.group(0).replace(m.group(1), '***REDACTED***'), text)
        
        return text
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter log record to redact sensitive data"""
        # Redact message
        if hasattr(record, 'msg'):
            record.msg = self._redact_sensitive_data(str(record.msg))
        
        # Redact args
        if hasattr(record, 'args') and record.args:
            if isinstance(record.args, dict):
                record.args = {
                    k: self._redact_sensitive_data(str(v)) if isinstance(v, str) else v
                    for k, v in record.args.items()
                }
            elif isinstance(record.args, (list, tuple)):
                record.args = tuple(
                    self._redact_sensitive_data(str(arg)) if isinstance(arg, str) else arg
                    for arg in record.args
                )
        
        return True


def setup_logging_with_filter():
    """
    Setup logging with sensitive data filtering.
    Call this at application startup.
    """
    # Get root logger
    root_logger = logging.getLogger()
    
    # Add sensitive data filter to all handlers
    sensitive_filter = SensitiveDataFilter()
    for handler in root_logger.handlers:
        handler.addFilter(sensitive_filter)
    
    # Also add to specific loggers
    for logger_name in ['uvicorn', 'uvicorn.access', 'uvicorn.error', 'fastapi']:
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers:
            handler.addFilter(sensitive_filter)
    
    logging.info("Logging configured with sensitive data filtering")


def redact_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Redact sensitive fields from a dictionary.
    Useful for logging request/response data.
    
    Args:
        data: Dictionary to redact
    
    Returns:
        Dictionary with sensitive fields redacted
    """
    if not isinstance(data, dict):
        return data
    
    redacted = data.copy()
    
    for key in redacted:
        if any(sensitive in key.lower() for sensitive in SENSITIVE_FIELDS):
            redacted[key] = "***REDACTED***"
        elif isinstance(redacted[key], dict):
            redacted[key] = redact_dict(redacted[key])
        elif isinstance(redacted[key], list):
            redacted[key] = [
                redact_dict(item) if isinstance(item, dict) else item
                for item in redacted[key]
            ]
    
    return redacted

# Made with Bob