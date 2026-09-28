# 建築みつも郎12 → ダイテック住宅クラウド 見積データ移行ツール

建築みつも郎12（通称: みつも郎 / 見積もろう）の見積データを、ダイテック「注文分譲クラウドDX / 住宅クラウド」へ取り込むための変換プログラムです。

## できること

| 機能 | 内容 |
|------|------|
| BCS.CSV 正規化 | みつも郎が出した BCS.CSV を検証・整形し、ダイテック取込用に出力 |
| フラット明細変換 | 名称・仕様・数量・単位・単価だけの CSV/Excel を BCS 階層形式へ変換 |
| 小計行の除外 | ダイテック取込で問題になりやすい小計・合計行（S/T/N）を自動除外 |
| 確認用Excel | 明細・サマリ・検証結果シート付きのレビュー用ブックを出力 |

両製品とも **BCS.CSV**（建築業協会関西支部の共通見積フォーマット）に対応しているため、基本ルートは次のとおりです。

```
みつも郎12 →（BCS.CSV / Excel / テキスト出力）→ 本ツール → BCS.CSV → ダイテック住宅クラウドへ取込
```

## セットアップ

```bash
pip install -r requirements.txt
```

## 使い方

### 1. みつも郎側でデータを出す

おすすめ順:

1. **BCS.CSV で出力**（可能ならこれが最短）
2. メニュー「入出力」→「書類のテキスト出力」で CSV/Excel
3. 「現在階層のテキスト入出力」で明細をテキスト出力

### 2. 本ツールで変換

```bash
# BCS.CSV / CSV / Excel いずれも可
python -m mitsumorou_to_daitec samples/sample_mitsumorou_bcs.csv \
  -o output/estimate_daitec_bcs.csv \
  --excel-review output/estimate_review.xlsx

# フラットな明細CSVの例
python -m mitsumorou_to_daitec samples/sample_mitsumorou_flat.csv \
  -o output/flat_daitec_bcs.csv
```

主なオプション:

- `-o` … 出力 BCS.CSV パス
- `--excel-review` … 確認用 Excel
- `--encoding cp932` … 出力文字コード（既定は Windows 向け cp932）
- `--keep-summary-rows` … 小計・合計行を残す
- `--sheet` … Excel のシート指定

### 3. ダイテック住宅クラウドへ取り込む

1. 注文分譲クラウドDX（住宅クラウド）にログイン
2. 見積書（または実行予算）の **外部データ取込**
3. 形式に **BCS.CSV** を選び、本ツールの出力ファイルを指定

※ 画面名称は契約プランやバージョンで多少異なります。取込メニューが見つからない場合はダイテックサポートへ「BCS.CSV取込」と問い合わせてください。

## サンプル

- `samples/sample_mitsumorou_bcs.csv` … BCS形式のサンプル
- `samples/sample_mitsumorou_flat.csv` … 階層なし明細のサンプル

## 注意事項

- 代価表の入れ子・当量が 1 以外の代価など、BCS 仕様上渡せない構造は単価のみ残る／欠落することがあります。
- 単価の小数点は BCS 仕様上非推奨です（警告を出します）。
- 顧客マスタ・物件マスタ・実行予算の紐付けまでは本ツールの対象外です（見積明細の移行が中心）。
- 本番データで試す前に、必ず **1件の見積で試験取込** をして金額・階層を確認してください。
- ダイテック独自の「クラウド入出力用EXCEL」テンプレート列が判明している場合は、その列順への出力も追加できます。

## テスト

```bash
pip install -r requirements.txt pytest
python -m pytest -q
```

## 今後の拡張案

- ダイテック「クラウド入出力用EXCEL」テンプレート完全準拠出力
- 複数見積の一括変換（フォルダ指定）
- みつも郎独自バイナリ書類（.xxx）からの直接読取（仕様公開時）
