#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#    Aria - A simple script for automatically grabbing news from the Internet.
#    Copyright (C) 2015  Genesis Di
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
