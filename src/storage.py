import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FILE_PATH = DATA_DIR / "highscore.json"


def ensure_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not FILE_PATH.exists():
        FILE_PATH.write_text(
            json.dumps({"highscore": 0}, indent=2),
            encoding="utf-8"
        )


def load_highscore() -> int:
    ensure_file()
    data = json.loads(FILE_PATH.read_text(encoding="utf-8"))
    return int(data.get("highscore", 0))


def save_highscore(value: int) -> None:
    ensure_file()
    FILE_PATH.write_text(
        json.dumps({"highscore": int(value)}, indent=2),
        encoding="utf-8"
    )
