# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/gwhjbh/gtfwwrfz/index.shtml"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(url, timeout=30000)
    page.wait_for_timeout(2000)
    print("GTFW BZ List Title:", page.title())
    links = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('.main_content a, .content_list a, ul li a, table a')).map(a => [(a.innerText || '').trim(), a.href]).filter(x => x[0].includes('标准') || x[0].includes('GB') || x[0].includes('废物') || x[0].includes('焚烧'));
    }''')
    for l in links[:15]:
        print("  ", l)
    b.close()
