# -*- coding: utf-8 -*-
"""用 Playwright 批量抓取生态环境部法规库全文 (mee.gov.cn/ywgz/fgbz)
用法: python mee_law_crawl.py <索引.json> <输出目录>
索引格式: {"法律": [{"title":..., "href":...}], ...}"""
import sys, json, re, time
from pathlib import Path
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
BASE = 'https://www.mee.gov.cn/ywgz/fgbz'

def fetch_body(pg, url):
    pg.goto(url, timeout=45000, wait_until='networkidle')
    pg.wait_for_timeout(2000)
    text = pg.eval_on_selector_all('body', 'els => els.map(e => e.innerText)')
    t = text[0] if text else ''
    # 去掉页面导航冗余，保留法规正文
    start = t.find('目　录')
    if start < 0: start = t.find('第一章')
    if start < 0: start = t.find('第一条')
    if start < 0:
        return None
    return t[start:]

def clean_title(t):
    return re.sub(r'[\/:*?"<>|\r\n]', '', t).strip()

if __name__ == '__main__':
    idx = json.load(open(sys.argv[1], encoding='utf-8'))
    out_root = Path(sys.argv[2]); out_root.mkdir(parents=True, exist_ok=True)
    ok = skip = fail = 0
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
        pg = b.new_page()
        for cat, items in idx.items():
            sub = out_root / cat; sub.mkdir(parents=True, exist_ok=True)
            for it in items:
                href = it['href']
                if not href.startswith('http'):
                    href = BASE + href.lstrip('.')
                name = clean_title(it['title'])
                fpath = sub / f'{name}.txt'
                if fpath.exists() and fpath.stat().st_size > 500:
                    skip += 1; print(f'⏭ [{cat}] {name}')
                    continue
                try:
                    body = fetch_body(pg, href)
                    if body and len(body) > 500:
                        fpath.write_text(body, encoding='utf-8')
                        ok += 1; print(f'✅ [{cat}] {name}: {len(body)} 字')
                    else:
                        fail += 1; print(f'❌ [{cat}] {name}: 正文为空')
                except Exception as e:
                    fail += 1; print(f'❌ [{cat}] {name}: {str(e)[:50]}')
                time.sleep(1)
        b.close()
    print(f'\n完成: ✅{ok}  ⏭{skip}  ❌{fail}')
