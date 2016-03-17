#!/usr/bin/env python3
# coding: utf-8

from urllib.request import urlopen, build_opener, Request
from urllib.parse import unquote_plus
import re
import json
from bs4 import BeautifulSoup

def get_contents(url):
    try:
        with urlopen(url) as f:
            result=f.read()
        return result
    except IOError:
        print('Could not open this url: %s'%url)
        

def download_movie(url):
    pat=re.compile(r'var swfConfig = ({.*?});')
    contents=get_contents(url)
    bs=BeautifulSoup(contents)
    title=bs.findAll('span', id='eow-title')[0].get('title')
    f_flv='%s.flv'%title
    with open('scripts.txt', 'w+') as f:
        for s in bs.findAll('script'):
            if s.string:
                f.write(s.string)
    for s in bs.findAll('script'):
        m=pat.search(s.string) if s.string else None
        if m:
            j=json.loads(m.group(1).replace('\\ ', '\\'))
            with open(f_flv, 'wb') as f:
                f.write(urlopen(j['args']['fmt_url_map'].aplit('|')[-1]).read())
            break
    
        
    
        
