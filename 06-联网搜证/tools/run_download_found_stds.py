# -*- coding: utf-8 -*-
"""下载通过 openstd 检索到的新标准 PDF."""
import sys, time, json, re
from pathlib import Path
import requests, ddddocr

BASE = "https://openstd.samr.gov.cn/bzgk/std"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1", "Upgrade-Insecure-Requests": "1",
}

ROOT_OUT = Path(r"F:\正式项目与模块化内容\冠志\MSDS\Word 覆写模块\数据库与推断引擎\法规匹配库\标准原文归档")

def fetch_std(hcno, out_path, ocr, max_try=10):
    out = Path(out_path)
    if out.exists() and out.stat().st_size > 1000:
        return ("skip", {"size": out.stat().st_size})
    s = requests.Session()
    h = dict(HEADERS)
    h["Referer"] = f"{BASE}/showGb?type=download&hcno={hcno}"
    s.headers.update(h)
    s.get(f"{BASE}/showGb?type=download&hcno={hcno}", timeout=25)
    for i in range(max_try):
        try:
            r = s.get(f"{BASE}/gc?_{int(time.time()*1000)}", timeout=25)
            if r.status_code != 200 or len(r.content) < 500:
                continue
            code = ocr.classification(r.content).strip()
            if len(code) != 4:
                continue
            rv = s.post(f"{BASE}/verifyCode", data={"verifyCode": code}, timeout=25)
            if rv.text.strip() == "success":
                for k in range(12):
                    time.sleep(1.5)
                    rd = s.get(f"{BASE}/viewGb?hcno={hcno}", timeout=120)
                    if rd.status_code == 200 and len(rd.content) > 1000:
                        out.write_bytes(rd.content)
                        return ("ok", {"try": i+1, "code": code, "size": len(rd.content)})
                return ("fail", {"stage": "download_empty", "code": code})
        except Exception as exc:
            time.sleep(1)
    return ("fail", {"stage": "captcha_exhausted"})

def main():
    json_path = Path("F:/正式项目与模块化内容/冠志/MSDS/Word 覆写模块/数据库与推断引擎/法规匹配库/tools/found_std_hcno.json")
    items = json.loads(json_path.read_text(encoding="utf-8"))
    ocr = ddddocr.DdddOcr(show_ad=False)
    
    ok = skip = fail = 0
    for it in items:
        std = it["std"]
        name = it["name"]
        hcno = it["hcno"]
        subdir = it["dir"]
        
        target_dir = ROOT_OUT / subdir
        target_dir.mkdir(parents=True, exist_ok=True)
        fname = re.sub(r'[\\/:*?"<>|]', "_", f"{std}_{name}.pdf")
        out_path = target_dir / fname
        
        print(f"\n[下载中] {std} - {name} -> {subdir}/...")
        st, detail = fetch_std(hcno, out_path, ocr)
        if st == "ok":
            ok += 1
            print(f"  ✅ 成功! 大小: {detail['size']} 字节 (尝试 {detail['try']} 次)")
        elif st == "skip":
            skip += 1
            print(f"  ⏭ 已存在，跳过 ({detail['size']} 字节)")
        else:
            fail += 1
            print(f"  ❌ 失败: {detail}")
        time.sleep(1)
        
    print(f"\n=== 下载总结: 成功 {ok} | 跳过 {skip} | 失败 {fail} ===")

if __name__ == '__main__':
    main()
