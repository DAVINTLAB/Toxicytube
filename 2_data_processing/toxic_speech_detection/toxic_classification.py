import sys
import os
import json
from detoxify import Detoxify

def classify_toxicity(input_path, limit=None, batch_size=100):
    filename = os.path.basename(input_path)
    if not filename.startswith("comments_") or not filename.endswith(".json"):
        print("Error: filename must follow the format comments_<VIDEO_ID>.json")
        return

    video_id = filename.replace("comments_", "").replace(".json", "")
    output_path = f"toxic_comments_{video_id}.json"

    with open(input_path, 'r', encoding='utf-8') as f:
        comments_data = json.load(f)

    if limit is not None:
        comments_data = comments_data[:limit]

    texts = [comment['message'] for comment in comments_data]
    model = Detoxify('unbiased')

    output_data = []

    print(f"Classifying {len(texts)} comments in batches of {batch_size}...")

    for i in range(0, len(texts), batch_size):
        batch_comments = texts[i:i + batch_size]
        batch_results = model.predict(batch_comments)

        available_scores = list(batch_results.keys())

        for j, comment in enumerate(comments_data[i:i + batch_size]):
            result = {
                "id": comment["id"],
                "author": comment["author"],
                "message": comment["message"],
                "publishedAt": comment["publishedAt"],
                "likeCount": comment["likeCount"],
            }
            for score_type in available_scores:
                result[score_type] = batch_results[score_type][j]
            output_data.append(result)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Arquivo salvo: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python toxic_classification.py comments_<VIDEO_ID>.json [NUM_COMMENTS]")
    else:
        input_file = sys.argv[1]
        try:
            limit = int(sys.argv[2]) if len(sys.argv) == 3 else None
        except ValueError:
            print("The second argument must be an integer.")
            sys.exit(1)
        classify_toxicity(input_file, limit)
