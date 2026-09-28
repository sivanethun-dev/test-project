"""BCS.CSV（建築業協会関西支部）共通見積フォーマットの定義と検証."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# BCS.CSV 標準カラム（19項目）
BCS_COLUMNS: list[str] = [
    "階層1",
    "階層2",
    "階層3",
    "階層4",
    "階層5",
    "階層6",
    "階層7",
    "層番号",
    "通番号",
    "行種",
    "名称下段",
    "仕様下段",
    "数量",
    "呼称",
    "単価",
    "備考下段",
    "名称上段",
    "仕様上段",
    "備考上段",
]

# 英語ヘッダーや別名へのマッピング
COLUMN_ALIASES: dict[str, str] = {
    "階層１": "階層1",
    "階層２": "階層2",
    "階層３": "階層3",
    "階層４": "階層4",
    "階層５": "階層5",
    "階層６": "階層6",
    "階層７": "階層7",
    "level1": "階層1",
    "level2": "階層2",
    "level3": "階層3",
    "level4": "階層4",
    "level5": "階層5",
    "level6": "階層6",
    "level7": "階層7",
    "層番": "層番号",
    "行種類": "行種",
    "名称": "名称下段",
    "細目名称": "名称下段",
    "仕様": "仕様下段",
    "規格": "仕様下段",
    "規格名称": "仕様下段",
    "単位": "呼称",
    "備考": "備考下段",
    "金額": "単価",  # 誤用時の救済（金額列がある場合は後段で無視）
}

# 行種コード
ROW_TYPES: dict[str, str] = {
    "D": "通常行",
    "A": "補助行",
    "P": "親行",
    "Q": "代価親行",
    "B": "別紙親行",
    "E": "エレメント行",
    "N": "QBE計行",
    "S": "小計行",
    "T": "合計行",
}

# ダイテック取込で問題になりやすい行種
SKIP_ROW_TYPES_FOR_DAITEC: frozenset[str] = frozenset({"N", "S", "T"})


@dataclass
class ValidationIssue:
    """1件の検証結果."""

    row_index: int  # 1始まり（ヘッダー除くデータ行）
    level: str  # "error" | "warning"
    message: str


@dataclass
class ValidationReport:
    """検証レポート."""

    issues: list[ValidationIssue] = field(default_factory=list)
    row_count: int = 0
    skipped_row_count: int = 0

    @property
    def errors(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.level == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.level == "warning"]

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


def normalize_header(name: str) -> str:
    """ヘッダー名を標準カラム名に正規化."""
    key = str(name).strip()
    if key in BCS_COLUMNS:
        return key
    return COLUMN_ALIASES.get(key, key)


def empty_bcs_row() -> dict[str, Any]:
    """空のBCS行を返す."""
    return {col: "" for col in BCS_COLUMNS}


def _to_int_or_blank(value: Any) -> str:
    if value is None or value == "":
        return ""
    try:
        return str(int(float(str(value).replace(",", ""))))
    except (TypeError, ValueError):
        return str(value).strip()


def _to_number_or_blank(value: Any) -> str:
    if value is None or value == "":
        return ""
    text = str(value).strip().replace(",", "")
    if text == "":
        return ""
    try:
        num = float(text)
        if num.is_integer():
            return str(int(num))
        return str(num)
    except ValueError:
        return text


def normalize_row(raw: dict[str, Any]) -> dict[str, Any]:
    """生データ行をBCS標準行に正規化."""
    mapped: dict[str, Any] = {}
    for key, value in raw.items():
        std = normalize_header(key)
        mapped[std] = value

    row = empty_bcs_row()
    for col in BCS_COLUMNS:
        if col not in mapped:
            continue
        value = mapped[col]
        if col.startswith("階層") or col in {"層番号", "通番号"}:
            row[col] = _to_int_or_blank(value)
        elif col in {"数量", "単価"}:
            row[col] = _to_number_or_blank(value)
        elif col == "行種":
            code = str(value).strip().upper() if value is not None else ""
            row[col] = code
        else:
            row[col] = "" if value is None else str(value).strip()
    return row


def validate_rows(
    rows: list[dict[str, Any]],
    *,
    drop_summary_rows: bool = True,
) -> tuple[list[dict[str, Any]], ValidationReport]:
    """BCS行を検証し、必要に応じて小計・合計行を除外する."""
    report = ValidationReport(row_count=len(rows))
    cleaned: list[dict[str, Any]] = []

    for idx, raw in enumerate(rows, start=1):
        row = normalize_row(raw)
        row_type = row["行種"]

        if drop_summary_rows and row_type in SKIP_ROW_TYPES_FOR_DAITEC:
            report.skipped_row_count += 1
            report.issues.append(
                ValidationIssue(
                    row_index=idx,
                    level="warning",
                    message=(
                        f"行種 '{row_type}'（{ROW_TYPES.get(row_type, '不明')}）は"
                        "ダイテック取込対象外のため除外しました"
                    ),
                )
            )
            continue

        if row_type and row_type not in ROW_TYPES:
            report.issues.append(
                ValidationIssue(
                    row_index=idx,
                    level="warning",
                    message=f"未知の行種コード '{row_type}' です",
                )
            )

        # 階層1は必須
        if not row["階層1"]:
            report.issues.append(
                ValidationIssue(
                    row_index=idx,
                    level="error",
                    message="階層1が空です",
                )
            )

        # 層番号・通番号・行種は通常必須
        for required in ("層番号", "通番号", "行種"):
            if not row[required]:
                report.issues.append(
                    ValidationIssue(
                        row_index=idx,
                        level="error",
                        message=f"{required}が空です",
                    )
                )

        # 通常行で名称が無い場合は警告
        if row_type == "D" and not row["名称下段"] and not row["名称上段"]:
            report.issues.append(
                ValidationIssue(
                    row_index=idx,
                    level="warning",
                    message="通常行に名称がありません",
                )
            )

        # 単価の小数点警告（BCS仕様上は整数推奨）
        unit_price = row["単価"]
        if unit_price and "." in str(unit_price):
            report.issues.append(
                ValidationIssue(
                    row_index=idx,
                    level="warning",
                    message=(
                        f"単価に小数点があります（{unit_price}）。"
                        "BCS.CSV仕様上、取込時に誤差が出る可能性があります"
                    ),
                )
            )

        cleaned.append(row)

    return cleaned, report
