from __future__ import annotations

from typing import Any

import requests

from tools._shared import TIMEOUT, domain, err

BASE = "https://hacker-news.firebaseio.com/v0"
VALID_TYPES = {"top", "new", "best"}


def _get(path: str) -> Any:
    response = requests.get(f"{BASE}/{path}.json", timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def get_hn_stories(story_type: str = "top", limit: int = 5) -> dict[str, Any]:
    try:
        if story_type not in VALID_TYPES:
            raise ValueError(f"Unsupported story_type: {story_type!r}. Use one of {sorted(VALID_TYPES)}")
        limit = max(1, min(int(limit or 5), 20))

        ids = (_get(f"{story_type}stories") or [])[:limit]
        items = []
        for story_id in ids:
            story = _get(f"item/{story_id}") or {}
            url = story.get("url") or f"https://news.ycombinator.com/item?id={story_id}"
            items.append({
                "title": story.get("title"),
                "url": url,
                "source": domain(url),
                "summary": f"{story.get('score', 0)} điểm, {story.get('descendants', 0)} bình luận",
                "score": story.get("score"),
            })
        return {"tool": "get_hn_stories", "story_type": story_type, "items": items, "item_count": len(items)}
    except Exception as exc:
        return err("get_hn_stories", exc)