import platform
import os
if 'Windows' in platform.system():
    # Improve OpenCV startup speed
    os.environ['OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS'] = '0'
import cv2
import sys
import numpy as np
from yolov4_cv import datadefine as df


def c_numpy(class_names, classid):
    if '3.6' in sys.version:    # check python version.
        label = np.array(class_names)[classid][0]
    else:
        label = class_names[classid]
    return label


class YOLOv4_CV:
    def __init__(self, checkpoint, cfg, input_size=(640, 640), conf=0.25, iou=0.45, draw_size=3, is_cuda=False):
        assert self.class_colors or self.class_names, 'You must inherit YOLOv5_ONNX_CV and define class_colors and class_names'
        self.input_size = input_size
        self.conf = conf
        self.iou = iou
        self.draw_size = draw_size
        self.model = self._build_model(checkpoint, cfg, input_size, is_cuda)

    def _build_model(self, checkpoint, cfg, input_size, is_cuda=False):
        net = cv2.dnn.readNetFromDarknet(cfg, checkpoint)
        if is_cuda:
            print('Attempty to use CUDA')
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
        else:
            print('Running on CPU')
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=input_size, scale=1/255, swapRB=True)
        return model

    def _detect(self, input, model):
        preds = model.detect(input, self.conf, self.iou)
        return preds

    def _draw_box(self, img, label, box, color, line_width):
        lw = line_width or max(round(sum(img.shape) / 2 * 0.003), 2)
        p1 = (int(box[0]), int(box[1]))
        p2 = (p1[0] + int(box[2]), p1[1] + int(box[3]))
        cv2.rectangle(img, p1, p2, color, thickness=lw, lineType=cv2.LINE_AA)
        tf = max(lw - 1, 1)
        w, h = cv2.getTextSize(label, 0, fontScale=lw / 3, thickness=tf)[0]
        outside = p1[1] - h >= 3
        p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
        cv2.rectangle(img, p1, p2, color, -1, cv2.LINE_AA)
        cv2.putText(img,
                    label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2),
                    0,
                    lw / 3,
                    (255, 255, 255),
                    thickness=tf,
                    lineType=cv2.LINE_AA)

    def _label_boxes(self, hide_conf):
        img = self.img
        for c_info in self.class_infos:
            color = self.class_colors[int(c_info.id) % len(self.class_colors)]
            label = c_numpy(self.class_names, c_info.id)
            if not hide_conf:
                label += f':{c_info.conf:.2f}'
            self._draw_box(img, label, c_info.box, color, self.draw_size)
        return img

    def _wrap_detection(self, outputs):
        result = []
        ids, confs, boxes = outputs
        for id, conf, box in zip(ids, confs, boxes):
            result.append(df.ClassInfo(id=id, name=c_numpy(self.class_names, id), conf=conf, box=box))
        return result

    def show_label_boxes(self, hide_conf=True):
        img = self._label_boxes(hide_conf)
        cv2.namedWindow('show_boxes', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
        cv2.imshow('show_boxes', img)

    def get_label_boxes_image(self, hide_conf=True):
        return self._label_boxes(hide_conf)

    def __call__(self, input):
        self.img = input.copy()
        outputs = self._detect(self.img, self.model)
        self.class_infos = self._wrap_detection(outputs)
        return self.class_infos