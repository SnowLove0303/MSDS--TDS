# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "https://hbba.sacinfo.org.cn/stdDetail/237e8c3bcf5d6c810d7b233a7e53fca8"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto("https://hbba.sacinfo.org.cn/", timeout=30000)
    page.wait_for_timeout(2000)
    print("HBBA Home:", page.title())
    
    # 搜索行业标准 WS 444 / JT/T 617
    page.fill('input[placeholder*="标准号"], input[type="text"]', 'JT/T 617')
    page.keyboard.press('Enter')
    page.wait_for_timeout(3000)
    print("Search URL:", page.url)
    
    links = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a, .el-table__row, table tr')).map(el => (el.innerText || '').trim()).filter(x => x.includes('617') || x.includes('JT'));
    }''')
    print("HBBA Results:", len(links))
    for l in links[:5]:
        print("  ", l[:100])
    b.close()
