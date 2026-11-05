from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import pandas as pd
import random


class DatasetType(Enum):
    CONTROLLED = "constructed"
    NATURALISTIC = "dialogue"
    LUDWIG = "ludwig"


_DEFAULT_PATHS: dict[DatasetType, str] = {
    DatasetType.CONTROLLED: "src/data/master_constructed.csv",
    DatasetType.NATURALISTIC: "src/data/master_dialogue.csv",
    DatasetType.LUDWIG: "src/data/ludwig.csv",
}

_OPTION_COLS = ["Option_1", "Option_2", "Option_3", "Option_4", "Option_5"]
_LUDWIG_OPTION_COLS = ["Implicature", "Incoherent"]


@dataclass
class DatasetConfig:
    dataset_type: str
    language: str | None = None
    task: str | None = None
    data_path: str | None = None
    shuffle_seed: int = 42
    root_dir: str = "."


@dataclass
class DataItem:
    item_id: int
    language: str
    task: str
    context: str
    options: list[str]
    answer_index: int
    original_row: dict[str, Any] = field(repr=False, default_factory=dict)


class PragmaticsDataset:

    def __init__(self, cfg: DatasetConfig | Any) -> None:
        self.cfg = cfg
        self.dataset_type = DatasetType(cfg.dataset_type)
        self.items: list[DataItem] = []
        self._rng = random.Random(cfg.shuffle_seed)
        self._load()

    def _resolve_path(self) -> Path:
        if self.cfg.data_path:
            return Path(self.cfg.root_dir) / self.cfg.data_path
        return Path(self.cfg.root_dir) / _DEFAULT_PATHS[self.dataset_type]

    def _load(self) -> None:
        df = pd.read_csv(self._resolve_path())
        df = self._filter(df)

        if self.dataset_type in (DatasetType.CONTROLLED, DatasetType.NATURALISTIC):
            self.items = self._parse_standard(df)
        else:
            self.items = self._parse_ludwig(df)

    def _filter(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.cfg.language:
            df = df[df["Language"].str.upper() == self.cfg.language.upper()]
        if self.cfg.task:
            df = df[df["Task"].str.lower() == self.cfg.task.lower()]
        return df.reset_index(drop=True)

    def _shuffle_options(self, options: list[str], answer_idx: int) -> tuple[list[str], int]:
        indexed = list(enumerate(options))
        self._rng.shuffle(indexed)
        new_answer = next(i for i, (orig, _) in enumerate(indexed) if orig == answer_idx)
        shuffled = [opt for _, opt in indexed]
        return shuffled, new_answer

    def _parse_standard(self, df: pd.DataFrame) -> list[DataItem]:
        items: list[DataItem] = []
        for _, row in df.iterrows():
            options = [str(row[c]) for c in _OPTION_COLS if pd.notna(row.get(c)) and str(row[c]).strip()]
            answer_idx = int(row["Answer"]) - 1
            options, answer_idx = self._shuffle_options(options, answer_idx)
            items.append(DataItem(
                item_id=int(row["Item_id"]),
                language=str(row["Language"]),
                task=str(row["Task"]),
                context=str(row["Context"]),
                options=options,
                answer_index=answer_idx,
                original_row=row.to_dict(),
            ))
        return items

    def _parse_ludwig(self, df: pd.DataFrame) -> list[DataItem]:
        items: list[DataItem] = []
        for _, row in df.iterrows():
            options = [str(row[c]).strip() for c in _LUDWIG_OPTION_COLS]
            answer_idx = 0
            options, answer_idx = self._shuffle_options(options, answer_idx)
            context = f"A:{str(row['Context'])}\nB:{str(row['Response'])}"
            items.append(DataItem(
                item_id=int(row["Item_id"]),
                language=str(row["Language"]),
                task=str(row["Task"]),
                context=context,
                options=options,
                answer_index=answer_idx,
                original_row=row.to_dict(),
            ))
        return items

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, idx: int) -> DataItem:
        return self.items[idx]

    def __iter__(self):
        return iter(self.items)

    def format_question(self, item: DataItem) -> str:
        lines = [item.context, ""]
        for i, opt in enumerate(item.options, 1):
            lines.append(f"{i}. {opt}")
        return "\n".join(lines)

    def get_answer_text(self, item: DataItem) -> str:
        return item.options[item.answer_index]

    def get_answer_number(self, item: DataItem) -> int:
        return item.answer_index + 1
