"""みつも郎形式 → BCS.CSV（ダイテック取込用）への変換."""

from __future__ import annotations

from typing import Any

from .bcs import (
    BCS_COLUMNS,
    ValidationReport,
    empty_bcs_row,
    normalize_row,
    validate_rows,
)
from .readers import looks_like_bcs


def _infer_level_from_indent(name: str) -> int:
    """先頭の空白・全角スペースから階層を推定（簡易）."""
    stripped = name.lstrip(" 　\t")
    indent = len(name) - len(stripped)
    if indent <= 0:
        return 1
    # 半角2文字 / 全角1文字 ≒ 1階層上とみなす
    return min(7, 1 + max(1, indent // 2))


def convert_flat_estimate_to_bcs(
    rows: list[dict[str, Any]],
    *,
    default_row_type: str = "D",
) -> list[dict[str, Any]]:
    """
    階層情報が薄いフラットな見積明細をBCS形式へ変換する.

    想定入力キー例: 名称 / 仕様 / 数量 / 単位 / 単価 / 備考
    またはすでに一部BCSカラムがある場合はそのまま利用。
    """
    result: list[dict[str, Any]] = []
    seq_by_level: dict[int, int] = {i: 0 for i in range(1, 8)}
    current_path = [0] * 7  # 階層1〜7の通番パス

    for raw in rows:
        # 既存のBCS行なら正規化のみ
        if "階層1" in raw or "行種" in raw:
            row = normalize_row(raw)
            result.append(row)
            continue

        original_name = str(raw.get("名称") or raw.get("名称下段") or raw.get("細目名称") or "")
        name = original_name.strip()
        spec = str(raw.get("仕様") or raw.get("仕様下段") or raw.get("規格") or "").strip()
        qty = raw.get("数量", "")
        unit = str(raw.get("単位") or raw.get("呼称") or "").strip()
        price = raw.get("単価", "")
        note = str(raw.get("備考") or raw.get("備考下段") or "").strip()
        explicit_type = str(raw.get("行種") or "").strip().upper()

        if not name and not spec and str(qty).strip() == "" and str(price).strip() == "":
            continue

        # 明示的な階層列があれば優先
        level = None
        for key in ("階層", "階層レベル", "level"):
            if key in raw and str(raw[key]).strip():
                try:
                    level = int(float(str(raw[key])))
                    break
                except ValueError:
                    pass
        if level is None:
            level = _infer_level_from_indent(original_name)
        level = max(1, min(7, level))

        # 数量・単価がなくインデントも浅い行は親行とみなす
        qty_blank = str(qty).strip() in {"", "nan", "None"}
        price_blank = str(price).strip() in {"", "nan", "None"}
        if explicit_type:
            row_type = explicit_type
        elif qty_blank and price_blank and level == 1:
            row_type = "P"
        else:
            row_type = default_row_type

        seq_by_level[level] += 1
        current_path[level - 1] = seq_by_level[level]
        # 下位階層をリセット
        for deeper in range(level, 7):
            seq_by_level[deeper + 1] = 0
            current_path[deeper] = 0

        row = empty_bcs_row()
        for i in range(1, level + 1):
            row[f"階層{i}"] = str(current_path[i - 1]) if current_path[i - 1] else ""

        row["層番号"] = str(level)
        row["通番号"] = str(seq_by_level[level])
        row["行種"] = row_type
        row["名称下段"] = name.lstrip(" 　\t")
        row["仕様下段"] = spec
        row["数量"] = "" if qty is None else str(qty).strip()
        row["呼称"] = unit
        row["単価"] = "" if price is None else str(price).strip()
        row["備考下段"] = note
        result.append(normalize_row(row))

    return result


def convert_to_daitec_bcs(
    rows: list[dict[str, Any]],
    *,
    drop_summary_rows: bool = True,
) -> tuple[list[dict[str, Any]], ValidationReport]:
    """入力行をダイテック取込用BCS.CSV行へ変換・検証する."""
    if looks_like_bcs(rows):
        normalized = [normalize_row(r) for r in rows]
    else:
        normalized = convert_flat_estimate_to_bcs(rows)

    return validate_rows(normalized, drop_summary_rows=drop_summary_rows)


def rows_to_dataframe_dict(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """書き出し用に列順を固定した辞書リストを返す."""
    return [{col: row.get(col, "") for col in BCS_COLUMNS} for row in rows]
