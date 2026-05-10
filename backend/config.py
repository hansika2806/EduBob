"""
Centralized configuration for EduBob application.
Contains all constants, timeouts, limits, and security settings.
"""
import os
from typing import Final

# ============================================================================
# Security Settings
# ============================================================================

# Code execution timeout (seconds)
CODE_EXECUTION_TIMEOUT: Final[int] = 5

# Maximum input lengths
MAX_CODE_LENGTH: Final[int] = 10000  # 10KB
MAX_PROMPT_LENGTH: Final[int] = 5000  # 5KB
MAX_TEST_CASES: Final[int] = 100
MAX_ASSIGNMENT_TITLE_LENGTH: Final[int] = 200
MAX_ASSIGNMENT_DESCRIPTION_LENGTH: Final[int] = 5000

# Forbidden code patterns for security
FORBIDDEN_IMPORTS: Final[set] = {
    'os', 'sys', 'subprocess', 'socket', 'urllib', 'requests',
    'http', 'ftplib', 'telnetlib', 'pickle', 'shelve', 'marshal',
    'importlib', '__import__', 'eval', 'exec', 'compile', 'open',
    'file', 'input', 'raw_input'
}

FORBIDDEN_BUILTINS: Final[set] = {
    'eval', 'exec', 'compile', '__import__', 'open', 'file',
    'input', 'raw_input', 'execfile', 'reload', 'vars', 'dir',
    'globals', 'locals', 'getattr', 'setattr', 'delattr', 'hasattr'
}

# ============================================================================
# Database Settings
# ============================================================================

# Database connection pool settings
DB_POOL_SIZE: Final[int] = 10
DB_MAX_OVERFLOW: Final[int] = 20
DB_POOL_TIMEOUT: Final[int] = 30  # seconds
DB_POOL_RECYCLE: Final[int] = 3600  # 1 hour

# ============================================================================
# API Settings
# ============================================================================

# Rate limiting
API_RATE_LIMIT_PER_MINUTE: Final[int] = 60

# Pagination
DEFAULT_PAGE_SIZE: Final[int] = 20
MAX_PAGE_SIZE: Final[int] = 100

# ============================================================================
# Watson X Settings
# ============================================================================

# Watson X API configuration
WATSONX_API_KEY: Final[str] = os.getenv("WATSONX_API_KEY", "")
WATSONX_PROJECT_ID: Final[str] = os.getenv("WATSONX_PROJECT_ID", "")
WATSONX_URL: Final[str] = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

# Watson X model parameters
WATSONX_MODEL_ID: Final[str] = "meta-llama/llama-3-70b-instruct"
WATSONX_MAX_NEW_TOKENS: Final[int] = 2000
WATSONX_MIN_NEW_TOKENS: Final[int] = 50
WATSONX_TEMPERATURE: Final[float] = 0.7
WATSONX_TOP_P: Final[float] = 0.9
WATSONX_TOP_K: Final[int] = 50

# Watson X timeout settings
WATSONX_TIMEOUT: Final[int] = 30  # seconds
WATSONX_MAX_RETRIES: Final[int] = 3

# ============================================================================
# Logging Settings
# ============================================================================

# Log levels
LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO")

# Sensitive fields to redact in logs
SENSITIVE_FIELDS: Final[set] = {
    'password', 'api_key', 'token', 'secret', 'authorization',
    'cookie', 'session', 'credentials'
}

# ============================================================================
# Assignment Generation Settings
# ============================================================================

# Default difficulty levels
DIFFICULTY_LEVELS: Final[list] = ["easy", "medium", "hard"]

# Assignment generation timeouts
ASSIGNMENT_GENERATION_TIMEOUT: Final[int] = 60  # seconds

# ============================================================================
# Code Review Settings
# ============================================================================

# Review categories
REVIEW_CATEGORIES: Final[list] = [
    "maintainability",
    "security", 
    "performance",
    "functionality",
    "style"
]

# Review severity levels
REVIEW_SEVERITIES: Final[list] = ["critical", "high", "medium", "low"]

# ============================================================================
# Environment Settings
# ============================================================================

# Environment detection
ENVIRONMENT: Final[str] = os.getenv("ENVIRONMENT", "development")
IS_PRODUCTION: Final[bool] = ENVIRONMENT == "production"
IS_DEVELOPMENT: Final[bool] = ENVIRONMENT == "development"

# Debug mode
DEBUG: Final[bool] = os.getenv("DEBUG", "False").lower() == "true"

# ============================================================================
# CORS Settings
# ============================================================================

# Allowed origins for CORS
CORS_ORIGINS: Final[list] = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000"
]

# ============================================================================
# File Upload Settings
# ============================================================================

# Maximum file sizes
MAX_UPLOAD_SIZE: Final[int] = 5 * 1024 * 1024  # 5MB

# Allowed file extensions
ALLOWED_CODE_EXTENSIONS: Final[set] = {
    '.py', '.js', '.java', '.cpp', '.c', '.cs', '.go', '.rs',
    '.rb', '.php', '.swift', '.kt', '.ts', '.jsx', '.tsx'
}

# Made with Bob
