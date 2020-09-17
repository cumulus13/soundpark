#!c:/SDK/Anaconda2/python.exe
from __future__ import print_function
import requests
from datetime import datetime
import sys, os
#import clipboard
#import argparse
if sys.version_info.major == 3:
    from urllib.parse import urlparse
    raw_input = input
else:
    from urlparse import urlparse

import re
from clint.textui import progress
from make_colors import make_colors
#from zipfile import ZipFile
from pydebugger.debug import debug

import cfscrape
#from mimetypes import guess_extension
import ast
import mimelist
cf = cfscrape.create_scraper()
from pause import pause

def proxy(proxy):
    proxy_list = {}
    if isinstance(proxy, list):
        for i in proxy:
            if "{" in i[0]:
                n = ast.literal_eval(i)
                if isinstance(n, dict):
                    proxy_list.update(n)
            else:
                j = urlparse(i)
                scheme = j.scheme
                netloc = j.netloc
                if "www." in netloc:
                    netloc = netloc.split('www.')[1]
                #if ":" in netloc:
                    #netloc = netloc.split(":")[0]
                proxy_list.update({scheme:scheme + "://" + netloc})
        return proxy_list
    elif isinstance(proxy, dict):
        return proxy
    return {}

def download(url, download_path = "downloads", saveas = None, proxies = {}, session = None, add_ext = False, max_try = 10, overwrite = True, remove_str = None):
    debug(url = url)
    debug(saveas = saveas)
    debug(download_path = download_path)
    debug(proxies = proxies)
    if not os.path.isdir(download_path):
        os.makedirs(download_path)
    if proxies:
        proxies = proxy(proxies)
    debug(proxies = proxies)
    if not session:
        session = cf
    if saveas:
        if saveas.lower() == 'poster' or saveas.lower() == 'thumb':
            session = cf    
    if not saveas:
        saveas = "file_" + datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')
    if download_path:
        saveas = os.path.join(download_path, saveas)
    n = 0
    progress_bar = progress.Bar(expected_size = 10, label = "connecting: ")
    error = False
    while 1:
        try:
            a = session.get(url, proxies = proxies)
            progress_bar.show(10)
            break
        except:
            progress_bar.label = "re-connecting: "
            progress_bar.show(n)
            n += 1
            if n == max_try:
                print(make_colors("Timeout Expected !", 'lightwhite', 'lightred', ['blink']))
                error = True
                break
    if error:
        return False
    headers = a.headers
    length = ''
    ext = ""
    debug(headers = headers)
    #raw_input("Enter to Continue")
    content_disposition = headers.get('Content-Disposition')
    if content_disposition:
        saveas = re.findall('filename+=+"(.*?)"$', content_disposition)[0]
        if download_path:
            saveas = os.path.join(download_path, saveas)

    length = headers.get('content-length')
    if length:
        length = int(length)
    ext = headers.get('Content-Type')
    debug(ext = ext)
    if ext:
        ext = mimelist.get(ext)
    label = "downloading " + os.path.basename(saveas) + ": "
    if add_ext and ext:
        saveas = saveas + "." + ext
    debug(add_ext = add_ext)
    debug(ext = ext)
    debug(saveas = saveas)
    if not overwrite:
        if os.path.isfile(saveas):
            q = raw_input(make_colors("overwrite file %s ? [y/n]: ", 'lightred', 'lightwhite', ['blink']))
            if q == 'y':
                pass
            else:
                try:
                    os.remove(saveas)
                except:
                    pass
    if remove_str:
        if isinstance(remove_str, list) or isinstance(remove_str, tuple):
            for i in remove_str:
                saveas = re.sub(i, "", saveas)
        elif isinstance(remove_str, str):
            debug(saveas = saveas)
            debug(remove_str = remove_str)
            saveas = re.sub(remove_str, "", saveas)
            debug(saveas = saveas)
    if length:
        with open(saveas, 'wb') as f:
            for ch in progress.bar(a.iter_content(chunk_size = 2391975), label, expected_size = (length/1024) + 1, ):
                if ch:
                    f.write(ch)
        if not os.path.splitext(saveas)[1].lower() == ".torrent" and not add_ext:
            saveas = saveas + ".torrent"
    else:
        print(make_colors("No Length data !", 'lightwhite', 'lightred', ['blink']))
        print(make_colors("Save As:", 'white', 'red') + " " + make_colors(saveas, 'red', 'white'))
        with open(saveas, 'wb') as f:
            f.write(a.content)
    return saveas

def download_img(url, download_path = os.getcwd(), saveas = None, proxies = {}, add_ext = False, max_try = 10, overwrite = True):
    if proxies:
        proxies = {}
    debug(url = url)
    debug(saveas = saveas)
    debug(download_path = download_path)
    debug(proxies = proxies)
    if proxies:
        proxies = proxy(proxies)
    debug(proxies = proxies)
    if not saveas:
        saveas = "file_" + datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')
    if download_path:
        saveas = os.path.join(download_path, saveas)
    n = 0
    progress_bar = progress.Bar(expected_size = 10, label = "connecting: ")
    a = None
    while 1:
        try:
            a = requests.get(url, proxies = proxies, timeout = 3)
            progress_bar.show(10)
            break
        except:
            n += 1
            progress_bar.label = "re-connecting: "
            progress_bar.show(n)
            if n == max_try:
                print(make_colors("Timeout Expected !", 'lightwhite', 'lightred', ['blink']))
                progress_bar.show(10)
                break

    headers = a.headers
    length = ''
    ext = ""
    debug(headers = headers)
    
    content_disposition = headers.get('Content-Disposition')
    if content_disposition:
        if 'filename=' in content_disposition:
            saveas_pre = re.split('attachment|;|filename|=',content_disposition)[-1]
            if download_path and saveas_pre:
                saveas = os.path.join(download_path, saveas_pre)

    length = headers.get('content-length')
    if not length:
        length = headers.get('Content-Length')
    debug(length = length)
    
    if length:
        length = int(length)
    ext = headers.get('Content-Type')
    debug(ext = ext)
    if ext:
        ext = mimelist.get2(ext)
        if ext:
            ext = ext[1]
    debug(ext = ext)
    
    label = "downloading " + os.path.basename(saveas) + ": "
    if add_ext and ext:
        saveas = saveas + "." + ext
    if saveas and not os.path.splitext(saveas)[1]:
        saveas = saveas + "." + ext
    debug(add_ext = add_ext)
    debug(ext = ext)
    debug(saveas = saveas)
    
    if not overwrite:
        if os.path.isfile(saveas):
            q = raw_input(make_colors("overwrite file %s ? [y/n]: ", 'lightred', 'lightwhite', ['blink']))
            if q == 'y':
                pass
            else:
                try:
                    os.remove(saveas)
                except:
                    pass
    debug(length = length)
    if length:
        with open(saveas, 'wb') as f:
            for ch in progress.bar(a.iter_content(chunk_size = 2391975), label, expected_size = (length/1024) + 1, ):
                debug(ch = ch)
                if ch:
                    f.write(ch)
        if not os.path.isfile(saveas):
            with open(saveas, 'wb') as f:
                f.write(a.content)
    else:
        print(make_colors("No Length data !", 'lightwhite', 'lightred', ['blink']))

    return saveas