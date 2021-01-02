import requests
from lxml import etree
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
r = requests.get("https://www.axutongxue.com/2020/12/contents.html",headers=headers).text

html = etree.HTML(r)

lis = html.xpath('//*[@id="menuList"]//li')
def write(name,start,end):
    all_li = ''
    f = open(name,'w',encoding='utf-8')
    for li in lis[int(start):int(end)]:
        one_li = etree.tostring(li,encoding='utf-8').decode('utf-8')
        all_li = all_li + one_li
    f.write(all_li)
    f.close()

write('./axu.html',0,len(lis)/2)
write('./axu2.html',len(lis)/2,len(lis))
