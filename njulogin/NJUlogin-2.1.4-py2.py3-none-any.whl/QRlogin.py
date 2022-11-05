import requests
import numpy as np
import time
import cv2
from lxml import etree

from .utils import config, urls, get_post
from .utils.clear import clear


class QR(object):
    def __init__(self, session: requests.Session, getTimeout: int = config.getTimeout):
        self.session = session
        self.getTimeout = getTimeout

    def getQR(self) -> np.ndarray:
        """获取二维码图片，返回numpy数组"""
        self.ts = int(time.time()*1000)
        url = urls.QRid % self.ts
        QRid = get_post.get(self.session, url, timeout=self.getTimeout).text
        self.QRid = QRid
        url = urls.QRimg % QRid
        QRdata = get_post.get(self.session, url, timeout=self.getTimeout).content
        qr =  cv2.imdecode(np.frombuffer(QRdata, np.uint8), cv2.IMREAD_COLOR)
        return qr[6:-6, 6:-6]

    def printQR(self):
        """打印二维码至终端，同时也会保存一份QR.png到当前目录"""
        QRimg = self.getQR()
        cv2.imwrite('QR.png', QRimg)
        char_full = '\u2588'
        char_up = '\u2580'
        char_down = '\u2584'
        for i in range(0, QRimg.shape[0]-3, 6):
            for j in range(0, QRimg.shape[1], 3):
                if QRimg[i, j, 0] < 128 and QRimg[i+3, j, 0] < 128:
                    print(char_full, end='')
                elif QRimg[i, j, 0] < 128 and QRimg[i+3, j, 0] >= 128:
                    print(char_up, end='')
                elif QRimg[i, j, 0] >= 128 and QRimg[i+3, j, 0] < 128:
                    print(char_down, end='')
                else:
                    print(' ', end='')
            print('')
        for j in range(0, QRimg.shape[1], 3):
            if QRimg[-1, j, 0] < 128:
                print(char_up, end='')
            else:
                print(' ', end='')
        print('')


class QRlogin(object):
    def __init__(self, headers: dict = config.headers, loginTimeout: int = config.loginTimeout, getTimeout: int = config.getTimeout):
        """
        QRlogin(headers: dict = config.headers, loginTimeout: int = config.loginTimeout, getTimeout: int = config.getTimeout)
        @description:
        二维码登录
        -------
        @param:
        headers: dict, 请求头
        loginTimeout: int, 登录超时时间，即二维码有效时间
        getTimeout: int, 请求超时时间，即在getTimeout秒内未获取到响应则抛出TimeoutError
        -------
        """
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.loginTimeout = loginTimeout
        self.getTimeout = getTimeout

    def getStatus(self, qr: QR) -> str:
        """等候扫码，返回扫码状态"""
        url =urls.status % (qr.ts, qr.QRid)
        session = self.session
        status = get_post.get(session, url, timeout=self.getTimeout).text
        return status

    def waitingLogin(self, qr: QR) -> bool:
        """等候登录，返回登录状态"""
        # 0: 未扫码, 1: 登录成功, 2: 已扫码未确认登录
        first0, first2 = False, False
        for _ in range(self.loginTimeout):
            status = self.getStatus(qr)
            try:
                status = int(status)
                if status not in [0, 1, 2]:
                    raise ValueError
            except ValueError:
                raise ValueError('未知状态，代码可能需要维护')
            if status == 0 and not first0:
                print('微信或南京大学APP扫码登录')
                first0 = True
            elif status == 2 and not first2:
                print('扫描成功，请在手机上『确认登录』')
                first2 = True
            elif status == 1:
                clear()
                return True
            time.sleep(1)
        clear()
        print('登录超时')
        return False

    def login(self, dest: str) -> requests.Session | None:
        url = urls.login % dest
        html = get_post.get(self.session, url, timeout=self.getTimeout).text
        qr = QR(self.session)
        clear()
        qr.printQR()
        if not self.waitingLogin(qr):
            return None
        
        selector = etree.HTML(html)
        data = {
            'lt': selector.xpath('//input[@name="lt"]/@value')[0],
            'uuid': qr.QRid,
            'dllt': selector.xpath('//input[@name="dllt"]/@value')[0],
            'execution': selector.xpath('//input[@name="execution"]/@value')[0],
            '_eventId': selector.xpath('//input[@name="_eventId"]/@value')[0],
            'rmShown': selector.xpath('//input[@name="rmShown"]/@value')[0]
        }
        res = get_post.post(self.session, url, data=data, timeout=self.getTimeout)
        if res.url == url or res is None:
            print('登录失败')
            return None
        print('登录成功')
        return self.session
