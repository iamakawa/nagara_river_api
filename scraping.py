import re
import requests
import json
import os
from bs4 import BeautifulSoup
# Webページを取得して解析する

load_url = "http://www.kasen.pref.gifu.lg.jp/h/Valley_6_448.html"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")
all_text = soup.text

regex = re.compile(' +')
list = []

all_text_list=all_text.split("\n")
#リストを1行ずづ読み込んで部分一致する行だけ抽出
for text in all_text_list:
    if ":" in text:
      if not "現在" in text:
        tsv_str = regex.sub('\t', text)
        fields = re.split('\s+', text)
        list.append(fields)

# print(list)

datas_tenminute = dict()
datas_onehour = dict()
datas_tenminute['fileds'] = [
  {"type":"timestamp","id":"時刻"},
  {"type":"numeric","id":"水位"},
  {"type":"text","id":"増減"}
]
datas_tenminute['records'] = []
datas_onehour['fileds'] = [
  {"type":"timestamp","id":"時刻"},
  {"type":"numeric","id":"水位"},
  {"type":"text","id":"増減"}
]
datas_onehour['records'] = []

for i in range(0,6):
  datas_tenminute['records'].append(list[i])
for i in range(6,len(list)):
  datas_onehour['records'].append(list[i])

os.makedirs('./data', exist_ok=True)
# 辞書オブジェクトをJSONファイルへ出力
with open('data/tenminutes.json', mode='wt', encoding='utf-8') as file:
  json.dump(datas_tenminute, file, ensure_ascii=False, indent=2)
with open('data/onehours.json', mode='wt', encoding='utf-8') as file:
  json.dump(datas_onehour, file, ensure_ascii=False, indent=2)