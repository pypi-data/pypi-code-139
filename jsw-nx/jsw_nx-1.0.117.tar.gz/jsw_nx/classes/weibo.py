import requests
import json
import re
from .lc_option import LcOption

# https://houbb.github.io/2019/02/25/github-09-pic-bed

API_URL = {
    'file': 'https://picupload.weibo.com/interface/pic_upload.php',
    'base64': 'https://picupload.weibo.com/interface/pic_upload.php?data=base64',
}
TARGET_RE = r'"pics":(.*)\}\}'
PIC_HOST_SM = 'https://tva1.sinaimg.cn/small/'
PIC_HOST_MW690 = 'https://tva1.sinaimg.cn/mw690/'
PIC_HOST_MW1024 = 'https://tva1.sinaimg.cn/mw1024/'
PIC_HOST_MW2048 = 'https://tva1.sinaimg.cn/mw2048/'
PIC_HOST_ORIGINAL = 'https://tva1.sinaimg.cn/large/'


# size: large|bmiddle|mw1024|mw690|small|square|thumb180|thumbnail

class Weibo:

    @property
    def headers(self):
        return {'Cookie': f'SUB={self.token}', 'Referer': 'https://weibo.com/'}

    def __init__(self):
        lc_opt = LcOption()
        res = lc_opt.get('60f768f6d9f1465d3b1d5c43')
        self.token = res['value']

    def upload(self, **kwargs):
        source = kwargs.get('source')
        debug = kwargs.get('debug', False)
        mode = kwargs.get('mode', 'file')
        files = {'pic1': source, }
        if mode == 'file':
            filep = open(source, 'rb')
            files = {'pic1': filep, }
        if mode == 'base64':
            filep = source
            files = {'b64_data': filep}
        res = requests.post(API_URL.get(mode, 'file'), files=files, headers=self.headers)
        html = res.text

        if debug:
            print("Response HTML: ", html)

        target_str = re.findall(TARGET_RE, html)[0]
        json_data = json.loads(target_str)
        picdata = json_data['pic_1']
        pid = picdata.get('pid', None)
        is_success = bool(pid) and picdata.get('width', 0) > 0

        if is_success:
            return {
                'success': True,
                'pid': pid,
                'url': PIC_HOST_ORIGINAL + picdata['pid'] + '.jpg',
                'sm': PIC_HOST_SM + picdata['pid'] + '.jpg',
                **picdata
            }
        else:
            return {
                'success': False,
                'pid': None,
                'url': None,
                **picdata
            }
