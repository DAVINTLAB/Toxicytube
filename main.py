import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')
VIDEO_ID = os.getenv('VIDEO_ID')

def get_video_comments(video_id, api_key, max_pages=50):
    comments = []
    url = f"https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&textFormat=plainText&part=snippet&videoId={video_id}&maxResults=100"

    for _ in range(max_pages):  # limit to avoid excessive calls
        response = requests.get(url)
        if response.status_code != 200:
            print("Request error:", response.text)
            break

        data = response.json()
        for item in data.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comment = {
                "id": item["id"],
                "author": snippet["authorDisplayName"],
                "message": snippet["textDisplay"],
                "publishedAt": snippet["publishedAt"],
                "likeCount": snippet["likeCount"]
            }
            comments.append(comment)

        next_page = data.get("nextPageToken")
        if not next_page:
            break
        url = f"https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&textFormat=plainText&part=snippet&videoId={video_id}&maxResults=100&pageToken={next_page}"

    return comments

def save_comments(comments, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(comments, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    try:
        n = int(input("Enter the number of top liked comments you want to collect: "))
    except ValueError:
        print("Please enter a valid integer number. ")
        exit()

    all_comments = get_video_comments(VIDEO_ID, API_KEY)
    top_comments = sorted(all_comments, key=lambda x: x["likeCount"], reverse=True)[:n]
    output_file = f'comments_{VIDEO_ID}.json'
    save_comments(top_comments, output_file)

    print(f"{len(top_comments)} top liked comments saved to {output_file}.")
