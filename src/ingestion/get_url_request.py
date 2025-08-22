from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

from src.ingestion.page_configurations import payload, headers

URL = "https://www.stblaw.com/dataservices/DataServices.Content.Services.Json.News/AllNews"

def post_news():
    r = requests.post(URL, data=payload, headers=headers, timeout=30)
    r.raise_for_status()
    print(r.text)
#Del post obtengo el id/epoch de la publicacion,
def get_guid_again():
    html = requests.get("https://www.stblaw.com/about-us/news", headers=headers, timeout=30).text
    soup=BeautifulSoup(html, 'html.parser')
    a=soup.select('[aria-label="Matter Highlights"]')
    for tag in a:
        guid_type=tag.get('href').split('=')[1]
        return guid_type
    return None
post_news()