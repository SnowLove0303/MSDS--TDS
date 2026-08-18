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
    
    # 模拟点击下载按钮
    dl_data = page.evaluate('''async () => {
        // 请求下载 word 接口
        const wordRes = await fetch('https://flk.npc.gov.cn/law-search/amazonFile/downloadFile?filePath=prod/20210610/1fe3ea13ca7b4e18ba5519ac531bf515.docx');
        // 请求下载 pdf 接口
        const pdfRes = await fetch('https://flk.npc.gov.cn/law-search/amazonFile/downloadFile?filePath=prod/20210610/966c289a2fcc45e589ddb739c0d07147.pdf');
        return {
            wordStatus: wordRes.status,
            pdfStatus: pdfRes.status,
            wordType: wordRes.headers.get('content-type'),
            pdfType: pdfRes.headers.get('content-type')
        };
    }''')
    print("Download API test:", dl_data)
    b.close()
