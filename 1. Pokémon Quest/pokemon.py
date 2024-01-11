# coding=utf-8
import io
import sys
import urllib.request
import random
import requests
import json
from lxml import etree
import csv
import  os
import  time
from urllib.request import Request, urlopen
_path='C:/Users/ASUS/Desktop/pokemenp/imgs/'
# 应用账号（请替换为真实账号）
app_key = '1058332250317672448'
# 应用密码（请替换为真实密码）
app_secret = 'MSMoKiuJ'
api_url = "https://api.xiaoxiangdaili.com/ip/get"

s_path ='pokemon.csv'
class Pokemon():
     def __init__(self):
         self.base_url = 'https://tw.portal-pokemon.com/play/pokedex/'
         self.pokemon_data=[]# 获取基本的url这里面的url都是真实的
         self.data_list=[]
         self.header = {
             "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
         self.uapools = [
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
             "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0",
             "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
             "Mozilla/5.0 (compatible; ABrowse 0.4; Syllable)",
         ]

     def getProxy(self):
         res = requests.get(api_url, params={'appKey': app_key, 'appSecret': app_secret, 'wt': 'text','cnt':1})
         content = str(res.content, 'utf-8')
         print("API response: " + content)
         return content
     def get_ip(self):
         p = self.getProxy()
         proxyMeta = "http://%(user)s:%(pass)s@%(proxy)s" % {
             "proxy": p,
             "user": app_key,
             "pass": app_secret,
         }
         proxies = {
             'http': proxyMeta,
             'https': proxyMeta,
         }
         return  proxies
     def get_randomheaders(self):
         thisua = random.choice(self.uapools)  # 随机选择一个请求头
         headers = ("User-Agent", thisua)  # 构建请求头
         opener = urllib.request.build_opener()  # 添加opener
         opener.addheaders = [headers]
         # 安装为全局
         urllib.request.install_opener(opener)  # 这边headers输出的是元组
         header = {}
         headers_list = list(headers)
         header[headers_list[0]] = headers_list[1]
         # header['Cookie'] = cookie.encode("utf-8").decode("latin1")
         # print(header)
         return header
# 获取基础url
     def get_paokemon_base_url(self):
         for i in range(1, 1011):  # Adjust range as needed
             formatted_number = str(i).zfill(4)
             url = f"{self.base_url}{formatted_number}"
             self.pokemon_data.append(url)
         return
#用于获取基础url后附带的宝可梦 比如 喷火龙，喷火龙集巨化
     def get_paokemon_base_urls2(self):
         pokemon_data_end=[]
         for i in range(len(self.pokemon_data)):
             pokemon_data_end.append(self.pokemon_data[i])
             for j  in range(1,4):
                 new_url = f"{self.pokemon_data[i]}_{j}"
                 pokemon_data_end.append(new_url)
         return pokemon_data_end
#获取html文本
     def get_url_html(self, url, headers,proxies):
         try:
             response = requests.get(url=url, headers=headers,proxies=proxies)
             return  response.text
         except Exception as e:
             print(e)
             return  None

     def save_image(self, save_path, img_name, image_url,headers,proxies):
         content = requests.get(image_url, headers=headers,proxies=proxies).content
         img_name = img_name.replace(' ', '') + image_url[-4:]
         # print(save_path + img_name)
         # exit()
         with open(save_path + img_name, 'wb') as f:
             f.write(content)
             print(img_name, "下载完成...")
     def na_data(self, start_html,num,headers, proxies):
         html = etree.HTML(start_html)
         data_item = {}
         elements_a = html.xpath('/html/body/div[1]/div/div[2]/div/div[2]/p')

         # print(elements) #[<Element p at 0x1ccd7337e80>, <Element p at 0x1ccd639bd40>, <Element p at 0x1ccd74e4e80>]
         # exit()
         if elements_a:
             data_item['编号']= elements_a[0].xpath('.//text()')[0]  # Adjust the index if needed
             # 如果不是超级巨化没有2
             # 执行一次 XPath 查询，并将结果存储在变量中
             # 检查是否有足够的元素
             if len(elements_a) > 3:
                 # 如果有足够的元素，提取所需的文本
                 data_item['姓名'] = elements_a[1].text + elements_a[2].text
             else:
                 # 如果元素不足，
                 data_item['姓名']=elements_a[1].text
             elements_b = html.xpath('/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/a/span')
             all_text_content = ""
             for element in elements_b:
                 element_text = element.text  # or element.string
                 if element_text:
                     all_text_content += element_text
             data_item['属性']=all_text_content
             all_text_content = ""
             elements_c = html.xpath('/html/body/div[1]/div/div[3]/div/div[3]/div[2]/div/div/a/span')
             for element in  elements_c:
                 element_text =element.text
                 if element_text:
                     all_text_content += element_text
             data_item['弱点']=all_text_content
             raw_text_list = html.xpath('/html/body/div[1]/div/div[3]/div/div[4]//text()')
             # 去掉空格和换行符，并过滤空字符串
             cleaned_text_list = [text.strip() for text in raw_text_list if text.strip()]
             # 打印或处理清理后的文本列表
             str_list=[]
             for text in cleaned_text_list:
                 str_list.append(text)
             str_attr=''.join(str_list)
             data_item['数据']=str_attr
             # 爬取图片
             t=html.xpath('/html/body/div[1]/div/div[3]/div/div[1]/div/img[3]')[0].get("src")
             img='https://tw.portal-pokemon.com'+t
             img_name=data_item['编号']+data_item['姓名']
             self.save_image(_path,img_name,img,headers,proxies)
             # print(img_name)
             # exit()
             data_item['imgs']=img
             self.data_list.append(data_item)
             with open(s_path, 'a', newline='', encoding='utf-8') as file:
                 writer = csv.DictWriter(file, fieldnames=self.data_list[0].keys())
                 # 写入表头
                 if file.tell() == 0:
                     writer.writeheader()
                 writer.writerow(self.data_list[-1])  # 每次更新时写入self.data_list的最后一个元素
             # print(self.data_list)
             # exit()
         else:
             print("此url无效")
             return  False # 判断是否需要重新ip
         return True
     def run(self):
         sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # 设置IO流解决某个字符不能编译的问题
         self.get_paokemon_base_url()
         pokemon_data_end=self.get_paokemon_base_urls2()  # 拿到url
         # 1.随机生成headers,代理
         headers = self.get_randomheaders()
         proxies = self.get_ip()
         for  i  in range(4037,len(pokemon_data_end)):
             # print(pokemon_data_end[i])
             # exit()
             # 2.发送请求，获取响应
             start_html= self.get_url_html(pokemon_data_end[i],headers=headers,proxies=proxies)

             if  start_html is not None:
             # 3.提取数据，下一个next_url；和该页url列表
                 random_=self.na_data(start_html,i,headers=headers,proxies=proxies)
                 if random_:
                    time.sleep(16)
                    headers = self.get_randomheaders()
                    proxies = self.get_ip()


                 # print(self.data_list[0].keys()) #dict_keys(['编号', '姓名', '属性', '弱点', '数据', 'imgs'])

                 print("-----------------第{}个宠物结束----------------！".format(i))
             else:
                 print("-----------------第{}个宠物失败录入----------------！".format(i))
                 continue



if __name__ == '__main__':
    Pokemon = Pokemon()
    Pokemon.run()

