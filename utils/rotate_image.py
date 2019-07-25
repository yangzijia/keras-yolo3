#数据集扩增
import cv2
import math
import numpy as np
import xml.etree.ElementTree as ET
import os

def rotate_image(src, angle, scale=1):
    w = src.shape[1]
    h = src.shape[0]
    # 角度变弧度
    rangle = np.deg2rad(angle)  # angle in radians
    # now calculate new image width and height
    nw = (abs(np.sin(rangle) * h) + abs(np.cos(rangle) * w)) * scale
    nh = (abs(np.cos(rangle) * h) + abs(np.sin(rangle) * w)) * scale
    # ask OpenCV for the rotation matrix
    rot_mat = cv2.getRotationMatrix2D((nw * 0.5, nh * 0.5), angle, scale)
    # calculate the move from the old center to the new center combined
    # with the rotation
    rot_move = np.dot(rot_mat, np.array([(nw - w) * 0.5, (nh - h) * 0.5, 0]))
    # the move only affects the translation, so update the translation
    # part of the transform
    rot_mat[0, 2] += rot_move[0]
    rot_mat[1, 2] += rot_move[1]
    dst = cv2.warpAffine(src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)
    # 仿射变换
    return dst

def rotate_box_center(coord, cx, cy, h, w, theta):
    M = cv2.getRotationMatrix2D((cx, cy), theta, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    M[0, 2] += (nW / 2) - cx
    M[1, 2] += (nH / 2) - cy
    v = [coord[0], coord[1], 1]
    calculated = np.dot(M, v)
    return int(calculated[0]), int(calculated[1])

def rotate_box(img, angle, xmin, ymin, xmax, ymax):
    (heigth, width) = img.shape[:2]
    (cx, cy) = (width // 2, heigth // 2)
    point = ((xmin + xmax) / 2., (ymin + ymax) / 2.)
    x, y = rotate_box_center(point, cx, cy, heigth, width, angle)
    box_w = abs(xmax - xmin)
    box_h = abs(ymax - ymin)
    rangle = round(np.deg2rad(angle), 2)  # angle in radians
    w = (abs(np.sin(rangle) * box_h) + abs(np.cos(rangle) * box_w))
    h = (abs(np.cos(rangle) * box_h) + abs(np.sin(rangle) * box_w))
    # w = abs(box_w * math.cos(angle)) + abs(box_h * math.sin(angle))
    # h = abs(box_h * math.cos(angle)) + abs(box_w * math.sin(angle))
    x1 = int(x - w/2.)
    x2 = int(x + w/2.)
    y1 = int(y - h/2.)
    y2 = int(y + h/2.)
    return x1, y1, x2, y2
    
def ListFilesToTxt(dir,file):
    for root, subdirs, files in os.walk(dir):
        for name in files:
            new_txt = name.split(".")[0]
            file.write(new_txt + " \n")
        
def write2txt(dir, outfile):
    file = open(outfile,"w")
    if not file:
        print ("cannot open the file %s for writing" % outfile)
    ListFilesToTxt(dir, file)
    file.close()

def check_dir(path):
    # 验证路径是否存在
    if not os.path.isdir(path):
        # 创建路径
        os.makedirs(path)

# 使图像旋转60,90,120,150,210,240,300度
input_path = '20190624/ccb_bigdata_laboratory/ljj_output'
output_path = '20190624/ccb_bigdata_laboratory/ljj_output_new'

imgpath = input_path + '/JPEGImages/'          #源图像路径
xmlpath = input_path + '/Annotations/'         #源图像所对应的xml文件路径
rotated_imgpath = output_path + '/JPEGImages/'
check_dir(rotated_imgpath)
rotated_xmlpath = output_path + '/Annotations/'
check_dir(rotated_xmlpath)
# create new train.txt
rotated_mainpath = output_path + '/ImageSets/Main/'
check_dir(rotated_mainpath)
outfile = rotated_mainpath + 'train.txt'
# 
for angle in (90, 180, 270, 360):
    for i in os.listdir(imgpath):
        a, b = os.path.splitext(i)                            #分离出文件名a
        img = cv2.imread(imgpath + a + '.jpg')
        tree = ET.parse(xmlpath + a + '.xml')
        root = tree.getroot()
        boxes = []
        for box in root.iter('bndbox'):
            xmin = float(box.find('xmin').text)
            ymin = float(box.find('ymin').text)
            xmax = float(box.find('xmax').text)
            ymax = float(box.find('ymax').text)
            boxes.append([xmin, ymin, xmax, ymax])
            cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), [255, 0, 0], 2)

        rotated_img = rotate_image(img,angle)
        cv2.imwrite(rotated_imgpath + a + '_'+ str(angle) +'d.jpg',rotated_img)

        print (str(i) + ' has been rotated for '+ str(angle)+'°')
        for box in boxes:
            xmin, ymin, xmax, ymax = box
            print("before -- ", (int(xmin), int(ymin)), (int(xmax), int(ymax)))
            #---------------------------------------------
            x1, y1, x2, y2 = rotate_box(img, angle, xmin, ymin, xmax, ymax)
            print("after --- ", (x1, y1), (x2, y2))
            # cv2.rectangle(rotated_img, (x1, y1), (x2, y2), [0, 0, 255], 2)   #可在该步骤测试新画的框位置是否正确
            # cv2.imshow('xmlbnd',rotated_img)
            # cv2.waitKey(0)
            #---------------------------------------------
            box.find('xmin').text = str(x1)
            box.find('ymin').text = str(y1)
            box.find('xmax').text = str(x2)
            box.find('ymax').text = str(y2)
        tree.write(rotated_xmlpath + a + '_'+ str(angle) +'d.xml')
        print (str(a) + '.xml has been rotated for '+ str(angle)+'°')

write2txt(rotated_imgpath, outfile)