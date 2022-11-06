from collections import namedtuple
import matplotlib.pyplot as plt
import cv2
from PIL import Image, ImageFont, ImageDraw
import numpy as np

Coords = namedtuple('Coords', ['latitude', 'longitude'])
CNN_coords = namedtuple('CNN_coords', ['class_name', 'prob', 'upper_left_coords', 'bottom_right_coords'])


def load_coords(file_name):
    with open(file_name, 'r', encoding='UTF-8') as file:
        coords_net = []
        for i, line in enumerate(file):
            if i != 0 and i < 5:
                str_ = line.rstrip()
                lon, lat = str_.split(',')
                coords_net.append(Coords(float(lat), float(lon)))

        return coords_net


def get_lat_lon_min_max_coords(coords_net):
    lat_max = max(abs(coords_net[0].latitude), abs(coords_net[1].latitude), abs(coords_net[2].latitude),
                  abs(coords_net[3].latitude))
    lat_min = min(abs(coords_net[0].latitude), abs(coords_net[1].latitude), abs(coords_net[2].latitude),
                  abs(coords_net[3].latitude))
    lon_max = max(abs(coords_net[0].longitude), abs(coords_net[1].longitude), abs(coords_net[2].longitude),
                  abs(coords_net[3].longitude))
    lon_min = min(abs(coords_net[0].longitude), abs(coords_net[1].longitude), abs(coords_net[2].longitude),
                  abs(coords_net[3].longitude))

    return lat_min, lat_max, lon_min, lon_max


def get_n_s_w_e(coords_net):
    res = []
    if coords_net[0].latitude > 0:
        res.append('N')
    else:
        res.append('S')

    if coords_net[0].longitude > 0:
        res.append('E')
    else:
        res.append('W')

    return res


def conver_grad_min_sec_to_text(coords, lat=True, n_s="N", e_w="E"):
    if lat:
        text = "{0:02d} {1:02d}'{2:02d}''{3:s}".format(coords[0], coords[1], int(coords[2]), n_s)
    else:
        text = "{0:02d} {1:02d}'{2:02d}''{3:s}".format(coords[0], coords[1], int(coords[2]), e_w)

    return text


def add_grid(image_file_name, save_name, num_of_grid_cells=None, dat_file_name=None,
             font=cv2.FONT_HERSHEY_COMPLEX,
             fontScale=None,
             fontColor=(0, 255, 255),
             thickness=None,
             lineType=2,
             grid_color=(0, 0, 0)):
    img = cv2.imread(image_file_name)

    shape = img.shape
    if not fontScale:
        fontScale = min(shape[0], shape[1]) / 1900

    if not thickness:
        thickness = int(min(shape[0], shape[1]) / 1900) + 1

    if not num_of_grid_cells:
        num_of_grid_cells = min(int(min(shape[0], shape[1]) / 250), 8)

    delta = int(max(shape) / num_of_grid_cells)

    dx, dy = delta, delta

    img[:, ::dy, :] = grid_color
    img[::dx, :, :] = grid_color

    if shape[0] > 3000:
        img[:, ::dy + 1, :] = grid_color
        img[::dx + 1, :, :] = grid_color

    if shape[0] > 8000:
        img[:, ::dy + 2, :] = grid_color
        img[::dx + 2, :, :] = grid_color

    if dat_file_name:

        coords = load_coords(dat_file_name)

        min_max = get_lat_lon_min_max_coords(coords)
        lon_start = min_max[2]
        lon_finish = min_max[3]
        delta_lon = lon_finish - lon_start
        ns = get_n_s_w_e(coords)
        grad_in_pix = delta_lon / shape[1]

        num_of_w_steps = int(shape[1] / dx)

        for st in range(num_of_w_steps + 1):
            # направление зависит от знака
            if ns[1] == 'E':
                next_lon = lon_start + grad_in_pix * delta * (st + 1)
                bottomLeftCornerOfText = [st * delta + 6, int(shape[0] / 2)]
            else:
                tail = int(shape[1] - num_of_w_steps * delta)
                start_w = shape[1] - tail

                if st == 0:
                    next_lon = lon_start + grad_in_pix * tail
                else:
                    next_lon = lon_start + grad_in_pix * delta * st
                bottomLeftCornerOfText = [start_w - st * delta + 6, int(shape[0] / 2)]

            lon_text = conver_grad_min_sec_to_text(convert_coords_to_grad_min_sec(next_lon), lat=False, e_w=ns[1])
            cv2.putText(img, lon_text,
                        bottomLeftCornerOfText,
                        font,
                        fontScale,
                        fontColor,
                        thickness,
                        lineType)

            lat_start = min_max[0]
            lat_finish = min_max[1]
            delta_lat = lat_finish - lat_start
            grad_in_pix = delta_lat / shape[0]

            num_of_h_steps = int(shape[0] / dy)
            tail = int(shape[0] - num_of_h_steps * delta)
            start_h = shape[0] - tail

            for st in range(num_of_h_steps + 1):
                if st == int(num_of_h_steps / 2):
                    continue

                if ns[0] == 'N':
                    if st == 0:
                        next_lat = lat_start + grad_in_pix * tail
                    else:
                        next_lat = lat_start + grad_in_pix * delta * st
                    bottomLeftCornerOfText = [int(shape[1] / 2) - 34, start_h - st * delta - 12]
                else:
                    next_lat = lat_start + grad_in_pix * delta * (st + 1)
                    bottomLeftCornerOfText = [int(shape[1] / 2) - 34, st * delta + 24]

                lat_text = conver_grad_min_sec_to_text(convert_coords_to_grad_min_sec(next_lat), lat=True, n_s=ns[0])
                cv2.putText(img, lat_text,
                            bottomLeftCornerOfText,
                            font,
                            fontScale,
                            fontColor,
                            thickness,
                            lineType)

    cv2.imwrite(save_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def convert_coords_to_grad_min_sec(lat_or_lon):
    grads = int(lat_or_lon)
    mins_float = (lat_or_lon - grads) * 60
    mins = int(mins_float)
    secs_float = (mins_float - mins) * 60

    return (grads, mins, secs_float)


def convert_coco_to_coords(coco_label_file, dat_file, img_file_name):
    coords_net = load_coords(dat_file)
    img = cv2.imread(img_file_name)

    shape = img.shape
    print(shape)
    img_height = shape[0]
    img_width = shape[1]

    n_s_w_e = get_n_s_w_e(coords_net)
    min_max = get_lat_lon_min_max_coords(coords_net)

    lat_start = min_max[0]
    lat_finish = min_max[1]
    delta_lat = lat_finish - lat_start
    grad_lat_in_pix = delta_lat / shape[0]

    lon_start = min_max[2]
    lon_finish = min_max[3]
    delta_lon = lon_finish - lon_start
    grad_lon_in_pix = delta_lon / shape[1]

    res = []

    with open(coco_label_file, "r") as f:
        for i, line in enumerate(f):
            str_y = line.rstrip().split(' ')
            class_name = int(str_y[1])
            prob = float(str_y[3])

            upper_left_x = float(str_y[5].rstrip())
            upper_left_y = float(str_y[6].rstrip())

            bottom_right_x = float(str_y[7].rstrip())
            bottom_right_y = float(str_y[8].rstrip())

            if n_s_w_e[0] == "N":
                ul_lat_yolo = lat_start + (img_height - upper_left_y) * grad_lat_in_pix
                br_lat_yolo = lat_start + (img_height - bottom_right_y) * grad_lat_in_pix

            else:
                ul_lat_yolo = -(lat_start + upper_left_y * grad_lat_in_pix)
                br_lat_yolo = -(lat_start + bottom_right_y * grad_lat_in_pix)

            if n_s_w_e[1] == "E":
                ul_lon_yolo = lon_start + upper_left_x * grad_lon_in_pix
                br_lon_yolo = lon_start + bottom_right_x * grad_lon_in_pix

            else:
                ul_lon_yolo = -(lon_start + (img_width - upper_left_x) * grad_lon_in_pix)
                br_lon_yolo = -(lon_start + (img_width - bottom_right_x) * grad_lon_in_pix)

            res.append(
                CNN_coords(class_name, prob, Coords(ul_lat_yolo, ul_lon_yolo), Coords(br_lat_yolo, br_lon_yolo)))

    return res


def crop_from_coords(dat_file, img_file_name, x_min, x_max, y_min, y_max, save_dat_name):
    coords_net = load_coords(dat_file)
    img = cv2.imread(img_file_name)

    shape = img.shape
    img_height = shape[0]
    img_width = shape[1]

    n_s_w_e = get_n_s_w_e(coords_net)
    min_max = get_lat_lon_min_max_coords(coords_net)

    lat_start = min_max[0]
    lat_finish = min_max[1]
    delta_lat = lat_finish - lat_start
    grad_lat_in_pix = delta_lat / shape[0]

    lon_start = min_max[2]
    lon_finish = min_max[3]
    delta_lon = lon_finish - lon_start
    grad_lon_in_pix = delta_lon / shape[1]

    res = []

    if n_s_w_e[0] == "N":
        ul_lat_yolo = lat_start + (img_height - y_min) * grad_lat_in_pix
        br_lat_yolo = lat_start + (img_height - y_max) * grad_lat_in_pix

    else:
        ul_lat_yolo = -(lat_start + y_min * grad_lat_in_pix)
        br_lat_yolo = -(lat_start + y_max * grad_lat_in_pix)

    if n_s_w_e[1] == "E":
        ul_lon_yolo = lon_start + x_min * grad_lon_in_pix
        br_lon_yolo = lon_start + x_max * grad_lon_in_pix

    else:
        ul_lon_yolo = -(lon_start + (img_width - x_min) * grad_lon_in_pix)
        br_lon_yolo = -(lon_start + (img_width - x_max) * grad_lon_in_pix)

    with open(save_dat_name, "w") as safe_f:
        safe_f.write('2\n')
        for i in range(2):
            safe_f.write('{0:f},{1:f}\n'.format(ul_lon_yolo, ul_lat_yolo))
            safe_f.write('{0:f},{1:f}\n'.format(br_lon_yolo, br_lat_yolo))

    return res


def convert_yolo_to_coords(yolo_label_file, dat_file, img_file_name):
    coords_net = load_coords(dat_file)
    img = cv2.imread(img_file_name)

    shape = img.shape
    print(shape)
    img_height = shape[0]
    img_width = shape[1]

    n_s_w_e = get_n_s_w_e(coords_net)
    min_max = get_lat_lon_min_max_coords(coords_net)

    lat_start = min_max[0]
    lat_finish = min_max[1]
    delta_lat = lat_finish - lat_start
    grad_lat_in_pix = delta_lat / shape[0]

    lon_start = min_max[2]
    lon_finish = min_max[3]
    delta_lon = lon_finish - lon_start
    grad_lon_in_pix = delta_lon / shape[1]

    res = []

    with open(yolo_label_file, "r") as f:
        for i, line in enumerate(f):
            str_y = line.rstrip().split(' ')
            class_name = int(str_y[0])
            prob = float(str_y[-1])

            box_center_x, box_center_y = float(str_y[1]), float(str_y[2])
            box_center_w, box_center_h = float(str_y[3]), float(str_y[4])

            upper_left_x = box_center_x - box_center_w / 2
            upper_left_y = box_center_y - box_center_h / 2

            bottom_right_x = box_center_x + box_center_w / 2
            bottom_right_y = box_center_y + box_center_h / 2

            if n_s_w_e[0] == "N":
                ul_lat_yolo = lat_start + (1.0 - upper_left_y) * img_height * grad_lat_in_pix
                br_lat_yolo = lat_start + (1.0 - bottom_right_y) * img_height * grad_lat_in_pix

            else:
                ul_lat_yolo = -(lat_start + upper_left_y * img_height * grad_lat_in_pix)
                br_lat_yolo = -(lat_start + bottom_right_y * img_height * grad_lat_in_pix)

            if n_s_w_e[1] == "E":
                ul_lon_yolo = lon_start + upper_left_x * img_width * grad_lon_in_pix
                br_lon_yolo = lon_start + bottom_right_x * img_width * grad_lon_in_pix

            else:
                ul_lon_yolo = -(lon_start + (1.0 - upper_left_x) * img_width * grad_lon_in_pix)
                br_lon_yolo = -(lon_start + (1.0 - bottom_right_x) * img_width * grad_lon_in_pix)

            res.append(
                CNN_coords(class_name, prob, Coords(ul_lat_yolo, ul_lon_yolo), Coords(br_lat_yolo, br_lon_yolo)))

    return res


if __name__ == "__main__":
    yolo_label_file_name = "D:\python\object_detector\pyqt_sns\detection\Mask-R-CNN-R101\labels\columbia 1.txt"
    dat_file_name = "D:\python\object_detector\pyqt_sns\\aes_imgs\\from browser\columbia 1.dat"

    img_file_name = "D:\python\object_detector\pyqt_sns\\aes_imgs\\from browser\columbia 1.jpg"

    res = convert_coco_to_coords(yolo_label_file_name, dat_file_name, img_file_name)

    print(res)

    crop_from_coords(dat_file_name, img_file_name, 10, 100, 10, 200, "res_crop.dat")
