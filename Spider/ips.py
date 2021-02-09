
import requests,random,json
from lxml import etree
import requests

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

temp_set = set()
def get_66ip():
    def parse_page(url):
        r = requests.get(url,headers=headers)
        if r.status_code == 200:

            html = etree.HTML(r.text)
        #     print(etree.tostring(html,encoding='utf-8').decode('utf-8'))
            trs = html.xpath('//div[@align="center"]/table//tr')
            for tr in trs[1:]:
        #             print(etree.tostring(tr,encoding='utf-8').decode('utf-8'))
                    ip = tr.xpath('.//td[1]/text()')[0]
                    port = tr.xpath('.//td[2]/text()')[0]
                    ip_port = ip+":"+port
                    temp_set.add(ip_port)
    def main():
        for i in range(1,34):
            url = "http://www.66ip.cn/areaindex_%d/1.html" %i
            parse_page(url)


    if __name__ == '__main__':
        main()
def pro():
    url = "http://proxylist.fatezero.org/proxy.list"
    r = requests.get(url,headers=headers)
    if r.status_code == 200:
        lists = r.text.split('\n')
        for i in lists[0:50]:
            try:
                li = json.loads(i,strict=False)
                if str(li['anonymity']) == 'high_anonymous' and str(li['type']) == 'http':

                    ip_port = str(li['host'])+":"+str(li['port'])
                    temp_set.add(ip_port)
            except:
                continue
def kuai():
    def parse_page(url):
        r = requests.get(url,headers=headers)
        html = etree.HTML(r.text)
        trs = html.xpath('//tbody//tr')    
        for tr in trs:
            ip = tr.xpath('./td[1]/text()')[0]
            port = tr.xpath('./td[2]/text()')[0]
            ip_port = ip+":"+port
            if ip_port in temp_set:
                temp_set.remove(ip_port)
            temp_set.add(ip_port)
            

    def main():
        for i in range(1,30):
            url = "https://www.kuaidaili.com/free/inha/%d" %i
            parse_page(url)


    if __name__ == '__main__':
        main()
def test_proxy():
    for ip_port in temp_set.copy():
        proxy = {
            'http':ip_port
        }
        try:
            r = requests.get('http://www.baidu.com',headers=headers,proxies=proxy,timeout=5)
            print(r.status_code)
            if r.status_code != 200:
                

                temp_set.remove(ip_port)

            else:
                print("true:{}".format(ip_port))
        except:
            temp_set.remove(ip_port)
            print("faild:{}".format(ip_port))
if __name__ == '__main__': 
    print("***正在抓取http代理ip***")
    # get_66ip()
    # kuai()
    pro()
    print("***success***")
    ago = len(temp_set)
    print("***正在检测http代理ip可用性***")
    test_proxy()
    present = len(temp_set)
    temp = list(temp_set)
    
    f = open('./ip_pool/pool.html','w',encoding='utf-8')
    for t in temp:

        f.write('\''+t+'\','+'\n')
    f.close
    print("***success***")
    print({'共抓取ip数':ago,'可用ip':present})
    print("***请在当前目录下pool.html文件查看成功抓取的可用ip***")

