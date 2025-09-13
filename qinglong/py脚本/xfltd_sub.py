import base64
import re
import urllib
from urllib.parse import unquote, urlparse, parse_qs

import requests
import yaml


LOGIN_URL = 'https://my.xfltd.org/api/v1/passport/auth/login'
SUB_URL = 'https://my.xfltd.org/api/v1/user/getSubscribe'

SUB_FILE = '/www/wwwroot/iptv/58493d82-25fb-4d83-88a8-491081d5d76c/sub_url_xfltd.txt'
CLASH_FILE = '/www/wwwroot/iptv/58493d82-25fb-4d83-88a8-491081d5d76c/sub_url_xfltd.yaml'

HEARDERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

CLASH_HEARDERS = {
    "User-Agent": "clash"
}


def login():
    """登录获取token"""
    data = {
        "email": "",
        "password": "",
        "captchaData": ""
    }
    response = requests.post(LOGIN_URL, json=data, headers=HEARDERS)
    if response.status_code == 200:
        return response.json().get('data')
    return None


def get_subscribe():
    """获取订阅连接"""
    login_data = login()
    if login_data:
        hearders = {
            "Authorization": login_data["auth_data"],
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        }
        response = requests.get(SUB_URL, headers=hearders)
        if response.status_code == 200:
            return response.json().get('data')


def get_url_data(url, headers=None):
    """获取订阅连接的内容"""
    if headers is None:
        headers = HEARDERS
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response


def url_decode_list(text1):
    """base64的订阅连接内容转换为订阅连接list"""
    content = base64.b64decode(text1).decode('utf-8')
    nodes = content.strip().splitlines()
    return nodes


def handler_nodes(nodes):
    """处理nodes节点，转换为自己的节点名称，便于匹配负载均衡"""
    parsed_nodes = []
    region_counter = {}

    for array_idx, node in enumerate(nodes, 1):
        # 找 # 后备注
        if '#' in node:
            remark = node.split('#', 1)[1]
            remark = unquote(remark)
        else:
            remark = "无备注"

        # 判断是否为统计信息
        if any(keyword in remark for keyword in ["剩余流量", "距离下次重置", "套餐到期"]):
            parsed_nodes.append({
                "array_index": array_idx,
                "raw": remark,
                "available": False,
                "region": "",
                "region_index": "",
                "rate": "",
            })
            continue

        # 提取倍率
        rate_match = re.search(r"x[\d\.]+", remark)
        rate = rate_match.group() if rate_match else ""

        # 提取地区名
        region = remark.split("|")[0].strip()
        region = region.replace(rate, "").strip()

        # 更新地区计数
        region_key = region
        region_counter.setdefault(region_key, 0)
        region_counter[region_key] += 1

        parsed_nodes.append({
            "array_index": array_idx,  # 原数组中的 index，可选
            "raw": remark,
            "available": True,
            "region": region,
            "region_index": region_counter[region_key],  # 地区内编号
            "rate": rate,
        })
    return parsed_nodes


if __name__ == '__main__':
    print('正在获取订阅地址...')
    subscribe_url = get_subscribe().get('subscribe_url')
    print('获取订阅地址内容...')
    text = get_url_data(subscribe_url).text
    print('写入内容到普通订阅文件中...')
    # 订阅连接地址内容写入文件，普通订阅地址
    with open(SUB_FILE, 'w') as f:
        f.write(text)

    print('获取clash订阅地址并写入到文件中...')
    clash_config = get_url_data(subscribe_url, CLASH_HEARDERS).content
    clash_config = clash_config.decode('utf-8')
    with open(CLASH_FILE, "w", encoding="utf-8") as f:
        f.write(clash_config)


