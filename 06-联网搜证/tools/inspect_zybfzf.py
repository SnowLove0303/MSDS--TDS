# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "https://flk.npc.gov.cn/detail?id=ff8080816f135f46016f1a8e1b6f0e4b&fileId=&type=&title=%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%81%8C%E4%B8%9A%E7%97%85%E9%98%B2%E6%B2%BB%E6%B3%95"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()
    page.goto(url, timeout=30000)
    page.wait_for_timeout(3000)
    
    data = page.evaluate('''async () => {
        const res = await fetch('https://flk.npc.gov.cn/law-search/search/flfgDetails?bbbs=ff8080816f135f46016f1a8e1b6f0e4b');
        return await res.json();
    }''')
    print("flfgDetails for 职业病防治法:", data)
    b.close()
