# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "http://mp.weixin.qq.com/s?src=11&timestamp=1787020271&ver=6911&signature=yIoaM4ktGI6Z39TRykx7020T1Pu*dwCE3lgNSiVf9I5Rt*gnFXYyrAeppAvw4NNI4exONyEqv8BEMmjj5MzqzNdmf2zwB2YDk5ec2NPikkOY64VexkF6x5n-Me7eklLT&new=1"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()
    page.goto(url, timeout=20000)
    page.wait_for_timeout(2000)
    print("Weixin Title:", page.title())
    content = page.evaluate('() => document.querySelector("#js_content").innerText')
    print("Content len:", len(content))
    print("Sample:\n", content[:400])
    b.close()
