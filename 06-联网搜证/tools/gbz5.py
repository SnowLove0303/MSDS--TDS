# -*- coding: utf-8 -*-
"""卫健委搜索站搜 GBZ 2.1-2019 公告附件"""
import time
from playwright.sync_api import sync_playwright
CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    pg = b.new_page()
    for url in [
        'http://so.nhc.gov.cn/searchResultList.shtml?searchWord=GBZ%202.1-2019',
        'https://www.nhc.gov.cn/wjw/pgw/201911/index.shtml',
    ]:
        try:
            pg.goto(url, timeout=45000, wait_until='domcontentloaded')
            pg.wait_for_timeout(3500)
            body = pg.evaluate('() => document.body.innerText')
            print(f'=== {url}')
            print('标题:', pg.title()[:50])
            print(body[:400].replace('\n',' | '))
            links = pg.evaluate('''() => Array.from(document.querySelectorAll('a')).map(a=>({t:(a.innerText||'').trim().slice(0,40), h:(a.href||'').slice(0,90)})).filter(x=>x.t)''')
            for l in links[:20]:
                if any(k in (l['t']+l['h']) for k in ['GBZ','职业接触','国卫通']):
                    print('  🔗', l['t'], '→', l['h'])
        except Exception as e:
            print(f'异常 {url}: {str(e)[:60]}')
        print()
    b.close()
