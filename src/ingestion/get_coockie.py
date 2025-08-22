from playwright.sync_api import sync_playwright

URL = "https://www.stblaw.com/about-us/news?newsType=e4c9c90e-743d-6a02-aaf8-ff0000765f2c"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()  # brand new: no cookies
    page = context.new_page()

    # Log Set-Cookie headers as they come in
    def log_response(resp):
        try:
            hdrs = resp.headers
            if any(k.lower() == "set-cookie" for k in hdrs.keys()):
                print("Set-Cookie on:", resp.url)
                print(hdrs.get("set-cookie"))
        except Exception:
            pass

    context.on("response", log_response)

    page.goto(URL, wait_until="domcontentloaded")
    page.wait_for_timeout(6000)  # give CF time to challenge

    cookies = context.cookies()
    cf = [c for c in cookies if c["name"] == "cf_clearance"]
    print("cf_clearance present:", bool(cf))
    if cf:
        print("Value:", cf[0]["value"])
        print("Expires (epoch):", cf[0]["expires"])

    browser.close()
