#!/usr/bin/env python2
# -*- coding:utf-8 -*-
__anthor__ = 'Chenxy'
import urllib2
import urllib
import json
import time
from bs4 import BeautifulSoup
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

i = 0
page_b = ''
first_url = 'https://cn.bing.com/images/async?q=cellphone+in+hand&first={}&count=35'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}
while True:
    page_url = first_url.format(i*35)
    i += 1
    try:
        page_req = urllib2.Request(url=page_url,headers=headers)
        page_html = urllib2.urlopen(page_req,timeout=5).read()
        page_soup = BeautifulSoup(page_html,'lxml')
        page_as = page_soup.find_all('a',attrs={"class":"iusc"})
        for page_a in page_as:
            img_href = page_a.get('m')
            img_data = json.loads(img_href)
            img_src = img_data['murl'].split('?')[0]
            #切片获取图片名称
            img_name = img_src.split('/')[-1]
            #指定路径
            file_path = 'D:/Bing/'
            #下载图片
            urllib.urlretrieve(img_src,filename=file_path+img_name)
            #time.sleep(1)
            print '下载成功：%s'%(img_name)

        if page_as[-1] != page_b:
            page_b = page_as[-1]
            continue
        else:
            break
    except Exception,e:
        print e