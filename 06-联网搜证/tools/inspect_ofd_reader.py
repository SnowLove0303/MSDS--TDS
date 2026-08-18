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
    
    # 查找所有 iframe
    for f in page.frames:
        if 'flkofd' in f.url:
            print("Found OFD reader frame:", f.url)
            # 等待 OFD 加载
            f.wait_for_timeout(4000)
            # 查看 OFD 内部的所有文字
            ofd_text = f.evaluate('''() => {
                const pages = document.querySelectorAll('.page, .text-layer, .content-layer, div[id*="page"]');
                return Array.from(pages).map(p => p.innerText).join('\\n--- PAGE ---\\n');
            }''')
            print("OFD Pages text len:", len(ofd_text))
            print("Sample OFD:\n", ofd_text[:500])
            
            # 查看所有文本 span
            all_spans = f.evaluate('''() => {
                const spans = document.querySelectorAll('span, div');
                const txts = Array.from(spans).map(s => s.innerText.trim()).filter(t => t.length > 0);
                return txts.slice(0, 50).join(' ');
            }''')
            print("Spans preview:\n", all_spans[:300])
    b.close()
