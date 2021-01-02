import requests
from lxml import etree
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
r = requests.get("https://www.axutongxue.com/2020/12/contents.html",headers=headers).text

html = etree.HTML(r)

lis = html.xpath('//*[@id="menuList"]//li')

f = open('./index2.html','w',encoding='gbk')
f.write('')
f.close()
f = open('./index2.html','a',encoding='gbk')
for li in lis:
    one_li = etree.tostring(li,encoding='gbk').decode('gbk')
    f.write(one_li)
    
f.close()
