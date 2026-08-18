# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    page = context.new_page()
    page.goto('https://www.mem.gov.cn/fw/flfgbz/fg/', timeout=30000)
    page.wait_for_timeout(2000)
    
    # 查找主内容区的所有链接
    links = page.evaluate('''() => {
        const rows = document.querySelectorAll('.list_content a, .main_content a, .content_list a, .table_list a, ul.list li a, .list-box a');
        if (rows.length > 0) {
            return Array.from(rows).map(a => [(a.innerText || '').trim(), a.href]);
        }
        return Array.from(document.querySelectorAll('a')).map(a => [(a.innerText || '').trim(), a.href]).filter(x => x[0].includes('法') || x[0].includes('条例'));
    }''')
    print("Found Law links in mem.gov.cn:")
    for l in links:
        print("  ", l)
    b.close()
