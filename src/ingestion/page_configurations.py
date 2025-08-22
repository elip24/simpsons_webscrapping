BASE_URL   = "https://www.stblaw.com/about-us/news"
API_URL    = "https://www.stblaw.com/dataservices/DataServices.Content.Services.Json.News/AllNews"

# Your current known-good defaults (fast path)
DEFAULT_PAGE_ID   = "7c5acb0e-743d-6a02-aaf8-ff0000765f2c"
DEFAULT_NEWS_TYPE = "e3c9c90e-743d-6a02-aaf8-ff0000765f2c"
DEFAULT_REFERER   = f"{BASE_URL}?newsType={DEFAULT_NEWS_TYPE}"


def make_payload(page_id:str, news_type:str,take:int =100)->dict:
    return  {
    "siteSearchId": "00000000-0000-0000-0000-000000000000",
    "pageId": page_id,
    "mediaMode": "News",
    "searchId": "",
    "searchCount": "",
    "clientSolutions": "",
    "industries": "",
    "practice": "",
    "offices": "",
    "newsType": news_type,
    "eNews": "",
    "calendar_from": "",
    "calendar_to": "",
    "searchTerm": "",
    "employeeUrl": "",
    "take": "100", #fijarse que pasa si pongo 1000
    "skip": "0",
    "page": "1",
    "pageSize": "100", #fijarse que pasa si pongo 1000
}

headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.stblaw.com/about-us/news?newsType=e3c9c90e-743d-6a02-aaf8-ff0000765f2c",
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
}
