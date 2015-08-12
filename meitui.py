# coding: utf-8

#####################################################
## 作者： witKernel
## 创始时间：2014-07-23

## 描述： 
##     下载 美腿网 网站图片 http://www.meitui.co/

## 注意：
##     需要BeautifulSoup支持

## 日志：

#####################################################

import os, sys
import urllib2,urllib
from bs4 import BeautifulSoup

min_page = 0
max_page = 505

pwd = sys.path[0] + os.sep + "img" + os.sep # 设置图片存放路径为 当前文件夹下的img文件夹
if os.path.exists(pwd) == False: # 若img文件夹不存在 新建文件夹img
    os.makedirs(pwd)

for i in range(min_page, max_page + 1):
    url = "http://www.meitui.co/club/thread-" + str(i) + "-1-1.html" # 设置请求网址

    try:
        html = urllib2.urlopen(url) # 通过urllib2请求URL
        soup = BeautifulSoup(html)
        img_src_parent = soup.findAll("div", { "class" : "tip_c xs0" })
        if not img_src_parent:
        	print '抱歉，' + str(i) + '不存在或已被删除或正在被审核'
        	continue
        n = 0
        for j in img_src_parent:
            img_src_a = j.a
            img_src = img_src_a.attrs["href"] # 取出img标签中src属性值，即获取图片URL
            if not img_src:
            	print '抱歉，' + str(i) + '不存在图片'
            	continue
            img_data = urllib.urlopen(img_src)
            name = pwd + str(i) + "-" + str(n) + ".jpg" # 设置图片路径即名称
            f = open(name, "wb") # 新建图片文件
            f.write(img_data.read()) #下载并保存图片
            f.close() # 关闭IO流
            print img_src 
            print (name + " Saved!")
            n += 1
            print "-" * 40

    except Exception:
    	print str(i) + "is Error!"
        pass
    print "+" * 40

print "Download completed!"
