import re
import time
from pathlib import Path

import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE = "https://www.boardofstudies.nsw.edu.au/ebos/static"
HEADERS = {"User-Agent": "Mozilla/5.0 (HSC learning project)"}

# Anchor paths to THIS file, not the current working directory:
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAGES = PROJECT_ROOT / "data" / "raw" / "pages"
PAGES.mkdir(parents=True,exist_ok=True)

def get_html(url, filename):
    """Fetch url, caching to data/raw/pages/. Returns local copy if it already exists."""
    path = PAGES / filename
    if path.exists():
        return path.read_text(encoding="utf-8")          # cache hit — no network
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    path.write_text(resp.text, encoding="utf-8")          # save for next time
    time.sleep(1)                                          # polite pause, only on real fetch
    return resp.text

def parse_course_page(html, year, course_name, course_code):
    """Parse one HSC course band page into a list of row dicts."""
    soup = BeautifulSoup(html, "html.parser")

    # candidature (your existing code)
    page_text = soup.get_text().replace("\xa0", " ")
    candidature = int(
        re.search(r"Candidature\s*-\s*([\d,]+)", page_text).group(1).replace(",", "")
    )

    rows = []
    for s in soup.find_all("strong"):
        label_text = s.get_text().replace("\xa0", " ").strip()
        if not label_text.startswith("Band"):
            continue
        cell_text = s.parent.get_text().replace("\xa0", " ")
        band = re.search(r"Band\s+(\S+)", label_text).group(1)
        percentage = float(re.search(r"\(([\d.]+)%\)", cell_text).group(1))

        # TODO: append a dict with these keys:
        #   band, percentage, candidature, year, course_name, course_code
        
        rows.append({
            "band" : band,
            "percentage" : percentage,
            "candidature" : candidature,
            "year" : year,
            "course_name" : course_name,
            "course_code" : course_code
        })


    return rows

def get_target_courses(year, targets):
    html = get_html(f"{BASE}/BDHSC_{year}_12.html", f"index_{year}.html")
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", href=re.compile(r"BDHSC_\d+_12_\d+\.html"))

    courses = []
    for a in links:
        # TODO: paste your working code_ + name extraction here,
        #       appending {"course_code": ..., "course_name": ...}
        href = a["href"]
        text = a.get_text(strip=True)
        course_code = re.search(r"_(\d+)\.html", href).group(1)
        course_name = re.match(r"(.+?)\s+\d+\s*unit", text).group(1)
        courses.append({
            "course_code" : course_code,
            "course_name" : course_name
        })

    index_df = pd.DataFrame(courses)
    return index_df[index_df["course_name"].isin(targets)]