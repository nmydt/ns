
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import os

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chromedriver = "/usr/bin/chromedriver"
# os.environ["webdriver.chrome.driver"] = chromedriver
# driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=chromedriver)
# driver.get("https://www.baidu.com")
# print(driver.title)
# driver.quit()
from lxml import etree
import requests,re
import random, time,os

User_Agent = [
	'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; KTXN)',
    'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
	'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0' 
]
headers = {}
headers['User-Agent'] = random.choice(User_Agent)
from lxml import etree
import requests
import random, time
from selenium import webdriver
import re,time,csv

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chromedriver = "/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=chromedriver)
def get_detail_urls(url):
    driver.get(url)
    source = driver.page_source
    
    html = etree.HTML(source)
    lis = html.xpath("//table[@class='tbspan']//a/@href")

    detail_urls = map(lambda url:"https://www.dytt8.net/"+url,lis)
    return detail_urls
def get_detail_content(url):

    driver.get(url)

    source = driver.page_source
    html = etree.HTML(source)    
    title = html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
    img = html.xpath("//img/@src")[0]
    zoom = html.xpath("//div[@id='Zoom']//text()")
    where = html.xpath("//div[@id='Zoom']//@href")[0]
    data = zooms(zoom,"◎年　　代")
    size = zooms(zoom,"◎文件大小")
    label = zooms(zoom,"◎标　　签")
    info = zooms(zoom,"◎主　　演　")
    actors = [info]
    for index,zo in enumerate(zoom):

        if zo.startswith("◎主　　演　"):
           
            for x in range(index+1,len(zoom)):
                actor = zoom[x].strip()
                if actor.startswith("◎"):
                    break
                actors.append(actor)
        elif zo.startswith("◎导　　演　"):
            actor = zooms(zoom,"◎导　　演　")
            actors.append(actor)
    intro = '*'
    for index,zo in enumerate(zoom):
        if zo.startswith("◎简　　介"):
            for x in range(index+1,index+2):
                intro = zoom[x].strip()
                
                if intro.startswith("◎"):
                    break
                
            
    movie = {
        "title":title,
        "img": img,
        "data": data,
        "size": size,
        "label": label,
        "where": where + " 详细页面：" + url,
        "actors": actors,
        "introduction": intro
        
    }
    return movie

def zooms(zoom,strs):
    for zo in zoom:
        if zo.startswith(strs):
            zo = zo.replace(strs,'').strip()
            return zo
        

        
    
def spider():
    headers = ['title','img','data','size','label','where','actors','introduction']
    fp = open('dytt.csv','a',newline='',encoding='utf-8')
    writer = csv.DictWriter(fp,headers)
    writer.writeheader()
    url = "https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html"
    for x in range(0,2):
        movies = []
        time.sleep(5)
        print("**"*30)
        print("第"+ str(x)+"页")
        print("**"*30)
        urll = url.format(x)
        try:
            detail_urls = get_detail_urls(urll)
        except:
            continue
        
        for a in detail_urls:            
            if a == "https://www.dytt8.net//html/gndy/dyzz/20181130/57856.html":
                continue
            try:
  
                movie = get_detail_content(a)
            except:
                continue
            
            
            movies.append(movie)
            print(movie)
           
        writer.writerows(movies)
        time.sleep(2)
      
            
        
if __name__ == '__main__':
#     fp = open('dytt.csv','w',newline='',encoding='utf-8')
#     fp.write('')
    spider()
    
