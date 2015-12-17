#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import sys
import urllib
import codecs

import sites

VERSION = 10000000  # Just an arbitary number

# Load config
if not os.path.exists('config.json'):
    print('Warning! config.json not found... Automatically generating one...')
    config = {
        'version': VERSION,
        'dataPath': os.getcwd() + os.sep + 'data.json'
    }
    fp = open('config.json', 'w')
    fp.write(json.dumps(config))
    empty_data_fp = open('data.json', 'w')
    empty_data_fp.write('{}')
    fp.close()
    empty_data_fp.close()
    useDataPath = True
else:
    try:
        fp = open('config.json', 'r')
        config = json.loads(fp.read())
        assert(config['version'] == VERSION)
        if config['dataPath']:
            assert(os.path.exists(config['dataPath']))
            useDataPath = True
        else:
            assert(os.path.exists(config['dataDir'] + os.sep + 'data.json'))
            useDataPath = False
        fp.close()
    except Exception as e:
        fp.close()
        print("Exception occurred! Invalid config.json or wrong version! Quitting...")
        sys.exit(1)

# Load data
try:                
    dataPath = config['dataPath'] if useDataPath else config['dataDir'] + os.sep + 'data.json'
    if os.path.exists(dataPath):
        data_fp = codecs.open(dataPath, 'r', 'utf-8')
        data = json.loads(data_fp.read())
        data_fp.close()
    else:
        data = []
    data = sorted(data, key=lambda i: i['timestamp'], reverse=True)
except Exception as e:
    data_fp.close()
    print("Exception occurred! Invalid data! Quitting...")
    sys.exit(1)

# Check if pictures exist
for node in data:
    if not os.path.exists(node['pic_path']):
        print(r'Warning!! Found news with title "' + node['title'] +
              r'" has a picture not found. Trying to redownload......')
        try:
            pic_path = 'pic' + os.sep + str(hash(str(node))) + '.jpg'
            # Still, makes sure that no pictures are downloaded with the same file name.
            urllib.request.urlretrieve(node['pic_src'], pic_path)
            node['pic'] = os.path.abspath(pic_path)
        except Exception as e:
            print(r'Warning!! Redownloading picture from news with title "' + node['title']
                  + r'" failed. This news might be invalid.')

# Get new data
timestamp_threshold = data[0]['timestamp'] if data else 0
print('Getting data from bjnews(新京报)......')
data.extend(sites.bjnews.get(timestamp_thr=timestamp_threshold))

# More sites to do

# Sort data
data = sorted(data, key=lambda j: j['timestamp'], reverse=True)

# Save data to JSON
data_fp = codecs.open(dataPath, 'w', 'utf-8')
data_fp.write(json.dumps(data, ensure_ascii=False, indent=4))
print('News downloading and saving finished... Quitting...')