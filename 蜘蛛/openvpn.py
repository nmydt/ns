import requests,re
from lxml import etree
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'referer': 'https://freevpn.gg/s/ALL'
}
ip = []

def parse_page(url):
    r = requests.get(url,headers=headers).content.decode('utf-8')
    ips = re.findall(r'<div\sclass="card-box">.*?>(.*?)<',r,re.DOTALL)
    speed_tags = re.findall(r'<p\sclass="card-text.*?<br>(.*?)<br>',r,re.DOTALL)
    speed = []
   
    for i in speed_tags:
        
        spee1 = re.search('.*?\s(.*?)m.*?\s|(uncheckable)',i)
        speed1 = spee1.group(1)

        spee2 = re.search(',\s(.*?)m|uncheckable',i)
        speed2 = spee2.group(1)
        speed.append({'speed1':speed1,'speed2':speed2})
    links_tag = re.findall(r'<a\sclass="btn.*?".*?"(.*?)"',r,re.DOTALL)
    link = []
    for i in links_tag:
        link_ta = "https://freevpn.gg"+i+'/udp'
        link.append(link_ta)
    for value in zip(ips,speed,link):
        
        ips,speed,link = value
        open = {
            'ip':ips,
            'speed':speed,
            'link':link
        }
        ip.append(link)
  

    
def spider():
    for i in range(1,3):
        print('*'*30)
        print(i)
        print('*'*30)
        url = 'https://freevpn.gg/s/HK?p=%x' %i
    
        parse_page(url)
        
if __name__ == '__main__':
    spider()
    f = open('/vpn/vpn.html','w',encoding='utf-8')
    for t in ip:

        f.write('<a href='+t+'>'+t+'</a>'+'<br>')
