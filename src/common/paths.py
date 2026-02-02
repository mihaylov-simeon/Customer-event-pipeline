from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def _file_uri(path: Path) -> str:
    return f"file://{path.as_posix()}"

# Inbox path
DATA_PATH = _file_uri(PROJECT_ROOT / "data" / "inbox")

# Bronze Layer Paths
BRONZE_PATH = _file_uri(PROJECT_ROOT / "data" / "bronze" / "events")
BRONZE_CHECKPOINT_PATH = _file_uri(PROJECT_ROOT / "data" / "bronze" / "_checkpoints" / "events")

# Silver Layer Paths
SILVER_PATH = _file_uri(PROJECT_ROOT / "data" / "silver" / "events")
SILVER_CHECKPOINT_PATH = _file_uri(PROJECT_ROOT / "data" / "silver" / "_checkpoints" / "events")

# Read Gold Layer Files
ACTIVE_USERS = _file_uri(PROJECT_ROOT / "data" / "gold" / "active_users_per_window")
EVENTS_PER_MINUTE = _file_uri(PROJECT_ROOT / "data" / "gold" / "events_per_minute")
MOST_PURCHASES_PER_DEVICE = _file_uri(PROJECT_ROOT / "data" / "gold" / "most_purchases_per_device")
REVENUE_PER_WINDOW = _file_uri(PROJECT_ROOT / "data" / "gold" / "revenue_per_window")

# Gold Checkpoint Paths
CHECKPOINT_ACTIVE_USERS_PER_WINDOW = _file_uri(PROJECT_ROOT / "data" / "gold" / "_checkpoints" / "active_users_per_window")
CHECKPOINT_REVENUE_PER_WINDOW = _file_uri(PROJECT_ROOT / "data" / "gold" / "_checkpoints" / "revenue_per_window")
CHECKPOINT_MOST_PURCHASES_PER_DEVICE = _file_uri(PROJECT_ROOT / "data" / "gold" / "_checkpoints" / "most_purchases_per_device")
CHECKPOINT_EVENTS_PER_MINUTE_PATH = _file_uri(PROJECT_ROOT / "data" / "gold" / "_checkpoints" / "events_per_minute")
