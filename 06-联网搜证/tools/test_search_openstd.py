import requests, re, json
from bs4 import BeautifulSoup

def search_openstd(query):
    url = "https://openstd.samr.gov.cn/bzgk/std/list"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    r = requests.get(url, params=params, headers=headers, timeout=15)
    
    soup = BeautifulSoup(r.text, "html.parser")
    results = []
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) >= 4:
            text_all = tr.get_text(separator=" ", strip=True)
            links = [a.get("href") for a in tr.find_all("a") if a.get("href")]
            # find hcno
            hcno = None
            for link in links:
                m = re.search(r'hcno=([A-Fa-f0-9]+)', link)
                if m:
                    hcno = m.group(1)
                    break
            if hcno:
                results.append({
                    "text": text_all,
                    "hcno": hcno,
                    "links": links
                })
    return results

if __name__ == "__main__":
    for q in ["GB 15603-2022", "GB 15258-2009", "GB 18597-2023", "GB 18484-2020", "GB 12158-2006", "GB 50016", "GB 50140"]:
        res = search_openstd(q)
        print(f"Query: {q} -> Found {len(res)} results")
        for r in res[:2]:
            print("  ", r["text"][:80], "HCNO:", r["hcno"])
