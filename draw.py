#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

class SelectArea(object):
    def __init__(self):
        self.area_list = []
        self.__point1 = None
        self.__point2 = None
        self.__img = None
        self.select_times = 0
        self.__show_img = None
        # self.length = cfg.GET_BBOX_DEFAULTS["model_image_size"][0]
    
    def clear(self):
        self.area_list = []
        self.__point1 = None
        self.__point2 = None
        self.__img = None
        self.select_times = 0
        self.__show_img = None

    def __on_mouse(self, event, x, y, flags, param):
        img2 = self.__show_img.copy()
        if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
            self.__show_img = self.__img.copy()
            self.__point1 = (x, y)
            cv2.circle(img2, self.__point1, 10, (0, 255, 255), 2)
            cv2.imshow('image', img2)
        # 按住左键拖曳
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):
            width = abs(self.__point1[0] - x)
            height = abs(self.__point1[1] - y)

            self.__show_img = self.__img.copy()

            w_h_msg = "width:{}, height:{}".format(width, height)
            if width > 416 and height > 416:
                color_msg = (0, 255, 0)
            else:
                color_msg = (0, 0, 255)
            cv2.putText(self.__show_img, w_h_msg, (self.__point1[0], self.__point1[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_msg, 1)

            cv2.rectangle(self.__show_img, self.__point1,
                          (x, y), (0, 255, 255), 2)
            cv2.imshow('image', self.__show_img)
        elif event == cv2.EVENT_LBUTTONUP:  # 左键释放
            self.__point2 = (x, y)
            min_x = min(self.__point1[0], self.__point2[0])
            min_y = min(self.__point1[1], self.__point2[1])
            width = abs(self.__point1[0] - self.__point2[0])
            height = abs(self.__point1[1] - self.__point2[1])
            area = width * height
            if area > 30:
                # w_h_msg = "width:{}, height:{}".format(width, height)
                # if width > 416 and height > 416:
                #     color_msg = (0, 255, 0)
                # else:
                #     color_msg = (0, 0, 255)
                # cv2.putText(self.__show_img, w_h_msg, (self.__point1[0], self.__point1[1] - 10),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_msg, 1)
                self.area_list.append({"point1": self.__point1, "point2": self.__point2,
                                    "box": [min_x, min_y, min_x+width, min_y+height], "width": width, "height": height})

        elif event == cv2.EVENT_RBUTTONDOWN:  # 右键点击
            point = (x, y)
            temp = []
            # delete box info
            for dicts in self.area_list:
                x1, y1 = dicts["point1"]
                x2, y2 = dicts["point2"]
                if x not in range(x1, x2) or y not in range(y1, y2):
                    temp.append(dicts)
            self.area_list = temp
        elif event == cv2.EVENT_RBUTTONUP:  # 右键释放
            self.__show_img = self.__img.copy()
            self.__refresh()

    def __refresh(self):
        msg = "confirm the area by Y and leave."
        cv2.putText(self.__show_img, msg, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 1)
        if len(self.area_list) > 0:
            for dicts in self.area_list:
                # w_h_msg = "width:{}, height:{}".format(dicts["width"], dicts["height"])
                # cv2.putText(self.__show_img, w_h_msg, (dicts["point1"][0], dicts["point1"][1] - 10), \
                #     cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
                cv2.rectangle(self.__show_img,
                              dicts["point1"], dicts["point2"], (255, 0, 0), 2)
        cv2.imshow('image', self.__show_img)

    def __get_box(self):
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('image', self.__on_mouse)
        while(1):
            self.__refresh()

            ch = 0xFF & cv2.waitKey(30)
            if ch == ord('y'):
                if len(self.area_list) <= 0:
                    self.area_list.append({"box": [0, 0, cfg.RESOLUTION[0], cfg.RESOLUTION[1]],
                                           "width": cfg.RESOLUTION[0], "height": cfg.RESOLUTION[1]})
                break
            elif ch == 27:
                self.area_list = []
                self.select_times += 1
                break
        cv2.destroyAllWindows()

    def run(self, frame):
        self.__img = frame
        self.__show_img = self.__img.copy()
        self.__get_box()
