# coding:utf8

import urllib, urllib2
from bs4 import BeautifulSoup
import os, sys

pwd = sys.path[0] + os.sep + "img" + os.sep # 设置图片存放路径为 当前文件夹下的img文件夹
if os.path.exists(pwd) == False: # 若img文件夹不存在 新建文件夹img
    os.makedirs(pwd)

# 访问连接,并对其数据 BeautifulSoup
def readPage(url):
    soup = None
    try:
        print u"请求网址为:" + url
        response = urllib2.urlopen(url)
        soup = BeautifulSoup(response.read())
    except Exception, e:
        raise e
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
        imageList.append(image.attrs["src"])
    return imageList


def downloadImage(url):
    # print url
    localPath = pwd + url.split("/")[4] + "-" + url.split("/")[5] + "-" + url.split("/")[6].replace("\r","")
    try:
        print url + u'开始下载!'
        filename, msg = urllib.urlretrieve(url, localPath.replace("\r",""), reporthook = reporthook)
    except Exception, e:
        raise e
    finally:
        urllib.urlcleanup()
        print localPath + u'下载完成!'


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


if __name__ == "__main__":
    url = 'http://www.mmkao.com/ROSI/'
    maxPage = 33
    mainAllList = list()
    for i in range(1,maxPage + 1):
        if i == 1:
            mainListSoup = readPage(url)
        else:
            mainListSoup = readPage(url + str(i) + '.html')
        mainList = analyzeMainList(mainListSoup, url)
        mainAllList.extend(mainList)
    n = 0
    for main in mainAllList:
        n = n + 1
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
        m = 0
        for image in imageAllList:
            m = m + 1
            downloadImage(image)
        print u"第" + str(n) + u"组已下完,还剩" + str(len(mainAllList) - m) + u"组图片"
        print u"="*40
        print u"="*40



