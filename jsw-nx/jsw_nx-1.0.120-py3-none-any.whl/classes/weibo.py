import requests
import json
import re
from .lc_option import LcOption

# https://houbb.github.io/2019/02/25/github-09-pic-bed


TARGET_RE = r'"pics":(.*)\}\}'
PIC_HOST = 'https://tva1.sinaimg.cn/'
SIZES = 'large|bmiddle|mw1024|mw690|small|square|thumb180|thumbnail'.split('|')
API_URL = 'https://picupload.weibo.com/interface/pic_upload.php?data=%s&mime=image%2F%s'


class Weibo:

    @property
    def headers(self):
        return {'Cookie': f'SUB={self.token}', 'Referer': 'https://weibo.com/'}

    def __init__(self):
        lc_opt = LcOption()
        res = lc_opt.get('60f768f6d9f1465d3b1d5c43')
        self.token = res['value']

    # Get the image url by pid and size.
    def get(self, pid, size='large'):
        if size not in SIZES:
            size = 'large'
        return PIC_HOST + size + '/' + pid

    # Get all kinds of image url by pid.
    def getall(self, pid):
        return {
            'large': PIC_HOST + 'large/' + pid + '.jpg',
            'bmiddle': PIC_HOST + 'bmiddle/' + pid + '.jpg',
            'mw1024': PIC_HOST + 'mw1024/' + pid + '.jpg',
            'mw690': PIC_HOST + 'mw690/' + pid + '.jpg',
            'small': PIC_HOST + 'small/' + pid + '.jpg',
            'square': PIC_HOST + 'square/' + pid + '.jpg',
            'thumb180': PIC_HOST + 'thumb180/' + pid + '.jpg',
            'thumbnail': PIC_HOST + 'thumbnail/' + pid + '.jpg',
        }

    # Upload image by url.
    def upload(self, **kwargs):
        source = kwargs.get('source')
        mode = kwargs.get('mode', 'file')
        transparent = kwargs.get('transparent', False)
        debug = kwargs.get('debug', False)
        files = {'pic1': source, }
        if mode == 'file':
            filep = open(source, 'rb')
            files = {'pic1': filep, }
        elif mode == 'base64':
            filep = source
            files = {'b64_data': filep}
        mime = 'gif' if transparent else 'jpeg'
        url = API_URL.format(mode, 'jpeg', mime)
        res = requests.post(url, files=files, headers=self.headers)
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
                'url': self.get(pid),
                **picdata
            }
        else:
            return {
                'success': False,
                'pid': None,
                'url': None,
                **picdata
            }
