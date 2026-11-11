from __future__ import annotations

import json
import urllib.request
from typing import Any

from tools._shared import domain, err

BASE = "https://hacker-news.firebaseio.com/v0"
VALID_TYPES = {"top", "new", "best"}


def _get(path: str, timeout: int = 10) -> Any:
    with urllib.request.urlopen(f"{BASE}/{path}.json", timeout=timeout) as response:
        return json.load(response)


def get_hn_stories(story_type: str = "top", limit: int = 5) -> dict[str, Any]:
    try:
        if story_type not in VALID_TYPES:
            raise ValueError(f"Unsupported story_type: {story_type!r}. Use one of {sorted(VALID_TYPES)}")

        try:
            clean_limit = int(limit or 5)
        except (TypeError, ValueError):
            clean_limit = 5
        clean_limit = max(1, min(clean_limit, 20))

        story_ids = _get(f"{story_type}stories") or []
        items = []
        for story_id in story_ids[:clean_limit]:
            story = _get(f"item/{story_id}") or {}
            if not isinstance(story, dict):
                continue
            url = story.get("url") or f"https://news.ycombinator.com/item?id={story_id}"
            items.append({
                "title": story.get("title", ""),
                "url": url,
                "source": domain(url) or "Hacker News",
                "summary": f"{story.get('score', 0)} điểm, {story.get('descendants', 0)} bình luận",
                "score": story.get("score"),
            })
        return {
            "tool": "get_hn_stories",
            "story_type": story_type,
            "items": items,
            "item_count": len(items),
        }
    except Exception as exc:
        return err("get_hn_stories", exc)
