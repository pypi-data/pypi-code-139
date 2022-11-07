import requests
import re
from bs4 import BeautifulSoup as Be
import os


def fbi_warning(page=2):
    """

    :param page: 下载图片页数，int型整数
    :return:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    }

    if not os.path.exists("FBIWarning"):
        os.makedirs("FBIWarning")

    num = 1
    for i in range(page):
        url = f"https://m.bcoderss.com/tag/美女/page/{i + 1}/"

        r = requests.get(url=url, headers=headers)
        html = r.text

        b = Be(html, 'lxml')
        img_url = b.find_all('img', class_="attachment-thumbnail size-thumbnail wp-post-image")
        try:
            for img in img_url:
                # print(a)
                e = re.search('<img alt=.*? class=.*? height=.*? src="(.*?)" title.*? width=.*?/>', str(img), re.S)
                print(f"第{i + 1}页|第{num}张图片：", e.group(1))
                get_img = requests.get(url=e.group(1))
                with open(f'FBIWarning/{num}.jpg', 'ab') as f:
                    f.write(get_img.content)
                num += 1
                # time.sleep(1)如。
        except:
            continue
