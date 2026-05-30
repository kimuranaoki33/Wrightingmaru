import os
import anthropic
from pathlib import Path


def load_sample_articles(samples_dir="samples"):
    samples_path = Path(samples_dir)
    articles = []
    for txt_file in sorted(samples_path.glob("*.txt")):
        text = txt_file.read_text(encoding="utf-8").strip()
        if text:
            articles.append(text)
    return articles


def generate_article(prompt_content: str, style_samples: list) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    samples_text = "\n\n---\n\n".join(style_samples[:5])

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": f"""以下は私が過去に書いたnote記事のサンプルです。
私の文体・言葉遣い・構成の癖・句読点の使い方をよく読み取ってください。

=== 私の記事サンプル ===
{samples_text}
========================

上記のサンプルから私の文体をしっかり学んで、以下の指示で記事を生成してください。

{prompt_content}

語尾・文の長さ・段落の区切り方・独特の表現など、私らしさを忠実に再現してください。
サンプルにはない情報は創作せず、文体だけを真似てください。""",
            }
        ],
    )

    return message.content[0].text


def get_multiline_input(prompt: str) -> str:
    print(prompt)
    lines = []
    while True:
        line = input()
        if line == "":
            if lines:
                break
        else:
            lines.append(line)
    return "\n".join(lines)


def main():
    print("=== Wrightingmaru - 文体生成アシスタント ===\n")

    samples = load_sample_articles()
    if not samples:
        print("⚠️  samples/ フォルダに .txt ファイルが見つかりません。")
        print("   自分の過去のnote記事をテキストファイルで保存してから実行してください。")
        print("   例: samples/article1.txt, samples/article2.txt")
        return

    print(f"✅ {len(samples)} 件のサンプル記事を読み込みました\n")
    print("モードを選んでください:")
    print("  1. テーマから生成（テーマを入力するだけ）")
    print("  2. 見出しから生成（見出しを貼り付けると本文も生成）")
    print()

    mode = input("番号を入力 (1 or 2) > ").strip()

    if mode == "2":
        headings = get_multiline_input(
            "見出しを貼り付けてください。貼り付け終わったら空行（Enter）を押してください:\n"
        )
        if not headings:
            print("見出しを入力してください。")
            return
        prompt_content = f"以下の見出し構成に従って、各セクションの本文を書いてください:\n\n{headings}"
    else:
        topic = input("どんなテーマで記事を書きますか？ > ").strip()
        if not topic:
            print("テーマを入力してください。")
            return
        prompt_content = f"テーマ「{topic}」で記事を書いてください。"

    print("\n生成中...\n")
    article = generate_article(prompt_content, samples)

    print("=== 生成された記事 ===\n")
    print(article)
    print("\n======================")

    output_path = Path("output.txt")
    output_path.write_text(article, encoding="utf-8")
    print(f"\n💾 output.txt に保存しました")


if __name__ == "__main__":
    main()
