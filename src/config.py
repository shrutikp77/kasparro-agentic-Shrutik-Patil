"""
Configuration Module

Centralized configuration for the content generation system.
Provides paths, environment settings, and system-wide constants.
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Dataset Configuration
DEFAULT_DATASET_PATH = os.getenv(
    "DEFAULT_DATASET_PATH",
    str(PROJECT_ROOT / "data" / "products.json")
)

# Output Configuration
OUTPUT_DIR = os.getenv("OUTPUT_DIR", str(PROJECT_ROOT / "output"))

# LLM Configuration
AGENT_DELAY = int(os.getenv("AGENT_DELAY", "5"))
DEFAULT_MAX_RETRIES = int(os.getenv("DEFAULT_MAX_RETRIES", "3"))
DEFAULT_MAX_TOKENS = int(os.getenv("DEFAULT_MAX_TOKENS", "2000"))

# Validation Configuration
MIN_FAQ_COUNT = 15  # Hard requirement from assignment
