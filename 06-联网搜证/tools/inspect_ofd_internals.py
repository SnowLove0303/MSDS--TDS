# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "https://flk.npc.gov.cn/detail?id=ff8081817a66b816017a7956b7db0ad4&fileId=&type=&title=%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E5%AE%89%E5%85%A8%E7%94%9F%E4%BA%A7%E6%B3%95"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()
    page.goto(url, timeout=30000)
    page.wait_for_timeout(3000)
    
    # 模拟在 OFD reader 内部点击放大/渲染全部
    f = next(f for f in page.frames if 'flkofd' in f.url)
    
    # 检查 ofd 内部变量与结构
    js_vars = f.evaluate('''() => {
        return {
            title: document.title,
            numPages: window.reader ? window.reader.numPages : 'NO_READER',
            textCount: document.querySelectorAll('.text, span, div').length
        };
    }''')
    print("OFD Reader JS Info:", js_vars)
    b.close()
