#!/usr/bin/env python3
# coding: utf-8

from urllib.request import urlopen, build_opener, HTTPCookieProcessor
from urllib.parse import urlencode
from http.cookiejar import CookieJar
import re
import os


url_encodes={
    '%26': '&', '%2F': '/', '%20': ' ', '%27': "'", '%28': '(',
    '%7D': '}', '%5B': '[', '%3D': '=', '%7B': '{', '%40': '@',
    '%3E': '>', '%22': '"', '%5C': '',  '%2C': ',', '%2B': '+',
    '%7C': '|', '%3F': '?', '%7E': '~', '%3B': ';', '%23': '#',
    '%2A': '*', '%5D': ']', '%3A': ':', '%24': '$', '%29': ')',
    '%60': '`', '%21': '!', '%25': '%', '%5E': '^', '%3C': '<'}

def get_contents(url, opener):
    try:
        with opener.open(url) as f:
            result=f.read().decode('utf-8')
        return result
    except IOError:
        print('Could not open this url: %s'%url)
        
def download(url, filename, opener):
    try:
        with opener.open(url) as f:
            result=f.read()
        with open(filename, 'wb') as f:
            f.write(result)      
    except IOError:
        print('Could not open this url: %s'%url)

def set_filename(contents, title_pat, dirpath):
    print('保存するファイル名を入力してください')
    print('入力が無い場合はサイトの動画名をファイル名にします')
    filename=input('filename:')
    if not filename:
        filename=title_pat.search(contents).group(1)
    for forbid in ('.,"…-=[]\/:;+*?<>|'):
        filename=filename.replace(forbid, '')
    filename=filename.replace(' ', '_')
    filename=dirpath+'\\'+filename+'.flv'
    return filename

def parse_url(contents, url_pat, split_pat):
    m=url_pat.search(contents).group(1)
    urllist=m.split(split_pat)
    for url in urllist:
        if url.startswith('http'):
            break
    url=url.replace('%25', '%')
    for key in url_encodes:
        url=url.replace(key, url_encodes[key])
    return url

def youtube(url, dirpath):
    opener=build_opener()
    contents=get_contents(url, opener)
    title_pat=re.compile('<meta name="title" content="(.*?)">')
    filename=set_filename(contents, title_pat, dirpath)
    url_pat=re.compile(r'"url_encoded_fmt_stream_map":"(.*?)"')
    split_pat='url='
    url=parse_url(contents, url_pat, split_pat)
    url=url.split('\\u0026')[0]
    download(url, filename, opener)

def cookielogin(site):
    opener=build_opener(HTTPCookieProcessor(CookieJar()))
    login_id=input('login id:')
    login_pass=input('login password:')
    if site=='niconico':
        post={'mail_tel': login_id, 'password': login_pass, 'auth_id': 'true'}
        data=urlencode(post)
        loginurl='https://account.nicovideo.jp/api/v1/login?show_button_twitter=1&site=niconico&show_button_facebook=1'
    with opener.open(loginurl, data.encode('utf-8')) as res:
        pass
    return opener

def niconico(url, dirpath):
    opener=cookielogin(site='niconico')
    contents=get_contents(url, opener)
    title_pat=re.compile('<title>(.*?)</title>')
    filename=set_filename(contents, title_pat, dirpath)
    url_pat=re.compile('<div id="watchAPIDataContainer".*?>(.*?)</div>')
    split_pat='%3D'
    url=parse_url(contents, url_pat, split_pat)
    download(url, filename, opener)
 
if __name__=='__main__':
    url=input('url:')
    subdir=input('directory:')
    dirpath='C:\\Users\\User\\Videos\\'
    dirpath+=subdir
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    #youtube(url, dirpath)
    niconico(url, dirpath)
    
