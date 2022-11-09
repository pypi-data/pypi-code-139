import requests
from requests_toolbelt import MultipartEncoder

def prediction(classes, ID, filename, username, Img):
    if classes == 'potato':
        url = "https://www.harvest-net.cn/api/prediction"
        header = {"Content-Type": "multipart/form-data"}
        m = MultipartEncoder(
          fields={
                 'openid': ID,
                 'username': username,
                 'content': (filename, open(Img, 'rb'), 'text/plain')}
          )
        res = requests.post(url=url, headers={'Content-Type': m.content_type}, data=m)
        print(res.content.decode('unicode-escape'))


    else:
        url = "https://www.harvest-net.cn/api/prediction_" + classes
        header = {"Content-Type": "multipart/form-data"}
        m = MultipartEncoder(
            fields={
                'openid': ID,
                'username': username,
                'content': (filename, open(Img, 'rb'), 'text/plain')}
        )
        res = requests.post(url=url, headers={'Content-Type': m.content_type}, data=m)
        print(res.content.decode('unicode-escape'))