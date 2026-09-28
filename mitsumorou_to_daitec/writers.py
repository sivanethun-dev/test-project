"""ダイテック取込用ファイルの書き出し."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from .bcs import BCS_COLUMNS, ValidationReport


def write_bcs_csv(
    rows: list[dict[str, Any]],
    path: Path,
    *,
    encoding: str = "cp932",
    with_header: bool = True,
) -> None:
    """
    BCS.CSVを書き出す.

    ダイテック / みつも郎ともに日本語Windows環境では cp932(Shift_JIS) が安全なことが多い。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame([{c: r.get(c, "") for c in BCS_COLUMNS} for r in rows], columns=BCS_COLUMNS)
    df.to_csv(
        path,
        index=False,
        encoding=encoding,
        header=with_header,
        lineterminator="\r\n",
    )


def write_review_excel(
    rows: list[dict[str, Any]],
    report: ValidationReport,
    path: Path,
) -> None:
    """確認用Excel（明細 + 検証結果）を書き出す."""
    path.parent.mkdir(parents=True, exist_ok=True)
    detail = pd.DataFrame([{c: r.get(c, "") for c in BCS_COLUMNS} for r in rows], columns=BCS_COLUMNS)
    issues = pd.DataFrame(
        [
            {"行番号": i.row_index, "レベル": i.level, "内容": i.message}
            for i in report.issues
        ]
    )
    summary = pd.DataFrame(
        [
            {"項目": "入力行数", "値": report.row_count},
            {"項目": "出力行数", "値": len(rows)},
            {"項目": "除外行数", "値": report.skipped_row_count},
            {"項目": "エラー数", "値": len(report.errors)},
            {"項目": "警告数", "値": len(report.warnings)},
        ]
    )
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        detail.to_excel(writer, sheet_name="見積明細", index=False)
        summary.to_excel(writer, sheet_name="サマリ", index=False)
        issues.to_excel(writer, sheet_name="検証結果", index=False)


def write_report_text(report: ValidationReport, path: Path) -> None:
    """検証レポートをテキストで書き出す."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "=== みつも郎 → ダイテック 移行検証レポート ===",
        f"入力行数: {report.row_count}",
        f"除外行数: {report.skipped_row_count}",
        f"エラー: {len(report.errors)}",
        f"警告: {len(report.warnings)}",
        "",
    ]
    for issue in report.issues:
        lines.append(f"[{issue.level}] 行{issue.row_index}: {issue.message}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
