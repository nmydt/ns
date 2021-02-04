import subprocess as sp
import requests,json,random,re
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
ip_pools=[] #未过滤的ip池
new_pools=[]#已过滤的ip池

"""
函数说明:获取IP代理

"""

def pro():
    
    url = "http://proxylist.fatezero.org/proxy.list"
    r = requests.get(url,headers=headers)
    lists = r.text.split('\n')
    for i in lists:
        try:
            li = json.loads(i,strict=False)
            if str(li['anonymity']) == 'high_anonymous' and str(li['type']) == 'http':

                ip_port = str(li['host'])+":"+str(li['port'])

                ip_pools.append(ip_port)
        except:
            continue


"""
函数说明:检查代理IP的连通性
Parameters:
	ip - 代理的ip地址
	lose_time - 匹配丢包数
	waste_time - 匹配平均时间
Returns:
	average_time - 代理ip平均耗时
Modify:
	2017-05-27
"""

def check_ip(ip, lose_time, waste_time):
    #命令 -n 要发送的回显请求数 -w 等待每次回复的超时时间(毫秒)
    cmd = "ping -w 3 %s"
    #执行命令
    p = sp.Popen(cmd % ip, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True) 
    #获得返回结果并解码
    out = p.stdout.read().decode("gbk")
    #丢包数
    lose_time = lose_time.findall(out)
    #当匹配到丢失包信息失败,默认为三次请求全部丢包,丢包数lose赋值为3
    if len(lose_time) == 0:
        lose = 3
    else:
        lose = int(lose_time[0])
    #如果丢包数目大于2个,则认为连接超时,返回平均耗时1000ms
    if lose > 25:
        #返回False
        return 1000
    #如果丢包数目小于等于2个,获取平均耗时的时间
    else:
        #平均时间
        average = waste_time.findall(out)
        #当匹配耗时时间信息失败,默认三次请求严重超时,返回平均好使1000ms
        if len(average) == 0:
            return 1000
        else:
            #
            average_time = float(average[0])
            #返回平均耗时
            return average_time

"""
函数说明:进一步检查代理IP的可用性
Parameters:
	ip_port - 代理ip

"""
def check_ip2(ip_port):
    proxy = {
        'http':ip_port
    }
    try:
        r = requests.get('http://www.baidu.com',headers=headers,proxies=proxy,timeout=5)
        if r.status_code != 200:
            print("faild:{}".format(ip_port))
            return -1
        else:
            return 200
    except:
        print("faild:{}".format(ip_port))
        return -1
"""
函数说明:初始化正则表达式
Parameters:
	无
Returns:
	lose_time - 匹配丢包数
	waste_time - 匹配平均时间

"""
def initpattern():
    #匹配丢包数
    lose_time = re.compile(u"\s(\d+)%", re.IGNORECASE)
    #匹配平均时间
    waste_time = re.compile(u"/(\d.*?)/", re.IGNORECASE)
    return lose_time, waste_time

"""
函数说明:保存代理

"""
def save_proxy():
    f = open('./ip_pool/ips.html','w')
    f.write(str(new_pools))

if __name__ == '__main__':
    #初始化正则表达式
    lose_time, waste_time = initpattern()
    #获取IP代理
    
    pro()
    #如果平均时间超过200ms重新选取ip
    for proxy in ip_pools:
        split_proxy = proxy.split(':')
        #获取IP
        ip = split_proxy[0]
        
        #检查ip
        average_time = check_ip(ip, lose_time, waste_time)
        print(average_time)
        if average_time < 200:
            if check_ip2(proxy)==200:
                print(proxy+"验证成功")
                new_pools.append(proxy)
    
    save_proxy()
