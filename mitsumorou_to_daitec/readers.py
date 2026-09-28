"""各種入力形式の読み込み."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import pandas as pd

from .bcs import BCS_COLUMNS, normalize_header


def detect_encoding(path: Path) -> str:
    """日本語環境でよく使われるエンコーディングを推定."""
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "cp932", "shift_jis", "utf-8"):
        try:
            raw.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue
    return "cp932"


def _dataframe_to_rows(df: pd.DataFrame) -> list[dict[str, Any]]:
    # ヘッダー正規化
    df = df.rename(columns={c: normalize_header(str(c)) for c in df.columns})
    # 完全空行を除外
    df = df.dropna(how="all")
    rows: list[dict[str, Any]] = []
    for _, series in df.iterrows():
        row = {col: series[col] if col in series and pd.notna(series[col]) else "" for col in df.columns}
        rows.append(row)
    return rows


def read_csv_file(path: Path) -> list[dict[str, Any]]:
    """CSV / BCS.CSV を読み込む."""
    encoding = detect_encoding(path)
    # 区切り文字の推定（カンマ / タブ）
    sample = path.read_text(encoding=encoding, errors="replace")[:4096]
    delimiter = "\t" if sample.count("\t") > sample.count(",") else ","

    df = pd.read_csv(
        path,
        encoding=encoding,
        dtype=str,
        keep_default_na=False,
        sep=delimiter,
        engine="python",
    )
    return _dataframe_to_rows(df)


def read_excel_file(path: Path, sheet_name: str | int | None = 0) -> list[dict[str, Any]]:
    """Excel（みつも郎のExcel出力 / クラウド入出力用）を読み込む."""
    df = pd.read_excel(path, sheet_name=sheet_name if sheet_name is not None else 0, dtype=str)
    df = df.fillna("")
    return _dataframe_to_rows(df)


def read_mitsumorou_text(path: Path) -> list[dict[str, Any]]:
    """
    みつも郎の「書類のテキスト出力」「現在階層のテキスト入出力」形式を想定して読み込む.

    想定カラム例:
      名称, 仕様, 数量, 単位, 単価, 備考
    階層情報が無い場合は後段の converter で補完する。
    """
    return read_csv_file(path)


def read_input(path: Path, sheet_name: str | int | None = 0) -> list[dict[str, Any]]:
    """拡張子に応じて入力を読み込む."""
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls", ".xlsm"}:
        return read_excel_file(path, sheet_name=sheet_name)
    if suffix in {".csv", ".txt", ".tsv"}:
        return read_csv_file(path)
    raise ValueError(f"未対応のファイル形式です: {suffix}")


def looks_like_bcs(rows: list[dict[str, Any]]) -> bool:
    """行データがBCS形式に近いか判定."""
    if not rows:
        return False
    keys = {normalize_header(k) for k in rows[0].keys()}
    required = {"階層1", "層番号", "通番号", "行種"}
    return required.issubset(keys) or sum(1 for c in BCS_COLUMNS if c in keys) >= 10


def write_preview_csv(rows: list[dict[str, Any]], path: Path) -> None:
    """デバッグ用にプレビューCSVを書き出す."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=BCS_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
