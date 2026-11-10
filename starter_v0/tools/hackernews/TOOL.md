---
name: hackernews
track: bonus
kind: live_api
provider: Hacker News Firebase API
requires_env: []
inputs: [story_type, limit]
outputs: [items, item_count]
side_effect: false
---
# hackernews

Fetches the current top, new, or best stories from Hacker News (public API, no key needed). Each item has title, url, source, and a short summary (points and comment count). Use only when the user explicitly mentions Hacker News or HN. It does not read article content (use `fetch`), search the web (use `lookup`), or search social media (use `social_search`).