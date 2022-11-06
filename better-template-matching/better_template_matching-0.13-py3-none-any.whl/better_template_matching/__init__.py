import os
import pathlib
import random
import re
import shutil
import webbrowser
from multiprocessing import Pool
from tempfile import TemporaryDirectory
from threading import Lock
from time import sleep, strftime
from typing import Union
import keyboard
import kthread
import numpy as np
import regex
import requests
import ujson
from a_pandas_ex_less_memory_more_speed import pd_add_less_memory_more_speed
from skimage.feature import match_template
import cv2
import pandas as pd
import glob
from flatten_everything import flatten_everything
from a_cv2_imshow_thread import add_imshow_thread_to_cv2
from windows_adb_screen_capture import ScreenShots
from collections import defaultdict

nested_dict = lambda: defaultdict(nested_dict)
from a_pandas_ex_plode_tool import pd_add_explode_tools
from a_pandas_ex_intersection_difference import pd_add_set

add_imshow_thread_to_cv2()
pd_add_set()
pd_add_explode_tools()
pd_add_less_memory_more_speed()


def use_black_and_white_pictures(img):
    if img.shape[-1] == 4:
        return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def intersects(box1, box2):
    return not (
        box1[2] < box2[0] or box1[0] > box2[2] or box1[1] > box2[3] or box1[3] < box2[1]
    )


def open_image_in_cv(image, channels_in_output=None):
    if isinstance(image, str):
        if os.path.exists(image):
            if os.path.isfile(image):
                image = cv2.imread(image, cv2.IMREAD_UNCHANGED)
        elif re.search(r"^.{1,10}://", str(image)) is not None:
            x = requests.get(image).content
            image = cv2.imdecode(np.frombuffer(x, np.uint8), cv2.IMREAD_COLOR)
        else:
            image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    elif "PIL" in str(type(image)):
        image = np.array(image)
    else:
        if image.dtype != np.uint8:
            image = image.astype(np.uint8)

    if channels_in_output is not None:
        if image.shape[-1] == 4 and channels_in_output == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        elif image.shape[-1] == 3 and channels_in_output == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        else:
            pass
    return image


def apply_matching_template(haystack: np.ndarray, needle: np.ndarray):
    reas = match_template(haystack, needle)
    return reas


def cropimage(img, coords):
    if sum(coords) == 0:
        return img
    return img[coords[1] : coords[3], coords[0] : coords[2]].copy()


def _findpics(liste):
    key, key2, x0, y0, x1, y1, haystack, needle = liste
    allresas = []

    try:
        allresas = apply_matching_template(haystack, needle)
    except Exception:
        pass
    return [key, key2, x0, y0, x1, y1, haystack, needle, allresas]


def find_pics(liste, workers=1):
    groupedresults = []
    if workers == 1:
        for coi in liste:
            groupedresults.append(_findpics(coi))
        groupedresults = [groupedresults]
    else:
        with Pool(workers) as p:
            groupedresults.append(p.map(_findpics, liste).copy())
    return groupedresults[0]


def resize_image(img, scale_percent=100, interpolation=cv2.INTER_AREA):
    width = int(img.shape[1] / 100 * scale_percent)
    height = int(img.shape[0] / 100 * scale_percent)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=interpolation)
    return resized


regex_compiled = regex.compile(
    r"[\\/]+[^\\/]*--(\d+)x(\d+)--(\d+)x(\d+)", flags=regex.IGNORECASE
)


def get_enumerated_file_path(folder, leading_zeros=8, ending=".png"):
    counter = 0
    if not os.path.exists(folder):
        os.makedirs(folder)
    newfilepath = os.path.join(folder, str(counter).zfill(leading_zeros) + ending)
    while os.path.exists(newfilepath):
        counter += 1
        newfilepath = os.path.join(folder, str(counter).zfill(leading_zeros) + ending)
    return newfilepath


def start_annotation_tool():
    dirname = os.path.join(os.path.abspath(os.path.dirname(__file__)))
    annotationtoolfiles = [
        x
        for x in [
            "canvas.min.js",
            "filesaver.min.js",
            "jszip.min.js",
            "ybat.css",
            "ybat.html",
            "ybat.js",
        ]
        if os.path.exists(os.path.join(dirname, x))
    ]
    if len(annotationtoolfiles) == 6:
        main_path_stringuri = pathlib.Path(os.path.join(dirname, "ybat.html")).as_uri()
        webbrowser.open(main_path_stringuri)
        print(
            "The annotation tool requires a class list like:\n\n\nclasses.txt\n\nbutton1\nbutton2\ntextfield1\ntextfield2"
        )
        print(
            "\n\nClick on: Save COCO when you are done and copy the file name of the generated file"
        )
    else:
        print(
            f"The annotation tool could not be found! Download it here:\nhttps://github.com/drainingsun/ybat\n\nPut it the folder of this module:\n{dirname}"
        )
    print(dirname)


def create_needle_images_from_annotations(
    cocojson,
    savefolder,
    outputfolder,
    expand_x_negative=200,
    expand_x_positive=200,
    expand_y_negative=200,
    expand_y_positive=200,
):
    r"""

    create_needle_images_from_annotations(
    cocojson=r"C:\Users\Gamer\Documents\Downloads\bboxes_coco (3).zip",
    savefolder=r'C:\testannonaton',
    outputfolder=r'C:\sadfafdxc22',
    expand_x_negative=200,
    expand_x_positive=200,
    expand_y_negative=200,
    expand_y_positive=200,
)
    """
    if cocojson.lower().endswith(".zip"):
        tempdict_ = TemporaryDirectory()
        shutil.unpack_archive(cocojson, tempdict_.name)
        cocojson = os.path.join(tempdict_.name, "coco.json")
    # r"C:\Users\Gamer\Documents\Downloads\bboxes_coco\coco.json"

    if not os.path.exists(outputfolder):
        os.makedirs(outputfolder)
    outputfolder_cropped = os.path.join(outputfolder, "cropped_view")
    if not os.path.exists(outputfolder_cropped):
        os.makedirs(outputfolder_cropped)
    outputfolder_screen = os.path.join(outputfolder, "screen_view")
    if not os.path.exists(outputfolder_screen):
        os.makedirs(outputfolder_screen)

    with open(cocojson, encoding="utf-8") as f:
        jsonfile = ujson.loads(f.read())
    df = pd.DataFrame(jsonfile["annotations"])
    df = pd.concat(
        [
            df,
            df.bbox.s_explode_lists_and_tuples().rename(
                columns={
                    "bbox_0": "start_x",
                    "bbox_1": "start_y",
                    "bbox_2": "needle_width",
                    "bbox_3": "needle_height",
                }
            ),
        ],
        axis=1,
    )
    df = df.drop(columns=["start_x", "start_y"])

    df = pd.concat(
        [
            df,
            df.segmentation.s_explode_lists_and_tuples().rename(
                columns={
                    "segmentation_0": "x0",
                    "segmentation_1": "y0",
                    "segmentation_2": "x1",
                    "segmentation_3": "y1",
                    "segmentation_4": "x2",
                    "segmentation_5": "y2",
                    "segmentation_6": "x3",
                    "segmentation_7": "y3",
                }
            ),
        ],
        axis=1,
    )
    dfkat = pd.DataFrame(jsonfile["categories"])
    dfim = pd.DataFrame(jsonfile["images"]).rename(columns={"id": "image_id"})
    dfim["file_path"] = dfim.file_name.apply(lambda x: os.path.join(savefolder, x))
    dfim["numpy_img"] = dfim.file_path.apply(
        lambda x: cv2.imread(x, cv2.IMREAD_UNCHANGED)
    )
    df = df.d_merge_multiple_dfs_and_series_on_one_column(
        [dfkat], "id"
    ).d_merge_multiple_dfs_and_series_on_one_column([dfim], "image_id")
    df["percent_difference_haystack_needle"] = 100 / df.width * df.needle_width
    df["needle_start_x"] = df.x0
    df["needle_start_y"] = df.y0
    df["needle_end_x"] = df.x2
    df["needle_end_y"] = df.y2

    df["needle_start_searching_x"] = df.x0 - expand_x_negative
    df["needle_start_searching_y"] = df.y0 - expand_y_negative
    df["needle_end_searching_x"] = df.x2 + expand_x_positive
    df["needle_end_searching_y"] = df.y2 + expand_y_positive
    columnssearch = [
        "needle_start_searching_x",
        "needle_start_searching_y",
        "needle_end_searching_x",
        "needle_end_searching_y",
    ]
    for col in columnssearch:
        df.loc[df[col] < 0, col] = 0
        if col == "needle_end_searching_x":
            df.loc[df[col] > df["width"], col] = df["width"].iloc[0]
        if col == "needle_end_searching_y":
            df.loc[df[col] > df["height"], col] = df["height"].iloc[0]
    for key, item in df.iterrows():
        file_ = f'{item["name"]}--{item.needle_start_searching_x}x{item.needle_start_searching_y}--{item.needle_end_searching_x}x{item.needle_end_searching_y}.png'
        outputpath = os.path.join(outputfolder, file_)
        print(outputpath)
        resultpic = cropimage(
            item.numpy_img.copy(),
            coords=(
                item.needle_start_x,
                item.needle_start_y,
                item.needle_end_x,
                item.needle_end_y,
            ),
        )
        cv2.imwrite(outputpath, resultpic)
        resultpiccropped = cropimage(
            item.numpy_img.copy(),
            coords=(
                item.needle_start_searching_x,
                item.needle_start_searching_y,
                item.needle_end_searching_x,
                item.needle_end_searching_y,
            ),
        )
        cv2.imwrite(os.path.join(outputfolder_cropped, file_), resultpiccropped)
        cv2.imwrite(os.path.join(outputfolder_screen, file_), item.numpy_img)
    return df


def switch_red_blue(img):
    if img.shape[1] == 4:
        image1 = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    else:
        image1 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return image1


timest = lambda: strftime("%Y_%m_%d_%H_%M_%S")


class PatternMatchingOnScreen:
    def __init__(self, needle_folder=None, scale_percent=50, debug_folder=None):
        self.scale_percent = scale_percent
        self.scale_percentvice = 100 / scale_percent
        self.sc = None  # = ScreenShots()
        self.monitor = None
        self.adb_path = None
        self.adb_serial = None
        self.hwnd = None
        self.needle_images = nested_dict()
        self.needle_folder = None
        if needle_folder is not None:
            self.needle_folder = (
                regex.sub(r"[\\/]*\s*$", "", needle_folder) + os.sep + "*.png"
            )
        self.image_original = None
        self.groupedresults = []
        self.df = pd.DataFrame()
        self.resize_interpolation = cv2.INTER_AREA
        self.untouchedimage = None
        self.untouchedimage_drawn = None
        self.cropped_haystack_images = []
        self.all_results_dataframes = []
        self.df_filtered_results_dataframes = pd.DataFrame()
        self.df = pd.DataFrame()
        self.debug_folder = debug_folder
        if self.debug_folder is not None:
            if not os.path.exists(self.debug_folder):
                os.makedirs(self.debug_folder)
        self.allres = None
        self.lock = Lock()
        self.show_results_thread = None
        self.show_results_video_thread = None

    def reconfigure_scale_size(
        self, scale_percent, substract_zoom_percent=10, add_zoom_percent=10
    ):
        self.scale_percent = scale_percent
        self.scale_percentvice = 100 / scale_percent
        self.get_needle_images(
            substract_zoom_percent=substract_zoom_percent,
            add_zoom_percent=add_zoom_percent,
        )
        return self

    def get_needle_images(self, substract_zoom_percent=10, add_zoom_percent=10):
        needletemp = {
            x: {
                "original_image": (open_image_in_cv(x, channels_in_output=3)),
                "crop_original_image": [
                    int(__) for __ in flatten_everything([regex_compiled.findall(x)])
                ],
            }
            for x in glob.glob(self.needle_folder)
        }
        counter = 0
        for needlet in needletemp.items():
            for durchg in range(
                int(
                    self.scale_percent
                    - self.scale_percent / 100 * substract_zoom_percent
                ),
                int(self.scale_percent + self.scale_percent / 100 * add_zoom_percent),
                1,
            ):
                self.needle_images[needlet[0]][durchg]["image"] = resize_image(
                    needlet[1]["original_image"], scale_percent=durchg
                )
                self.needle_images[needlet[0]][durchg]["cropped_coords"] = [
                    int(x / 100 * durchg) for x in needlet[1]["crop_original_image"]
                ]
                self.needle_images[needlet[0]][durchg][
                    "imagebw"
                ] = use_black_and_white_pictures(
                    resize_image(needlet[1]["original_image"], scale_percent=durchg)
                )

                if self.debug_folder is not None:
                    cv2.imwrite(
                        os.path.join(
                            self.debug_folder, fr"{durchg}{counter}_color.png"
                        ),
                        self.needle_images[needlet[0]][durchg]["image"],
                    )
                    cv2.imwrite(
                        os.path.join(self.debug_folder, fr"{durchg}{counter}_bw.png"),
                        self.needle_images[needlet[0]][durchg]["imagebw"],
                    )

                    # cropcoords = ([int(x / 100 * durchg) for x in needlet[1]["crop_original_image"]])
                    cropcoords = [
                        int(x / self.scale_percentvice)
                        for x in needlet[1]["crop_original_image"]
                    ]

                    croppedim = cropimage(self.image_original, cropcoords)
                    cv2.imwrite(
                        os.path.join(
                            self.debug_folder, f"{durchg}{counter}_cropped.png"
                        ),
                        croppedim,
                    )
                    counter += 1
        return self

    def configure_monitor(self, monitor=1):
        self.sc = ScreenShots()
        self.monitor = monitor
        self.sc.choose_monitor_for_screenshot(monitor)
        return self

    def configure_adb(
        self, adb_path=r"C:\ProgramData\adb\adb.exe", adb_serial="localhost:5555"
    ):
        self.adb_path = adb_path
        self.adb_serial = adb_serial
        self.sc = ScreenShots(hwnd=None, adb_path=adb_path, adb_serial=adb_serial)
        return self

    def configure_window(self, regular_expression=None, hwnd=None):
        self.sc = ScreenShots(hwnd=hwnd)
        if hwnd is None and regular_expression is not None:
            self.sc.find_window_with_regex(regular_expression)
        self.hwnd = self.sc.hwnd
        return self

    def get_screenshot(
        self, interpolation=cv2.INTER_AREA, grayscale=True, save_in_folder=None
    ):
        if self.adb_path is not None and self.adb_serial is not None:
            self.image_original = self.sc.imget_adb().copy()
        elif self.hwnd is not None:

            self.image_original = self.sc.imget_hwnd().copy()
        elif self.monitor is not None:
            self.image_original = self.sc.imget_monitor().copy()
        self.image_original = open_image_in_cv(
            self.image_original, channels_in_output=3
        )
        self.untouchedimage = self.image_original.copy()
        if self.scale_percent != 100:
            self.image_original = resize_image(
                self.image_original,
                scale_percent=self.scale_percent,
                interpolation=interpolation,
            )
        if grayscale:
            self.image_original = use_black_and_white_pictures(
                open_image_in_cv(self.image_original, channels_in_output=3)
            )
        if save_in_folder is not None:
            untouchedimage = get_enumerated_file_path(
                save_in_folder, leading_zeros=8, ending=".png"
            )
            cv2.imwrite(untouchedimage, self.untouchedimage)

        return self

    def get_croped_image_coords(self, grayscale=True):
        counter = 0
        allcheck = []
        for key, item in self.needle_images.items():
            for key2, item2 in item.items():
                cropcoords = item2["cropped_coords"]
                croppedim = cropimage(self.image_original, cropcoords)
                if self.debug_folder is not None:

                    cv2.imwrite(
                        os.path.join(
                            self.debug_folder, f"{counter}{key2}_cropimage.png"
                        ),
                        croppedim,
                    )
                    counter += 1
                if grayscale:
                    allcheck.append(
                        (key, key2, *cropcoords, croppedim, (item2["imagebw"]))
                    )
                else:
                    # allcheck.append((key, key2, *cropcoords, croppedim, (item2["image"])))
                    allcheck.append(
                        (key, key2, *cropcoords, croppedim, (item2["image"]),)
                    )

        self.cropped_haystack_images = allcheck.copy()
        return self

    def template_matching_to_dataframe(self, grayscale=True, workers=3):
        allres = find_pics(self.cropped_haystack_images, workers=workers)
        self.allres = allres.copy()
        if grayscale:
            alldataframes = [
                (
                    pd.DataFrame(x[-1]).assign(
                        aa_filepath=x[0],
                        aa_zoomfactor=x[1],
                        aa_crop_x0=x[2],
                        aa_crop_y0=x[3],
                        aa_crop_x1=x[4],
                        aa_crop_y1=x[5],
                        aa_cropped_haystack_x=x[6].shape[1],
                        aa_cropped_haystack_y=x[6].shape[0],
                        aa_cropped_needle_x=x[7].shape[1],
                        aa_cropped_needle_y=x[7].shape[0],
                    ),
                    pd.DataFrame(x[-1]),
                )
                for x in allres
                if np.any(x[-1])
            ]
        else:
            alldataframes = [
                (
                    pd.DataFrame(np.squeeze(x[-1])).assign(
                        aa_filepath=x[0],
                        aa_zoomfactor=x[1],
                        aa_crop_x0=x[2],
                        aa_crop_y0=x[3],
                        aa_crop_x1=x[4],
                        aa_crop_y1=x[5],
                        aa_cropped_haystack_x=x[6].shape[1],
                        aa_cropped_haystack_y=x[6].shape[0],
                        aa_cropped_needle_x=x[7].shape[1],
                        aa_cropped_needle_y=x[7].shape[0],
                    ),
                    pd.DataFrame(np.squeeze(x[-1])),
                )
                for x in self.allres
                if np.any(x[-1])
            ]
        self.all_results_dataframes = alldataframes.copy()
        return self

    def sort_result_dfs(self):
        gefundenebilder = []
        for dffull, df in self.all_results_dataframes:
            yaxis = df[df.max().sort_values().index[-1]]
            ywert = yaxis.max()
            y_koordinate = yaxis.name
            xaxis = df.loc[
                (df[y_koordinate] <= ywert) & (df[y_koordinate] >= ywert - (ywert / 10))
            ]
            x_koordinate = xaxis.index[0]
            df.at[x_koordinate, y_koordinate] = -100
            x_koordinate, y_koordinate = y_koordinate, x_koordinate
            dfnew = (
                dffull.loc[xaxis.index][
                    [
                        "aa_filepath",
                        "aa_zoomfactor",
                        "aa_crop_x0",
                        "aa_crop_y0",
                        "aa_crop_x1",
                        "aa_crop_y1",
                        "aa_cropped_haystack_x",
                        "aa_cropped_haystack_y",
                        "aa_cropped_needle_x",
                        "aa_cropped_needle_y",
                    ]
                ].assign(aa_x=x_koordinate, aa_y=y_koordinate, aa_conf=ywert)
            ).copy()
            gefundenebilder.append(dfnew)
        self.df_filtered_results_dataframes = pd.concat(
            gefundenebilder, ignore_index=True
        )
        return self

    def filter_duplicated_results(self, thresh=0.6):
        allresultsx = []
        for name, dfx in self.df_filtered_results_dataframes.groupby(["aa_filepath"]):

            dfx = dfx.loc[dfx.aa_conf > thresh]
            if dfx.empty:
                continue
            df = (dfx.sort_values(by="aa_conf", ascending=False)).copy()
            df["aa_real_x_start"] = df.aa_crop_x0 + df.aa_x
            df["aa_real_x_start"] = df["aa_real_x_start"] * self.scale_percentvice

            df["aa_real_y_start"] = df.aa_crop_y0 + df.aa_y
            df["aa_real_y_start"] = df["aa_real_y_start"] * self.scale_percentvice
            df["aa_real_y_start"] = df["aa_real_y_start"].astype(np.uint32)
            df["aa_real_x_start"] = df["aa_real_x_start"].astype(np.uint32)
            df["aa_width"] = df["aa_cropped_needle_x"] * self.scale_percentvice
            df["aa_height"] = +df["aa_cropped_needle_y"] * self.scale_percentvice
            df["aa_real_y_end"] = df["aa_real_y_start"] + df["aa_height"]
            df["aa_real_x_end"] = df["aa_real_x_start"] + df["aa_width"]
            # allresultsx2.append(df.copy())
            # allresultsx.append(df.copy())
            while not df.empty:
                box1 = (
                    df.aa_real_x_start.iloc[0],
                    df.aa_real_y_start.iloc[0],
                    df.aa_real_x_end.iloc[0],
                    df.aa_real_y_end.iloc[0],
                )
                df["aa_intersects"] = df.apply(
                    lambda x: intersects(
                        box1,
                        box2=(
                            x.aa_real_x_start,
                            x.aa_real_y_start,
                            x.aa_real_x_end,
                            x.aa_real_y_end,
                        ),
                    ),
                    axis=1,
                )
                allresultsx.append(df[:1].copy())

                df = df.loc[df.aa_intersects == False].copy()

        try:
            df = (
                pd.concat(allresultsx)
                .reset_index(drop=True)
                .sort_values(by="aa_conf", ascending=False)
            )
            df["aa_pure_filename"] = df.aa_filepath.apply(lambda x: x.split(os.sep)[-1])

            self.df = df.copy()
            # from a_pandas_ex_less_memory_more_speed import pd_add_less_memory_more_speed
            self.df = self.df.reset_index(drop=True)
            self.df[
                "aa_same_zoom_factor"
            ] = self.df.aa_zoomfactor.ds_value_counts_to_column()
            self.df = self.df.sort_values(
                by=["aa_same_zoom_factor", "aa_conf"], ascending=[False, False]
            )
            self.df = self.df.ds_reduce_memory_size(verbose=False)
        except Exception as fe:
            print(
                f"Error: {fe} if none of the needle images is on the screen, you can ignore it! {timest()}".replace(
                    "\n", " "
                ).replace(
                    "\r", " "
                ),
                end="\r",
            )

            allcols = [
                "aa_filepath",
                "aa_zoomfactor",
                "aa_crop_x0",
                "aa_crop_y0",
                "aa_crop_x1",
                "aa_crop_y1",
                "aa_cropped_haystack_x",
                "aa_cropped_haystack_y",
                "aa_cropped_needle_x",
                "aa_cropped_needle_y",
                "aa_x",
                "aa_y",
                "aa_conf",
                "aa_real_x_start",
                "aa_real_y_start",
                "aa_width",
                "aa_height",
                "aa_real_y_end",
                "aa_real_x_end",
                "aa_intersects",
                "aa_pure_filename",
                "aa_same_zoom_factor",
            ]
            self.df = pd.DataFrame(columns=allcols)
        return self

    def draw_results(self):
        image = self.untouchedimage.copy()
        try:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        except Exception:
            pass
        fontdistance1 = -10
        for key, item in self.df.iterrows():
            try:
                x_1_match0 = int(item.aa_real_x_start)
                y_1_match0 = int(item.aa_real_y_start)
                height_haystack0 = int(item.aa_real_y_end)
                width_haystack0 = int(item.aa_real_x_end)
                r_, g_, b_ = (
                    random.randrange(50, 255),
                    random.randrange(50, 255),
                    random.randrange(50, 255),
                )
                image = cv2.rectangle(
                    image,
                    (x_1_match0, y_1_match0),
                    (width_haystack0, height_haystack0),
                    color=(0, 0, 0),
                    thickness=item.aa_same_zoom_factor * 2,
                )
                image = cv2.rectangle(
                    image,
                    (x_1_match0, y_1_match0),
                    (width_haystack0, height_haystack0),
                    color=(r_, g_, b_),
                    thickness=item.aa_same_zoom_factor,
                )
                image = cv2.putText(
                    image,
                    str(item.aa_conf),
                    (x_1_match0, y_1_match0 - fontdistance1),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (0, 0, 0),
                    3,
                )
                image = cv2.putText(
                    image,
                    str(item.aa_conf),
                    (x_1_match0, y_1_match0 - fontdistance1),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (r_, g_, b_),
                    1,
                )

                item.aa_pure_filename
                image = cv2.putText(
                    image,
                    str(item.aa_pure_filename),
                    (x_1_match0, y_1_match0 - fontdistance1 * 4),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (0, 0, 0),
                    3,
                )
                image = cv2.putText(
                    image,
                    str(item.aa_pure_filename),
                    (x_1_match0, y_1_match0 - fontdistance1 * 4),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (r_, g_, b_),
                    1,
                )
            except Exception as fe:
                self.untouchedimage_drawn = image.copy()
                pass
        self.untouchedimage_drawn = image.copy()
        return image

    def get_detection_results_as_df(self):
        return self.df

    def get_screenshot_and_start_detection(
        self,
        grayscale=True,
        interpolation=cv2.INTER_AREA,
        thresh=0.6,
        save_screenshot_in_folder=None,
        workers=3,
        show_results=False,
        sleep_time_for_results=0.1,
        quit_key_for_results="q",
    ):
        if show_results:
            self.lock.acquire()
        try:
            self.get_screenshot(
                interpolation=interpolation,
                grayscale=grayscale,
                save_in_folder=save_screenshot_in_folder,
            )
            self.get_croped_image_coords(grayscale=grayscale)
            self.template_matching_to_dataframe(grayscale=grayscale, workers=workers)
            # alldataframes=self.all_results_dataframes.copy()
            self.sort_result_dfs()
            self.filter_duplicated_results(thresh=thresh)
        except Exception as da:
            print(
                f"Error: {da} if none of the needle images is on the screen, you can ignore it! {timest()}".replace(
                    "\n", " "
                ).replace(
                    "\r", " "
                ),
                end="\r",
            )
            allcols = [
                "aa_filepath",
                "aa_zoomfactor",
                "aa_crop_x0",
                "aa_crop_y0",
                "aa_crop_x1",
                "aa_crop_y1",
                "aa_cropped_haystack_x",
                "aa_cropped_haystack_y",
                "aa_cropped_needle_x",
                "aa_cropped_needle_y",
                "aa_x",
                "aa_y",
                "aa_conf",
                "aa_real_x_start",
                "aa_real_y_start",
                "aa_width",
                "aa_height",
                "aa_real_y_end",
                "aa_real_x_end",
                "aa_intersects",
                "aa_pure_filename",
                "aa_same_zoom_factor",
            ]
            self.df = pd.DataFrame(columns=allcols)
        if show_results:
            self.lock.release()
            if self.show_results_thread is None:
                self.show_results_thread = kthread.KThread(
                    target=self._show_results,
                    name="results",
                    args=(quit_key_for_results, sleep_time_for_results),
                )
                self.show_results_thread.start()
            elif not self.show_results_thread.is_alive():
                self.show_results_thread = kthread.KThread(
                    target=self._show_results,
                    name="results",
                    args=(quit_key_for_results, sleep_time_for_results),
                )
        return self

    def save_screenshots_for_creating_needle_images(self, folder, hotkey="ctrl+alt+p"):
        def get_screenshot():
            self.get_screenshot(
                interpolation=cv2.INTER_AREA, grayscale=False, save_in_folder=folder,
            )
            print("Screenshot saved")

        keyboard.add_hotkey(hotkey, get_screenshot)
        return self

    def _show_results(
        self, quit_key="q", sleep_time: Union[float, int] = 0.05,
    ):
        def activate_stop():
            nonlocal stop
            stop = True

        stop = False
        keyboard.add_hotkey(quit_key, activate_stop)
        cv2.destroyAllWindows()
        sleep(1)
        while not stop:
            screenshot_window = self.draw_results()
            if cv2.waitKey(1) & 0xFF == ord(quit_key):
                cv2.waitKey(0)

            cv2.imshow("", screenshot_window)
            sleep(sleep_time)
        keyboard.remove_all_hotkeys()
        return self

    def _show_results_as_video(
        self,
        grayscale=True,
        interpolation=cv2.INTER_AREA,
        thresh=0.8,
        workers=3,
        quit_key="q",
        sleep_time: Union[float, int] = 0.05,
    ):
        def activate_stop():
            nonlocal stop
            stop = True

        stop = False
        keyboard.add_hotkey(quit_key, activate_stop)
        cv2.destroyAllWindows()
        sleep(1)
        while not stop:
            self.get_screenshot_and_start_detection(
                grayscale=grayscale,
                interpolation=interpolation,
                thresh=thresh,
                show_results=True,
                workers=workers,
                sleep_time_for_results=sleep_time,
                quit_key_for_results=quit_key,
            )
            sleep(sleep_time)
        keyboard.remove_all_hotkeys()

    def show_results_as_video(
        self,
        grayscale=True,
        interpolation=cv2.INTER_AREA,
        thresh=0.8,
        workers=3,
        quit_key="q",
        sleep_time: Union[float, int] = 0.05,
    ):
        self.show_results_video_thread = kthread.KThread(
            target=self._show_results_as_video,
            name="videothread",
            args=(grayscale, interpolation, thresh, workers, quit_key, sleep_time,),
        )
        self.show_results_video_thread.start()


if __name__ == "__main__":
    # Let's say to want to automate Bluestacks, and
    # therefore, need to detect different icons (needles) on your screen (haystack).

    # https://github.com/hansalemaos/screenshots/raw/main/templatematching1.png

    # Create an instance
    template_matching = PatternMatchingOnScreen(
        scale_percent=25, needle_folder=None, debug_folder=None,
    )
    # Choose a screenshot method to take the screenshot

    # configure_window gets screenshots from a specific window, works also for background windows
    template_matching.configure_window(
        regular_expression=r"[bB]lue[sS]tacks.*", hwnd=None
    )

    # configure_monitor takes screenshots of the whole screen
    template_matching.configure_monitor(monitor=1)

    # If you are using bluestacks or an Android Phone, you can also connect over adb
    template_matching.configure_adb(
        adb_path=r"C:\ProgramData\adb\adb.exe", adb_serial="localhost:5735"
    )

    # Use save_screenshots_for_creating_needle_images to save screenshots on your HDD each time you press the hotkey
    # (This step can also be done with any other screenshot tool)
    template_matching.save_screenshots_for_creating_needle_images(
        folder="c:\\templatemat", hotkey="ctrl+alt+p"
    )

    # After you are done, start the annotation tool (https://github.com/drainingsun/ybat) to crop the icons quickly.
    # the requested class file (ybat) should look like this. It can be saved as txt

    """
    playstore_icon
    gamecenter_icon
    systemapps_icon
    roblox_icon
    bluestacks_x_icon
    spiele_und_gewinne_icon
    kamera_icon
    einstellungen_icon
    chrome_icon
    media_manager_icon
    """
    # The files of the tool are included in this module.
    # If you encounter any problem, download the ybat files and put them in the folder of this module
    # After you are done, click on "Save COCO", and copy the link of the zipfile
    # (This step can also be done with any other tool, e.g., Photoshop)
    #
    # https://github.com/hansalemaos/screenshots/raw/main/templatematching2.png
    # https://github.com/hansalemaos/screenshots/blob/main/templatematching3.png

    start_annotation_tool()

    # After you are done, use this function to format the screenshots
    create_needle_images_from_annotations(
        cocojson=r"C:\Users\Gamer\Documents\Downloads\bboxes_coco.zip",  # generated file by ybat
        savefolder=r"C:\screenshots_for_detection",
        # The folder where the screenshots you took are located, In my case:"c:\\templatemat"
        outputfolder=r"C:\detectiontest",  # Folder to save the results, that means the needle images you are going to use.
        expand_x_negative=200,  # you can limit the search region on the screen - saves time and false positives
        expand_x_positive=200,
        expand_y_negative=200,
        expand_y_positive=200,
    )

    # After completing this step,
    # you should have something like this in your output folder:
    # https://github.com/hansalemaos/screenshots/raw/main/templatematching4.png
    # (The 2 additional folders in the output folder can be deleted, they are for debugging)

    # If you want to change the search region for a picture, you only have to change the file name:

    # Here is one example:
    # C:\detectiontest\playstore_icon--0x0--200x300.png
    # The region (0,0), (200,300) will be checked for the image C:\detectiontest\playstore_icon--0x0--200x300.png

    # if we rename the file to
    # C:\detectiontest\playstore_icon--0x0--500x600.png
    # the region will change to (0,0), (500,600)
    # You can rename the file, but don't change the format (NAME)--(XCOORD)x(YCOORD)--(XCOORD)x(YCOORD).png
    #

    r"""
    Some examples of file names
    C:\detectiontest\playstore_icon--0x0--478x451.png
    C:\detectiontest\gamecenter_icon--244x0--781x451.png
    C:\detectiontest\systemapps_icon--528x0--1067x448.png
    C:\detectiontest\roblox_icon--833x0--1342x448.png
    C:\detectiontest\bluestacks_x_icon--1101x0--1643x449.png
    C:\detectiontest\spiele_und_gewinne_icon--1347x0--1920x452.png
    C:\detectiontest\kamera_icon--426x203--931x738.png
    C:\detectiontest\einstellungen_icon--537x200--1038x735.png
    C:\detectiontest\chrome_icon--643x199--1140x734.png
    C:\detectiontest\media_manager_icon--744x194--1250x738.png
    """

    # The needle images have been created, so let's start from the beginning
    # scale_percent is not important when creating the needle images,
    # but it is for detection. The smaller the picture is, the faster
    # is the detection, but the detection is usually not as good as with high resolution.
    #
    # You don't have to worry about resizing the output results when using scale_percent,
    # The correct coordinates will be automatically calculated
    # after the detection is done.

    template_matching = (
        PatternMatchingOnScreen(
            scale_percent=25, needle_folder=r"C:\detectiontest", debug_folder=None,
        )
        # .configure_window(regular_expression=rr"[bB]lue[sS]tacks.*", hwnd=None)
        # .configure_adb(adb_path=r"C:\ProgramData\adb\adb.exe", adb_serial="localhost:5735")
        .configure_monitor(monitor=1)
    )

    # Let's read the needle images that we have just created
    # substract_zoom_percent and add_zoom_percent are important to detect different sizes.
    # If you have a needle image with a size 100x100
    # and pass substract_zoom_percent=3, add_zoom_percent=3
    # the module will try to detect images with the size of:
    # 97x97, 98x98, 99x99, 100x100, 101x101, 102x102, 103x103
    # if you want all of needle images smaller than the original images, you could pass:
    # get_needle_images(substract_zoom_percent=6, add_zoom_percent=-3)
    # which will check for needle images with the 94-97% of the size of
    # the original image
    template_matching.get_needle_images(substract_zoom_percent=3, add_zoom_percent=3)

    # Lets get the results - grayscale=True is a lot faster, use it whenever you can.
    # You can use multiple processors (workers) for the detection
    # If you get an error (e.g., freeze_support), make sure you follow the multiprocessing guidelines:
    # https://docs.python.org/3/library/multiprocessing.html
    # if __name__ == '__main__': must be in your code when using multiprocessing (Windows)

    df = template_matching.get_screenshot_and_start_detection(
        grayscale=True,
        interpolation=cv2.INTER_AREA,
        thresh=0.8,
        save_screenshot_in_folder=None,
        workers=3,
        show_results=False,
        sleep_time_for_results=0.1,
        quit_key_for_results="q",
    ).get_detection_results_as_df()

    r"""
        The coords/height/width have been automatically ajusted to the original size of the screenshot 
    
                                                              aa_filepath  aa_zoomfactor  aa_crop_x0  aa_crop_y0  aa_crop_x1  aa_crop_y1  aa_cropped_haystack_x  aa_cropped_haystack_y  aa_cropped_needle_x  aa_cropped_needle_y  aa_x  aa_y   aa_conf  aa_real_x_start  aa_real_y_start  aa_width  aa_height  aa_real_y_end  aa_real_x_end  aa_intersects                               aa_pure_filename  aa_same_zoom_factor
    0               C:\detectiontest\roblox_icon--833x0--1342x448.png             22         183           0         295          98                    112                     98                   23                   32    33    23  0.990465              864               92        92        128            220            956           True               roblox_icon--833x0--1342x448.png                   10
    1        C:\detectiontest\bluestacks_x_icon--1101x0--1643x449.png             22         242           0         361          98                    119                     98                   31                   36    32    19  0.981858             1096               76       124        144            220           1220           True        bluestacks_x_icon--1101x0--1643x449.png                   10
    2  C:\detectiontest\spiele_und_gewinne_icon--1347x0--1920x452.png             22         296           0         422          99                    105                     99                   49                   36    32    19  0.975440             1312               76       196        144            220           1508           True  spiele_und_gewinne_icon--1347x0--1920x452.png                   10
    3             C:\detectiontest\chrome_icon--643x199--1140x734.png             22         141          43         250         161                    109                    118                   21                   29    34    44  0.967109              700              348        84        116            464            784           True             chrome_icon--643x199--1140x734.png                   10
    4      C:\detectiontest\media_manager_icon--744x194--1250x738.png             22         163          42         275         162                    112                    120                   23                   31    34    44  0.966091              788              344        92        124            468            880           True      media_manager_icon--744x194--1250x738.png                   10
    5               C:\detectiontest\playstore_icon--0x0--478x451.png             22           0           0         105          99                    105                     99                   23                   32    29    23  0.963209              116               92        92        128            220            208           True               playstore_icon--0x0--478x451.png                   10
    6      C:\detectiontest\einstellungen_icon--537x200--1038x735.png             22         118          44         228         161                    110                    117                   22                   29    34    44  0.952688              608              352        88        116            468            696           True      einstellungen_icon--537x200--1038x735.png                   10
    7              C:\detectiontest\kamera_icon--426x203--931x738.png             22          93          44         204         162                    111                    118                   23                   29    34    45  0.952173              508              356        92        116            472            600           True              kamera_icon--426x203--931x738.png                   10
    8            C:\detectiontest\gamecenter_icon--244x0--781x451.png             22          53           0         171          99                    118                     99                   30                   34    35    21  0.941764              352               84       120        136            220            472           True            gamecenter_icon--244x0--781x451.png                   10
    9           C:\detectiontest\systemapps_icon--528x0--1067x448.png             22         116           0         234          98                    118                     98                   30                   34    34    21  0.938213              600               84       120        136            220            720           True           systemapps_icon--528x0--1067x448.png                   10
    
    
        """

    # if you want to see the results as a video
    #
    template_matching.show_results_as_video()
    # https://github.com/hansalemaos/screenshots/raw/main/templatematching5.png
    # https://github.com/hansalemaos/screenshots/blob/main/templatematching6.png
    # The thicker the outline is, the more images with the same aspect ratio have been found,
    # that usually means that the chance is lower of them being false positives
