from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

from src.ingestion.page_configurations import payload, headers, make_payload, API_URL, BASE_URL, DEFAULT_PAGE_ID, \
    DEFAULT_NEWS_TYPE


def warm_cookies(session: requests.Session,referer:str)-> None:
    response = session.get(referer)
    response.raise_for_status()


def post_once(session: requests.Session, page_id: str, news_type: str) -> dict:
    referer = f"{BASE_URL}?newsType={news_type}"
    warm_cookies(session, referer)
    r = session.post(
        API_URL,
        data=make_payload(page_id, news_type),
        headers=headers,
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def get_guid_and_id_again():
    html = requests.get(url=BASE_URL, headers=headers, timeout=30).text
    soup=BeautifulSoup(html, 'html.parser')
    id=soup.select_one('#actual-page-id')['value']
    a=soup.select_one('[aria-label="Matter Highlights"]')
    guid_type = a.get('href').split('=')[1]
    return id,guid_type


with requests.Session() as session:
    #Go for my default pageId and newsId
    try:
        data = post_once(session, DEFAULT_PAGE_ID, DEFAULT_NEWS_TYPE)

    except requests.HTTPError:
        items = []

    # If empty due to change of either pageId or site News id , this activates
    if not items:
        print("Trying to get id an news type again , change it in the config")
        fresh_page_id, fresh_news_type = get_guid_and_id_again(session)
        if fresh_page_id and fresh_news_type:
            data = post_once(session, fresh_page_id, fresh_news_type)
