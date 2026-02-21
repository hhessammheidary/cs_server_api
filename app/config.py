import json
import os
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE = Path("/app") if Path("/app").exists() else Path(".")
SERVERS_FILE = os.environ.get("SERVERS_FILE", str(BASE / "servers.json"))

QUERY_TIMEOUT = float(os.environ.get("QUERY_TIMEOUT", "3.0"))

API_KEY = os.environ.get("API_KEY", "your-secret-api-key-here-change-this")

def load_servers() -> List[Dict]:
    p = Path(SERVERS_FILE)
    if not p.exists():
        raise FileNotFoundError(f"{p} not found. Please create servers.json with a list of servers.")
    data = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "servers" in data:
        return data["servers"]
    if isinstance(data, list):
        return data
    raise ValueError("servers.json must be either {\"servers\": [...]} or a list of server objects.")
