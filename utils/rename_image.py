#coding=utf-8  
  
import os

path = 'C:\\Users\\zjyang\\Desktop\\营业厅标注\\zk\\'

count = 1
for file in os.listdir(path):
    os.rename(os.path.join(path,file),os.path.join(path,"%04d.jpg" % count))
    count+=1
