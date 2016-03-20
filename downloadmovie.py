#!/usr/bin/env python3
# coding: utf-8

from urllib.request import urlopen, build_opener, Request
from urllib.parse import unquote_plus
import re
import json
from bs4 import BeautifulSoup
import os


url_encodes={
    '%26': '&', '%2F': '/', '%20': ' ', '%27': "'", '%28': '(',
    '%7D': '}', '%5B': '[', '%3D': '=', '%7B': '{', '%40': '@',
    '%3E': '>', '%22': '"', '%5C': '',  '%2C': ',', '%2B': '+',
    '%7C': '|', '%3F': '?', '%7E': '~', '%3B': ';', '%23': '#',
    '%2A': '*', '%5D': ']', '%3A': ':', '%24': '$', '%29': ')',
    '%60': '`', '%21': '!', '%25': '%', '%5E': '^', '%3C': '<',
    '%252C': ','}

def get_contents(url):
    try:
        with urlopen(url) as f:
            result=f.read().decode('utf-8')
        return result
    except IOError:
        print('Could not open this url: %s'%url)
        
def download(url, filename):
    try:
        with urlopen(url) as f:
            result=f.read()
        with open(filename, 'wb') as f:
            f.write(result)
            
    except IOError:
        print('Could not open this url: %s'%url)
       
def youtube(url, dirpath):
    contents=get_contents(url)
    print('保存するファイル名を入力してください')
    print('入力が無い場合はyoutubeの動画名をファイル名にします')
    filename=input('filename:')
    if not filename:
        title_pat=re.compile('<meta name="title" content="(.*?)">')
        title=title_pat.search(contents).group(1)
        filename=title+'.flv'
    filename=dirpath+'\\'+filename
    pat=re.compile(r'"url_encoded_fmt_stream_map":"(.*?)"')
    m=pat.search(contents).group(1)
    urllist=m.split('url=')
    for url in urllist:
        if url.startswith('http'):
            break
    for key in url_encodes:
        url=url.replace(key, url_encodes[key])
    url=url.split('\\u0026')[0]
    download(url, filename)

if __name__=='__main__':
    url=input('url:')
    subdir=input('directory:')
    dirpath='C:\\Users\\User\\Videos\\'
    dirpath+=subdir
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    youtube(url, dirpath)
    
