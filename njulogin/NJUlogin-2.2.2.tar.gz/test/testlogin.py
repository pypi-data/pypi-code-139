from NJUlogin.pwdLogin import pwdLogin
from NJUlogin.QRlogin import QRlogin

dest = 'http://p.nju.edu.cn/cas/&renew=true'
mobile_headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; M2007J1SC Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.97 Mobile Safari/537.36 cpdaily/9.0.15 wisedu/9.0.15'
}
qrlogin = QRlogin(headers=mobile_headers)
pwdlogin = pwdLogin('XXXXXXXXX', 'XXXXXXXXX', mobileLogin=True, headers=mobile_headers)
session = pwdlogin.login(dest)
