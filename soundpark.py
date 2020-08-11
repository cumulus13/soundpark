#!c:/SDK/Anaconda2/python.exe
from __future__ import print_function
import traceback
import os, sys
from safeprint import print as sprint
#  import io
#  sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
#  sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
os.environ.update({'PYTHONIOENCODING':'UTF-8'})
sys.excepthook = traceback.format_exc
import argparse
from bs4 import BeautifulSoup as bs
from pydebugger.debug import debug
from make_colors import make_colors
from configset import configset
import cfscrape
import clipboard
import time
import progressbar
try:
    import makelist
except:
    from . import makelist
#import requests
if sys.version_info.major == 3:
    from urllib.parse import urlparse, unquote
    raw_input = input
else:
    from urlparse import urlparse
    from urllib import unquote, quote
from getpass import getpass
import re
from pprint import pprint
import inspect
import argparse


class soundpark(object):
    def __init__(self, configname = 'soundpark.ini', username = None, password = None, download_path = os.getcwd(), login = True, bar=None):
        super(soundpark, self)
        self.configname = os.path.join(os.path.dirname(__file__), configname)
        self.conf = configset(self.configname)
        self.sess = cfscrape.Session()
        self.headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
        self.sess.headers.update(self.headers)
        #self.sess = requests.session()
        self.url = 'https://sound-park.world'
        label = make_colors('[Connection]', 'white', 'blue')
        self.prefix = '{variables.task} >> {variables.subtask}'
        self.variables =  {'task': '--', 'subtask': '--'}
        self.max_value = 10
        self.bar = bar
        if not self.bar:
            self.bar = progressbar.ProgressBar(max_value = self.max_value, prefix = self.prefix, variables = self.variables)
        self.username = username
        self.password = password
        if login:
            self.login()
            
    def seedr(self, torrent):
        try:
            from seedr2.seedr import seedr
        except:
            seedr2_module = self.conf.get_config('seedr', 'path')
            if not seedr2_module:
                seedr2_module = raw_input('Please input seedr module path: ')
                if not os.path.isdir(seedr2_module):
                    return False
                else:
                    self.conf.write_config('seedr', 'path', seedr2_module)
            sys.path.insert(0, seedr2_module)
            debug(sys_path = sys.path)
            #self.pause()
            try:
                from seedr2.seedr import seedr
            except:
                traceback.format_exc(detach=False)
                from seedr import seedr
                    
        st = seedr()
        st.add(torrent)
        cprocess = 'start cmd /c "seedr2 -s -sd"'
        os.system(cprocess)

    def del_evenReadonly(self, action, name, exc):
        import stat
        os.chmod(name, stat.S_IWRITE)
        os.remove(name)
            
    def show_image(self, url, cover_dir):
        try:
            from . import download
        except:
            import download
        download.download_img(url, cover_dir)
        try:
            import tkimage
        except:
            from . import tkimage
        from multiprocessing import Process
        tx = Process(target=tkimage.main, args=(cover_dir, ))
        tx.start()
        
    def progress(self, value, task, subtask, tcf='lw', tcg='bl', stcf = 'b', stcg = 'lg', tattr = [], stattr = [], max_value=None):
        task = make_colors(task, tcf, tcg, attrs=tattr)
        subtask = make_colors(subtask, stcf, stcg, attrs=stattr) + " "
        if max_value:
            self.bar.max_value = max_value
        return self.bar.update(value, task=task, subtask=subtask)
        
    def pause(self, page=''):
        lineno = str(inspect.stack()[1][2])
        import msvcrt
        if page:
            page = make_colors("[" + str(page) + "]", "lw", "bl")
        else:
            page = make_colors("[" + str(lineno) + "]", "lw", "bl")
        note = make_colors("Enter to Continue . ", "lw", "lr") + "[" + page + "] " + make_colors("x|q = exit|quit", "lw", "lr")
        print(note)
        q = msvcrt.getch()
        if q == 'x' or q == 'q':
            sys.exit(make_colors("EXIT !", 'lw','lr'))
        
    def login(self, username = None, password = None, cookies = None, url_back = None, timeout = 60):
        if not cookies:
            cookies = {}
        if not url_back:
            url_back = self.url
        if not username:
            username = self.username
        if not password:
            password = self.password
        if not username:
            username = self.conf.get_config('auth', 'username')
        if not password:
            password = self.conf.get_config('auth', 'password')
        if not username:
            username = raw_input('USERNAME or EMAIL: ')
        if not password:
            password = getpass('PASSWORD:')
        url = self.url + '/login'
        data = {
            'username': username,
            'password': password,
            'returnto': url_back,
            'return': 'yes',
            'is_submit': 'ENTER',
        }
        debug(data = data)
        n = 1
        error_get = False
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3860.5 Safari/537.36',
        }
        self.sess.headers.update(headers)
        debug(sess_header = self.sess.headers)
        while 1:
            self.progress(5, "[LOGIN]", "login")
            try:
                a = self.sess.post(url, data = data, timeout = timeout, cookies = cookies, headers = headers)
                content = a.content
                #print("Content [login] =", content)
                debug(content = content)
                cookies = a.cookies.get_dict()
                debug(cookies = cookies)
                debug(sess_cookies = self.sess.cookies)
                debug(headers = a.headers)
                self.progress(10, "[LOGIN]", "success")
                return content, self.sess
                #break
            except:
                n += 1
                self.progress(10, "[LOGIN]", "ERROR [" + str(n) + "]", stcf="lw", stcg="lr", stattr=['blink'])
                if n == 10:
                    error_get = True
                    break
                    
        debug(error_get = error_get, debug = True)
        if error_get:
            self.progress(10, "[LOGIN]", "Timeout Expected !", stcf="lw", stcg="lr", stattr=['blink'])
            sys.exit()
        debug(len_content = len(content))
        return content, self.sess
        
        
    def proxy(self, proxy):
        debug(proxy = proxy)
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
        elif isinstance(proxy, str) or isinstance(proxy, unicode):
            debug("proxy is str")
            scheme = urlparse(self.url).scheme
            debug(scheme = scheme)
            proxy_list.update({scheme: scheme + "://" +proxy ,})
            debug(proxy_list = proxy_list)
            return proxy_list
        return {}

    def home(self, url = None, cookies = None, timeout = 5, content = None, sess = None):
        if sess:
            self.sess = sess
        data = {}
        n = 1
        t = 1
        error_get = False
        if not cookies:
            cookies = {}
        debug(cookies = cookies)
        if not url:
            url = self.url
        debug(url = url)
        
        if not content:
            while 1:
                self.progress(5, "[GET-Home]", "start")
                try:
                    self.bar.label = make_colors("[GET-Home]", 'black', 'yellow')
                    a = self.sess.get(url, cookies = cookies, timeout = timeout)
                    self.progress(5, "[GET-Home]", "finish")
                    break
                except:
                    self.bar.update(t)
                    t += 1
                    if t == 10:
                        error_get = True
                        break
            if error_get:
                self.progress(10, "[HOME]", "Timeout Expected !", stcf="lw", stcg="lr", stattr=['blink'])
                sys.exit(make_colors("Timeout Expected !", 'lightwhite', 'lightred', ['blink']))

            content = a.content
            cookies = a.cookies.get_dict()
            debug(cookies = cookies)
        #debug(cls = 'cls')
        #print("content =", content)
        #debug(content = content)
        b = bs(content, 'lxml')
        title_release = b.find('div', {'id': 'left-column',}).find_all('h1', {'class': 'index_title',})
        debug(title_release = title_release)
        ul_release = b.find('div', {'id': 'left-column',}).find_all('ul', {'class': 'releases',})
        debug(ul_release = ul_release)
        
        nb = 1
        m = 1
        for i in title_release:
            self.progress(nb, "[Listing]", str(nb)+"st", max_value=len(title_release))
            data.update({n: {'title_release': i.text, 'data': {}}})
            #debug(data = data)
            genres = {}
            data_ul_release = ul_release[title_release.index(i)]
            all_li = data_ul_release.find_all('li')
            debug(all_li = all_li)
            
            #m = 1
            for x in all_li:
                a = x.find('a')
                link = a.get('href')
                debug(link = link)
                thumb = a.find('div', {'class': 'img_header2_right',}).find('img').get('src')
                debug(thumb = thumb)
                title = a.find('div', {'class': 'img_header2_right',}).find('img').get('alt')
                debug(title = title)
                data_genres = x.find('div', {'class': 'genres',})
                a_genres = data_genres.find_all('a')
                for g in  a_genres:
                    genres.update({
                        g.get('title'): re.sub("\n", "", g.get('href')),
                    })
                debug(genres = genres)
                data.get(n).get('data').update(
                    {
                        m: {
                            'title': title,
                            'thumb': thumb,
                            'link': link,
                            'genres': genres,                            
                        }
                    })
                m += 1
            nb += 1
            n += 1
            self.progress(len(title_release), "[Listing]", "done", max_value=len(title_release))
        self.bar.max_value = self.max_value
        debug(data = data)
        
        div_last_release = b.find('div', {'id': 'right-column',}).find_all('div', {'class': 'lastreleases',})
        debug(div_last_release = div_last_release)
        new_music = {}
        w = 1
        for i in  div_last_release:
            a = i.find('a')
            link = a.get('href')
            title = a.get('title')# .encode('utf-8')
            thumb = a.find('img').get('src')
            span = i.find('span').text
            debug(span = span)
            new_music.update({
                w: {
                    'title': title,
                    'link': link,
                    'thumb': thumb,
                },
            })
            w += 1
        debug(new_music = new_music)
        return data, new_music, b, cookies
    
    def genres(self, bs_object = None, url = None, timeout = 3):
        data = {}
        #bar = progress.Bar(expected_size = 10, label = '[GET-Genres]')
        n = 1
        t = 1
        error_get = False
        if not bs_object:
            if not url:
                url = self.url
            while 1:
                self.progress(5, "[GET-All-Genres]", "start")
                try:
                    a = self.sess.get(url, timeout = timeout)
                    self.progress(10, "[GET-All-Genres]", "finish")
                    bs_object = bs(a.content, 'lxml')
                    break
                except:
                    self.progress(t, "[Get-All-Genres]", "try !")
                    t += 1
                    if t == 10:
                        error_get = True
                        break                        
            
        if error_get:
            self.progress(self.bar.max_value, "[Get-All-Genres]", "Timeout Expected !", stcf="lw", stcg="lr", stattr=['blink'])
            sys.exit(make_colors("Timeout Expected !", 'lightwhite', 'lightred', ['blink']))
        div_bottom = bs_object.find('div', {'id': 'bottom',})# .find('nav', {'id': 'genre-block'})
        debug(div_bottom = div_bottom)
        #genre_titles = div_bottom.find_all('a', {'class': re.compile('gl'),})
        #debug(genre_titles = genre_titles, debug = True)
        genre_lists = div_bottom.find_all('ul', {'id': 'genre_list',})
        debug(genre_lists = genre_lists)
        for x in genre_lists:
            genre_titles = x.find_all('a', {'class': re.compile('gl'),})
            debug(genre_titles = genre_titles)
            #self.pause()
            for i in genre_titles:
                #data.update({n: {'title': i.text, 'data': {},}})
                data.update({n: {'title': i.text.lower(), 'link': i.get('href'),}})
                #all_li_genre_list = genre_lists[genre_titles.index(i)].find_all('li')
                #  m = 1
                #  for x in  all_li_genre_list:
                    #  a_link = x.find('a')
                    #  link = a_link.get('href')
                    #  title = a_link.text
                    #  a_data = {title: link,}
                    #  data.get(n).get('data').update({m: a_data,})
                    #  m += 1
                n += 1
        debug(data = data)
        return data
        
    def set_colored(self, background):
        foreground = 'white'
        if 'green' in background:
            foreground = 'white'
        elif 'white' in background:
            foreground = 'red'
        elif 'cyan' in  background:
            foreground = 'white'
        
        return foreground, background
    
    def details(self, url, sess = None, timeout = 10, print_list = True, max_try=100):
        clipboard.copy(url)
        if sess:
            self.sess = sess
        nt = 1
        debug(url = url)
        #self.pause()
        while 1:
            self.progress(50, "[Get-Details]", "start", max_value=max_try)
            try:
                a = self.sess.get(url, timeout = timeout)
                self.progress(100, "[Get-Details]", "finish", max_value=max_try)
                self.bar.max_value = self.max_value
                break
            except:
                #traceback.format_exc()
                self.progress(nt, "[Get-Details]", "re-connecting", stcf="lw", stcg="lr", stattr=['blink'], max_value=max_try)
                if nt == 100:
                    self.progress(100, "[Get-Details]", "Timeout Expected !", stcf="lw", stcg="lr", stattr=['blink'])
                    self.bar.max_value = self.max_value
                    return False, make_colors("[Get-Details] Timeout Expected !", 'lw','lr', ['blink'])
                else:
                    nt += 1                
                    self.progress(nt, "[Get-Details]", "re-connecting", stcf="lw", stcg="lr", stattr=['blink'], max_value=max_try)
                    
                
        b = bs(a.content, 'lxml')
        info_torrents = {}
        div_idetails = b.find('div', {'class': 'idetails',})
        cover = b.find('img', {'class':'linked-image'}).get('src')
        info_torrents.update({'cover':cover})
        debug(cover = cover)
        a_link_uploader = div_idetails.find('a')
        debug(a_link_uploader = a_link_uploader)
        uploader = a_link_uploader.text
        debug(uploader = uploader)
        info_torrents.update({'uploader':uploader})
        link_uploader = a_link_uploader.get('href')
        debug(link_uploader = link_uploader)
        info_torrents.update({'link_uploader':link_uploader})
        idetails = re.split(":|Date|Remove from favorites|\!|Add to favorites|\n|Added|  |Views| : ", div_idetails.text)
        debug(idetails = idetails)
        idetails = list(filter(None, idetails))
        debug(idetails = idetails)
        added = idetails[0].strip()
        debug(added = added)
        info_torrents.update({'added':added})
        views = idetails[2].strip()
        debug(views = views)
        info_torrents.update({'views':views})
        div_details_list = b.find('ul', {'class': 'details-list',})
        debug(div_details_list = div_details_list)
        link_download = div_details_list.find('a', {'class': 'dnl',}).get('href')
        debug(link_download = link_download)
        info_torrents.update({'link_download':link_download})
        download_content = self.sess.get(self.url + link_download)
        #print("download_content:")
        #print(download_content.content)
        debug(download_header = download_content.headers)
        all_li = div_details_list.find_all('li')
        debug(all_li = all_li)
        all_li_text = []
        for i in all_li:
            all_li_text.append(i.text)
        debug(all_li_text = all_li_text)
        #pprint(all_li_text)
        data_artist = {}
        #link_download = ''
        for i in all_li_text:
            if ":" in i:
                key = None
                value = None
                data = re.split(": |\n|\t", i)
                debug(data = data)
                adding = True
                if len(data) == 2:
                    key, value = data
                    if 'ALBUM' in key:
                        key = re.split(" / ", key)[0]
                    elif 'DATE' in key:
                        key = re.split(" / ", key)[1]                    
                    elif 'DURATION' in key:
                        key = key.strip()[:-1]
                    elif 'RATING' in key:
                        value = "/".join(list(filter(None, re.split(" |  |/", value)))[:2])
                    elif 'VOTE' in key:
                        adding = False
                    elif 'DOWNLOAD' in key:
                        adding = False
                    if adding:
                        data_artist.update({key.strip(): value.strip(),})
                if len(data) == 3:
                    key1, key2, value = data
                    debug(data = data)
                    debug(key1 = key1)
                    debug(key2 = key2)
                    debug(value = value)
                    #self.pause()
                    if 'Clients' in key1:
                        seeds = re.findall('(\d+).*?/', value)
                        debug(seeds = seeds)
                        peers = re.findall('Peers:(.*?).$', value)
                        debug(peers = peers)
                        data_artist.update({'SEEDS': seeds[0],'PEERS': peers[0].strip(),})
                    elif 'DOWNLOAD' in key1:
                        downloaded = re.findall('(\d+)\)', value)[0].strip()
                        data_artist.update({'DOWNLOADED': downloaded,})
                    elif 'Size' in key1:
                        size = re.findall('\d+.*?[aA-zZ]{2}', key2)[0].strip()
                        data_artist.update({'SIZE': size,})
                        files = re.findall('(\d+)\)', value)[0].strip()
                        data_artist.update({'FILES': files,})
                    
        debug(data_artist = data_artist)
        
        n = 1
        description = b.find('div', {'class': 'descr',})
        debug(description = description)
        #self.pause()
        data_desc = ''
        if description:
            data_desc = description.text
        debug(data_desc = data_desc)
        data_desc = unquote(data_desc.encode('utf-8'))
        tracks = {}
        if data_desc:
            all_cd = b.find_all('div', {'class':'headfolder folded clickable'})
            all_cd_title = b.find_all('span', {'style':'font-size:18px'})
            debug(all_cd = all_cd)
            debug(all_cd_title = all_cd_title)
            
            #self.pause()
            all_tracks = None
            pre_info_add = []
            info_add = []
            if description.find('strong'):
                debug("description strong")
                #self.pause()
                all_tracks = re.split("\d+:\d.*?\.|\d+:\d{2}|\d+\.", data_desc)
                debug(all_tracks = all_tracks)
                all_tracks = list(filter(None, all_tracks))
                debug(all_tracks = all_tracks)
                all_duration = re.findall("\d+:\d{2}", data_desc)
                debug(all_duration = all_duration)
                all_titles_add = []
                tn = 1
                for i in all_tracks:
                    debug(i = i)
                    if all_duration:
                        try:
                            duration = all_duration[all_tracks.index(i)],
                            if "(" == i.strip()[-1]:
                                title = i.strip()[:-1]
                            else:
                                title = i.strip()
                            all_titles_add.append({'track': tn, 'title': title, 'duration': duration[0]})
                            tn += 1
                        except IndexError:
                           pre_info_add.append(i)
                        #finally:
                        #    traceback.format_exc()
                            
                    else:
                        all_titles_add.append({'track': tn, 'title': i.strip(), 'duration': ''})
                        tn += 1
                debug(pre_info_add = pre_info_add)
                
                for i in pre_info_add:
                    if ")" == i[0]:
                        info_add.append(i[1:])
                debug(info_add = info_add)
                #self.pause()
                debug(all_titles_add = all_titles_add)
                tracks.update({"CD1":all_titles_add})
                #self.pause()
            elif description.find('span') and not all_cd:
                debug("description span")
                #data_desc = re.sub(" :", ": \n", data_desc)
                #data_desc = re.sub('(\d+\.)', r'\n\1', data_desc)
                self.pause()
                #print(data_desc)
                span = description.find('span')
                span_extract = span.extract()
                debug(span_extract = span_extract)
                re_data1 = re.sub('(<span.*?>)','', str(span_extract))
                debug(re_data1 = re_data1)
                re_data2 = re.sub('</span><br/><br/>', '\n', re_data1)
                debug(re_data2 = re_data2)
                re_data3 = re.sub('<br/>', '\n', re_data2)
                debug(re_data3 = re_data3)
                tracks = re.sub('</span>', '', re_data3)
                debug(tracks = tracks)
                #print("\n")
                #print(re_data4)
                self.pause()
            elif description.find('br') and not all_cd:
                debug("description br")
                #self.pause()
                tracks =  str(re.sub('(\s)(\d+.)', r'\n\2', data_desc))
                debug(tracks = tracks)
                #self.pause()
            else:
                debug("description else")
                #self.pause()
                all_track_percd = description.find_all(['div', 'span'], {'class':'bodyfolder'})
                debug(all_track_percd = all_track_percd)
                #self.pause()
                if all_track_percd:
                    debug(all_track_percd_text = all_track_percd[0].text)
                
                for i in all_cd:
                    cd = i.text
                    tracks.update({cd:{}})
                    all_titles = re.split('\d+\..', all_track_percd[all_cd.index(i)].find('p').text)
                    debug(all_titles = all_titles)
                    all_titles = list(filter(None, all_titles))
                    all_titles_add = []
                    debug(all_titles = all_titles)
                    tn = 1
                    for t in all_titles:
                        if unquote(t).strip():
                            duration = re.findall("\d+:\d{2}", t)
                            if not duration:
                                duration = ''
                            all_titles_add.append({'track': tn, 'title': t.strip(), 'duration': duration})
                            tn+=1
                    
                    debug(all_titles_add = all_titles_add)
                    tracks.update({cd:all_titles_add})
                debug(tracks = tracks)
            
        if print_list:
            print("\n")
            for i in data_artist:
                if data_artist.get(i):
                    print(make_colors(str(i), 'cyan') + (13 - len(str(i))) * " "  + " : " + make_colors(unquote(data_artist.get(i).encode('utf-8')), 'yellow'))
            print(make_colors("PLAYLIST:", 'white', 'blue'))
            if isinstance(tracks, str):
                print(make_colors(tracks, 'lc'))
                print("\n")
            else:
                for i in tracks:
                    print(make_colors(unquote(i.encode('utf-8')), 'lw','bl') + ": ")
                    this_tracks = tracks.get(i)
                    for i in this_tracks:
                        number = str(i.get('track'))
                        if len(number) == 1 and len(this_tracks) > 9:
                            number = '0' + number
                        elif len(number) == 1 and len(this_tracks) > 99:
                            number = '00' + number
                        elif len(number) == 2 and len(this_tracks) > 99:
                            number = '0' + number                
                        print("   " + make_colors(number, 'green') + ". " + make_colors(sprint(i.get('title')), 'lightcyan') + " [" + make_colors(sprint(i.get('duration')), 'white') + "]")
            if info_add:
                print(make_colors("\n".join(info_add), 'lm'))
                    
        data_video = b.find('iframe')
        if data_video:
            data_video = data_video.get('src')
            debug(data_video = data_video)
            if print_list:
                if data_video:
                    print(make_colors('VIDEO:', 'black', 'green') + " " + make_colors(data_video, 'ly'))
        
        return data_artist, tracks, data_video, link_download, download_content.content, info_torrents
            
    def get_genre(self, url, uploaded_for = None, sort_by = None, on_page = None, sorting = None, active_only = None, lossly_only = None, sess = None, data = None, page = None, rtype = 'get', timeout = 5, login = False, max_try=100):
        debug(url = url)
        data_sort_by = ['date', 'title', 'pop', 'rating']
        if sess:
            self.sess = sess
        nt = 1
        params = {}
        if page:
            params.update({'page': str(page),})
        if uploaded_for and str(uploaded_for).isdigit():
            params.update({'interval': str(uploaded_for), 'filter': '1',})
        if sort_by and sort_by in data_sort_by:
            params.update({'sort': sort_by, 'filter': '1',})
        if on_page and str(on_page).isdigit():
            params.update({'num': on_page, 'filter': '1',})
        if sorting:
            if sorting == 'desc':
                params.update({'desc': 'yes', 'filter': '1',})
            elif sorting == 'asc':
                params.update({'desc': 'no', 'filter': '1',})
        if active_only:
            if isinstance(active_only, bool):
                params.update({'seed': '1', 'filter': '1',})
            elif isinstance(active_only, int) and active_only == 1:
                params.update({'seed': '1', 'filter': '1',})
            elif isinstance(active_only, int) and str(active_only).strip() == '1':
                params.update({'seed': '1', 'filter': '1',})
        if lossly_only:
            if isinstance(lossly_only, bool):
                params.update({'lossless': '1', 'filter': '1',})
            elif isinstance(lossly_only, int) and lossly_only == 1:
                params.update({'lossless': '1', 'filter': '1',})
            elif isinstance(lossly_only, int) and str(lossly_only).strip() == '1':
                params.update({'lossless': '1', 'filter': '1',})
        
        if login:
            self.login()
        if uploaded_for or sort_by or on_page or sorting or active_only or lossly_only:
            rtype = 'post'
        
        while 1:
            try:
                if rtype == 'post':
                    self.progress(50, "[Get-Genre]", "start" , max_value=max_try)
                    a = self.sess.post(url, timeout = timeout, data = params)
                else:
                    a = self.sess.get(url, timeout = timeout, params = params)
                self.progress(1, "[Get-Genre]", "processing" , max_value=max_try)
                self.bar.max_value = self.max_value
                break
            except:
                self.progress(nt, "[Get-Genre]", "re-connecting", stcf="lw", stcg="lr", stattr=['blink'], max_value=max_try)
                if nt == 100:
                    self.progress(100, "[Get-Genre]", "Timeout Expected !", stcf="lw", stcg="lr", stattr=['blink'])
                    self.bar.max_value = self.max_value
                    break
                else:
                    nt += 1                
                    self.progress(nt, "[Get-Genre]", "re-connecting", stcf="lw", stcg="lr", stattr=['blink'], max_value=max_try)
                
        b = bs(a.text, 'lxml')
        #  with open(os.path.join(os.path.dirname(__file__), 'result.html'), 'wb') as f:
            #  f.write(str(a.content))
        #  with open(os.path.join(os.path.dirname(__file__), 'result2.html'), 'wb') as f:
            #  f.write(str(b))
        #debug(b = b)
        left_column = b.find('div', {'id':'columns'})
        debug(left_column = left_column)
        all_table = left_column.find_all('table', {'class': 'browse_albums',})
        debug(all_table = all_table)
        if not all_table:
            return {}
        if not data:
            data = {}
        n = 1
        self.bar.max_value = len(all_table)
        for i in all_table:
            data.update({n:{}})
            if n > len(all_table):
                n = len(all_table)
            self.progress(n, "[Get-Genre]", "processing")
            all_tr = i.find_all('tr')
            #for x in all_tr:
            all_td_0 = all_tr[0].find_all('td')
            data_title = all_td_0[0].find_all('a')
            title = data_title[0].text
            debug(title = title)
            #data.get(n).update({'title':title})
            link = data_title[0].get('href')
            debug(link = link)
            #data.get(n).update({'link':link})
            ng = 1
            genres = {}
            data_genres = data_title[1:]
            for g in data_genres:
                genres.update({
                    ng: {
                        'name': g.text,
                        'link': g.get('href'),
                    },
                })
            debug(genres = genres)
            #data.get(n).update({'genres':genres})
            data_idetails = all_td_0[1]
            debug(data_idetails = data_idetails)
            date = data_idetails.find('span').text
            debug(date = date)
            #data.get(n).update({'date':date})
            data_rating = data_idetails.find('div', {'itemprop': 'aggregateRating',}).find_all('span')
            debug(data_rating = data_rating)
            rating = ''
            votes = ''
            if len(data_rating) == 2:
                rating = data_rating[0].text
                votes = data_rating[1].text
            else:
                rating = data_rating[0].text
            debug(rating = rating)
            #data.get(n).update({'rating':rating})
            debug(votes = votes)
            data.update({n: {'votes':votes}})
            link_download = data_idetails.find('a', {'class': 'dnl',}).get('href')
            debug(link_download = link_download)
            #data.get(n).update({'download':link_download})
            all_text = data_idetails.text
            debug(all_text = all_text)
            comments = re.findall("Comments:(.*?)Views", all_text)
            debug(comments = comments)
            #data.get(n).update({'comments':comments[0].strip()})
            views = re.findall("Views:(.*?)DOWNLOAD", all_text)
            debug(views = views)
            #data.get(n).update({'views':views[0].split("\t")[0].strip()})
            thumb = all_tr[1].find('a').find('img').get('src')
            debug(thumb = thumb)
            #data.get(n).update({'thumb':thumb})
            data_artist = all_tr[1].find('td', {'class': 'descr',})
            span_artist = data_artist.find('span', {'itemprop': 'byArtist',})
            artist = span_artist.find('span', {'itemprop': 'name',}).text
            debug(artist = artist)
            #data.get(n).update({'artist':artist})
            album = span_artist.find('span', {'itemprop': 'album',}).text
            debug(album = album)
            #data.get(n).update({'album':album})
            all_text = data_artist.text
            debug(all_text = all_text)
            #release = re.findall("Release year / Date:(.*?)Country", all_text)
            release = re.findall("Release year / Date:(.*?\d{4})", all_text)
            if not release:
                release = [""]
            debug(release = release)
            #data.get(n).update({'release':release[0].strip()})
            country = re.findall("Country:(.*?)Style", all_text)
            if not country:
                country = [""]
            debug(country = country)
            #data.get(n).update({'country':country[0].strip()})
            style = re.findall("Style:(.*?)Label", all_text)
            if not style:
                style = re.findall("Style:(.*?)Site", all_text)
            if not style:
                style = re.findall("Style:(.*?)Duration", all_text)
            if not style:
                style = re.findall("Style:(.*?)File", all_text)            
            debug(style = style)
            if not style:
                style = ["--"]
            #data.get(n).update({'style':style[0].strip()})
            label = re.findall("Label:(.*?)Duration", all_text)
            debug(label = label)
            if not label:
                label = re.findall("Label:(.*?)File Format:", all_text)
                debug(label = label)
            if not label:
                label = [""]
                #data.get(n).update({'label':label[0].strip()})
            duration = re.findall("Duration:(.*?)File Format", all_text)
            debug(duration = duration)
            if not duration:
                duration = [""]
            #data.get(n).update({'duration':duration[0].strip()})
            file_format = re.findall("File Format:(.*?)Quality", all_text)
            debug(file_format = file_format)
            #data.get(n).update({'format':file_format[0].strip()})
            quality = re.findall("Quality:(.*?)$", all_text)
            debug(quality = quality)
            #data.get(n).update({'quality':quality[0].strip()})
            #site = [""]
            site = re.findall("Site:(.*?)Duration", all_text)
            if not site:
                site = [""]
                #data.get(n).update({'site':site[0].strip()})
            #n += 1
            try:
                data.update({
                    n: {
                        'title': title,
                        'link': link,
                        'genres': genres,
                        'date': date,
                        'rating': rating,
                        'votes': votes,
                        'download': link_download,
                        'comments': comments[0].strip(),
                        'views': views[0].split("\t")[0].strip(),
                        'thumb': thumb,
                        'artist': artist,
                        'album': album,
                        'release': release[0].strip(),
                        'country': country[0].strip(),
                        'style': style[0].strip(),
                        'label': label[0].strip(),
                        'duration': duration[0].strip(),
                        'format': file_format[0].strip(),
                        'quality': quality[0].strip(),
                        'site': site[0].strip(),
                    },
                })
                n += 1
            except:
                debug(all_text = all_text, debug = True)
                traceback.format_exc()
                self.pause()
        #self.pause()
        #pprint(data)
        debug(rtype = rtype)
        debug(params = params)
        self.progress(len(all_table), "[Get-Genre]", "finish")
        print("\n")
        return data

    def search(self, query, sess = None, timeout = 5, max_try=30):
        if sess:
            self.sess = sess
        data = {}
        url = self.url + '/search'
        debug(url = url)
        query = query.replace(' ', '+')
        debug(query = query)
        params = {'q': query,}
        debug(params = params)
        nt = 1
        while 1:
            self.progress(max_try/2, "[Search]", "start", max_value=max_try)
            try:
                a = self.sess.get(url, params = params, timeout = timeout)
                self.progress(max_try, "[Search]", "done", max_value=max_try)
                break
            except:
                self.progress(nt, "[Search]", "re-connecting", stcf="lw", stcg="lr", stattr=['blink'], max_value=max_try)
                if nt == max_try:
                    self.progress(max_try, "[Search]", "Timeout Expected !", stcf="lw", stcg="lr", stattr=['blink'])
                    self.bar.max_value = self.max_value
                    break
                else:
                    nt += 1                
                    self.progress(nt, "[Search]", "re-connecting", stcf="lw", stcg="lr", stattr=['blink'], max_value=max_try)
                
        b = bs(a.content, 'lxml')
        result = 0
        div_search_result = b.find('div', {'id': 'searth_result',})
        debug(div_search_result = div_search_result)
        if div_search_result:
            result = re.findall("results(.*?)album", div_search_result.text)
            debug(result = result)
            if result:
                result = result[0].strip()
        debug(result = result)
        #self.pause()
        if not result:
            return {}
        else:
            all_div = b.find('div', {'id': 'content',}).find_all('div', {'class': 'div-rellist',})
            n = 1
            for i in all_div:
                data_thumb = i.find('i').find('a')
                thumb = data_thumb.find('img').get('src')
                debug(thumb = thumb)
                link = data_thumb.get('href')
                debug(link = link)
                data_title = i.find('h3').find('a')
                title = data_title.text
                debug(title = title)
                data_genres = i.find('div').find_all('a')[1:]
                genres = {}
                ng = 1
                for g in data_genres:
                    name = g.text
                    glink = g.get('href')
                    genres.update({
                        ng: {
                            'name': name,
                            'link': glink,
                        },
                    })
                    ng += 1
                debug(genres = genres)
                data.update({
                    n: {
                        'thumb': thumb,
                        'link': link,
                        'title': title,
                        'genres': genres,
                    },
                })
                n += 1
        #pprint(data)
        return data
        
    def print_nav(self, note=1):
        if note == 2:
            note1 = make_colors("[e[x]it or [q]uit for exit]: ", "lightwhite", "red") + ", " + make_colors("Download it with seedr [y]: ", 'white', 'blue')
        else:
            note1 = "Select number for details" + " (" + make_colors("[n]t = set for last numbers day", 'white', 'blue') + ", " + make_colors("desc|ast = sort by descending or ascending", 'white', 'magenta') + ", " + make_colors("sd = sort by date", 'white', 'green') + ", " + make_colors("sn = sort by name", 'black', 'cyan') + ", " + make_colors("sp = sort by popularity", 'red', 'white') + ", " + make_colors("sr = sort by ratting", 'black', 'white') + ", " + make_colors("sa = show for active torrent only", 'black', 'yellow') + ", " +  make_colors("sl = show lossly only (default lossly and mp3)", 'white', 'blue') + ", " + make_colors("c = show by genre or type 'c=[genre_name]'", 'white', 'blue') + ", " + make_colors("lg = show all genres", 'black', 'yellow') + ", " + make_colors("r = reset all setting", 'white', 'red') + ", " + make_colors("w = refresh", 'green') + ", " + make_colors("h = goto Home", 'white', 'magenta') + ", " + make_colors("x|q = exit/quit", 'white', 'red') + " " + make_colors("or you can type anything for searching", 'lw', 'bl') + ", " + make_colors("all of set can type on one line", 'cyan') + ": "
        q = raw_input(note1)
        return q
    
    def navigator(self, login = True, data = None, new_music = None, all_genres = None, print_list = True, uploaded_for = '360', sort_by = 'date', on_page = '40', sorting = 'desc', active_only = None, lossly_only = None, use_genre = False, search = False):
        sess = None 
        link_download = None
        debug(data = data)
        #self.pause()
        if login:
            login_content, sess = self.login()
        if not data and not search:
            data, new_music, bs_object, cookies = c.home(sess = sess)
        #if not all_genres and not search:
        if not all_genres and not search:
            all_genres = self.genres(bs_object)
        else:
            if not all_genres:
                all_genres = self.genres()
        #debug(all_genres = all_genres)
        #self.pause()
        choice = ['green', 'cyan', 'magenta', 'red']
        debug(data = data)
        #from pprint import  pprint
        #pprint(data)
        if not data and not search:
            sys.exit(make_colors("No Data !", 'white', 'red', ['blink']))
        if print_list and not search:
            if data:
                debug(data = data)
                #self.pause()
                if use_genre:
                    for i in data:
                        debug(data_get_i = data.get(i))
                        if data.get(i):
                            genres = []
                            genre_list = data.get(i).get('genres')
                            debug(genre_list = genre_list)
                            if genre_list:
                                for g in genre_list:
                                    genres.append(genre_list.get(g).get('name'))
                                debug(genres = genres)
                            number = ''
                            if len(str(i)) == 1:
                                number = '0' + str(i)
                            else:
                                number = str(i)
                            genre_str = ''
                            debug(genres = genres)
                            if genre_list:
                                genre_str = "\\".join(genres)[:10] + " ..."
                            title = data.get(i).get('title')
                            debug(title = title)
                            if title:
                                title = title#.encode('utf-8')
                            else:
                                title = ''
                            release = data.get(i).get('release')
                            debug(release = release)
                            if release:
                                release = release.encode('utf-8')
                            else:
                                release = ''
                            duration = data.get(i).get('duration')
                            debug(duration = duration)
                            if not duration:
                                duration = ''
                            views = data.get(i).get('views')
                            debug(views = views)
                            if not views:
                                views = ''
                            try:
                                print(" " + make_colors(str(number) + ".", 'cyan') + " " + make_colors(title, 'yellow') + "[" +  make_colors(release, 'white', 'blue') + "] [" + make_colors(duration, 'black', 'green') + "] [" + make_colors(views, 'white', 'magenta') + "] [" + make_colors(genre_str, 'black', 'white') + "]" + " ")
                            except:
                                sprint(" " + make_colors(str(number) + ".", 'cyan') + " " + make_colors(title, 'yellow') + "[" +  make_colors(release, 'white', 'blue') + "] [" + make_colors(duration, 'black', 'green') + "] [" + make_colors(views, 'white', 'magenta') + "] [" + make_colors(genre_str, 'black', 'white') + "]" + " ")
                            #self.pause()
                else:
                    nc = 0
                    for i in data:
                        title_release = data.get(i).get('title_release')
                        try:
                            print(make_colors(title_release.encode('utf-8'), 'white', 'blue') + ": ")
                        except:
                            pass
                        datas = data.get(i).get('data')
                        if datas:
                            fore, back = self.set_colored(choice[nc])
                            nc += 1
                            for x in datas:
                                genres = []
                                genre_list = datas.get(x).get('genres')
                                for genre in genre_list:
                                    genres.append(genre)
                                debug(genres = genres)
                                if len(str(x)) == 1:
                                    number = '0' + str(x)
                                else:
                                    number = str(x)
                                print(" " + make_colors(str(number) + ". " + datas.get(x).get('title').encode('utf-8'), fore, back) + "[" + make_colors("\\".join(genres)[:10] + " ...", 'black', 'white') + "]")
            print("\n")
        else:
            #  def search(self, query, sess = None, timeout = 5, max_try=30):
            #debug(search = search, debug = True)
            if search:
                data = self.search(search, sess)
                debug(data = data)
                if print_list:
                    nc = 0
                    print("\n")
                    for i in data:
                        if len(str(i)) == 1:
                            number = '0' + str(i)
                        else:
                            number = str(i)
                        fore, back = self.set_colored(choice[nc])
                        if nc == 3:
                            nc = 0
                        else:
                            nc += 1
                        genres = []
                        genre_list = data.get(i).get('genres')
                        debug(genre_list = genre_list)
                        for genre in genre_list:
                            genres.append(genre_list.get(genre).get('name'))
                            debug(genres = genres)
                        try:
                            print(make_colors(str(number) + ". " + data.get(i).get('title').encode('utf-8'), fore, back) + "[" + make_colors("\\".join(genres)[:20] + " ...", 'black', 'white') + "]")
                        except:
                            sprint(make_colors(str(number) + ". " + data.get(i).get('title'), fore, back) + "[" + make_colors("\\".join(genres)[:20] + " ...", 'black', 'white') + "]")
                    print("\n")
        q = self.print_nav()
        debug(q = q)
        if q:
            if not os.path.isdir(os.path.join(os.path.dirname(__file__), 'cover_downloads')):
                os.makedirs(os.path.join(os.path.dirname(__file__), 'cover_downloads'))
            else:
                import shutil
                shutil.rmtree(os.path.join(os.path.dirname(__file__), 'cover_downloads'), onerror = self.del_evenReadonly)
                os.makedirs(os.path.join(os.path.dirname(__file__), 'cover_downloads'))
            debug(q = str(q).strip())
            #self.pause()
            if str(q).strip().isdigit():
                torrent_file = None
                d = None
                if not search:
                    if use_genre:
                        link = self.url + data.get(int(str(q).strip())).get('link')
                        debug(link = link)
                        data_artist, data_playlist, data_video, link_download, magnet, info_torrents = self.details(link)
                        debug(magnet = magnet)
                        debug(link_download = link_download)
                        if link_download:
                            try:
                                from . import download
                            except:
                                import download
                            torrent_file = download.download(self.url + link_download, download_path="torrent_downloads", session = self.sess, remove_str = "\[Sound-Park.ru\] ")
                        cover_link = self.url + info_torrents.get('cover')
                        self.show_image(cover_link, os.path.join(os.path.dirname(__file__), 'cover_downloads'))
                    else:
                        for i in data:
                            if data.get(i).get('data').get(int(str(q).strip())):
                                d = data.get(i).get('data').get(int(str(q).strip()))
                                if d:
                                    link = self.url + d.get('link')
                                    debug(link = link)
                                    
                                    data_artist, data_playlist, data_video, link_download, magnet, info_torrents = self.details(link)
                                    debug(magnet = magnet)
                                    debug(link_download = link_download)
                                    if link_download:
                                        try:
                                            from . import download
                                        except:
                                            import download
                                        torrent_file = download.download(self.url + link_download, download_path="torrent_downloads", session = self.sess, remove_str = "\[Sound-Park.ru\] ")
                                        #qd = raw_input("Download it ? [y/n] or just enter: ")
                                        #if qd and str(qd).strip() == 'y':
                                        #    torrent_file = download.download(self.url + link_download, download_path="torrent_downloads")
                                    break
                        cover_link = self.url + info_torrents.get('cover')
                        self.show_image(cover_link, os.path.join(os.path.dirname(__file__), 'cover_downloads'))
                        if not d:
                            print(make_colors("No Data Found !", "lightwhite", "lightred"))
                            qr = raw_input(make_colors("Enter to Continue ! [e[x]it or [q]uit for exit]: ", "lightwhite", "blue"))
                            if qr == 'x' or qr == 'y' or qr == 'q':
                                sys.exit(make_colors("System Exit !", "lightwhite", "lightred"))
                else:
                    link = self.url + data.get(int(q)).get('link')
                    debug(link = link, debug = True)
                                
                    data_artist, data_playlist, data_video, link_download, magnet, info_torrents = self.details(link)
                    debug(magnet = magnet, debug = True)
                    debug(link_download = link_download)
                    if link_download:
                        try:
                            from . import download
                        except:
                            import download
                            torrent_file = download.download(self.url + link_download, download_path="torrent_downloads", session = self.sess, remove_str = "\[Sound-Park.ru\] ")
                            #qd = raw_input("Download it ? [y/n] or just enter: ")
                            #if qd and str(qd).strip() == 'y':
                            #    torrent_file = download.download(self.url + link_download, download_path="torrent_downloads")
                    cover_link = self.url + info_torrents.get('cover')
                    self.show_image(cover_link, os.path.join(os.path.dirname(__file__), 'cover_downloads'))
                qr = self.print_nav(2)
                if qr == 'x' or qr == 'q':
                    sys.exit(make_colors("System Exit !", "lightwhite", "lightred"))
                elif qr == 'y':
                    self.seedr(torrent_file)
                return self.navigator(False, data, all_genres = all_genres, use_genre = use_genre)
            elif str(q).strip() == 'x' or str(q).strip() == 'q':
                sys.exit(make_colors("Exit Bye .. bye ..", 'white', 'red'))
            elif str(q).strip() == 'r':
                return self.navigator(False, data, new_music, all_genres, False)
            elif str(q).strip() == 'h':
                return self.navigator(False)
            elif str(q).strip() == 'lg':
                if not all_genres:
                    all_genres = self.genres()
                all_genres_print = []
                for i in all_genres:
                    all_genres_print.append(all_genres.get(i).get('title'))
                #makelist.makeList(all_genres_print, 4)
                sprint(" / ".join(all_genres_print))
                return self.navigator(False, data, new_music, all_genres, False, use_genre = use_genre, search = search)
            elif str(q).strip() == 'w':
                if sys.platform == 'win32':
                    os.system('cls')
                else:
                    os.system('clear')                
                return self.navigator(False, data, new_music, all_genres, print_list, uploaded_for, sort_by, on_page, sorting, active_only, lossly_only, use_genre, search)
            elif re.findall("c=(.*?)$.*?", str(q).strip()) or re.findall("c=(.*?)$", str(q).strip()) or str(q).strip() == 'c':
                #data_sort_by = ['date', 'title', 'pop', 'rating']
                qc = ''
                if str(q).strip() == 'c':
                    qc = raw_input(make_colors("Genre Name: ", 'white', 'blue'))
                else:
                    q = str(q).strip()
                    if "=" in re.findall("c=(.*?) ", str(q).strip()):
                        qc = re.findall("c=(.*?) ", str(q).strip())[0].strip()
                    else:
                        qc = re.findall("c=(.*?)$", str(q).strip())[0].strip()
                
                debug(qc = qc)
                #self.pause()
                check_sort_rate = re.findall('.*?(sr.).*?', q)
                check_sort_pop = re.findall('.*?(sp.).*?', q)
                check_sort_name = re.findall('.*?(sn.).*?', q)
                check_sort_date = re.findall('.*?(sd.).*?', q)
                if check_sort_rate and  check_sort_rate[0].strip() == 'sr':
                    sort_by = 'rating'
                elif check_sort_pop and check_sort_pop[0].strip() == 'sp':
                    sort_by = 'pop'
                elif check_sort_name and check_sort_name[0].strip() == 'sn':
                    sort_by = 'title'
                elif check_sort_date and check_sort_date[0].strip() == 'sd':
                    sort_by = 'date'
                
                check_sort_desc = re.findall('.*?(.desc.).*?', q)
                if check_sort_desc and  check_sort_desc[0].strip() == 'desc':
                    sorting ='desc'                                
                check_sort_asc = re.findall('.*?(.asc.).*?', q)
                if check_sort_asc and check_sort_asc[0].strip() == 'asc':
                    sorting ='asc'                                
                check_sort_active_only = re.findall('.*?(sa.).*?', q)
                if check_sort_active_only and check_sort_active_only[0].strip() == 'sa':
                    active_only = True                         
                check_sort_lossy_only = re.findall('.*?(sl.).*?', q)
                if check_sort_lossy_only and check_sort_lossy_only[0].strip() == 'sl':
                    lossly_only = True                
                check_number_days = re.findall('.*?(\d+t).*?', q)
                if check_number_days and check_number_days[-1] == 't' and check_number_days[:-1].isidigit():
                    uploaded_for = check_number_days[:-1]
                debug(qc = str(qc).strip())
                #self.pause()
                if qc:
                    genre_found = ''
                    for i in all_genres:
                        if all_genres.get(i).get('title') == str(qc).strip():
                            genre_found = all_genres.get(i)
                            break
                    debug(genre_found = genre_found)
                    #self.pause()
                    if genre_found:
                        genre_url = self.url + genre_found.get('link')
                        debug(genre_url = genre_url)
                        #self.pause()
                        data = self.get_genre(genre_url, uploaded_for, sort_by, on_page, sorting, active_only, lossly_only, sess, login = False)
                        debug(data = data)
                        use_genre = True
                    #self.pause()
                    #  def navigator(self, login = True, data = None, new_music = None, all_genres = None, print_list = True, uploaded_for = '360', sort_by = 'date', on_page = '40', sorting = 'desc', active_only = None, lossly_only = None, use_genre = False, search = False):
                    if use_genre:
                        return self.navigator(False, data, new_music, all_genres, True, uploaded_for, sort_by, on_page, sorting, active_only, lossly_only, True)
                    else:
                        print(make_colors('No Data Genre', 'white', 'red', ['blink']))
                        return self.navigator(False, data, new_music, all_genres, False, use_genre = False)
                else:
                    print(make_colors('No Genre Input', 'white', 'red', ['blink']))
                    return self.navigator(False, data, new_music, all_genres, False, use_genre = False)                    
            else:
                return self.navigator(login=False, print_list=True, search = q)
        return self.navigator(False)
        
    def usage(self, bar=None):
        if bar:
            self.bar = bar
        parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
        parser.add_argument('SEARCH', help='Search for', action='store')
        parser.add_argument('-U', '--username', help='Username login', action='store')
        parser.add_argument('-P', '--password', help='Password login', action='store')
        parser.add_argument('-su', '--set-upload', help='Set upload for time filter, default: 360 for 360 days', action='store', default=360)
        parser.add_argument('-s', '--sort', help='Set sort by filter: "date", default: date', action='store')
        parser.add_argument('-sp', '--sort-page', help='Show numbers item per page, default 40 items per page', default=40)
        parser.add_argument('-st', '--sorting', help='Set shorting "desc" or "asc" of filter, default="desc"', default='desc')
        parser.add_argument('-sa', '--set-active', help='Set show for active torrent only of filter', action='store_true')
        parser.add_argument('-sl', '--set-lossy', help='Set download/show for lossy (ex: *.flac) of filter', action='store_true')
        parser.add_argument('-sg', '--set-use-genre', help='Set use genre filters', action='store_true')
        parser.add_argument('-g', '--genre', help='Change genre', action='store')
        parser.add_argument('-v', '--download-video', help='Download video is exists')
        parser.add_argument('-p', '--download-path', action='store', help='Download Path')
        parser.add_argument('-t', '--timeout', action='store', help='Set timeout requests second', default=5, type=int)
        parser.add_argument('--max-try', action='store', help='Set max trying or requests', default=30, type=int)
        
        if len(sys.argv) == 1:
            #parser.print_help()
            self.bar = progressbar.ProgressBar(max_value = self.max_value, prefix = self.prefix, variables = self.variables)
            print(make_colors('use "-h" for help', 'lr', 'lw'))
            self.navigator()
        elif len(sys.argv) == 2 and not sys.argv[1] in ['-g', '--genre', '-v', '--download-video', '-p', '--download-path']:
            self.bar = progressbar.ProgressBar(max_value = self.max_value, prefix = self.prefix, variables = self.variables)
            #self.search(sys.argv[1])
            self.navigator(True, None, None, None, True, search = sys.argv[1])
        else:
            self.bar = progressbar.ProgressBar(max_value = self.max_value, prefix = self.prefix, variables = self.variables)
            args = parser.parse_args()
            if args.SEARCH:
                self.search(args.SEARCH, args.timeout, args.max_try)
            else:
                #  def navigator(self, login = True, data = None, new_music = None, all_genres = None, print_list = True, uploaded_for = '360', sort_by = 'date', on_page = '40', sorting = 'desc', active_only = None, lossly_only = None, use_genre = False)
                if args.username or args.password:
                    login = True
                self.navigator(True, None, None, None, True, args.set_upload, args.sort, args.sort_page, args.sorting, args.set_active, args.set_lossy, args.set_use_genre)
        
if __name__ == '__main__':
    c = soundpark(login = False, bar = True)
    #c.navigator()
    #content, sess = c.login()
    c.usage()
    #c.details('https://sound-park.world/album/torrent-113233-fm-discography-1986-2020', sess)
    #c.details('https://sound-park.world/album/torrent-264829-inferno-requiem-shanhai-2019', sess)
    #c.details('https://sound-park.world/album/torrent-291318-motley-crue-goin-out-swinging-compilation-2cd-2020', sess)
    #c.details('https://sound-park.world/album/torrent-288082-iron-maiden-100-iron-maiden-2020', sess)
    #c.details('https://sound-park.world/album/torrent-160496-bad-company-rough-diamonds-fame-and-fortune-lossless-1982-1986', sess)
    #c.get_genre("https://sound-park.world/music/instrumental_rock", 360, 'title', 16, 'asc', 1, 1)
    #c.search('Tony Macalpine')
    #c.navigator(False)
    #cookies, headers, content = c.login()
    #print("Content =",  content, "[316]")
    #data, new_music, bs_object, cookies = c.home()
    #c.genres(bs_object)