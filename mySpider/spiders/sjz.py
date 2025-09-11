import requests
import scrapy
import time
import hashlib
from base64 import b64decode
from Crypto.Cipher import AES

from Crypto.Util.Padding import unpad
import struct

from itemadapter import ItemAdapter
from mySpider.items import ItcastItem

import ast

class SjzSpider(scrapy.Spider):
    name = "sjz"
        # === key 和 iv 的 words ===
    key_words = [
        875652709, 929261158, 912602681, 962814305,
        959656038, 859333937, 808608355, 946025318
    ]
    iv_words = [
        1665232450, 2037021011, 1196389236, 1433161059
    ]
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'origin': 'https://www.acgice.com',
        'priority': 'u=1, i',
        'referer': 'https://www.acgice.com/',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'
    }
    # === 转换为 bytes ===
    key = b''.join(struct.pack('>I', w) for w in key_words)
    iv = b''.join(struct.pack('>I', w) for w in iv_words)
    def __init__(self, starturl=None, c_class=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if c_class is None:
            c_class = ['ammo']
        self.starturl = starturl
        self.c_class=c_class


        # === 修复 base64 填充 ===
    def fix_base64_padding(self,s):
        return s + '=' * ((4 - len(s) % 4) % 4)


    # === 解密函数 ===
    def decrypt(self,cipher_b64, key, iv):
        try:
            cipher_bytes = b64decode(cipher_b64)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(cipher_bytes), AES.block_size)
            return plaintext.decode('utf-8')
        except Exception as e:
            return f"解密失败: {e}"

    def gettoken(self,a):
        # 1. 获取 10 位 Unix 时间戳（秒级）
        tim = str(int(time.time()-3))
        # 2. 第一次 MD5 (a + tim)
        #print(a+tim)
        a1 = hashlib.md5((a + tim).encode()).hexdigest()
        #print(a1)
        # 3. 第二次 MD5 (tim + a1)
        #print(tim+a1)
        result = hashlib.md5((tim + a1+'私自使用，后果自负！我方保留起诉权利！').encode()).hexdigest()
    
        return result, tim  # 同时返回结果和时间戳，方便调用方使用
    def get_maxpagenumber(self,start_url2):

        url = "&".join(start_url2.replace("pagenumber", '1').split('&')[:5])
        token, times = self.gettoken(url.split('?')[1])
        #print(token, times)
        #print(url)
        url = url + f'&token={token}&timestamp={times}'
        res=requests.get(url,headers=self.headers)
        count=int(res.json()['count'])
        if count%10!=0:
            return int(count/10)+1
        else:
            return int(count/10)


    def start_requests(self):

        print('------------------------------------程序kaishi___________________________')
        for c in self.c_class:
            start_url2=self.starturl.replace("c_class", c)
            pagemax = self.get_maxpagenumber(start_url2)
            for i in range(1,pagemax+1):
                url="&".join(start_url2.replace("pagenumber",str(i)).split('&')[:5])
                yield scrapy.Request(
                    url=url,
                    meta={
                        'needs_timestamp': True,  # 标记这个请求需要添加时间戳
                        'base_url': url,  # 传递基础URL
                        'tokendata': url.split('?')[1],  # 传递token
                        'c_class': c  # 传递其他参数
                    },
                    headers=self.headers,
                    method='get',
                    callback=self.parse,
                    cb_kwargs={'c_class': c},
                )

    def parse(self, response,**kwargs):
        c_class=kwargs['c_class']
        try:
            data=self.fix_base64_padding(response.json()['data'])
            data=self.decrypt(data, self.key, self.iv)
            lst = ast.literal_eval(data)

            for i in lst:
                print(i)
                id=i["id"]
                token,times=self.gettoken('id='+str(id))
                #url = f"https://api.acgice.com/api/sjz/hour?id={id}&token={token}&timestamp={times}"
                headers = {
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                    'origin': 'https://www.acgice.com',
                    'priority': 'u=1, i',
                    'referer': 'https://www.acgice.com/',
                    'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'
                }

                yield scrapy.Request(
                    url=f"https://api.acgice.com/api/sjz/hour?id={id}",
                    headers=headers,
                    meta={
                        'needs_timestamp': True,  # 标记这个请求需要添加时间戳
                        'base_url': f"https://api.acgice.com/api/sjz/hour?id={id}",  # 传递基础URL
                        'tokendata': 'id='+str(id),  # 传递token
                    },
                    callback=self.parselist,
                    cb_kwargs={'i':i,'c_class': c_class},
                )
        except:
            pass

    def parselist(self,response,**kwargs):
        item=ItcastItem()
        indexdata=kwargs['i']
        c_class = kwargs['c_class']
        listdata=self.decrypt(response.json()['data'], self.key, self.iv)
        zddata={}
        zddata['indexdata']=indexdata
        zddata['listdata']=listdata
        zddata['c_class'] = c_class
        item['jsondatas']=zddata
        yield item