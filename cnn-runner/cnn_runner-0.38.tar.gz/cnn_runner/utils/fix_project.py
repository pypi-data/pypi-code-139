import json
import glob
import os

CATEGORIES = [
    {"supercategory": "type", "id": 1, "name": "ro_pf"},
    {"supercategory": "type", "id": 2, "name": "ro_sf"},
    {"supercategory": "type", "id": 3, "name": "ro_cil_p"},
    {"supercategory": "type", "id": 4, "name": "mz_v"},
    {"supercategory": "type", "id": 5, "name": "mz_nv"},
    {"supercategory": "type", "id": 6, "name": "tr_"},
    {"supercategory": "type", "id": 7, "name": "tr_op"},
    {"supercategory": "type", "id": 8, "name": "mz_ot"},
    {"supercategory": "type", "id": 9, "name": "ru_ot"},
    {"supercategory": "type", "id": 10, "name": "ru_zk"},
    {"supercategory": "type", "id": 11, "name": "bns_ot"},
    {"supercategory": "type", "id": 12, "name": "bns_zk"},
    {"supercategory": "type", "id": 13, "name": "gr_b"},
    {"supercategory": "type", "id": 14, "name": "gr_vent_kr"},
    {"supercategory": "type", "id": 15, "name": "gr_vent_pr"},
    {"supercategory": "type", "id": 16, "name": "bass"},
    {"supercategory": "type", "id": 17, "name": "ro_cil_ss"},
    {"supercategory": "type", "id": 18, "name": "ro_cil_sp"},
    {"supercategory": "type", "id": 19, "name": "gr_b_act"},
    {"supercategory": "type", "id": 20, "name": "gr_vent_kr_akt"}
]

CATEGORIES_CONVERTER = {
    1: 1,  # "ro_pf",
    2: 2,  # "ro_sf",
    3: 2,  # "ro_cil_p",
    4: 3,  # "mz_v",
    5: 3,  # "mz_nv",
    6: 4,  # "tr_",
    7: -1,  # "tr_op",
    8: 5,  # "mz_ot",
    9: 6,  # "ru_ot",
    10: -1,  # "ru_zk",
    11: 7,  # "bns_ot",
    12: 8,  # "bns_zk",
    13: 9,  # "gr_b",
    14: 10,  # "gr_vent_kr",
    15: 11,  # "gr_vent_pr",
    16: -1,  # "bass",
    17: 2,  # "ro_cil",
    18: 2,  # "ro_cil",
    19: 9,  # "gr_b",
    20: 10,  # "gr_vent_kr"
}


def coco_analyzer_list_of_ds(coco_list, categories=CATEGORIES, converter=None):
    category_ids = {}

    for coco_dataset_filename in coco_list:
        ds_name = os.path.basename(coco_dataset_filename)

        with open(coco_dataset_filename) as f:
            d = json.load(f)

            images = d["images"]
            annotation = d["annotations"]

            print("Number of images in the dataset: {0:d}".format(len(images)))
            print("Number of annotations in the dataset: {0:d}".format(len(annotation)))
            category_ids[ds_name] = {}
            for ann in annotation:
                id = ann["category_id"]
                if converter:
                    id = converter[id]

                if id > 0:
                    if id in category_ids[ds_name]:
                        category_ids[ds_name][id] += 1
                    else:
                        category_ids[ds_name][id] = 1

    head = "|{0:^20s}|".format("Class")
    for coco in coco_list:
        ds_name = os.path.basename(coco)
        head += "{0:^20s}|".format(ds_name)

    head += "{0:^20s}|".format("Total")

    print("-" * len(head))
    print(head)
    print("-" * len(head))

    total_in_file = [0] * (len(coco_list) + 1)

    bottom = "|{0:^20s}|".format("Total")

    for k in range(len(categories)):

        cls_name = categories[k]["name"]

        str_tek = "|{0:^20s}|".format(cls_name)

        cls_total = 0

        for i, coco in enumerate(coco_list):
            ds_name = os.path.basename(coco)

            id = k + 1
            if converter:
                id = converter[id]

            if id in category_ids[ds_name]:
                str_tek += "{0:^20d}|".format(category_ids[ds_name][id])
                cls_total += category_ids[ds_name][id]
                total_in_file[i] += category_ids[ds_name][id]
            else:
                str_tek += "{0:^20s}|".format("-")

        str_tek += "{0:^20d}|".format(cls_total)
        total_in_file[-1] += cls_total

        print(str_tek)

    for t in total_in_file:
        bottom += "{0:^20d}|".format(t)

    print("-" * len(head))
    print(bottom)
    print("-" * len(head))


def coco_analyzer(coco_dataset_filename, categories=CATEGORIES):
    with open(coco_dataset_filename) as f:
        d = json.load(f)

        images = d["images"]
        annotation = d["annotations"]

        print("Number of images in the dataset: {0:d}".format(len(images)))
        print("Number of annotations in the dataset: {0:d}".format(len(annotation)))
        category_ids = {}
        for ann in annotation:
            id = ann["category_id"]
            if id in category_ids:
                category_ids[id] += 1
            else:
                category_ids[id] = 1

        head = "{0:^20s}|{1:^10s}".format("Class", "Count")
        print("-" * len(head))
        print(head)
        print("-" * len(head))

        for k in range(len(category_ids)):

            cls_name = categories[k]["name"]
            if k + 1 in category_ids:
                cls_count = category_ids[k + 1]
            else:
                cls_count = 0

            print("{0:^20s}|{1:^10d}".format(cls_name, cls_count))

        print("-" * len(head))


def fix_filenames(folder, file_ext='.jpg'):
    images = glob.glob(folder + "/*" + file_ext)
    for img in images:
        dirname = os.path.dirname(img)
        basename_new = "id_" + os.path.basename(img)
        print(os.path.join(dirname, basename_new))
        if not os.path.basename(img).startswith("id_"):
            os.rename(img, os.path.join(dirname, basename_new))


def fix_project_images_ids(filename, save_filename=None, is_name_fix=True):
    with open(filename) as f:
        d = json.load(f)
        via_img_metadata = {}
        for name in d["_via_img_metadata"]:
            name_list = name.split(".")
            if 'jpg' in name_list[-1]:
                ext = '.jpg'
            else:
                ext = '.png'
            name_new = ""
            for i in range(len(name_list) - 1):
                name_new += name_list[i]
            if is_name_fix:
                name_new = "id_" + name_new + ext
            else:
                name_new = name_new + ext

            new_record = d["_via_img_metadata"][name]
            new_record["filename"] = name_new
            via_img_metadata[name_new] = new_record

        d["_via_img_metadata"] = via_img_metadata

        via_image_id_list = []
        for name in d["_via_image_id_list"]:
            name_list = name.split(".")
            if 'jpg' in name_list[-1]:
                ext = '.jpg'
            else:
                ext = '.png'
            name_new = ""
            for i in range(len(name_list) - 1):
                name_new += name_list[i]

            if is_name_fix:
                name_new = "id_" + name_new + ext
            else:
                name_new = name_new + ext
            via_image_id_list.append(name_new)

        d["_via_image_id_list"] = via_image_id_list

        if not save_filename:
            dirname = os.path.dirname(filename)
            save_filename = os.path.join(dirname, "via_project_new.json")
        else:
            dirname = os.path.dirname(filename)
            save_filename = os.path.join(dirname, save_filename)

        with open(save_filename, 'w') as f_save:
            json.dump(d, f_save)


def fix_coco_category_names(data_coco_filename, categories=CATEGORIES, save_filename=None):
    with open(data_coco_filename) as f:
        d = json.load(f)

        category_old = d["categories"]
        print("\nOLD categories:\n")
        print(category_old)

        d["categories"] = categories

        print("\nNEW categories:\n")
        print(categories)

        if not save_filename:
            dirname = os.path.dirname(data_coco_filename)
            save_filename = os.path.join(dirname, "data_coco_new.json")
        else:
            dirname = os.path.dirname(data_coco_filename)
            save_filename = os.path.join(dirname, save_filename)

        with open(save_filename, 'w') as f_save:
            json.dump(d, f_save)


if __name__ == "__main__":
    # fix_coco_category_names("D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проект Жукова\data_coco.json")
    coco_names = ["D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проект Жукова\\jukov.json",
                  "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\18.10\\sp_18_10.json",
                  "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\19.10\sp_19_10.json",
                  "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\20.10\sp_20_10.json",
                  "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\24.10\sp_24_10.json",
                  "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\26.10\\04_Сжатые и отфильтрованные\sp_26_10_04.json",
                  "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\26.10\\05\sp_26_10_05.json"]

    coco_names_train = ["D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проект Жукова\\jukov.json",
                        "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\19.10\sp_19_10.json",
                        "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\24.10\sp_24_10.json",
                        "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\26.10\\05\sp_26_10_05.json",
                        "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\26.10\\04_Сжатые и отфильтрованные\sp_26_10_04.json"]

    coco_names_test = [
        "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\18.10\\sp_18_10.json",
        "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\20.10\sp_20_10.json"
        ]

    # coco_analyzer("D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проект Жукова\data_coco_new.json")
    coco_analyzer_list_of_ds(coco_names_test, converter=CATEGORIES_CONVERTER)

    # fix_coco_category_names("D:\python\datasets\\aes dataset fine\images\\val\data_coco.json")
