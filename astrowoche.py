"""Generate a date-checked preview of the Leo horoscope for the calendar."""
from datetime import datetime
import gzip
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

SOURCE = "https://www.astrowoche.de/tageshoroskop/heute/loewe"
PARTS = ("Vormittag", "Nachmittag", "Abend")


class TextBlocks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.tag = None
        self.fragments = []

    def handle_starttag(self, tag, attrs):
        if tag in {"h1", "h2", "h3", "p"}:
            self.tag = tag
            self.fragments = []

    def handle_data(self, data):
        if self.tag:
            self.fragments.append(data)

    def handle_endtag(self, tag):
        if tag == self.tag:
            self.blocks.append((tag, " ".join("".join(self.fragments).split())))
            self.tag = None


def excerpt(text, budget, always_mark=False):
    words = text.split()
    return " ".join(words[:budget]) + (" …" if len(words) > budget or always_mark else "")


def parse_horoscope(html, day):
    parser = TextBlocks()
    parser.feed(html)
    blocks = parser.blocks
    heading = re.compile(r"Tageshoroskop\s*[-–]\s*Löwe für den " + re.escape(day.strftime("%d.%m.%Y")))
    for index, (tag, text) in enumerate(blocks):
        if tag == "h1" and heading.fullmatch(text):
            break
    else:
        raise ValueError("Datierte Löwe-Überschrift fehlt oder Datum stimmt nicht.")

    result = {"date": day.isoformat(), "title": "", "sections": {}}
    part = None
    for tag, text in blocks[index + 1:]:
        if tag in {"h1", "h2"}:
            if tag == "h2" and not result["title"] and part is None and text:
                result["title"] = excerpt(text, 4)
                continue
            break
        if tag == "h3":
            part = text if text in PARTS else None
        if tag == "p" and part and text and part not in result["sections"]:
            result["sections"][part] = excerpt(text, 5, always_mark=True)
            if len(result["sections"]) == len(PARTS):
                break
    if not result["title"] or set(result["sections"]) != set(PARTS):
        raise ValueError("Die erwarteten Abschnitte fehlen.")
    return result


def main(path):
    now = datetime.now(ZoneInfo("Europe/Berlin"))
    if now.month != 12 or now.day > 24:
        return
    try:
        request = Request(SOURCE, headers={"Accept": "text/html", "Accept-Encoding": "gzip"})
        with urlopen(request, timeout=20) as response:
            payload = response.read(3_000_000)
            if response.headers.get("Content-Encoding") == "gzip":
                payload = gzip.decompress(payload)
            html = payload.decode(response.headers.get_content_charset() or "utf-8")
        result = parse_horoscope(html, now.date())
    except (OSError, ValueError) as error:
        print(f"::warning::Astrowoche-Vorschau übersprungen: {error}")
        return
    path.write_text(json.dumps(result, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
