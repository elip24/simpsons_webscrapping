import json
from playwright.sync_api import sync_playwright
from src.ingestion.page_configurations import headers

start_url='https://www.stblaw.com/about-us/news/view/2025/07/22/televisaunivision-completes-$1.5-billion-senior-secured-notes-offering?Culture=en'

def extract_article_text(page):
    paragraphs = page.locator("#news-content p").all_inner_texts()
    return "\n\n".join(p.strip() for p in paragraphs)

def get_elements_from_label(page, label_search):
    heading = page.get_by_role("heading", name=f"{label_search}")
    items = heading.locator("xpath=following-sibling::ul/li/a")
    elements = items.all_inner_texts()
    return elements

def get_correct_id_json(page,meta=None):
    data = page.locator("script[type='application/ld+json']").all_text_contents()
    for txt in data:
        try:
            obj = json.loads(txt)
            candidates = [obj]
            news_json = [c for c in candidates if c.get("@type") == 'NewsArticle']
            if news_json:
                break
        except Exception:
            continue
    return news_json

def get_news_articles(playwright,start_url,meta=None):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(extra_http_headers=headers)
    page=context.new_page()
    page.goto(start_url)

    try:
        json_id=get_correct_id_json(page)
        print(json_id)
        headline=json_id[0].get("headline")
        datemodified=json_id[0].get("dateModified")
        lawyer_names,lawyer_links=[],[]
        for lawyer in json_id[0].get("author"):
            lawyer_names.append(lawyer.get("name"))
            lawyer_links.append(lawyer.get("url"))

    except Exception:
        pass
    text=extract_article_text(page)
    practices=get_elements_from_label(page,'Related Practice Areas')
    industries = get_elements_from_label(page, 'Related Industries')


    all_news = {
        "datemodified":datemodified,
        "url": start_url,
        "practices": practices,
        "industries": industries,
        "lawyer_names": lawyer_names,
        "lawyer_links": lawyer_links,
        "text": text,
    }
    # This is because there is some information in the meta not in the url (like the id or the exact time of publication for some reason)
    if meta:
        all_news.update(meta)
    print(all_news)
    page.close()
    context.close()
    browser.close()

with sync_playwright() as playwright:
    get_news_articles(playwright, start_url)