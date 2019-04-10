# 发送请求任务

import requests

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}
def send_request(url,parmas=None,data=None,headers=headers):
    """
    :param url: 请求的url地址
    :param parmas: get请求的查询参数
    :param data: post请求的表单数据
    :param headers: 请求的请求头
    :return:
    """

    if parmas and data:
        print('参数错误')
        return
    elif not parmas and not data:
        response = requests.get(url,headers=headers)
    elif parmas:
        response = requests.get(url,params=parmas,headers=headers)
    elif data:
        response = requests.post(url,data=data,headers=headers)

    if response.status_code == 200:

        return response.text,response.url





