#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
dynadot API
dynadot.com 接口解析操作库
DOC: https://www.dynadot.com/zh/domain/api3.html#set_dns2
@author: eric hu
github: nameyule
"""

from logging import DEBUG, basicConfig, info, warning, error, debug

import sys

from re import compile

try:
    # python 2
    from urllib import urlencode
    from urllib2 import urlopen, Request
except ImportError:
    # python 3
    from urllib.parse import urlencode
    from urllib.request import urlopen, Request


__version__ = "${BUILD_SOURCEBRANCHNAME}@${BUILD_DATE}"  # CI 时会被Tag替换
__description__ = "automatically update DNS records to dynamic local IP [自动更新DNS记录指向本地IP]"
__doc__ = """
根据github开源项目ddns[%s]改写。原项目信息如下：
(i) homepage or docs [文档主页]: https://ddns.newfuture.cc/
(?) issues or bugs [问题和帮助]: https://github.com/NewFuture/DDNS/issues
""" % (__version__)


# API 配置
config_api= {
    'site': "api.dynadot.com",
    'action': 'api3.xml', 
    'method': "GET", # 请求方法
    'iptype': 4
}

# DNS 配置
config_url={
    'key':'$YOUR OWN TOKEN CREATED BY DYNADOT$',
    'command': 'set_dns2',
    'domain': '$YOUR MAIN DOMAIN$',
    'main_record_type0': 'a',
    'main_record0': '',
    'subdomain0': '$YOUR SUBDOMAIN1$',
    'sub_record_type0': 'a',
    'sub_record0': '',
    'subdomain1': '$YOUR SUBDOMAIN2$',
    'sub_record_type1': 'cname',
    'sub_record1': ''
}

config_ip=['$YOUR FIRST IP$','$YOUR 2ND IP$','YOUR CNAME']

#----------------------------------
# GET PUBLIC IP ADDRESS
#----------------------------------

def _open(url, reg):
    try:
        debug("open: %s", url)
        res = urlopen(
            Request(url, headers={'User-Agent': 'curl/7.63.0-ddns'}),  timeout=60
        ).read().decode('utf8')
        debug("response: %s",  res)
        return compile(reg).search(res).group()
    except Exception as e:
        error(e)

def get_ip(ip_type):
    """
    get IP address
    """
    # IPV4正则
    IPV4_REG = r'((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])'
    # IPV6正则
    # https://community.helpsystems.com/forums/intermapper/miscellaneous-topics/5acc4fcf-fa83-e511-80cf-0050568460e4
    IPV6_REG = r'((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))'

    url4="https://pv.sohu.com/cityjson?ie=utf-8"
    url6="https://ipv6-test.com/api/myip.php"

    return _open(url4, IPV4_REG) if ip_type==4  else _open(url6, IPV6_REG)


#----------------------------------
# DNS UPDATE REQUEST
#----------------------------------

def dnsrequest(site, method,action,  params):
    """
    发送请求数据
    """
    apiurl='https://' + site + '/' + action

    req = Request('%s?%s' % (apiurl,urlencode(params))) 
    with urlopen(req) as f:
        res = f.read()
        if res.lower().find('success')>=0:
            info("[DEBUG] %s", res )
        else:
            raise Exception("DNS Update Failed.")

def update_dns():
    site=config_api['site']
    method= config_api['method']
    action= config_api['action']
    # 实时获取公网IP
    config_ip[1]=get_ip(config_api['iptype']) 

    # 将IP赋值给对应域名
    config_url['main_record0']=config_ip[0]
    config_url['sub_record0']=config_ip[1]
    config_url['sub_record1']=config_ip[2]

    # 更新DNS
    try:
        res = dnsrequest(site, method, action, config_url)
    except Exception as e:
        error(e)

if __name__ == '__main__':
    update_dns()
