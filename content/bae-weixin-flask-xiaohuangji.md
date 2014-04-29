layout: post
title: BAE上面搭建微信版本小黄鸡
date: 2013-05-14 00:32
comments: true
categories: [python]

前端时间人人<code>小黄鸡</code>火极一时，贱贱的回复热心喜爱，看了github上面的源码，是调用的simsimi，那好，用微信公共帐号实现一个吧。

服务端是BAE平台 <code>python</code> + <code>flask</code>

requests包请自行上传，sae不晓得，bae上面木有～，gist如下：

<code>index.py</code>

```py
#-*- coding:utf-8 -*-

from bae.api import logging
from flask import Flask, g, request, make_response
from simsimi import *
import xml.etree.ElementTree as ET
import hashlib
import time


app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return '您进错页面了亲～';

@app.route('/connect', methods=['GET', 'POST'])
def site_connect():
    logging.debug('into connect %s' % (request.method))

    if request.method == 'GET':# 网站接入，参看微信官方wiki
        return auth()
    else: # 获取用户发送过来的消息，并且echo
        return say()

def say():
    xml = request.data
    xml_recv = ET.fromstring(xml)
    to_user_name = xml_recv.find('ToUserName').text
    from_user_name = xml_recv.find('FromUserName').text
    content = xml_recv.find('Content').text

    logging.debug('to_user_name : %s, from_user_name : %s, content : %s' % (to_user_name, from_user_name, content))

    content = handle({'message': '%s' % (content)}, None)

    reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%d</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"  % (from_user_name, to_user_name, int(time.time()), content)

    logging.debug('reply : %s' % (reply))

    reponse = make_response(reply)
    reponse.content_type = 'application/xml'
    return reponse


def auth():
    token = "xxx" # xxx为微信添加的token，每个人可能不一样
    signature = request.args['signature']
    timestamp = request.args['timestamp']
    nonce = request.args['nonce']
    echostr = request.args['echostr']

    logging.debug('signature : %s, timestamp : %s, nonce : %s, echostr : %s' % (signature, timestamp, nonce, echostr))

    tmp_arr = [token, timestamp, nonce]
    tmp_arr.sort()
    tmp_str = ''.join(tmp_arr)
    code = hashlib.sha1(tmp_str).hexdigest()

    if code == signature:
        return echostr
    else:
        return ''

from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)
```

<code>simsimi.py</code>

```py
#-*-coding:utf-8-*-

# 从simsimi读数据

import requests
import cookielib
import socket
import random

SIMSIMI_KEY = ''

class SimSimi:

    def __init__(self):
        self.session = requests.Session()
        self.chat_url = 'http://www.simsimi.com/func/req?lc=ch&msg=%s'
        self.api_url = 'http://api.simsimi.com/request.p?key=%s&lc=ch&ft=1.0&text=%s'
        if not SIMSIMI_KEY:
            self.initSimSimiCookie()

    def initSimSimiCookie(self):
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:18.0) Gecko/20100101 Firefox/18.0'})
        self.session.get('http://www.simsimi.com/talk.htm')
        self.session.headers.update({'Referer': 'http://www.simsimi.com/talk.htm'})
        self.session.get('http://www.simsimi.com/talk.htm?lc=ch')
        self.session.headers.update({'Referer': 'http://www.simsimi.com/talk.htm?lc=ch'})

    def getSimSimiResult(self, message, method='normal'):
        if method == 'normal':
            r = self.session.get(self.chat_url % message)
        else:
            url = self.api_url % (SIMSIMI_KEY, message)
            r = requests.get(url)
        return r

    def chat(self, message=''):
        if message:
            r = self.getSimSimiResult(message, 'normal' if not SIMSIMI_KEY else 'api')
            try:
                answer = r.json()['response']
                return answer.encode('utf-8')
            except:
                return random.choice(['呵呵', '。。。', '= =', '=。='])
        else:
            return '叫我干嘛'

simsimi = SimSimi()

def handle(data, bot):
    return simsimi.chat(data['message'])

if __name__ == '__main__':
    print handle({'message': '最后一个问题'}, None)
    print handle({'message': '还有一个问题'}, None)
    print handle({'message': '其实我有三个问题'}, None)
```

<code>app.conf</code>

```
handlers:
  - url : /static/(.*)
    script: /static/$1

  - url : /.*
    script: index.py

  - expire : .jpg modify 10 years
  - expire : .swf modify 10 years
  - expire : .png modify 10 years
  - expire : .gif modify 10 years
  - expire : .JPG modify 10 years
  - expire : .ico modify 10 years
```

玩的愉快～
