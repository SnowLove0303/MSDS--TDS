# -*- coding: utf-8 -*-
import urllib.parse
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
q = "中华人民共和国安全生产法 全文 gov.cn"
encoded_q = urllib.parse.quote(q)
url = f"https://www.bing.com/search?q={encoded_q}"
print("URL:", url)

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    page = context.new_page()
    page.goto(url, timeout=25000, wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    links = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('h2 a')).map(a => ({
            text: a.innerText.trim(),
            href: a.href
        }));
    }''')
    print("Found h2 links:", len(links))
    for l in links[:5]:
        print("  ", l)
    b.close()
