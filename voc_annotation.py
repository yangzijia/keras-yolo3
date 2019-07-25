import xml.etree.ElementTree as ET
import os


# 标签分类（注意顺序需要和VOTT中的一样）
classes = ['person','tvmonitor','cellphone','head']
# 导出的voc格式数据集地址（此路径中不能出现中文）
dir_path = '20190624/ccb_bigdata_laboratory'
# dir_path = '20190624/ccb_buesness_hall'

dir_list = [
    "ljj_output",
    "lyc_output",
    "smz_output",
    "yjh_output",
    "yzj_output",
    "zc_output",
    "zk_output"
]

def convert_annotation(image_id, list_file, folder_path):
    in_file = open('%s/Annotations/%s.xml'%(folder_path, image_id),'r', encoding='UTF-8')
    tree=ET.parse(in_file)
    root = tree.getroot()
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(float(xmlbox.find('xmin').text)), int(float(xmlbox.find('ymin').text)), int(float(xmlbox.find('xmax').text)), int(float(xmlbox.find('ymax').text)))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

def write_to_txt(image_set, list_file, folder_path):
    # image_ids = open('%s/ImageSets/Main/%s.txt'%(folder_path, classes[0] + "_" + image_set)).read().strip().split()
    image_ids = open('%s/ImageSets/Main/%s.txt'%(folder_path, "train")).read().strip().split()
    
    for image_id in image_ids:
        if image_id != '0' and image_id != '1' and image_id != '-1':
            list_file.write('%s/JPEGImages/%s.jpg'% (folder_path, image_id))
            convert_annotation(image_id, list_file, folder_path)
            list_file.write('\n')
    return list_file

list_file = open('{}_{}.txt'.format('voc/voc_train', '1'), 'w')
for i, dirs in enumerate(dir_list):
    folder_path = dir_path + "/" + dirs + "_new"
    list_file = write_to_txt('train', list_file, folder_path)  
    # list_file = write_to_txt('val', list_file, folder_path)  
list_file.close()