# -*- coding: utf-8 -*-
"""
Class definition of YOLO_v3 style detection model on image and video
"""
import time
import cv2
import numpy as np
from my_yolo import YOLO
from PIL import Image
import logger as logger
import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"

class detect_wave:

    def __init__(self, model_path, video_path, out_video_path, is_check_line, is_put_out_video, x_error_range, y1_diff_frame, y2_diff_frame):

        if os.path.exists('logs/all.log'):
            os.remove('logs/all.log')
        '''
        参数设置
        '''
        self.video_path = video_path
        self.out_video_path = out_video_path  # 校验视频输出位置
        self.is_check_line = is_check_line   # 是否检测视频中的两条直线
        self.is_put_out_video = is_put_out_video    # 是否将校验视频输出
        self.x_error_range = x_error_range  # x 轴误差范围(像素)
        self.y1_diff_frame = y1_diff_frame # 100 帧之内判断为同一水波

        # self.model_path = 'wave/model/trained_wave_161_weights_final.h5'
        # self.model_path = 'wave/model/trained_wave_71_weights_final.h5'
        self.model_path = model_path
        self.classes_path = 'model_data/wave_voc_classes.txt'

        self.frame_v = 20    # 帧率 (帧/s)
        self.y_error_range = 7   # y 轴误差范围(像素)
        self.y2_diff_frame = y2_diff_frame
        self.relative_ratio = 1  # 比率（视频中两条线的真实长度与视频中像素长度的比值）
        self.unit = "像素"   # 单位
        self.check_side_length = 80

    def get_detect_list(self):
        yolo = YOLO(image=False, input=self.video_path, output='', model_path=self.model_path, classes_path=self.classes_path)
        cap = cv2.VideoCapture(self.video_path)
        detect_list = []
        while True:
            return_value, frame_lwpcv = cap.read()
            if return_value:
                image = Image.fromarray(frame_lwpCV)
                image, avg_point_list = yolo.detect_image(image)

                detect_list.append(avg_point_list)
            else:
                break

        return detect_list

    def detect_video(self):

        yolo = YOLO(image=False, input=self.video_path, output='', model_path=self.model_path, classes_path=self.classes_path)

        log = logger.Logger('logs/all.log',level='debug')

        line_list = []
        if self.is_check_line:
            line_list = self.check_lines(47.9)
            print(line_list)

        # 帧数
        # 存储水波速度结果 list
        wave_list = []
        vid = cv2.VideoCapture(self.video_path)
        if not vid.isOpened():
            raise IOError("Couldn't open webcam or video")
        frame = 1
        while True:
            return_value, frame_lwpCV = vid.read()
            if frame_lwpCV is None:
                break
            image = Image.fromarray(frame_lwpCV)
            image, avg_point_list = yolo.detect_image(image)
            if frame == 309:
                print(111)
            if len(avg_point_list) != 0:
                for vals in avg_point_list:
                    avg_point_x = vals['x']
                    avg_point_y = vals['y']

                    # 第一次出现标识框
                    if len(wave_list) == 0:
                        dist = {'x1': avg_point_x, 'y1': avg_point_y, 'f1': frame}
                        wave_list.append(dist)
                    else:
                        new_dist = {}
                        # 判断是否属于某一水波 的延申，判断条件： (new)x 属于(old)x 误差范围error_range内，并且，(new)y >= (old)y
                        not_storage = False
                        for val in wave_list:
                            # if in_error_range(avg_point_x, avg_point_y, val):   
                            #  (frame - val['f1']) < self.y1_diff_frame and \
                            if frame != val['f1']  and \
                                avg_point_x in range(val['x1'] - self.x_error_range, val['x1'] + self.x_error_range + 1)  and \
                                avg_point_y >= (val['y1'] - self.y_error_range):

                                if avg_point_y >= val['y1']:
                                    if 'y2' in val:
                                        if (frame - val['f2']) < self.y2_diff_frame :
                                        # if (avg_point_y - val['y2']) < 50:
                                            new_dist = val
                                            break
                                    else:
                                        if (frame - val['f1']) < self.y1_diff_frame:
                                            new_dist = val
                                            break
                                    
                                if avg_point_y in range(val['y1'] - self.y_error_range, val['y1']):
                                    not_storage = True
                                    break

                        if 'x1' in new_dist:
                            if 'y2' in new_dist:
                                if avg_point_y < (new_dist['y2'] - self.y_error_range):
                                    continue
                            # 如果存在则添加或者替换v（速度）
                            length = avg_point_y - int(new_dist['y1'])
                            # 单位为 秒 s
                            use_time = (frame - int(new_dist['f1'])) / self.frame_v
                            velocity = round(length * self.relative_ratio / use_time, 2)

                            if length < -int(self.y_error_range):
                                # 相同 x 位置出现第二条水波
                                # 判断为新水波
                                dist = {'x1': avg_point_x, 'y1': avg_point_y, 'f1': frame}
                                wave_list.append(dist)
                            elif velocity != 0:
                                new_dist['v'] = velocity

                                new_dist['x2'] = avg_point_x
                                new_dist['y2'] = avg_point_y
                                new_dist['f2'] = frame

                                log.logger.info("now_dist {x: %s, y: %s, f: %s, v: %s}" % (avg_point_x, avg_point_y, frame, velocity))
                                log.logger.info("after list %s" % wave_list)
                        else:
                            # 否则判断为新水波
                            if not not_storage:
                                dist = {'x1': avg_point_x, 'y1': avg_point_y, 'f1': frame}
                                wave_list.append(dist)

            frame += 1
            result = np.asarray(image)
            # 标识出视频中的两条直线
            if self.is_check_line:
                for line in line_list:
                    cv2.line(result, (line['x1'], line['y1']), (line['x2'], line['y2']), (0, 0, 255), 2)

            cv2.putText(result, text=str(frame), org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.50, color=(255, 0, 0), thickness=2)
            cv2.namedWindow("result", cv2.WINDOW_NORMAL)
            cv2.imshow("result", result)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        print("result:")
        aa = 0
        new_wave_list = []
        for  val in wave_list:
            if 'x2' in val:
                new_wave_list.append(val)
                print("%s第一次出现坐标 (%s, %s)，帧数为 %s ；\n最后出现的坐标 (%s, %s)，帧数为 %s。 速度为 %s （%s/s）\n " % (aa, 
                    val['x1'], val['y1'], val['f1'], val['x2'], val['y2'], val['f2'], val['v'], self.unit))
                aa += 1
        for index, val in enumerate(new_wave_list):
            print("%s %s %s %s %s %s %s " % (index, val['x1'], val['y1'], val['f1'], val['x2'], val['y2'], val['f2']))
        if self.is_check_line:
            print("视频中标志线的距离是：%s" % line_list[1]['real_length'])
        yolo.close_session()

        self.check_velocity(new_wave_list, line_list)


    # 对水波速率进行检验
    def check_velocity(self, wave_list, line_list):
        camera = cv2.VideoCapture(self.video_path)
        # 是否将检测视频输出
        global writer
        # 检验框边长
        

        if self.is_put_out_video:
            # 视频的宽度
            width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            # 视频的高度
            height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # 视频的帧率
            fps = camera.get(cv2.CAP_PROP_FPS)
            # 视频的编码
            fourcc = int(camera.get(cv2.CAP_PROP_FOURCC))

            # 定义视频输出
            writer = cv2.VideoWriter(self.out_video_path, fourcc, fps, (width, height))

        background = None
        # 帧数
        frame = 1
        
        while True:
            # 读取视频流
            grabbed, frame_lwpCV = camera.read()
            # 对帧进行预处理，先转灰度图，再进行高斯滤波。
            # 用高斯滤波进行模糊处理，进行处理的原因：每个输入的视频都会因自然震动、光照变化或者摄像头本身等原因而产生噪声。对噪声进行平滑是为了避免在运动和跟踪时将其检测出来。
            if frame_lwpCV is None:
                break
            gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)

            # 将第一帧设置为整个输入的背景
            if background is None:
                background = gray_lwpCV
                continue
            # 对于每个从背景之后读取的帧都会计算其与北京之间的差异，并得到一个差分图（different map）。
            # 还需要应用阈值来得到一幅黑白图像，并通过下面代码来膨胀（dilate）图像，从而对孔（hole）和缺陷（imperfection）进行归一化处理
            for index, val in enumerate(wave_list):
                # left = 0
                # top = 0
                # right = 0
                # bottom = 0

                if 'x2' in val and frame in range(val['f1'], val['f2'] + 1):
                    if frame == val['f1']:
                        point_x = val['x1']
                    else:
                        point_x = int((val['x2'] - val['x1']) * (frame - val['f1']) / (val['f2'] - val['f1']) + val['x1'])

                    point_y = int(val['y1'] + val['v'] * (frame - val['f1']) / self.frame_v)

                    diff_length = (self.check_side_length / 2)

                    left = int(point_x - diff_length)
                    right = int(point_x + diff_length)
                    top = int(point_y - diff_length)
                    bottom = int(point_y + diff_length)

                    cv2.rectangle(frame_lwpCV, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame_lwpCV, str(index), (left, top - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(frame_lwpCV, str(frame), (10, 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                
            # 标识出视频中的两条直线
            if self.is_check_line:
                for line in line_list:
                    cv2.line(frame_lwpCV, (line['x1'], line['y1']), (line['x2'], line['y2']), (0, 0, 255), 2)

            cv2.imshow('checking', frame_lwpCV)

            if self.is_put_out_video:
                writer.write(frame_lwpCV)

            time.sleep(0.05)
            key = cv2.waitKey(1) & 0xFF
            frame += 1
            # 按'esc'健退出循环
            if key == ord("q"):
                break

        # When everything done, release the capture
        camera.release()
        if self.is_put_out_video:
            writer.release()
        cv2.destroyAllWindows()


    # 检测视频中的直线坐标
    def check_lines(self,diff_y):
        camera = cv2.VideoCapture(self.video_path)

        # 视频的宽度
        width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        # 视频的高度
        height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print(width, height)

        line_list = []
        new_line_list = []
        while True:
            # 读取视频流
            grabbed, frame_lwpCV = camera.read()
            if frame_lwpCV is None:
                break
            gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)
            # time.sleep(0.1)
            # 霍夫直线检测
            edges = cv2.Canny(gray_lwpCV, 15, 30, apertureSize=3)  # 4 5 6
            # tmp_lines = 0
            # if num == 1 or num == 4 or num == 6:
            #     tmp_lines = 250
            # elif num == 2:
            #     tmp_lines = 170
            # elif num == 3:
            #     tmp_lines = 240
            # elif num == 4:
            #     tmp_lines = 170
            # print(tmp_lines)
            lines = cv2.HoughLines(edges, 1, np.pi / 180, 190)    # 4 5 6
            
            if lines is not None and len(lines) > 2:

                for index, line in enumerate(lines):
                    dist = {}
                    rho, theta = line[0]
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a * rho
                    y0 = b * rho

                    x1 = int(x0 + 1000 * (-b))
                    y1 = int(y0 + 1000 * a)
                    x2 = int(x0 - 1000 * (-b))
                    y2 = int(y0 - 1000 * a)

                    # y=kx+b
                    if x1 != x2:
                        k = (y2 - y1) / (x2 - x1)
                        b = y1 - (k * x1)

                        x1 = 0
                        y1 = int(b)
                        x2 = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
                        y2 = int(k * x2 + b)

                        tmp_y = 1000
                        # if num==2 or num == 3:
                        #     tmp_y = 228

                        if index > 0:
                            for val in line_list:
                                if abs(val['y1'] - y1) > diff_y and abs(k - val['k']) < 0.02 and abs(k) < 0.08 and y1 < tmp_y \
                                and y1>100 and y1<250 :
                                    real_length = abs(val['y1'] - y1) * (1 - abs(k))
                                    dist = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'real_length': real_length}
                                    new_line_list.append(val)
                                    new_line_list.append(dist)

                                    return new_line_list
                        else:
                            if y1 < tmp_y and y1> 100 and y1<200:
                                dist = {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'k': k}
                                line_list.append(dist)
        ####################################
        #             cv2.line(frame_lwpCV, (x1, y1), (x2, y2), (0, 0, 255), 2)
        #     cv2.imshow("line", frame_lwpCV)
        #     key = cv2.waitKey(1) & 0xFF
        #     # 按'esc'健退出循环
        #     if key == ord("q"):
        #         break
        # camera.release()
        # cv2.destroyAllWindows()
        #####################################

if __name__ == '__main__':
    # detect_video()

    line_list = []
    # 测试检测视频中的两条直线
    num = 3
    video_name = 173
    video_path = 'D:/yolov3/doc/wave/20_frame/'+str(video_name)+'/'+str(video_name)+'_'+str(num)+'.mp4'
    out_video_path = "D:/yolov3/doc/wave/out/"+str(video_name)+"/"+str(video_name)+"_" + str(num) + ".mp4"  # 校验视频输出位置
    is_check_line = True   # 是否检测视频中的两条直线
    is_put_out_video = True    # 是否将校验视频输出
    x_error_range = 60  # x 轴误差范围(像素)
    y1_diff_frame = 145 # 100 帧之内判断为同一水波
    model_path = 'wave/model/trained_wave_161_weights_final.h5'
    d = detect_wave(model_path,video_path, out_video_path, is_check_line, is_put_out_video, x_error_range, y1_diff_frame,50)
    if is_check_line:
        line_list = d.check_lines(47.9)
        print(line_list)

    camera = cv2.VideoCapture(video_path)

    background = None
    # 帧数
    frame = 1
    
    while True:
        # 读取视频流
        grabbed, frame_lwpCV = camera.read()
        # 对帧进行预处理，先转灰度图，再进行高斯滤波。
        # 用高斯滤波进行模糊处理，进行处理的原因：每个输入的视频都会因自然震动、光照变化或者摄像头本身等原因而产生噪声。对噪声进行平滑是为了避免在运动和跟踪时将其检测出来。
        if frame_lwpCV is None:
            break
        gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)

        # 将第一帧设置为整个输入的背景
        if background is None:
            background = gray_lwpCV
            continue
            
        # 标识出视频中的两条直线
        if is_check_line:
            for line in line_list:
                cv2.line(frame_lwpCV, (line['x1'], line['y1']), (line['x2'], line['y2']), (0, 0, 255), 2)

        cv2.imshow('checking', frame_lwpCV)

        time.sleep(0.05)
        key = cv2.waitKey(1) & 0xFF
        frame += 1
        # 按'esc'健退出循环
        if key == ord("q"):
            break

    # When everything done, release the capture
    camera.release()

    cv2.destroyAllWindows()


    