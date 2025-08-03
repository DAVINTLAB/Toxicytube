import sys
import os
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

def classify_sentiments(input_path, limit=None):
    # Extract VIDEO_ID from the file name
    filename = os.path.basename(input_path)
    if not filename.startswith("comments_") or not filename.endswith(".json"):
        print("Error: filename must follow the format comments_<VIDEO_ID>.json")
        return

    video_id = filename.replace("comments_", "").replace(".json", "")
    output_path = f"Sentiments_{video_id}_XLM-T.json"

    # Load comments
    with open(input_path, "r", encoding="utf-8") as f:
        comments_data = json.load(f)

    if limit is not None:
        comments_data = comments_data[:limit]

    texts = [comment["message"] for comment in comments_data]

    print("Loading XLM-Roberta model for sentiment analysis...")
    model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

    print(f"Classifying {len(texts)} comments...")

    results = sentiment_pipeline(texts, truncation=True, padding=True, max_length=512)

    # Output structure
    output_data = []
    for i, comment in enumerate(comments_data):
        result = {
            "id": comment["id"],
            "author": comment["author"],
            "message": comment["message"],
            "publishedAt": comment["publishedAt"],
            "likeCount": comment["likeCount"],
            "sentiment_label": results[i]["label"],
            "sentiment_score": results[i]["score"]
        }
        output_data.append(result)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Saved file: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python SentimentsClassificationWithXLM.py comments_<VIDEO_ID>.json [NUM_COMENTÁRIOS]")
    else:
        input_file = sys.argv[1]
        try:
            limit = int(sys.argv[2]) if len(sys.argv) == 3 else None
        except ValueError:
            print("The second argument must be an integer.")
            sys.exit(1)
        classify_sentiments(input_file, limit)
