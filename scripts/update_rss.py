import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Kaynak sayfa (Archaeology projects)
URL = "https://researchportal.helsinki.fi/en/organisations/archaeology/projects/"

# Tarayıcı gibi görünmek için header ekliyoruz (403 hatasını önler)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

def fetch_html(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text

def parse_items(html: str):
    soup = BeautifulSoup(html, "lxml")
    items = []
    for proj in soup.select(".rendering_upmproject_short"):
        title_el = proj.select_one(".title span")
        link_el = proj.select_one(".title a")
        period_el = proj.select_one(".period")
        type_el = proj.select_one(".type")

        title = title_el.text.strip() if title_el else "Untitled"
        link = link_el["href"].strip() if link_el and link_el.has_attr("href") else URL
        period = period_el.get_text(" ", strip=True) if period_el else ""
        ptype = type_el.get_text(" ", strip=True) if type_el else ""

        pub_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        description = (f"{period} | {ptype
