from bs4 import BeautifulSoup
import csv

with open("data/twse.html","r",encoding="big5",errors="ignore") as f:
    soup=BeautifulSoup(f,"html.parser")

stocks=[]
seen=set()

for tr in soup.find_all("tr"):

    td=tr.find_all("td")

    if len(td)==0:
        continue

    text=td[0].get_text(strip=True)

    if "　" not in text:
        continue

    code,name=text.split("　",1)

    code=code.strip()
    name=name.strip()

    if not (len(code)==4 and code.isdigit()):
        continue

    if code in seen:
        continue

    seen.add(code)

    stocks.append([code+".TW",name])

with open("data/watch_symbols.csv","w",newline="",encoding="utf-8") as f:
    csv.writer(f).writerows(stocks)

print("上市股票：",len(stocks))
