# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "https://flk.npc.gov.cn/detail?id=ff8081817a66b816017a7956b7db0ad4&fileId=&type=&title=%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E5%AE%89%E5%85%A8%E7%94%9F%E4%BA%A7%E6%B3%95"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    page = context.new_page()
    page.goto(url, timeout=30000)
    page.wait_for_timeout(3000)
    
    # 查找下载按钮及包含的下载事件
    btn_info = page.evaluate('''() => {
        const btns = Array.from(document.querySelectorAll('.download-btn, .down-load, .download, button, span, a')).filter(el => (el.innerText || '').includes('下载') || (el.innerText || '').includes('WPS') || (el.innerText || '').includes('公报'));
        return btns.map(el => ({
            tag: el.tagName,
            class: el.className,
            text: (el.innerText || '').trim(),
            html: el.outerHTML
        }));
    }''')
    for b_item in btn_info:
        print("  ", b_item)
    b.close()
