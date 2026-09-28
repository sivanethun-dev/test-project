"""コマンドライン入口."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .converter import convert_to_daitec_bcs
from .readers import read_input
from .writers import write_bcs_csv, write_report_text, write_review_excel


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mitsumorou-to-daitec",
        description=(
            "建築みつも郎12の見積データを、ダイテック住宅クラウド取込用の"
            "BCS.CSV（および確認用Excel）へ変換します。"
        ),
    )
    parser.add_argument("input", type=Path, help="みつも郎から出力した CSV / TXT / Excel")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="出力する BCS.CSV のパス（省略時は input 名_daitec_bcs.csv）",
    )
    parser.add_argument(
        "--excel-review",
        type=Path,
        help="確認用Excelの出力パス（省略可）",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="検証レポート(.txt)の出力パス（省略可）",
    )
    parser.add_argument(
        "--encoding",
        default="cp932",
        choices=["cp932", "utf-8-sig", "utf-8"],
        help="出力CSVの文字コード（既定: cp932）",
    )
    parser.add_argument(
        "--keep-summary-rows",
        action="store_true",
        help="小計・合計行（S/T/N）を除外せず残す",
    )
    parser.add_argument(
        "--sheet",
        default=0,
        help="Excel入力時のシート名または番号（既定: 0）",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    input_path: Path = args.input
    if not input_path.exists():
        print(f"入力ファイルが見つかりません: {input_path}", file=sys.stderr)
        return 1

    sheet: str | int
    try:
        sheet = int(args.sheet)
    except (TypeError, ValueError):
        sheet = str(args.sheet)

    try:
        raw_rows = read_input(input_path, sheet_name=sheet)
    except Exception as exc:  # noqa: BLE001 - CLIでは要約して返す
        print(f"読み込みに失敗しました: {exc}", file=sys.stderr)
        return 1

    rows, report = convert_to_daitec_bcs(
        raw_rows,
        drop_summary_rows=not args.keep_summary_rows,
    )

    output_path = args.output or input_path.with_name(f"{input_path.stem}_daitec_bcs.csv")
    write_bcs_csv(rows, output_path, encoding=args.encoding)

    if args.excel_review:
        write_review_excel(rows, report, args.excel_review)
    if args.report:
        write_report_text(report, args.report)
    else:
        # 標準でも簡易レポートを隣に出す
        default_report = output_path.with_suffix(".report.txt")
        write_report_text(report, default_report)

    print(f"変換完了: {output_path}")
    print(
        f"行数={len(rows)} / 除外={report.skipped_row_count} / "
        f"エラー={len(report.errors)} / 警告={len(report.warnings)}"
    )
    if report.errors:
        print("エラーがあるため、取込前に内容を確認してください。", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
