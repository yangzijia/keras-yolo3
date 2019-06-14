#coding=utf-8  
  
import os

path = 'E:\\engyne_work\\safety_belt\\picture\\new_image\\'

count = 1
for file in os.listdir(path):
    os.rename(os.path.join(path,file),os.path.join(path,"%04d.jpg" % count))
    count+=1
