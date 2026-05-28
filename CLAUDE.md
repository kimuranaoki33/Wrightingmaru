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

## 今後の拡張方針

- サンプル記事が増えたらRAG（ベクトル検索）で関連記事だけを選択する仕組みを追加
- Web UI化（Streamlit または Next.js）
- note.com からの記事自動取得
