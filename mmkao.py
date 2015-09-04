# coding:utf8

import urllib, urllib2
import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
import os, sys, time
from pprint import pprint

TIMEOUT = 60

imageCount = 0

pwd = sys.path[0] + os.sep + "img" + os.sep # 设置图片存放路径为 当前文件夹下的img文件夹
if os.path.exists(pwd) == False: # 若img文件夹不存在 新建文件夹img
    os.makedirs(pwd)

# 访问连接,并对其数据 BeautifulSoup
def readPage(url):
    soup = None
    try:
        print u"请求网址为: %s" % url
        response = requests.get(url, timeout = TIMEOUT)
        response.encoding = 'gb2312'
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception, e:
        print e
    return soup

def analyzeMainList(soup, url):
    mainList = list()
    for a in soup.select(".photo > li > a"):
        mainList.append(url + a.attrs["href"])
    # print mainList
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
    localPath = pwd + url.split("/")[4] + "-" + url.split("/")[5] + "-" + url.split("/")[6].replace("\r","")
    print u'%s 开始下载!' % url
    try:
        r = requests.get(url, timeout = TIMEOUT)
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
    time.sleep(2)
    return imageAllList

def main():
    url = 'http://www.mmkao.com/ROSI/'
    maxPage = 1
    pool = Pool(processes=10)
    mainAllList = []
    for x in [pool.apply_async(getMainAllList, (i,url)) for i in range(1,maxPage + 1)]:
        mainAllList.append(x.get())
    pool.close()
    pool.join()
    print 'mainAllList', len(mainAllList)
    pool = Pool(processes=4)
    imageAllList = []
    for x in [pool.apply_async(getImageAllList, (main, mainAllList[0])) for main in mainAllList[0]]:
        imageAllList.extend(x.get())
    print 'imageAllList', len(imageAllList)
    pool.close()
    pool.join()
    pool = Pool(processes=4)
    for img in sorted(imageAllList):
        pool.apply_async(downloadImage, (img,))
    pool.close()
    pool.join()
    print '共下载%s张图片' % imageCount

        


if __name__ == "__main__":
    main()