#coding=utf-8
#必应图片爬虫
import re
import os
import urllib.request
url = 'http://cn.bing.com/images/search?q=hand+cellphone&FORM=HDRSC2'
coding = 'utf-8'
thepath = 'D:\\test\\'
 
def get():
    try:
        html = urllib.request.urlopen(url).read().decode(coding)
    except:
        print('error')
        print(url)
        return
    title = re.search("<title>.*</title>", html).group()
    title = title[7:-20]
    pic_url = re.findall('http://.{1,100}.jpg|http://.{1,100}.png|http://.{1,100}.jpeg',str(html),re.IGNORECASE)
    pic_url = list(set(pic_url))
    path = thepath + title
    try:
        os.mkdir(path)
    except:
        return
    i = 1
    for each in pic_url:
        try:
            pic= urllib.request.urlopen(each,timeout=10).read()
        except:
            continue
        file = path + '\\' + title + str(i) + '.jpg'
        fp = open(file,'wb')
        fp.write(pic)
        fp.close()
        i=i+1
    if not os.listdir(path):
        os.removedirs(path)
        print('error')
        print(url)
 
get()