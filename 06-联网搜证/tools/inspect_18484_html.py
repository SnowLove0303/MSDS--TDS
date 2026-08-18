# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/gthw/gtfwwrkzbz/202012/t20201217_813589.shtml"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(url, timeout=30000)
    page.wait_for_timeout(2000)
    
    # 查找文章区域的全部 html
    content_html = page.evaluate('''() => {
        const el = document.querySelector('.content_body, #main_content, .article-content, #content, .con, .content');
        return el ? el.innerHTML : document.body.innerHTML.substring(0, 2000);
    }''')
    print("Article Content HTML:\n", content_html[:1500])
    b.close()
