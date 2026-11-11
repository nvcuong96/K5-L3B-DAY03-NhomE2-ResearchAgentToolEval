from __future__ import annotations

import json
import urllib.request
from typing import Any

from tools._shared import err

BASE = "https://hacker-news.firebaseio.com/v0"
VALID_STORY_TYPES = {"top", "new", "best"}


def _get(path: str, timeout: int = 10) -> Any:
    with urllib.request.urlopen(f"{BASE}/{path}.json", timeout=timeout) as r:
        return json.load(r)


def get_hn_stories(story_type: str = "top", limit: int = 5) -> dict[str, Any]:
    try:
        clean_story_type = str(story_type or "top").lower().strip()
        if clean_story_type not in VALID_STORY_TYPES:
            clean_story_type = "top"

        try:
            clean_limit = int(limit)
        except (ValueError, TypeError):
            clean_limit = 5
        clean_limit = max(1, min(clean_limit, 20))

        ids = _get(f"{clean_story_type}stories")[:clean_limit]
        items = []
        for i in ids:
            s = _get(f"item/{i}")
            if not isinstance(s, dict):
                continue
            items.append({
                "title": s.get("title", ""),
                "url": s.get("url", f"https://news.ycombinator.com/item?id={i}"),
                "source": "Hacker News",
                "summary": f"{s.get('score', 0)} điểm, {s.get('descendants', 0)} bình luận",
            })
        return {
            "tool": "hackernews",
            "story_type": clean_story_type,
            "items": items,
            "item_count": len(items),
        }
    except Exception as exc:
        return err("hackernews", exc)