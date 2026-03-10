import feedparser
import json
import os

FEEDS = {
    "Tinuiti":      "https://tinuiti.com/feed/",
    "Pacvue":       "https://www.pacvue.com/feed/",
    "Skai":         "https://skai.io/feed/",
    "Teikametrics": "https://www.teikametrics.com/feed/",
    "Perpetua":     "https://perpetua.io/feed/",
    "Adbrew":       "https://adbrew.io/feed/",
    "Xnurta":       "https://www.xnurta.com/feed/",
    "Quartile":     "https://www.quartile.com/feed/",
}

SEEN_FILE = "seen_entries.json"

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return json.load(f)
    return {}

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f, indent=2)

def main():
    seen = load_seen()

    for agency, url in FEEDS.items():
        feed = feedparser.parse(url)
        prev = set(seen.get(agency, []))
        curr = []
        new  = []

        for entry in feed.entries[:10]:
            eid = entry.get("id") or entry.get("link")
            curr.append(eid)
            if eid not in prev:
                new.append({"title": entry.title, "link": entry.link})

        seen[agency] = curr
        if new:
            print(f"[{agency}] 새 항목 {len(new)}건")
            for item in new:
                print(f"  • {item['title']}")
                print(f"    {item['link']}")
        else:
            print(f"[{agency}] 변경 없음")

    save_seen(seen)

if __name__ == "__main__":
    main()
