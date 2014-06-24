#!/usr/bin/python
#coding: utf-8

import urllib
import urllib2
import re
import time
import codecs
import os
import random
import socket
import ConfigParser

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


page_title = re.compile(r'<title>(.+?)</title>')
song_id = re.compile(r'song/(\d+)')
song_loction = re.compile(r'<location>(.+)</location>')
song_name = re.compile(r'<title>.*?<!\[CDATA\[(.+?)\]\]>.*?</title>')

def page_view(urlstr, parentdir='songs'):
    """
    return the title of a page, and all song ids in this page
    """

    try:
        response = urllib2.urlopen(add_header(urlstr))
    except:
        print 'Fail to retrieve song list, check your Internet connection:'
        print urlstr
        return False

    html = response.read()

    title = page_title.search(html)
    title = title.group(1).strip() if title else time.ctime()
    if u'专辑' in title:
        title = title[:title.index(u'专辑')]

    if not os.path.exists(parentdir):
        os.mkdir(parentdir)

    songids = set(song_id.findall(html))

    return valid_path(title), songids

def fetch_song(id, dir):
    """
    fetch a song of a given id, and save it under dir
    """

    socket.setdefaulttimeout(300)

    global song_loction, song_name

    try:
        response = urllib2.urlopen(add_header('http://www.xiami.com/song/playlist/id/%s'%id))
    except:
        print 'Fail to download song %s once, check your Internet connect'%id
        time.sleep(5)
        return False

    page = response.read()
    time.sleep(5)

    try:
        name = song_name.search(page).group(1).strip()
        name += '.mp3'
        addr = song_loction.search(page).group(1).strip()
    except:
        print page
        return False

    if os.path.exists(os.path.join(dir, valid_path(name))):
        return True

    song_addr = mp3_decode(addr.strip())
    try:
        print 'downloading', name
        urllib.urlretrieve(song_addr, os.path.join(dir, valid_path(name)))
        time.sleep(5)
        urllib.urlcleanup()
        return True

    except socket.timeout:
        return False

    except Exception, e:
        print name, e.message
        time.sleep(5)
        return False


def mp3_decode(s):

    col = int(s[0]) #number of column
    content = s[1:]
    basic = len(content)/col    #length of each row, the basic length
    extra = len(content)%col    #num of rows that are one char longer

    matrix = []
    index = 0
    for i in xrange(extra):
        matrix.append(content[index:index+basic+1])
        index += (basic+1)

    for i in xrange(col-extra):
        matrix.append(content[index:index+basic])
        index += basic


    url = ''
    for i in xrange(basic):
        for j in xrange(col):
            url += matrix[j][i]
    for i in xrange(extra):
        url += matrix[i][-1]

    url = urllib.unquote(url)
    url = url.replace('^', '0')

    return url

def add_header(urlstr):
    """
    add headers for a url, return a request
    """
    agents = [("User-Agent", "Chrome/23.0.1271.64"),
    ("User-Agent", "Chrome/20.0.371.32"),
    ("User-Agent", "Chrome/32.1.1238.64"),
    ("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1"),
    ("User-Agent", "Opera/8.0 (Macintosh; PPC Mac OS X; U; en)"),
    ("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13"),
    ("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) "),
    ("User-Agent", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;)"),
    ("User-Agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"),
    ("User-Agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"),
    ("User-Agent", "Internet Explorer 7 (Windows Vista)"),
    ("User-Agent", "Mozilla/4.0 (compatible; MSIE 4.01; Windows XP)"),
    ("User-Agent", "Mozilla/4.5 [ja] (Win7; I)"),
    ("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:9.0.1) Gecko/20100101 Firefox/9.0.1"),
    ("User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)"),
    ("User-Agent", "Internet Explorer 9 (Windows 7)"),
    ("User-Agent", "Opera/7.51 (Windows NT 5.1; U)"),
    ("User-Agent", "Opera/7.50 (Windows XP; U)"),
    ("User-Agent", "Mozilla/4.8 [en] (Windows NT 5.1; U)"),
    ("User-Agent", "Netscape 4.8 (Windows Vista)"),
    ("User-Agent", "Opera/7.50 (Windows XP; U)"),
    ("User-Agent", "Chrome/32.3.1352.64"),
    ("User-Agent", "Chrome/27.2")]
    request = urllib2.Request(urlstr)
    agent = agents[random.randint(0, len(agents)-1)]
    request.add_header(agent[0], agent[1])
    request.set_proxy('202.195.192.197:3128','http')

    return request



def valid_path(name):
    return name.replace('"','').replace('?','').replace('*','').replace('<','').replace('>','')\
        .replace('&#039;', "'").strip()


if __name__=='__main__':

    config = ConfigParser.ConfigParser()
    config.readfp(codecs.open('config', 'rb', 'utf-8'))
    urls = set(map(lambda x:x.strip(), config.get('global', 'url').split(';')))
    outdir = config.get('global', 'outdir')

    for url in urls:
        album, songids = page_view(url, outdir)
        if not os.path.exists(os.path.join(outdir, album)):
            os.mkdir(os.path.join(outdir, album))
        for songid in songids:
            print 'processing', songid
            try:
                fetch_song(songid, os.path.join(outdir, album))
            except:
                print 'fail to download', songid