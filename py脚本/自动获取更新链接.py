import requests
import json
from enum import Enum
import sys
import os

# 添加 notify.py 所在的目录到 sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

# 导入函数
from notify import pushplus_bot


class WebType(Enum):
    XFLTD = 0
    OKYRIN = 1

class FILE_DATA_PATH(Enum):
    XFLTD = 'D:/XFLTD.yaml'
    OKYRIN = 'OKYRIN'


def get_request_params(jc_tyjpe):
    headers = {}
    url = ''
    data = {}
    if jc_tyjpe == WebType.XFLTD:
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-language": "zh-CN",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://my.xfltd.org",
            "priority": "u=1, i",
            "referer": "https://my.xfltd.org/",
            "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
        }
        url = "https://my.xfltd.org/api/v1/passport/auth/login"
        data = {
            "email": "tangjuxiong754@gmail.com",
            "password": "aPRmJ.zKuV2iaY3",
            "captchaData": ""
        }

    if jc_tyjpe == WebType.OKYRIN:
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-language": "zh-CN",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://www.okyrin.net",
            "priority": "u=1, i",
            "referer": "https://www.okyrin.net/",
            "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
        }
        url = "https://voop.okyrin.top/api/v1/passport/auth/login"
        data = {
            "email": "2386584329@qq.com",
            "password": "tjx20011019",
            "captchaData": ""
        }

    data = json.dumps(data, separators=(',', ':'))
    return headers, url, data


def get_auth_data(jc_type):
    headers, url, data = get_request_params(jc_type)
    response = requests.post(url, headers=headers, data=data)
    auth_data = json.loads(response.text).get("data")['auth_data']
    print('auth_data:', auth_data)
    return auth_data


def get_subscribe(auth_data, jc_type):
    h = {}
    u = ''
    if jc_type == WebType.OKYRIN:
        h = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "authorization": auth_data,
            "content-language": "zh-CN",
            "origin": "https://www.okyrin.net",
            "priority": "u=1, i",
            "referer": "https://www.okyrin.net/",
            "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
        }
        u = "https://voop.okyrin.top/api/v1/user/getSubscribe"
    elif jc_type == WebType.XFLTD:
        h = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "authorization": auth_data,
            "content-language": "zh-CN",
            "priority": "u=1, i",
            "referer": "https://my.xfltd.org/",
            "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        }
        u = "https://my.xfltd.org/api/v1/user/getSubscribe"
    r = requests.get(u, headers=h)
    data = json.loads(r.text).get("data")
    subscribe_url = data["subscribe_url"]
    print(jc_type.name + '_subscribe_url:', subscribe_url)
    return subscribe_url


def get_clash_content(_subscribe_url, _jc_type):
    print('获取clash订阅地址并写入到文件中...')
    response = requests.get(_subscribe_url, headers={"User-Agent": "clash"})
    clash_config = response.content.decode('utf-8')
    with open(FILE_DATA_PATH[_jc_type.name].value, 'w', encoding="utf-8") as f:
        f.write(clash_config)


type_list = [WebType.XFLTD]
CLASH_FILE = ''

if __name__ == '__main__':
    for jc_type in type_list:
        auth_data = get_auth_data(jc_type)
        subscribe_url = get_subscribe(auth_data, jc_type)
        get_clash_content(subscribe_url, jc_type)
    # pushplus_bot('更新链接', subscribe_url)

