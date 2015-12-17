#! /usr/bin/env python3
# -*- coding: utf-8 -*-


def get(timestamp_thr=0):
    import httplib2
    import urllib.request
    import os
    import sys
    import json
    import time
    
    TIMEFORMAT = '%Y-%m-%d %X'
    
    h = httplib2.Http(os.devnull) # Currently no cache file is needed
    (resp_headers, content) = h.request("http://www.bjnews.com.cn/api/get_hotlist.php", "GET")
    if resp_headers['status'] != '200':
        print("Fatal Error: return value " + resp_headers['status'] + "!! Check Internet connection... Exiting...")
        sys.exit(1)
    try:
        tmpdata = json.loads(str(content.decode('unicode-escape')))['list']
        if not os.path.exists('pic'):
            os.mkdir('pic')
        data = []
        for i in tmpdata:
            if i['hot_pic'] and time.mktime(time.strptime(i['submit_time'], TIMEFORMAT)) > timestamp_thr:
                tmp = {}
                tmp['title'] = i['title']
                tmp['time'] = time.strptime(i['submit_time'], TIMEFORMAT)
                tmp['timestamp'] = time.mktime(tmp['time'])
                tmp['source'] = '新京报'
                pic_path = 'pic' + os.sep + str(hash(str(tmp))) + '.jpg'
                # Makes sure that no pictures are downloaded with the same file name.
                urllib.request.urlretrieve(i['hot_pic'],pic_path)
                tmp['pic'] = os.path.abspath(pic_path)
                tmp['pic_src'] = i['hot_pic']
                data.append(tmp)
    except Exception as e:
        print("Exception occurred! Quitting... " + 'Exception' + ":" + str(e))
        sys.exit(1)
    data = sorted(data, key=lambda j: j['timestamp'], reverse=True)
    return data
