# -*- coding: utf-8 -*-
"""批量抓取生态环境部法律/行政法规全文 (mee.gov.cn/ywgz/fgbz)
用法: python mee_flfg_crawl.py <索引.json> <输出目录>
从页面提取标题和正文, 存为 txt."""
import sys, json, re, time
from pathlib import Path
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
BASE = 'https://www.mee.gov.cn/ywgz/fgbz'

def fetch_page(pg, url):
    pg.goto(url, timeout=45000, wait_until='networkidle')
    pg.wait_for_timeout(2500)
    data = pg.evaluate(r"""() => {
        const text = document.body.innerText;
        let title = document.title.replace(/_.*/, '').trim();
        // 若 title 是跳转提示, 用 h1
        if (!title || title.includes('跳转')) {
            const h1 = document.querySelector('h1, .title, .art_title, #title');
            if (h1) title = h1.innerText.trim();
        }
        let start = text.indexOf('目　录');
        if (start < 0) start = text.indexOf('第一章');
        if (start < 0) start = text.indexOf('第一条');
        if (start < 0) start = text.indexOf('（');
        return {title: title, body: start >= 0 ? text.slice(start) : text.slice(500)};
    }""")
    return data

def clean(s):
    return re.sub(r'[\/:*?"<>|\r\n]', '', s).strip()

if __name__ == '__main__':
    idx = json.load(open(sys.argv[1], encoding='utf-8'))
    out_root = Path(sys.argv[2]); out_root.mkdir(parents=True, exist_ok=True)
    ok = skip = fail = 0
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
        pg = b.new_page()
        for cat, items in idx.items():
            if not items: continue
            sub = out_root / cat; sub.mkdir(parents=True, exist_ok=True)
            for it in items:
                href = it['href']
                if 'most.gov.cn' in href or 'mem.gov.cn' in href or 'sthjt' in href:
                    continue   # 跳过外部链接
                if not href.startswith('http'):
                    # 索引 href 相对各分类子页: 法律在 fl/, 行政法规在 xzfg/
                    subpath = {'法律': 'fl', '行政法规': 'xzfg', '规章': 'guizhang'}.get(cat, '')
                    href = f'{BASE}/{subpath}/' + href.lstrip('./')
                try:
                    data = fetch_page(pg, href)
                    title = clean(data['title']) or f'{cat}_{href.split("/")[-1].replace(".shtml","")}'
                    body = data['body']
                    # 跳转页检测: 标题含'跳转'或正文开头是跳转提示
                    if title and ('跳转' in title or '继续' in title[:10]):
                        # 可能是限流, 等待后重试一次
                        pg.wait_for_timeout(5000)
                        pg.goto(href, timeout=45000, wait_until='networkidle')
                        pg.wait_for_timeout(2500)
                        data = pg.evaluate(r"""() => {
                            const text = document.body.innerText;
                            let title = document.title.replace(/_.*/, '').trim();
                            let start = text.indexOf('目　录');
                            if (start < 0) start = text.indexOf('第一章');
                            if (start < 0) start = text.indexOf('第一条');
                            return {title: title, body: start >= 0 ? text.slice(start) : text.slice(500)};
                        }""")
                        title = clean(data['title'])
                        body = data['body']
                    if len(body) < 200:
                        fail += 1; print(f'❌ [{cat}] {title[:30]}: 正文过短')
                        continue
                    fpath = sub / f'{title}.txt'
                    if fpath.exists() and fpath.stat().st_size > 500:
                        skip += 1; print(f'⏭ [{cat}] {title[:30]}')
                        continue
                    fpath.write_text(body, encoding='utf-8')
                    ok += 1; print(f'✅ [{cat}] {title[:35]}: {len(body)} 字')
                except Exception as e:
                    fail += 1; print(f'❌ [{cat}] {href[-30:]}: {str(e)[:40]}')
                time.sleep(2)
        b.close()
    print(f'\n完成: ✅{ok}  ⏭{skip}  ❌{fail}')
