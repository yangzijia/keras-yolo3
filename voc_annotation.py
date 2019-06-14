import xml.etree.ElementTree as ET
# 标签分类（注意顺序需要和VOTT中的一样）
classes = ['helmet_safe', 'helmet_unsafe']
# 导出的voc格式数据集地址（此路径中不能出现中文）
folder_path = 'E:/engyne_work/helmet_detect/helmet_image/all_image/annotation/helmet_safe_unsafe/workers_hat_output'
def convert_annotation(image_id, list_file):
    in_file = open('%s/Annotations/%s.xml'%(folder_path, image_id))
    tree=ET.parse(in_file)
    root = tree.getroot()
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
def write_to_txt(image_set, list_file):
    image_ids = open('%s/ImageSets/Main/%s.txt'%(folder_path, classes[0] + "_" + image_set)).read().strip().split()
    for image_id in image_ids:
        if image_id != '0' and image_id != '1' and image_id != '-1':
            list_file.write('%s/JPEGImages/%s.jpg'% (folder_path, image_id))
            convert_annotation(image_id, list_file)
            list_file.write('\n')
    return list_file
list_file = open('%s.txt' % 'voc_train_4', 'w')
list_file = write_to_txt('train', list_file)  
list_file = write_to_txt('val', list_file)  
list_file.close()