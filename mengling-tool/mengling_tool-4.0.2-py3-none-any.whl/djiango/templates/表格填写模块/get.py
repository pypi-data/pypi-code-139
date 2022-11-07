import os
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, Http404
from django.shortcuts import render

# 未解决非mysql数据的情况
pass


def getWhere(request: WSGIRequest):
    key_values = list()
    for i in ['1', '2', '3']:
        key, value = request.GET.get(f'fkey{i}', ''), request.GET.get(f'fvalue{i}', '')
        if len(key) > 0 and len(value) > 0:
            key_values.append((key, value))
    if request.GET.get('mh', '0') == '1':
        return ' and '.join(f"`{k}` like '%{v}%'" for k, v in key_values)
    else:
        return ' and '.join(f"`{k}` = '{v}'" for k, v in key_values)


def getOther(request: WSGIRequest, order_name0='', cellnum: int = None):
    page = int(request.GET.get('page', 1))
    order_name, order = request.GET.get('okey', order_name0), request.GET.get('ovalue', 'down')
    if len(order_name) > 0:
        other = f'order by `{order_name}` {"desc" if order == "down" else "asc"} '
    else:
        other = ''
    if cellnum:
        other += f'limit {page * cellnum - cellnum},{cellnum}'
    return other


def if_download(request: WSGIRequest):
    ifd = request.GET.get('download', '0')
    return ifd == '1'


def getDownload(request: WSGIRequest, file_path):
    with open(file_path, 'rb') as f:
        try:
            response = HttpResponse(f)
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
        except Exception:
            raise Http404


def getTable(request: WSGIRequest, liedts: list, maxpage: int,
             lies: list = None, title='', helpdt: dict = dict(),
             cookie_name0='table', table_width=None, table_height=None,
             if_view_find=False, finds: list = None, find_num=3,
             if_view_lie=False,
             if_view_add=False, add_key_lies: list = None,
             if_view_download=False):
    if lies is None:
        if len(liedts) > 0:
            lies = list(liedts[0].keys())
        else:
            lies = []
    finds = finds if finds else lies
    add_key_lies = add_key_lies if add_key_lies else []
    maxpage = max((0, maxpage))
    page = int(request.GET.get('page', 1))
    page = page if page < maxpage else maxpage
    page = max((0, page))
    find_num = min(find_num, 3) if find_num > 0 else 1

    mapdt = {'liedts': liedts, 'lies': lies, 'page': page, 'maxpage': maxpage,
             'if_view_lie': 'true' if if_view_lie else 'false',
             'if_view_find': 'true' if if_view_find else 'false',
             'finds': finds, 'find_num': find_num,
             'cookie_name0': cookie_name0,
             'table_width': table_width if table_width else '',
             'table_height': table_height if table_height else '',
             'title': title, 'helpdt': helpdt,
             'if_view_add': 'true' if if_view_add else 'false', 'add_key_lies': add_key_lies,
             'if_view_download': 'true' if if_view_download else 'false'}
    return render(request, f'表格填写模块/mian.html', mapdt)
