import json
import urllib.request

BASE = "https://hacker-news.firebaseio.com/v0"

def _get(path: str):
    with urllib.request.urlopen(f"{BASE}/{path}.json", timeout=10) as r:
        return json.load(r)

def get_hn_stories(story_type: str = "top", limit: int = 5) -> dict:
    limit = max(1, min(limit, 20))
    ids = _get(f"{story_type}stories")[:limit]
    items = []
    for i in ids:
        s = _get(f"item/{i}")
        items.append({
            "title": s.get("title", ""),
            "url": s.get("url", f"https://news.ycombinator.com/item?id={i}"),
            "source": "Hacker News",
            "summary": f"{s.get('score', 0)} điểm, {s.get('descendants', 0)} bình luận",
        })
    return {"items": items, "item_count": len(items)}