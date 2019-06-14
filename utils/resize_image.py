import cv2
import os

image_size = 416
source_path = 'E:/engyne_work/wave_detect/176/images/'
target_path = 'E:/engyne_work/wave_detect/176/images_416_size/'

if not os.path.exists(target_path):
    os.makedirs(target_path)

image_list = os.listdir(source_path)

i = 0
for file in image_list:
    i = i+1
    image_source = cv2.imread(source_path + file)
    image = cv2.resize(image_source, (image_size, image_size), 0, 0, cv2.INTER_LINEAR)
    cv2.imwrite(target_path + str(i) + ".jpg", image)
print("resize image finished.")