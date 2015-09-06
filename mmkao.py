#!/usr/bin/env pyhton
#coding:utf8

import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
import os, sys, time

TIMEOUT = 30

imageCount = 0

imgType = ('Beautyleg', 'RQ-STAR', 'ROSI', 'ligui', 'Ugirls', 'XiuRen', 'DISI', 'NAKED-ART', 'PANS', '3Agirl', 'ShowTimeDancer', 'MYGIRL')

def setPath(url):
    path = sys.path[0] + os.sep + "img" + os.sep + url.split("/")[-3] + os.sep + url.split("/")[-2].split(url.split("/")[-3])[1] + os.sep# 设置图片存放路径
    if os.path.exists(path) == False: # 若文件夹不存在 新建文件夹img
        os.makedirs(path)
    return path

def request(url):
    try:
        headers = {
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Cache-Control': 'max-age=0',
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9'
             }
        response = requests.get(url, headers = headers, timeout = TIMEOUT)
    except requests.exceptions.Timeout, e:
        print '-' * 100
        print 'url: %s\nreason: %s' % (url, e)
        print '-' * 100
    except Exception, e:
        print e
    return response

# 访问连接,并对其数据 BeautifulSoup
def readPage(url):
    soup = None
    try:
        print u"请求网址为: %s" % url
        response = request(url)
        response.encoding = 'gb2312'
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception, e:
        print e
    return soup

def analyzeMainList(soup, url):
    mainList = list()
    if soup:
        for a in soup.select(".photo > li > a"):
            mainList.append(url + a.attrs["href"])
    return mainList

def analyzeImagePageList(soup, url):
    imageListPage = list()
    imageListPage.append(url)
    for a in soup.select(".image > a")[1:-1]:
        imageListPage.append(url[:url.rfind('/') + 1] + a.attrs["href"])
    # print imageListPage
    return imageListPage

def analyzeImageList(soup):
    imageList = list()
    for image in soup.select(".file > img"):
        imageList.append(image.attrs["src"].split('\r')[0])
    return imageList

def downloadImage(url):
    path = setPath(url)
    localPath = path + url.split("/")[4] + "-" + url.split("/")[5] + "-" + url.split("/")[6]
    print u'%s 开始下载!' % url
    try:
        r = request(url)
        f = open(localPath, 'wb')
        f.write(r.content)
    except Exception, e:
        print e
    else:
        global imageCount
        imageCount += 1
        print u'%s 下载完成!' % localPath
    finally:
        f.close()
        print '=' * 100

def reporthook(blocks_read, block_size, total_size):
    if not blocks_read:
        print 'Connection opened'
        return
    if total_size < 0:
        print 'Read %d blocks (%d bytes)' % (blocks_read, blocks_read * block_size)
    else:
        amount_read = blocks_read * block_size
        print 'Read %d blocks, or %d/%d' % (blocks_read, amount_read, total_size)
    return

def getMainAllList(i, url):
    if i == 1:
        mainListSoup = readPage(url)
    else:
        mainListSoup = readPage('%s%s.html' % (url, i))
    return analyzeMainList(mainListSoup, url)

def getImageAllList(main, mainAllList):
    try:
        imageListSoup = readPage(main)
        imagePageList = analyzeImagePageList(imageListSoup, main)
        imageAllList = list()
        for imagePage in imagePageList:
            if imagePage == main:
                imageList = analyzeImageList(imageListSoup)
            else:
                imageListSoup = readPage(imagePage)
                imageList = analyzeImageList(imageListSoup)
            imageAllList.extend(imageList)
    except Exception, e:
        print e
    time.sleep(2)
    return imageAllList

def main():
    imgTypeIndex = -1
    minPage = -1
    maxPage = -1
    while not 0 <= imgTypeIndex < len(imgType):
        try:
            imgTypeIndex = int(raw_input('Please entry img type index[0-11]: '))
        except Exception, e:
            imgTypeIndex = -1
            print e
    while not 0 < minPage:
        try:
            minPage = int(raw_input('Please entry min page: '))
        except Exception, e:
            minPage = -1
            print e
    while not minPage <= maxPage:
        try:
            maxPage = int(raw_input('Please entry max page: '))
        except Exception, e:
            maxPage = -1
            print e
    url = 'http://www.mmkao.com/%s/' % imgType[imgTypeIndex]
    pool1 = Pool(processes=10)
    mainAllList = []
    for x in [pool1.apply_async(getMainAllList, (i,url)) for i in range(minPage,maxPage + 1)]:
        mainAllList.extend(x.get())
    pool1.close()
    pool1.join()
    print 'mainAllList: ', len(mainAllList)
    pool2 = Pool(processes=5)
    imageAllList = []
    for x in [pool2.apply_async(getImageAllList, (main, mainAllList)) for main in mainAllList]:
        imageAllList.extend(x.get())
    print 'imageAllList', len(imageAllList)
    pool2.close()
    pool2.join()
    pool3 = Pool(processes=10)
    for img in sorted(imageAllList):
        pool3.apply_async(downloadImage, (img,))
    pool3.close()
    pool3.join()
    print '共下载%s张图片' % imageCount

if __name__ == "__main__":
    main()
