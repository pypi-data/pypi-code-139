import json


def merge_projects(filename_list, output_filename="via_project_merged.json"):
    via2 = {}
    with open(filename_list[0], 'r') as f:
        via2 = json.load(f)

    if '_via_data_format_version' not in via2:
        via2['_via_data_format_version'] = '2.0.10'
        via2['_via_image_id_list'] = via2['_via_img_metadata'].keys()

    discarded_count = 0
    for i in range(1, len(filename_list)):
        with open(filename_list[i], 'r') as f:
            pdata_i = json.load(f)
            for metadata_i in pdata_i['_via_img_metadata']:
                if metadata_i not in via2['_via_img_metadata']:
                    via2['_via_img_metadata'][metadata_i] = pdata_i['_via_img_metadata'][metadata_i]
                    via2['_via_image_id_list'].append(metadata_i)
                else:
                    discarded_count = discarded_count + 1

    with open(output_filename, 'w') as fout:
        json.dump(via2, fout)

    print('Written merged project to %s (discarded %d metadata)' % (output_filename, discarded_count))


if __name__ == "__main__":
    coco_names_train = ["D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проект Жукова\\via_project.json",
                  "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\18.10\\via_project.json",
                  "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\19.10\\via_project.json",
                  "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\20.10\\via_project.json",
                  "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\24.10\\via_project.json",
                  "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\26.10\\04_Сжатые и отфильтрованные\\via_project.json",
                  "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\26.10\\05\\via_project.json",
                  ]

    coco_names_val = [
        "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\18.10\\via_project.json",
        "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\\20.10\\via_project.json",
        "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\На тестирование\\25.10\На тест\\via_project.json",
        "D:\python\datasets\\02_На разметку_Денис\Размеченные проекты\Проекты Спесивцевой\На тестирование\\20.10\\via_project.json"
    ]

    out_name = "D:\python\datasets\\aes dataset fine\images\\train\\train.json"

    merge_projects(coco_names_train, out_name)
