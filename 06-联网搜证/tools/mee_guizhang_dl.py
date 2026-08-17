# -*- coding: utf-8 -*-
"""用 Playwright + requests 批量下载生态环境部规章全文 (mee.gov.cn/ywgz/fgbz/guizhang)
87 部规章分 7 页 (gzk/index_1~6.shtml)。文字版 DOCX/DOC 直链下载。
用法: python mee_guizhang_dl.py <输出目录>"""
import sys, re, pathlib, requests, time
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
PAGES = ['https://www.mee.gov.cn/ywgz/fgbz/guizhang/'] + \
        [f'https://www.mee.gov.cn/gzk/index_{i}.shtml' for i in range(1, 7)]

def grab_rows(pg, url):
    pg.goto(url, timeout=45000, wait_until='networkidle')
    pg.wait_for_timeout(2000)
    return pg.evaluate('''() => {
        const out = [];
        document.querySelectorAll('li.skipAutoFix').forEach(li => {
            const dl = [...li.querySelectorAll('a')].find(a => a.textContent.includes('下载文字版'));
            const title = li.innerText.trim().replace(/下载文字版|下载图片版/g, '').trim();
            if (dl) out.push({title: title, docx: dl.href});
        });
        return out;
    }''')

def download(out_dir, name, url):
    fname = re.sub(r'（.*?）', '', name).strip()
    for ext in ('.docx', '.doc'):
        if (out_dir / (fname + ext)).exists():
            return ('skip', None)
    sess = requests.Session(); sess.trust_env = False
    sess.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0.0.0 Safari/537.36',
                         'Referer': 'https://www.mee.gov.cn/'})
    try:
        resp = sess.get(url, timeout=90)
        head = resp.content[:4]
        if resp.status_code == 200 and (head[:2] == b'\xd0\xcf' or head[:2] == b'PK'):
            ext = '.doc' if head[:2] == b'\xd0\xcf' else '.docx'
            (out_dir / (fname + ext)).write_bytes(resp.content)
            return ('ok', len(resp.content))
        return ('fail', f'HTTP{resp.status_code}')
    except Exception as e:
        return ('fail', str(e)[:40])

if __name__ == '__main__':
    out_dir = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '部门规章')
    out_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
        pg = b.new_page()
        total_ok = total_skip = total_fail = 0
        for url in PAGES:
            print(f'--- {url} ---')
            rows = grab_rows(pg, url)
            for r in rows:
                lines = [l.strip() for l in r['title'].split('\n') if l.strip() and not l.strip().isdigit()]
                name = lines[0] if lines else '规章'
                st, info = download(out_dir, name, r['docx'])
                if st == 'ok':
                    total_ok += 1; print(f'✅ {name}: {info}')
                elif st == 'skip':
                    total_skip += 1
                else:
                    total_fail += 1; print(f'❌ {name}: {info}')
            time.sleep(1)
        b.close()
    print(f'\n完成: ✅{total_ok}  ⏭{total_skip}  ❌{total_fail}')
