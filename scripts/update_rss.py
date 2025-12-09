import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Kaynak sayfa (Archaeology projects)
URL = "https://researchportal.helsinki.fi/en/organisations/archaeology/projects/"

def fetch_html(url: str) -> str:
    resp = requests.get(url, timeout=30)
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
        description = (f"{period} | {ptype}").strip(" |")

        item_xml = (
            "<item>\n"
            f"  <title>{title}</title>\n"
            f"  <link>{link}</link>\n"
            f"  <description>{description}</description>\n"
            f"  <pubDate>{pub_date}</pubDate>\n"
            f"  <guid>{link}</guid>\n"
            "</item>"
        )
        items.append(item_xml)
    return items

def build_rss(items):
    channel = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<rss version=\"2.0\">\n"
        "  <channel>\n"
        "    <title>Archaeology - University of Helsinki</title>\n"
        f"    <link>{URL}</link>\n"
        "    <description>Auto-updated feed (University of Helsinki Archaeology projects)</description>\n"
        f"    {'\\n'.join(items)}\n"
        "  </channel>\n"
        "</rss>\n"
    )
    return channel

def main():
    html = fetch_html(URL)
    items = parse_items(html)
    rss_xml = build_rss(items)
    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write(rss_xml)

if __name__ == "__main__":
    main()
