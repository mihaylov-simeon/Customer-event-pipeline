import sys
from pathlib import Path

# Project root fixer
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Full path prefix
PATH_PREFIX = "/Users/simeonmihaylov/Coding-projects/portfolio-project-2"

# Inbox path
DATA_PATH = f"file://{PATH_PREFIX}/data/inbox"

# Bronze Layer Paths
BRONZE_PATH = f"file://{PATH_PREFIX}/data/bronze/events"
BRONZE_CHECKPOINT_PATH = f"file://{PATH_PREFIX}/data/bronze/_checkpoints/events"

# Silver Layer Paths
SILVER_PATH = f"file://{PATH_PREFIX}/data/silver/events"
SILVER_CHECKPOINT_PATH = f"file://{PATH_PREFIX}/data/silver/_checkpoints/events"

# Read Gold Layer Files
ACTIVE_USERS = f"file://{PATH_PREFIX}/data/gold/active_users_per_window"
EVENTS_PER_MINUTE = f"file://{PATH_PREFIX}/data/gold/events_per_minute"
MOST_PURCHASES_PER_DEVICE = f"file://{PATH_PREFIX}/data/gold/most_purchases_per_device"
REVENUE_PER_WINDOW = f"file://{PATH_PREFIX}/data/gold/revenue_per_window"

# Gold Checkpoint Paths
CHECKPOINT_ACTIVE_USERS_PER_WINDOW = f"file://{PATH_PREFIX}/data/gold/_checkpoints/active_users_per_window"
CHECKPOINT_REVENUE_PER_WINDOW = f"file://{PATH_PREFIX}/data/gold/_checkpoints/revenue_per_window"
CHECKPOINT_MOST_PURCHASES_PER_DEVICE = f"file://{PATH_PREFIX}/data/gold/_checkpoints/most_purchases_per_device"
CHECKPOINT_EVENTS_PER_MINUTE_PATH = f"file://{PATH_PREFIX}/data/gold/_checkpoints/events_per_minute"