import cv2
import numpy as np
import math


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
    dst = cv2.warpAffine(src, rot_mat, (int(math.ceil(nw)), int(
        math.ceil(nh))), flags=cv2.INTER_LANCZOS4)
    # 仿射变换
    return dst

def rotate_box_center(coord, cx, cy, h, w, theta):
    # opencv calculates standard transformation matrix
    M = cv2.getRotationMatrix2D((cx, cy), theta, 1.0)
    # Grab  the rotation components of the matrix)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cx
    M[1, 2] += (nH / 2) - cy
    # Prepare the vector to be transformed
    v = [coord[0], coord[1], 1]
    # Perform the actual rotation and return the image
    calculated = np.dot(M, v)
    return int(calculated[0]), int(calculated[1])

def rotate_box(img, angle, xmin, ymin, xmax, ymax):
    (heigth, width) = img.shape[:2]
    (cx, cy) = (width // 2, heigth // 2)
    point = ((xmin + xmax) / 2., (ymin + ymax) / 2.)
    x, y = rotate_box_center(point, cx, cy, heigth, width, angle)
    w = width * math.cos(angle) + heigth * math.sin(angle)
    h = height * math.cos(angle) + width * math.sin(angle)
    return x, y, w, h

path = "C:/Users/zjyang/Desktop/test/0001.jpg"
angle = 30
point = (200, 300)
img = cv2.imread(path)

cv2.circle(img, point, 2, (0, 0, 255), 4)

cv2.imshow("img", img)

rotated_img = rotate_image(img, angle)

(heigth, width) = img.shape[:2]
(cx, cy) = (width // 2, heigth // 2)

x, y = rotate_box_center(point, cx, cy, heigth, width, angle)
print(x, y)
cv2.circle(rotated_img, (x, y), 10, (0, 255, 0), 4)



cv2.imshow("rotated_img", rotated_img)
cv2.waitKey(0)
