# -*- coding: utf-8 -*-
import urllib.parse
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
q = "中华人民共和国安全生产法 全文 2021 mem.gov.cn"
encoded_q = urllib.parse.quote(q)
url = f"https://www.bing.com/search?q={encoded_q}"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    page = context.new_page()
    page.goto(url, timeout=25000)
    page.wait_for_timeout(2000)
    
    results = page.evaluate('''() => {
        const algos = document.querySelectorAll('li.b_algo');
        return Array.from(algos).map(el => {
            const h2 = el.querySelector('h2');
            const a = h2 ? h2.querySelector('a') : null;
            return {
                title: h2 ? h2.innerText.trim() : '',
                href: a ? a.href : '',
                snippet: el.innerText.substring(0, 150)
            };
        });
    }''')
    print("Found algos:", len(results))
    for r in results[:4]:
        print("Title:", r["title"])
        print("Href:", r["href"])
        print("---")
        
    if results and results[0]["href"]:
        target_page = context.new_page()
        target_page.goto(results[0]["href"], timeout=30000)
        target_page.wait_for_timeout(2000)
        print("Landed URL:", target_page.url)
        print("Landed Title:", target_page.title())
        content = target_page.evaluate('() => document.body.innerText')
        print("Content sample:", content[:300])
        target_page.close()
        
    b.close()
