"""THE config — darkfactory.json at the repo root pipes every value to its
slot at runtime (the client.json pattern: the program is complete; the config
is the instance). Env vars override individual knobs (CI tuning); the API key
itself is NEVER in the config — only the NAME of the env var that holds it."""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "darkfactory.json").read_text())


def knob(name: str, env: str = None):
    """config value, overridable by env (env wins when set)."""
    v = os.environ.get(env) if env else None
    return v if v is not None else CFG[name]


# the model pipes to every runtime via the env MiniMaxRuntime already reads
os.environ.setdefault("CAVE_MINIMAX_MODEL", CFG["model"])

FACTORY_NAME = CFG["factory_name"]
PLAYERS = list(CFG["players"])
DEV_ROUNDS = int(knob("dev_rounds", "FACTORY_DEV_ROUNDS"))
LIVE_ROUNDS = int(knob("live_rounds", "FACTORY_LIVE_ROUNDS"))
REPLICATES = int(knob("replicates", "FACTORY_REPLICATES"))
MAX_RULES = int(knob("max_rules", "FACTORY_MAX_RULES"))
MAX_RUNS_PER_DAY = int(knob("max_runs_per_day", "FACTORY_MAX_RUNS_PER_DAY"))
API_KEY_ENV = CFG["api_key_env"]
CHARTER = CFG["charter"]
WORLD_DIR = CFG["world_dir"]


def have_key() -> bool:
    return bool(os.environ.get(API_KEY_ENV))
