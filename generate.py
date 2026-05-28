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


def generate_article(topic: str, style_samples: list) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Use up to 5 samples to stay within token limits
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

上記のサンプルから私の文体をしっかり学んで、
以下のテーマで私が書いたような記事を生成してください。

テーマ: {topic}

語尾・文の長さ・段落の区切り方・独特の表現など、私らしさを忠実に再現してください。
サンプルにはない情報は創作せず、文体だけを真似てください。""",
            }
        ],
    )

    return message.content[0].text


def main():
    print("=== Wrightingmaru - 文体生成アシスタント ===\n")

    samples = load_sample_articles()
    if not samples:
        print("⚠️  samples/ フォルダに .txt ファイルが見つかりません。")
        print("   自分の過去のnote記事をテキストファイルで保存してから実行してください。")
        print("   例: samples/article1.txt, samples/article2.txt")
        return

    print(f"✅ {len(samples)} 件のサンプル記事を読み込みました\n")

    topic = input("どんなテーマで記事を書きますか？ > ").strip()
    if not topic:
        print("テーマを入力してください。")
        return

    print("\n生成中...\n")
    article = generate_article(topic, samples)

    print("=== 生成された記事 ===\n")
    print(article)
    print("\n======================")

    # Save to file
    output_path = Path("output.txt")
    output_path.write_text(article, encoding="utf-8")
    print(f"\n💾 output.txt に保存しました")


if __name__ == "__main__":
    main()
