# test-project 引き継ぎメモ（ChatGPT／外部チャット用）

**作成:** 2026-10-30（Asia/Tokyo）  
**リポジトリ:** https://github.com/sivanethun-dev/test-project  
**基準ブランチ:** `main`  
**このファイルの場所:** リポジトリ直下 `HANDOFF.md`  
**元クラウドチャット:** https://cursor.com/agents/bc-01a18d4d-7675-795a-af1d-dda0e29a9e2a

> Cursor Canvas は Cursor 外（ChatGPT 等）から開けないため、同じ内容をこの Markdown に置いています。  
> 当チャットでは共有URL確認のみで、コード変更はなし（この引き継ぎファイル追加を除く）。

---

## 1. 目的

`sivanethun-dev/test-project` は Cursor Cloud Agent 用の個人作業置き場。テーマは固定ではなく、メモ・調査レポート・小さなツールをブランチ／PR単位で蓄積している。

| 系統 | 目的 | 状態 |
|------|------|------|
| 投資調査 | SNS投資ポストを「使える／ノイズ／破棄」に分類し、帰宅後の保有データ突合用にする。売買推奨ではない。 | 第1・2弾は `main`。第4弾・リテラシー・連続増配・TQQQ検証は PR #3（未マージ） |
| 見積データ移行 | 建築みつも郎12 → ダイテック住宅クラウドへ BCS.CSV 経由で見積明細を取り込む変換ツール | PR #5（DRAFT） |
| ファッション比較 | UNFILO BREEZEMOVE とワイド／ストレート系の比較評価 | PR #4（DRAFT） |
| その他チャット | 化粧水・旅行保険・ローン・駅の道順など一問一答。リポへの成果物なし | エージェント履歴のみ |

---

## 2. 登録済みデータ・主要結論

### 調査候補（優先）

| コード | 名称 | 出典 | 要点 |
|--------|------|------|------|
| 464A | QPSホールディングス | 第1弾 | 小型SAR衛星。唯一の成長テーマ調査候補。IR突合必須 |
| 8524 | 北洋銀行 | 第2弾 | 年4回配当は公式確認済。利回り・地銀リスクは未検証 |

### 整理用（買う根拠にはしない）

- 半導体工程別マップ（前工程／後工程／素材／パワー）
- 高配当10選（時点切れ価格）
- 連続増配30選＋花王（PR #3）
- AI冷却・IOWNのボトルネック整理（テーマのみ採用）

### 破棄・接触禁止

LINE／DMキーワード誘導、非現実リターン（300倍等）、底値宣言＋枚数指定、南鳥島イットリウム煽り5銘柄、Ferrari演出FOMO。  
原則「誰が・いくら儲かった・必ず・今すぐ・DM/LINE」は勧誘扱い。

---

## 3. 決定事項（運用ルール）

| 決定 | 内容 |
|------|------|
| 判断の一次情報 | 決算・適時開示・有報・公式IRのみ。SNSは銘柄名・テーマのヒント止まり |
| レポートの性質 | 情報の質の評価であり売買推奨ではない |
| 帰宅後手順 | 破棄枠除外 → 保有・検討リストと突合 → 優先銘柄だけIR調査 → 自分のルールでエントリー判断 |
| コード確認 | SNSの証券コードは必ず再確認（例: キオクシアを6758と誤記） |
| みつも郎移行範囲 | 見積明細（BCS.CSV）が中心。顧客マスタ・物件紐付けは対象外。本番前に1件試験取込推奨 |
| BREEZEMOVE結論 | 猛暑通勤・セットアップなら機能利点あり。ワイドストレート好きなら利点薄い（テーパード） |

---

## 4. 現在の進捗

- `main` 上のレポート: **2本**（第1・2弾）
- 中身あり未マージPR: **3本**（#3, #4, #5）
- マージ済PR: **#2**
- 当チャットの差分（引き継ぎ前）: **なし**

| PR | タイトル | ブランチ | 状態 |
|----|----------|----------|------|
| #2 | SNS投資ポスト評価レポート（第1＋第2弾） | （当時）cursor/sns-investment-report-0092 | MERGED → main |
| #3 | 投資リテラシー＋SNS評価＋連続増配30選解析 | `cursor/sns-investment-report-0092` | OPEN / DRAFT |
| #4 | UNFILO BREEZEMOVE ファッション比較 | `cursor/unfilo-breezemove-compare-8321` | OPEN / DRAFT |
| #5 | みつも郎12 → ダイテック BCS 移行ツール | `cursor/mitsumorou-daitec-migration-63d9` | OPEN / DRAFT |
| #1 | Update README to say hello | `cursor/readme-hello-3aef` | OPEN / DRAFT（実質無視可） |

**注意:** PR #2 マージ後も同ブランチ `cursor/sns-investment-report-0092` 上で PR #3 が続いている。`main` には第1・2弾だけ。第3弾ファイルはリポ上に見当たらず、第4弾・関連メモが PR #3 側。

PRリンク:

- https://github.com/sivanethun-dev/test-project/pull/3
- https://github.com/sivanethun-dev/test-project/pull/4
- https://github.com/sivanethun-dev/test-project/pull/5

---

## 5. 残っている作業

### 投資系統

| 作業 | 詳細 |
|------|------|
| PR #3 のマージ判断 | 第4弾・リテラシー基礎・連続増配30選・TQQQ検証を main に取り込むか決める |
| QPS 464A IR突合 | 決算・打上げ計画・防衛案件・希薄化・競合（レポート内チェックリスト） |
| 北洋銀行 8524 確認 | 利回り再計算、配当性向・自己資本・不良債権、増配持続性、NISA設計 |
| 自宅リスト再分類 | 配当／半導体前工程／後工程／素材／その他でテーマ偏りチェック |
| 高配当・連続増配の再計算 | 投稿時点価格は古い。利回り・減配履歴を一次情報で更新 |

### みつも郎移行（PR #5）

| 作業 | 詳細 |
|------|------|
| 試験取込 | 生成 BCS.CSV をダイテック「外部データ取込」で1件テスト |
| 独自Excel対応 | ダイテック「クラウド入出力用EXCEL」列仕様が分かれば出力形式追加可 |
| スコープ外確認 | 顧客マスタ・物件紐付けは別途 |

### その他

- PR #4 のマージ／クローズ判断
- PR #1（hello）はクローズ候補
- **保有・検討リストの実データはこのリポに未登録**（レポートは突合用テンプレのみ）

---

## 6. ファイル一覧

### main（現行）

| パス | 説明 |
|------|------|
| `README.md` | プレースホルダ（`# test-project` のみ） |
| `HANDOFF.md` | 本引き継ぎメモ（外部チャット共有用） |
| `reports/2026-08-06_SNS投資ポスト評価レポート.md` | 第1弾。詐欺除外・QPS調査候補 |
| `reports/2026-08-10_SNS投資ポスト評価レポート.md` | 第2弾。北洋銀行・半導体マップ・高配当メモ |

### ブランチ `cursor/sns-investment-report-0092`（PR #3・未マージ）

| パス | 説明 |
|------|------|
| `reports/2026-08-12_SNS投資ポスト評価レポート_第4弾.md` | 半導体ニッチ／AI冷却・IOWN／破棄投稿 |
| `reports/2026-08-12_S&P_NDX_TQQQ40年倍率の検証.md` | 40年倍率クレームの検証メモ |
| `reports/2026-08-14_連続増配株30選_解析レポート.md` | 連続増配ランキング解析 |
| `reports/投資リテラシー基礎メモ.md` | 投資 vs 投機、SNSフィルタ、90日学習プラン |

GitHub上の表示例（ブランチ指定）:

- https://github.com/sivanethun-dev/test-project/tree/cursor/sns-investment-report-0092/reports

### ブランチ `cursor/mitsumorou-daitec-migration-63d9`（PR #5・未マージ）

| パス | 説明 |
|------|------|
| `mitsumorou_to_daitec/*.py` | BCS検証・変換・CLI・I/O |
| `requirements.txt` | 依存 |
| `samples/sample_mitsumorou_bcs.csv` | BCSサンプル |
| `samples/sample_mitsumorou_flat.csv` | フラット明細サンプル |
| `tests/test_converter.py` | 変換テスト |
| `.gitignore` | 追加 |
| `README.md` | 使い方を拡充（ブランチ上） |

関連エージェント: https://cursor.com/agents/bc-01a0e7ad-022e-7cee-9d7b-9c15b98a63d9

### ブランチ `cursor/unfilo-breezemove-compare-8321`（PR #4・未マージ）

| パス | 説明 |
|------|------|
| `reports/2026-08-25_UNFILO_BREEZEMOVE製品比較評価.md` | BREEZEMOVE vs ワイド／ストレート比較 |

関連エージェント: https://cursor.com/agents/bc-01a03871-1f1f-7b95-ba5f-09fe18128321

---

## 7. 次チャットへの開始ヒント

- **投資続き** → PR #3 ブランチを checkout／マージ検討から
- **みつも郎** → `cursor/mitsumorou-daitec-migration-63d9`
- **新規タスク** → `main` から新ブランチ

ChatGPT 等に渡すときは、次のいずれかを渡せば読める:

1. **このファイルの GitHub URL**（マージ後）:  
   https://github.com/sivanethun-dev/test-project/blob/main/HANDOFF.md  
2. **生テキスト URL**（マージ後）:  
   https://raw.githubusercontent.com/sivanethun-dev/test-project/main/HANDOFF.md  
3. またはこの `HANDOFF.md` の全文をそのまま貼り付け

---

## 8. 第1弾・第2弾の超要約（main上）

### 第1弾（2026-08-06）

- **結論:** そのまま買う材料としてはほぼ使えない。調査候補は QPS（464A）のみ。
- 破棄: LINE誘導・300倍約束など2件
- ノイズ: 煽り・チャート占い・定番大型株リスト
- 帰宅後: 破棄除外 → 自宅リスト突合 → QPSだけIR調査

### 第2弾（2026-08-10）

- **結論:** 買い推奨としては使えないが、使える入口は増えた。
- 調査候補: 北洋銀行（8524）年4回配当（公式一致）
- 整理用: 高配当10選、半導体工程別マップ
- ノイズ: DM誘導、相場8箇条の盲信、他人の配当目標の丸写し
