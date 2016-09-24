# -*- coding: utf-8 -*-

import os
import json

from urllib import urlencode
from hashlib import md5
from time import time

import tornado.httpclient

APP_ID = '066ece45c805d77a7f1eee93'
TOKEN = 'APj0nwkI1Ku35VqoHv5tMOsDj5Mb8NeX'
BASE_URL = 'https://api.superid.me/v1'
NONCE = 'TakeMeHome'

def generateSignature(urldict):
    urls = []
    for k in urldict.keys():
        urls.append('%s=%s' % (k, urldict[k]))

    urls.sort()
    args = '&'.join(urls)
    print args
    string = '%s:%s' % (args, TOKEN)
    print 'url', string
    signature = md5(string).hexdigest()
    return signature.upper()

class FaceRequests:
    def __init__(self):
        self.client = tornado.httpclient.HTTPClient()

    def createGroup(self, group):
        timestamp = int(time())
        noncestr = NONCE
        data = {'name': group}
        query = {
            'app_id': APP_ID,
            'timestamp': timestamp,
            'noncestr': noncestr
        }

        signature = generateSignature(query)
        query['signature'] = signature
        address = BASE_URL + '/group/create?' + urlencode(query)
        print address
        body = json.dumps(query)
        request = tornado.httpclient.HTTPRequest(address, 'POST', body=body)
        response = self.client.fetch(request)
        return response

    def groupList(self):
        query = {}
        timestamp = int(time())
        noncestr = NONCE

        query['app_id'] = APP_ID
        query['timestamp'] = timestamp
        query['noncestr'] = noncestr
        signature = generateSignature(query)
        query['signature'] = signature
        address = BASE_URL + '/group/list?' + urlencode(query)
        print address
        response = self.client.fetch(address)
        return response

if __name__ == '__main__':
    requests = FaceRequests()
    res = requests.createGroup('test')
    print res.body
    # query = {}
    # timestamp = int(time())
    # print timestamp
    # noncestr = NONCE
    #
    # query['app_id'] = APP_ID
    # query['timestamp'] = timestamp
    # query['noncestr'] = noncestr
    # query['a'] = 2
    # query['b'] = 3
    # signature = generateSignature(query)
    # print signature
