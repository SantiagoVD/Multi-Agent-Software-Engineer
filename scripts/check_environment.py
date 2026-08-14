"""Report local runtime prerequisites without modifying the environment."""

import json
import shutil
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import settings


def main() -> int:
    print(f"Python: {sys.version.split()[0]}")
    print(f"Git: {'available' if shutil.which('git') else 'missing'}")
    print(f"Node: {'available' if shutil.which('node') else 'missing'}")
    try:
        with urlopen(f"{settings.ollama_base_url.rstrip('/')}/api/tags", timeout=3) as response:
            payload = json.loads(response.read().decode("utf-8"))
        models = [item.get("name") for item in payload.get("models", [])]
        print(f"Ollama: online; models={models}")
        return 0 if settings.ollama_model in models else 1
    except (OSError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"Ollama: unavailable ({exc})")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
