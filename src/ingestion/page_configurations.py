NEWS_LIST = "https://www.stblaw.com/about-us/news?newsType=e3c9c90e-743d-6a02-aaf8-ff0000765f2c"

payload = {
    "siteSearchId": "00000000-0000-0000-0000-000000000000",
    "pageId": "7c5acb0e-743d-6a02-aaf8-ff0000765f2c",
    "mediaMode": "News",
    "searchId": "",
    "searchCount": "",
    "clientSolutions": "",
    "industries": "",
    "practice": "",
    "offices": "",
    "newsType": "e3c9c90e-743d-6a02-aaf8-ff0000765f2c",
    "eNews": "",
    "calendar_from": "",
    "calendar_to": "",
    "searchTerm": "",
    "employeeUrl": "",
    "take": "100",
    "skip": "0",
    "page": "1",
    "pageSize": "100",
}

headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",  # <-- form-encoded
    "X-Requested-With": "XMLHttpRequest",
    "Referer": NEWS_LIST,
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
}
