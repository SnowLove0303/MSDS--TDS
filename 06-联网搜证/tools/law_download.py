# -*- coding: utf-8 -*-
"""国内法规 PDF 直链批量下载.
用法: python law_download.py <法规.json> <输出目录>
清单项: {"name": 法规名, "pdf": 官方PDF直链}"""
import sys, json, re
from pathlib import Path
import requests

def download(url, out_path):
    out = Path(out_path)
    if out.exists() and out.stat().st_size > 1000:
        return ("skip", out.stat().st_size)
    s = requests.Session(); s.trust_env = False
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36",
        "Referer": re.sub(r"(https?://[^/]+).*", r"\1/", url),
    })
    try:
        r = s.get(url, timeout=120)
        if r.status_code == 200 and len(r.content) > 1000:
            # 支持 PDF/DOCX/DOC，按内容自动选择扩展名
            head = r.content[:4]
            if head[:4] == b"%PDF":
                ext = ".pdf"
            elif head[:2] == b"PK":
                ext = ".docx"
            elif head[:2] == b"\xd0\xcf":
                ext = ".doc"
            else:
                return ("fail", f"非文档: {r.content[:30]}")
            real = out.with_suffix(ext)
            real.write_bytes(r.content)
            if real != out and out.exists():
                out.unlink()   # 删除错误的旧扩展名文件
            return ("ok", len(r.content))
        return ("fail", f"HTTP {r.status_code}")
    except Exception as e:
        return ("fail", str(e)[:60])

if __name__ == "__main__":
    lst = json.load(open(sys.argv[1], encoding="utf-8"))
    out_root = Path(sys.argv[2]); out_root.mkdir(parents=True, exist_ok=True)
    ok = skip = fail = 0
    for it in lst:
        name = it["name"]
        fname = re.sub(r'[\/:*?"<>|]', "", name)   # 不带扩展名, download 自动判断
        sub = out_root / it.get("dir", ""); sub.mkdir(parents=True, exist_ok=True)
        st, info = download(it["pdf"], sub / fname)
        if st == "ok": ok += 1; print(f"✅ {name}: {info} 字节")
        elif st == "skip": skip += 1; print(f"⏭ {name}: 已存在 {info} 字节")
        else: fail += 1; print(f"❌ {name}: {info}")
    print(f"\n完成: ✅{ok}  ⏭{skip}  ❌{fail}")
