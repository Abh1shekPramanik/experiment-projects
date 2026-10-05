import json
import time
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from markdownify import markdownify as md

def get_all_urls():
    response = requests.get("https://fastapi.tiangolo.com/sitemap.xml")
    soup = BeautifulSoup(response.text, "lxml-xml")

    urls = [loc.text for loc in soup.find_all("loc")]
    return urls[:10]

def scrape_page(url):
    try:
        response = requests.get(url)
        time.sleep(2)
        soup = BeautifulSoup(response.text, "html.parser")

        article = soup.find("article")

        title = soup.find("h1").get_text(strip=True)

        content = md(str(article))
        content = re.sub(r"<[^>]+>", "", content)
        content = re.sub(r"\n{3,}", "\n\n", content)

        headings = soup.select("h1, h2")
        heading_list = [h.get_text(strip=True) for h in headings]

        page_data = {
        "url": url,
        "title": title,
        "headings": heading_list,
        "content": content,
        }

        path = urlparse(url).path
        slug = path.strip("/").split("/")[-1] or "index"

        with open(f"data/raw/{slug}.json", "w") as f:
            json.dump(page_data, f, indent=2)

        print(f"Saved: {title}")

    except Exception as e:
        print(f"Error in {url}: {e}")
    
    time.sleep(2)


urls = get_all_urls()
for url in urls:
    scrape_page(url)

# print(urls)