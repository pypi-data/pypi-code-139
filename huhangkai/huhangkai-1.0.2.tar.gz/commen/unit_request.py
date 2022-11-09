import re

from requests import ReadTimeout, ConnectTimeout
from requests.exceptions import MissingSchema

from commen.unit_dict import Dict
from commen.unit_logger import logger

import requests
import json
import time


def get_url(url, kwargs):
    tmp = re.findall(r'\{.+}', url)
    if not tmp:
        return url
    if kwargs.get(tmp[0][1:-1]):
        url = url.replace(tmp[0], kwargs.get(tmp[0][1:-1]))
        url = url.split('{')[0]
        return url
    else:
        assert False, "字段：" +tmp[0][1:-1] + "，为必填字段"


def unit_http_requester(method, url, params=None, data=None, headers=None, host=None, timeout=None, init_headers={},
                        _route=""):
    if headers.get("headers"):
        _headers = init_headers
        tmp = headers.pop("headers")
        if isinstance(tmp, dict):
            _headers.update(headers)
            _headers.update(tmp)
    else:
        headers.pop("headers")
        _headers = headers

    if url[0] == '/' and host:
        if _route and _route[0] != '/':
            _route = '/' + _route
        url = host + _route + url

    logger.info("接口请求参数method: %s, url: %s" % (method, url))
    logger.info("接口请求参数headers: %s" % str(headers))
    logger.info("接口请求参数params: %s" % str(params)) if params else logger.info("接口请求参数data: %s" % str(data))
    time_s = time.time()
    try:
        res = requests.request(method, url, params=params, json=data, headers=headers, timeout=timeout/1000)
        logger.info("接口响应时间: %.3f秒" % (time.time() - time_s))
        try:
            res.rsp = Dict(json.loads(res.text))
        except:
            res.rsp = res.text
        logger.info("接口返回http_code: %s" % res.status_code)
        logger.info("接口数据res: %s" % str(res.rsp))
        return res
    except ReadTimeout:
        assert False, "接口响应时间%.3f秒, 超过设置的时间%.3f秒" % (time.time() - time_s, timeout / 1000)
    except ConnectTimeout:
        assert False, "接口响应时间%.3f秒, 超过设置的时间%.3f秒" % (time.time() - time_s, timeout / 1000)
    except MissingSchema:
        assert False, "url不对，无域名"
    except Exception as e:
        print(e)
        assert False, "调用接口报错"


def get_variable(app_key, env):
    project = requests.post('http://127.0.0.1:8000/variable/variable/',
                            json={"app_key": app_key, "environment": env}).json()
    _variable = {}
    for v in project.get('variables'):
        if v.get('type') == 0:
            _variable[v.get('name')] = v.get('value')
        elif v.get('type') == 1:
            _variable[v.get('name')] = json.loads(v.get('value'))
        elif v.get('type') == 2:
            _variable[v.get('name')] = int(json.loads(v.get('value')))
    return _variable