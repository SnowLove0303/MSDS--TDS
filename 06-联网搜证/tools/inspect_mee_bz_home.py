# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "https://www.mee.gov.cn/ywgz/fgbz/bz/"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(url, timeout=30000)
    page.wait_for_timeout(2000)
    print("MEE BZ Home Title:", page.title())
    
    # 查找标准栏目链接
    bz_cats = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a')).map(a => [(a.innerText || '').trim(), a.href]).filter(x => x[0].includes('标准') || x[0].includes('水') || x[0].includes('大气') || x[0].includes('固') || x[0].includes('土壤') || x[0].includes('监测'));
    }''')
    for c in bz_cats[:20]:
        print("  ", c)
    b.close()
