from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Any


@dataclass
class Verse:
    ref: str
    text: str


class VerseStore:
    def __init__(self, json_path: Path):
        self.json_path = Path(json_path)
        self._verses: List[Verse] = []
        self._index_file = self.json_path.with_suffix(".idx.json")
        self._load()

    def _load(self) -> None:
        if not self.json_path.exists():
            raise FileNotFoundError(f"Verses file not found: {self.json_path}")
        data: List[Dict[str, Any]] = json.loads(self.json_path.read_text(encoding="utf-8"))
        self._verses = [Verse(ref=item["ref"], text=item["text"]) for item in data if "ref" in item and "text" in item]
        if not self._verses:
            raise ValueError("No verses found in the verses file.")

    def random(self) -> Verse:
        return random.choice(self._verses)

    def next(self) -> Verse:
        """Sequential verse selection with persisted index."""
        state = self._read_state()
        idx = (state.get("index", -1) + 1) % len(self._verses)
        state["index"] = idx
        self._write_state(state)
        return self._verses[idx]

    def _read_state(self) -> Dict[str, Any]:
        try:
            return json.loads(self._index_file.read_text(encoding="utf-8")) if self._index_file.exists() else {}
        except Exception:
            return {}

    def _write_state(self, state: Dict[str, Any]) -> None:
        try:
            self._index_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass
