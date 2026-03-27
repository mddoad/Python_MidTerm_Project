import json
from pathlib import Path

class JsonStore:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load(self) -> list[dict]:
        if not self.file_path.exists():
            return []
        with self.file_path.open('r', encoding='utf-8') as f:
            return json.load(f)
        
    def save(self, data: list[dict]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)