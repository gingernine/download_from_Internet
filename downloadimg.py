#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import re
import glob
from urllib.request import urlopen, build_opener, Request

url = input('url > ')
title = ''
img_tag = []
img_url = []
directory_path = 'C:\\Users\\User\\Pictures'

pat_title = re.compile(r'<title>(.*?)</title>')
pat_a1 = re.compile(r'<a[\s]*href[\s]*=.*?>')
pat_a2 = re.compile(r'href[\s]*="(.*)"')
pat_img1 = re.compile(r'<img[\s]*src[\s]*=.*?>')
pat_img2 = re.compile(r'src[\s]*="(.*?)"')
pat_path1 = re.compile(r'.+/(.*)')
pat_path2 = re.compile(r'./(.*)')
pat_path3 = re.compile(r'.+/(.*)/(.*)')
pat_rootpath = re.compile(r'(http://.*?)(/.*)')
img_extension = ['.jpg','.png','.gif','.bmp','.php']

def image_download(url, filepath):
    """
    画像をダウンロードしてファイルに書き込む
    """
    opener = build_opener()
    req = Request(url, headers={'User-Agent': 'Magic Browser'})
    with open(filepath, 'wb') as img_file:
        img_file.write(opener.open(req).read())

def parse_img_path(url, tag, pat):
    img_path = pat.search(tag)
    img_abspath=''
    if img_path:
        tmp = img_path.group(1)
        for extension in img_extension:
            #if img_title in atag.group():
            if tmp.find(extension)>0:
                if tmp.startswith('http://'):
                    img_abspath = tmp
                    break
                if tmp.startswith('/'):
                    rootpath = pat_rootpath.search(url).group(1)
                    img_abspath = rootpath+tmp
                    break
                if tmp.startswith('./'):
                    url_hierarchy = pat_path1.search(url).group(1)
                    img_hierarchy = pat_path2.search(tmp).group(1)
                    img_abspath = url.replace(url_hierarchy, img_hierarchy)
                    break
                if tmp.startswith('../'):
                    url_hierarchy1 = pat_path3.search(url).group(1)
                    url_hierarchy2 = pat_path3.search(url).group(2)
                    img_hierarchy = pat_path2.search(tmp).group(1)
                    img_abspath = url.replace(
                                url_hierarchy1+'/'+url_hierarchy2, img_hierarchy)
                    break
                else:
                    url_hierarchy = pat_path1.search(url).group(1)
                    img_abspath = url.replace(url_hierarchy, tmp)
                    break
                break
    return img_abspath, extension

class ReadHtml(object):
    """
    webサイトからHtmlを取り込むクラス
    """
    def __init__(self, url):
        self.url = url
        
    def readhtml(self):
        req = Request(self.url, headers={'User-Agent': 'Magic Browser'})
        page_html = urlopen(req).read().decode('utf-8')
        return page_html

class ImageParse(ReadHtml):
    """
    webサイトから画像を取り込むクラス
    """
    def parseimage(self, directory_path, relativepath='', img_title=''):
        directory_path = directory_path+'\\'+relativepath
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        page_html = self.readhtml()
        a_tag = pat_a1.findall(page_html)
        img_tag = pat_img1.findall(page_html)
        for tag in a_tag:
            img_url.append(parse_img_path(self.url, tag, pat_a2))
        for tag in img_tag:
            img_url.append(parse_img_path(self.url, tag, pat_img2))
        return img_url, directory_path

imageparse = ImageParse(url)
relativepath=input('"C:\\Users\\User\\Pictures"下の保存先のフォルダ名 > ')
img_url, directory_path = imageparse.parseimage(directory_path, relativepath)

for url, extension in img_url:
    if url:
        pat_imgname = re.compile(r'(.*)[.|:|/](.+?%s)'%extension)
        img_name = pat_imgname.search(url).group(2)
        if '?' in img_name:
            img_name = img_name.split('?')[1].split('=')[1]
        filepath=directory_path+'\\'+img_name
        image_download(url, filepath)
        

def delete_gintama():
    gintamajpg_names=glob.glob('C:\\Users\\User\\Pictures\\gintama\\*.jpg')
    for gintamajpg in gintamajpg_names:
        flag=False
        with open(gintamajpg, 'rb') as ginsan:
            ginread=ginsan.read()
            if len(ginread)==5138:
                flag=True
        if flag:
            os.remove(gintamajpg)


#delete_gintama()

#dirname='C:\\Users\\User\\Pictures\\gintama2'
#if not os.path.exists(dirname):
#    os.makedirs(dirname)
    
def rename_gintama(dirname):
    gintamajpg_names=glob.glob('C:\\Users\\User\\Pictures\\gintama\\*.jpg')
    for i,gintamajpg in enumerate(gintamajpg_names):
        with open(gintamajpg, 'rb') as ginsan:
            ginread=ginsan.read()
        new_file_name=dirname+'/'+'gintama%d.jpg'%i
        with open(new_file_name, 'wb') as ginsan:
            ginsan.write(ginread)


        
