# Amazonサイトのスクレイピング

## 対象ウェブサイト
Amazon Japan（https://www.amazon.co.jp）

## スクリプト

### 1. 1st_page_products.py
このスクリプトは、Amazonで「デザイン経営」を検索し、検索結果に表示される200件のアイテムのリンクと画像を取得します。

### 2. recommended_pages.py
このスクリプトは以下の処理を行います：
- 「デザイン経営」を初期検索語としてAmazonで検索
- 検索結果ページから書籍の商品リンクと画像リンクを取得
- 最大5ページまでの検索結果をスクレイピング
- 最後に取得した商品のURLから新しい検索語を生成し、検索を継続

## 技術的注記
Chromeの拡張機能に問題があったため、ブラウザベースのソリューションの代わりにPythonモジュールのBeautiful Soupを使用してウェブスクレイピングを行いました。

## 現在の課題
`recommended_pages.py`スクリプトには以下の問題があります：
1. 商品名を取得する際の文字エンコーディングの問題
2. 100サンプルのデータを収集できない（5秒のランタイム設定が原因の可能性）

## 今後の改善点
時間が許せば、以下の点に取り組む予定です：
- 文字エンコーディングの問題を解決
- 目標サンプル数に到達するようにデータ収集を最適化
- データ収集とレート制限の回避のバランスを取るようにリクエストのタイミングを調整

## 依存関係
- Python 3.x
- requests
- beautifulsoup4
- fake-useragent