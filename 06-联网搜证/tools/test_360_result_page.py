# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "https://www.so.com/link?m=ukNsqGmfEO9ZP%2FQXnvEA5Ep4o71xkb6LGsxNEAaBXgO4N1wuaaJWwNFV0UuxLoOD7LcHuhJbszp%2F3rtRCEMggxVEZGQ8Oo7KSpZHtcO7LmPrfQnPbTqaZjLGI8HXYeAN2lzwxHJgaNdgGrvvGtJbsVryQfklywC%2FZ2lX0YQxiXli4X7UW4DcazGDC3fGsQ%2FWjCpDr7%2BneQL6XugRaN5v1Ey9SoRW1m459c7QIrYRMxac0hbfx1TICe%2BrTnKuZu%2Bes%2Fr6ohBcKH7iFXRmf11ILWUeIQjK44174AWxAuxlrMbPWpshwnH8AvtfO5uQD3Uc3i%2B%2BdLtMcapa%2BWcf8WmjcjV4nC4BoV3CtC2S4wkqrFuJ98xwQJAHE%2FdsCX6Ne%2BhmdbVEuyB6pn5k%3D"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()
    page.goto(url, timeout=20000)
    page.wait_for_timeout(2000)
    print("Title:", page.title())
    print("URL:", page.url)
    text = page.evaluate('() => document.body.innerText')
    print("Text length:", len(text))
    print("Sample:\n", text[:500])
    b.close()
