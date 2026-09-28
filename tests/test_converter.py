"""変換ロジックの単体テスト."""

from __future__ import annotations

from pathlib import Path

from mitsumorou_to_daitec.converter import convert_to_daitec_bcs
from mitsumorou_to_daitec.readers import read_input
from mitsumorou_to_daitec.writers import write_bcs_csv

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "samples"


def test_bcs_sample_converts_and_drops_summary(tmp_path: Path) -> None:
    rows = read_input(SAMPLES / "sample_mitsumorou_bcs.csv")
    converted, report = convert_to_daitec_bcs(rows)
    assert report.ok
    assert report.skipped_row_count == 1  # 小計行
    assert len(converted) == 9
    assert converted[0]["行種"] == "P"
    assert converted[1]["名称下段"] == "仮囲い"

    out = tmp_path / "out.csv"
    write_bcs_csv(converted, out, encoding="utf-8-sig")
    assert out.exists()
    text = out.read_text(encoding="utf-8-sig")
    assert "仮囲い" in text
    assert "小計" not in text


def test_flat_sample_builds_hierarchy() -> None:
    rows = read_input(SAMPLES / "sample_mitsumorou_flat.csv")
    converted, report = convert_to_daitec_bcs(rows)
    assert report.ok
    assert len(converted) >= 8
    # 先頭は親相当の階層1
    assert converted[0]["階層1"] == "1"
    names = [r["名称下段"] for r in converted]
    assert "構造用合板" in names
