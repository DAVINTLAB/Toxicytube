import json
import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env file (or set directly here)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Prompt used for classification
prompt_template = """You are a sentiment analyzer.
Classify the sentiment of the following comment as "positive", "negative", or "neutral".
Respond with the corresponding word only.

Comment: "{}"
Sentiment:"""

def classify_sentiment(comment):
    try:
        prompt = prompt_template.format(comment)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        result = response.choices[0].message.content.strip().lower()
        return result
    except Exception as e:
        print("Error classifying comment:")
        print(e)
        return "error"

def main(input_file, max_comments=None):
    with open(input_file, "r", encoding="utf-8") as f:
        comments = json.load(f)

    if max_comments:
        comments = comments[:max_comments]

    print(f"Classifying {len(comments)} comments using GPT...")

    for comment in comments:
        text = comment.get("message", "")
        comment["sentiment"] = classify_sentiment(text)

    #output_file = input_file.replace(".json", "_GPT.json")
    video_id = os.path.basename(input_file).replace("comments_", "").replace(".json", "")
    output_file = f"Sentiments_{video_id}_GPT.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(comments, f, indent=2, ensure_ascii=False)

    print(f"File saved: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python SentimentsClassificationWithGPT.py <arquivo_json> [max_comments]")
    else:
        input_path = sys.argv[1]
        max_count = int(sys.argv[2]) if len(sys.argv) > 2 else None
        main(input_path, max_count)
