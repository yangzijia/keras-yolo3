import cv2
import xml.etree.ElementTree as ET

# dir_path = "C:/Users/zjyang/Desktop/12_new_output"
# image_name = "0001_30d" # .jpg

dir_path = "20190624/ccb_bigdata_laboratory/smz_output_new"
image_name = "0028_360d"

image_path = dir_path + "/JPEGImages/" + image_name + ".jpg"
xml_path = dir_path + "/Annotations/" + image_name + ".xml"

boxes_list = []

in_file = open(xml_path, 'r', encoding='UTF-8')
tree=ET.parse(in_file)
root = tree.getroot()
for obj in root.iter('object'):
    # difficult = obj.find('difficult').text
    # cls = obj.find('name').text
    # if cls not in classes or int(difficult)==1:
    #     continue
    # cls_id = classes.index(cls)
    xmlbox = obj.find('bndbox')
    b = (int(float(xmlbox.find('xmin').text)), int(float(xmlbox.find('ymin').text)), int(float(xmlbox.find('xmax').text)), int(float(xmlbox.find('ymax').text)))
    boxes_list.append(b)
    # list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

image = cv2.imread(image_path)
for box in boxes_list:
    x1, y1, x2, y2 = box
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow("image", image)

cv2.waitKey(0)

cv2.destroyAllWindows()