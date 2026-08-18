# -*- coding: utf-8 -*-
import requests, ddddocr, time

BASE = "https://openstd.samr.gov.cn/bzgk/std"
ocr = ddddocr.DdddOcr(show_ad=False)

def test_one(hcno, name):
    print(f"\nTesting {name} (hcno: {hcno})...")
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    r1 = s.get(f"{BASE}/showGb?type=download&hcno={hcno}", timeout=10)
    print("showGb status:", r1.status_code, "len:", len(r1.text))
    if "下载" not in r1.text and "验证码" not in r1.text:
        print("Not downloadable via showGb download, checking online...")
        r_on = s.get(f"{BASE}/showGb?type=online&hcno={hcno}", timeout=10)
        print("showGb online status:", r_on.status_code, "len:", len(r_on.text))

test_one("4D487D68BF0BD87E68CE0EA68183DAD6", "GB 15258-2009 (强制)")
test_one("4BB90BF6C7015DF7E4905694A80F7C57", "GB 15603-2022 (强制)")
test_one("846FBB803D7FCB2929D4AF45801E4E56", "GB/T 18664-2002 (推荐)")
