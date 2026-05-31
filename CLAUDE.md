# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 概要

Wrightingmaru は、ユーザーの過去のnote記事から文体を学習し、同じ文体で新しい記事を生成するCLIツール。Python + Claude API（anthropic SDK）で構成される。

## セットアップと実行

```bash
# 依存パッケージのインストール
pip install -r requirements.txt

# APIキーを設定（.env.example をコピーして .env を作成）
cp .env.example .env
# .env を編集して ANTHROPIC_API_KEY を設定

# 実行
ANTHROPIC_API_KEY=sk-ant-xxx python generate.py
```

## ファイル構成

- `generate.py` — メインスクリプト。サンプル記事の読み込み・Claude API呼び出し・出力を担当
- `samples/*.txt` — ユーザーの過去記事をテキストで保存するフォルダ（最大5件使用）
- `output.txt` — 生成結果の保存先（gitignore済み）

## アーキテクチャ

Claude API にサンプル記事を渡し、指定テーマで文体を再現させる **few-shot プロンプティング** のアプローチ。ベクトルDBは使用していない。

使用モデル: `claude-opus-4-5`（`generate.py` の `generate_article` 関数内）

## note出力のMarkdownルール

生成記事はnoteに直接貼り付けられるMarkdown形式で出力する。`generate.py` のプロンプトに以下のルールが埋め込まれている。

**使用できる記法：**
- 見出し：`# 大見出し`、`## 中見出し`、`### 小見出し`
- 強調：`**太字**`
- 引用：`> 引用テキスト`
- 箇条書き：`- 項目`
- 番号付きリスト：`1. 項目`
- 取り消し線：`~~テキスト~~`
- 区切り線：`---`

**太字の制約（CommonMark仕様）：**
`**` の直後・直前に句読点・カギカッコ等の約物を置くと太字が無効になる。
- NG：`**「テキスト」**`
- OK：`「**テキスト**」`

## ユーザーの文体データ（蓄積・随時更新）

実際の投稿から分析した文体の特徴。新しいコメント・記事が届くたびに `samples/` に追加し、この分析も更新する。

**トーン・口調：**
- 関西出身だが文章は標準語ベース。関西弁は軽くにじむ程度（こてこてではない）
- 残る関西由来の表現：「むかんね」「しんどい」「ええわ」「よくない？」
- 語尾：「〜ね」「〜ね〜」「〜よ」「〜かな」「〜かもです」「〜てみては」が頻出
- 「ストレスフリー」などカタカナ語を自然に混ぜる
- 絵文字を自然に使う（多用しすぎず、感情が乗る場面だけ）：😃 😂 など

**文の構造：**
- 短文とだらっとした長文が混在する。整えすぎない
- 「ただし、〜」「ただ、〜」で逆接を入れるのが特徴
- 「まぁ〜でもええわ」「〜かし」「〜すぎ」など、独特の口語フレーズをそのまま使う
- 体験談ベースで書く。断言より「〜かな」「〜感じ」「〜そうですね」で終わることが多い
- 比喩で場面を描写する：「ハッカーみたいにバチバチに」など
- 締めは押しつけがましくない提案形：「〜てみては」「〜といいと思うよ」

**sampleファイル：**
- `samples/01_keyboard_article.txt` — iPhoneキーボード記事（note投稿済み完成版）
- `samples/02_dryer_article.txt` — 乾燥機レビュー記事（note投稿済み完成版）

## 今後の拡張方針

- サンプル記事が増えたらRAG（ベクトル検索）で関連記事だけを選択する仕組みを追加
- Web UI化（Streamlit または Next.js）
- note.com からの記事自動取得
