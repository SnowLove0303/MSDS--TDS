# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/gwhjbh/gtfwwrfz/202302/t20230206_1015383.shtml" # GB 18597-2023 MEE官网

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(url, timeout=30000)
    page.wait_for_timeout(2000)
    print("MEE 18597 Title:", page.title())
    
    # 查找 PDF 附件
    pdf_links = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a')).map(a => [(a.innerText || '').trim(), a.href]).filter(x => x[1].endsWith('.pdf') || x[0].includes('PDF') || x[0].includes('下载'));
    }''')
    print("PDF links on MEE 18597:", pdf_links)
    b.close()
