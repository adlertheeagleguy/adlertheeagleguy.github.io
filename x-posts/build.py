#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
SOURCE_PATH = ROOT.parent / "stuff" / "bookmarks.jsonl"
DATA_DIR = ROOT / "data"
FOLDERS_DIR = ROOT / "folders"


FOLDER_CONFIG = [
    {
        "slug": "ai-software",
        "name": "AI & Software",
        "description": "AI tools, coding workflows, developer products, and software demos.",
        "keywords": {
            "ai": 4,
            "gpt": 7,
            "chatgpt": 8,
            "openai": 8,
            "claude": 8,
            "llm": 7,
            "llms": 7,
            "agent": 6,
            "agents": 6,
            "prompt": 5,
            "prompting": 5,
            "browser use": 8,
            "developer": 5,
            "developers": 5,
            "coding": 7,
            "code review": 8,
            "programming": 7,
            "software": 6,
            "terminal": 6,
            "cli": 7,
            "api": 5,
            "github": 6,
            "repo": 4,
            "tool": 3,
            "tools": 3,
            "app": 3,
            "apps": 3,
            "macos": 6,
            "ios": 5,
            "swift": 6,
            "vscode": 7,
            "visual studio code": 8,
            "theme": 4,
            "localhost": 7,
            "local development": 7,
            "local project": 6,
            "public url": 6,
            "volume control": 7,
            "domain": 4,
            "tls": 6,
            "auth": 4,
            "apple silicon": 6,
            "metal gpu": 6,
            "open source": 6,
            "tool for developers": 8,
            "app store": 3,
            "diff": 4,
            "automation": 5,
        },
        "authors": {
            "andrewfarah": 14,
            "aibuilderclub_": 14,
            "rowancheung": 10,
            "brian_lovin": 9,
            "benjdicken": 10,
            "openclaw": 10,
        },
    },
    {
        "slug": "business-markets",
        "name": "Business & Markets",
        "description": "Founders, sales, investing, company strategy, and market commentary.",
        "keywords": {
            "startup": 8,
            "startups": 8,
            "founder": 6,
            "founders": 6,
            "business": 6,
            "business owner": 6,
            "company": 5,
            "companies": 5,
            "revenue": 8,
            "profit": 8,
            "sales": 7,
            "market": 5,
            "markets": 5,
            "investor": 7,
            "investors": 7,
            "investing": 7,
            "finance": 7,
            "financial": 7,
            "economy": 6,
            "economic": 6,
            "pricing": 6,
            "enterprise": 5,
            "saas": 7,
            "capital": 5,
            "valuation": 8,
            "earnings": 6,
            "delivery target": 8,
            "$tsla": 8,
            "stock": 5,
        },
        "authors": {
            "trungtphan": 14,
            "autismcapital": 14,
            "stevenmarkryan": 12,
            "sixsigmacapital": 12,
            "optionslearn": 11,
            "techsalesguy": 11,
            "teslashanghai": 12,
            "paulg": 8,
        },
    },
    {
        "slug": "space-science",
        "name": "Space & Science",
        "description": "Spaceflight, astronomy, engineering, and natural science posts.",
        "keywords": {
            "space": 7,
            "starship": 10,
            "spacex": 10,
            "nasa": 10,
            "moon": 7,
            "mars": 7,
            "rocket": 7,
            "rockets": 7,
            "orbit": 7,
            "astronomy": 8,
            "artemis": 10,
            "earth": 5,
            "science": 6,
            "scientist": 6,
            "scientists": 6,
            "physics": 8,
            "lab": 5,
            "research": 5,
            "eclipse": 6,
            "planet": 4,
            "apollo": 8,
            "earthrise": 8,
            "sls": 8,
            "aviation": 3,
            "pilot": 3,
        },
        "authors": {
            "nasaearth": 16,
            "considercosmos": 14,
            "interstellargw": 14,
            "johnkrausphotos": 13,
            "sciencegirl": 10,
            "rainmaker1973": 10,
            "astro_clay": 12,
            "erikkuna": 10,
        },
    },
    {
        "slug": "health-fitness",
        "name": "Health & Fitness",
        "description": "Training, nutrition, body composition, and performance advice.",
        "keywords": {
            "health": 7,
            "fitness": 8,
            "protein": 8,
            "diet": 8,
            "nutrition": 8,
            "exercise": 7,
            "training": 7,
            "sleep": 7,
            "muscle": 8,
            "longevity": 8,
            "cardio": 8,
            "gym": 8,
            "workout": 8,
            "running": 7,
            "recovery": 6,
            "metabolism": 7,
            "body fat": 8,
            "calories": 8,
            "strength": 7,
            "belly": 4,
            "posture": 8,
            "neck": 3,
            "chin tuck": 8,
            "chin tucks": 8,
        },
        "authors": {
            "coachdango": 14,
            "coachgeoffreed": 14,
            "chamberoffit": 14,
            "fitfusion__": 10,
            "ted_ryce": 10,
            "conor_harris_": 10,
        },
    },
    {
        "slug": "food-travel-places",
        "name": "Food, Travel & Places",
        "description": "Recipes, restaurants, local finds, travel clips, and destination posts.",
        "keywords": {
            "food": 6,
            "recipe": 10,
            "recipes": 10,
            "restaurant": 10,
            "restaurants": 10,
            "cooking": 8,
            "cook": 5,
            "chef": 6,
            "kitchen": 7,
            "breakfast": 7,
            "lunch": 6,
            "dinner": 7,
            "pasta": 7,
            "taco": 8,
            "tacos": 8,
            "burrito": 8,
            "salad": 7,
            "bread": 6,
            "dessert": 7,
            "desserts": 7,
            "drink": 5,
            "drinks": 5,
            "vegas": 7,
            "las vegas": 8,
            "travel": 6,
            "trip": 5,
            "hotel": 6,
            "city": 3,
        },
        "authors": {
            "soulfoodiiee": 16,
            "vegasstarfish": 16,
            "tastyuk": 15,
            "tasty": 15,
            "ribzoftiktok": 15,
            "southdallasfood": 14,
            "summer_food": 12,
            "bigksque1": 10,
        },
    },
    {
        "slug": "politics-history-society",
        "name": "Politics, History & Society",
        "description": "Government, policy, history, geopolitics, and civic commentary.",
        "keywords": {
            "politics": 7,
            "policy": 7,
            "government": 8,
            "america": 6,
            "american": 6,
            "trump": 9,
            "biden": 9,
            "election": 8,
            "democrat": 8,
            "democrats": 8,
            "republican": 8,
            "republicans": 8,
            "senate": 8,
            "congress": 8,
            "war": 6,
            "history": 7,
            "civilization": 8,
            "society": 6,
            "revolution": 8,
            "immigration": 8,
            "administration": 6,
            "legislative": 6,
            "faith": 4,
            "violence": 4,
            "taxes": 6,
            "freedom": 5,
            "western civilization": 10,
            "state": 3,
        },
        "authors": {
            "thebabylonbee": 15,
            "catturd2": 14,
            "rothmus": 14,
            "arthurmacwaters": 14,
            "mericamemed": 14,
            "reddit_lies": 12,
            "libsoftiktok": 12,
            "orwellngoode": 12,
            "joelwberry": 12,
            "kylenabecker": 12,
            "chrismartzwx": 12,
            "cwboca": 11,
        },
    },
    {
        "slug": "design-media-ideas",
        "name": "Design, Media & Ideas",
        "description": "Design craft, photography, film, architecture, writing, and creative inspiration.",
        "keywords": {
            "design": 8,
            "designer": 7,
            "branding": 8,
            "brand": 4,
            "logo": 7,
            "typography": 8,
            "creative": 7,
            "art": 4,
            "illustration": 8,
            "architecture": 8,
            "interior": 7,
            "photo": 3,
            "photography": 8,
            "film": 7,
            "cinematic": 8,
            "movie": 6,
            "cinema": 7,
            "tenet": 8,
            "dune": 8,
            "book": 5,
            "books": 5,
            "essay": 6,
            "writing": 6,
            "slide": 4,
            "slides": 4,
            "wallpaper": 6,
            "wallpapers": 6,
        },
        "authors": {
            "evalovesdesign": 16,
            "jasonjoyride": 11,
            "jordymaui": 10,
            "paulwilsonimage": 10,
            "koreanoli": 10,
        },
    },
    {
        "slug": "humor-internet-culture",
        "name": "Humor & Internet Culture",
        "description": "Memes, absurd clips, parody posts, and internet-native ephemera.",
        "keywords": {
            "meme": 9,
            "memes": 9,
            "shitpost": 10,
            "shitposting": 10,
            "funny": 7,
            "hilarious": 7,
            "parody": 6,
            "joke": 6,
            "jokes": 6,
            "lol": 5,
            "lmao": 5,
            "lmfao": 5,
            "internet hall of fame": 10,
            "clip": 4,
            "clips": 4,
            "no context": 8,
            "greentext": 8,
        },
        "authors": {
            "shitpostgate": 18,
            "interneth0f": 18,
            "nocontextmemes": 16,
            "picturesfoider": 16,
            "videosinfolder": 16,
            "humansnocontext": 16,
            "nocontexthumans": 16,
            "everythingooc": 16,
            "localbateman": 14,
            "wildtiktokss": 14,
            "crazyclipsonly": 14,
            "shitposts_mp4": 16,
            "hourly_shitpost": 16,
            "greentextrepost": 16,
            "reelshitposts": 16,
            "nocontextbrits": 14,
            "womenpostingls": 14,
            "horsehater69": 14,
            "delusionposting": 14,
            "prisonmitch": 12,
            "hitrw93": 8,
        },
    },
    {
        "slug": "culture-life-entertainment",
        "name": "Culture, Life & Entertainment",
        "description": "Sports, relationships, movies, music, faith, and broader cultural commentary.",
        "keywords": {
            "friend": 4,
            "friends": 4,
            "grieve": 7,
            "music": 5,
            "song": 5,
            "sports": 6,
            "football": 6,
            "basketball": 8,
            "hockey": 8,
            "olympic": 7,
            "olympics": 7,
            "stanley cup": 9,
            "airline": 5,
            "aviation": 7,
            "pilot": 7,
            "family": 4,
            "parents": 4,
        },
        "authors": {
            "bobgoff": 12,
            "_zeets": 10,
            "clintfiore": 10,
            "playteaux1": 10,
        },
    },
]


WORD_PATTERN = re.compile(r"\b[\w']+\b")
URL_PATTERN = re.compile(r"https?://\S+")


def parse_json_stream(path: Path) -> list[dict[str, Any]]:
    text = path.read_text()
    decoder = json.JSONDecoder()
    index = 0
    rows: list[dict[str, Any]] = []
    while index < len(text):
        while index < len(text) and text[index].isspace():
            index += 1
        if index >= len(text):
            break
        obj, index = decoder.raw_decode(text, index)
        rows.append(obj)
    return rows


def normalize_text(value: str) -> str:
    cleaned = URL_PATTERN.sub(" ", value.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def compile_folder_patterns() -> list[dict[str, Any]]:
    compiled: list[dict[str, Any]] = []
    for folder in FOLDER_CONFIG:
        keyword_patterns = []
        for phrase, weight in folder["keywords"].items():
            pattern = re.compile(r"\b" + re.escape(phrase.lower()) + r"\b")
            keyword_patterns.append((pattern, weight))
        compiled.append(
            {
                **folder,
                "keywords_compiled": keyword_patterns,
                "author_lookup": {key.lower(): value for key, value in folder["authors"].items()},
            }
        )
    return compiled


COMPILED_FOLDERS = compile_folder_patterns()
FOLDER_LOOKUP = {folder["slug"]: folder for folder in COMPILED_FOLDERS}


def classify_bookmark(bookmark: dict[str, Any]) -> dict[str, str]:
    author = bookmark.get("author") or {}
    handle = (bookmark.get("authorHandle") or "").lower()
    main_text = normalize_text(bookmark.get("text") or "")
    quoted_text = normalize_text((bookmark.get("quotedTweet") or {}).get("text") or "")
    author_context = normalize_text(
        " ".join(
            filter(
                None,
                [
                    handle,
                    bookmark.get("authorName") or "",
                    author.get("bio") or "",
                    author.get("location") or "",
                ],
            )
        )
    )

    scores: list[tuple[int, str]] = []
    for folder in COMPILED_FOLDERS:
        score = folder["author_lookup"].get(handle, 0)
        for pattern, weight in folder["keywords_compiled"]:
            if pattern.search(main_text):
                score += weight
            elif quoted_text and pattern.search(quoted_text):
                score += max(1, weight - 2)
            elif author_context and pattern.search(author_context):
                score += max(1, weight // 2)

        if folder["slug"] == "humor-internet-culture":
            if any(token in handle for token in ["meme", "shitpost", "nocontext", "posting", "folder", "ooc"]):
                score += 6
        if folder["slug"] == "food-travel-places":
            if any(token in handle for token in ["food", "tasty", "vegas", "recipe", "cook"]):
                score += 4
        if folder["slug"] == "design-media-ideas":
            if any(token in handle for token in ["design", "photo", "image", "film", "cinema", "art"]):
                score += 4

        scores.append((score, folder["slug"]))

    scores.sort(key=lambda item: item[0], reverse=True)
    top_score, top_slug = scores[0]
    if top_score <= 0:
        top_slug = "culture-life-entertainment"

    return {
        "slug": top_slug,
        "name": FOLDER_LOOKUP[top_slug]["name"],
    }


def to_timestamp(value: str | None) -> int:
    if not value:
        return 0
    return int(datetime.strptime(value, "%a %b %d %H:%M:%S %z %Y").timestamp())


def project_bookmark(bookmark: dict[str, Any]) -> dict[str, Any]:
    media_objects = []
    for media in bookmark.get("mediaObjects") or []:
        projected = {
            "type": media.get("type"),
            "url": media.get("url"),
            "expandedUrl": media.get("expandedUrl"),
            "width": media.get("width"),
            "height": media.get("height"),
            "altText": media.get("altText"),
        }
        if media.get("videoVariants"):
            projected["videoVariants"] = media.get("videoVariants")
        media_objects.append(projected)

    projected = {
        "id": bookmark.get("id"),
        "tweetId": bookmark.get("tweetId"),
        "url": bookmark.get("url"),
        "text": bookmark.get("text"),
        "authorHandle": bookmark.get("authorHandle"),
        "authorName": bookmark.get("authorName"),
        "authorProfileImageUrl": bookmark.get("authorProfileImageUrl"),
        "postedAt": bookmark.get("postedAt"),
        "postedAtTimestamp": to_timestamp(bookmark.get("postedAt")),
        "language": bookmark.get("language"),
        "engagement": bookmark.get("engagement") or {},
        "mediaObjects": media_objects,
        "links": bookmark.get("links") or [],
        "tags": bookmark.get("tags") or [],
        "folder": bookmark.get("folder"),
    }
    if bookmark.get("quotedTweet"):
        quoted = bookmark["quotedTweet"]
        projected["quotedTweet"] = {
            "id": quoted.get("id"),
            "text": quoted.get("text"),
            "authorHandle": quoted.get("authorHandle"),
            "authorName": quoted.get("authorName"),
            "postedAt": quoted.get("postedAt"),
            "url": quoted.get("url"),
            "mediaObjects": quoted.get("mediaObjects") or [],
        }
    return projected


def build_shell(title: str, folder_slug: str | None, asset_prefix: str) -> str:
    folder_attr = f' data-folder-slug="{folder_slug}"' if folder_slug else ""
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="color-scheme" content="light dark">
    <title>{title}</title>
    <link rel="stylesheet" href="{asset_prefix}assets/styles.css">
  </head>
  <body{folder_attr}>
    <div class="site-shell">
      <header class="hero">
        <div class="hero-copy">
          <p class="eyebrow">X Bookmark Archive</p>
          <h1>{title}</h1>
          <p class="hero-text">A static view of the full bookmark set, grouped into context-aware folders and searchable in the browser.</p>
        </div>
        <div class="hero-meta">
          <label class="search">
            <span>Search posts, authors, and quoted tweets</span>
            <input id="search-input" type="search" placeholder="Try: Starship, recipes, Babylon Bee, diff tool">
          </label>
          <div class="stats-row">
            <div class="stat-card">
              <span class="stat-label">Visible</span>
              <strong id="visible-count">0</strong>
            </div>
            <div class="stat-card">
              <span class="stat-label">Folders</span>
              <strong id="folder-count">0</strong>
            </div>
          </div>
        </div>
      </header>

      <main class="layout">
        <aside class="sidebar">
          <div class="sidebar-panel">
            <div class="panel-header">
              <h2>Folders</h2>
              <a class="home-link" href="{asset_prefix}index.html">All bookmarks</a>
            </div>
            <nav id="folder-nav" class="folder-nav" aria-label="Folders"></nav>
          </div>
        </aside>

        <section class="content">
          <div id="folder-summary" class="folder-summary"></div>
          <div id="posts" class="posts" aria-live="polite"></div>
          <button id="load-more" class="load-more" type="button" hidden>Load more</button>
          <p id="empty-state" class="empty-state" hidden>No bookmarks matched the current filter.</p>
        </section>
      </main>
    </div>

    <script src="{asset_prefix}data/bookmarks.js"></script>
    <script src="{asset_prefix}assets/app.js"></script>
  </body>
</html>
"""


def write_site_shells(data: dict[str, Any]) -> None:
    if FOLDERS_DIR.exists():
        for child in FOLDERS_DIR.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
    ROOT.joinpath("index.html").write_text(build_shell("All Bookmarks", None, ""))
    for folder in data["folders"]:
        folder_dir = FOLDERS_DIR / folder["slug"]
        folder_dir.mkdir(parents=True, exist_ok=True)
        title = f"{folder['name']} Bookmarks"
        folder_dir.joinpath("index.html").write_text(build_shell(title, folder["slug"], "../../"))


def main() -> None:
    bookmarks = parse_json_stream(SOURCE_PATH)

    folder_counts: Counter[str] = Counter()
    normalized_rows = []
    projected_rows = []
    for bookmark in bookmarks:
        folder = classify_bookmark(bookmark)
        bookmark["folder"] = folder["name"]
        normalized_rows.append(bookmark)
        projected_rows.append(project_bookmark(bookmark))
        folder_counts[folder["slug"]] += 1

    SOURCE_PATH.write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in normalized_rows)
    )

    folder_payload = []
    for folder in COMPILED_FOLDERS:
        folder_payload.append(
            {
                "slug": folder["slug"],
                "name": folder["name"],
                "description": folder["description"],
                "count": folder_counts[folder["slug"]],
            }
        )

    site_payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "folders": folder_payload,
        "bookmarks": projected_rows,
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.joinpath("bookmarks.js").write_text(
        "window.XPOSTS_DATA = " + json.dumps(site_payload, ensure_ascii=False, separators=(",", ":")) + ";\n"
    )

    write_site_shells(site_payload)

    print("Updated", SOURCE_PATH)
    print("Generated", ROOT / "index.html")
    for folder in folder_payload:
        print(f"{folder['count']:>4}  {folder['name']}")


if __name__ == "__main__":
    main()
