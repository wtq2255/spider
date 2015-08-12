# encoding:utf-8
import urllib2,urllib,xlwt
from bs4 import BeautifulSoup



def getTitle(item):
    """获取文章题目，传入 HTML ，获取其题目并返回"""
    title = item.find('li','title_li').find_all('a')[1].string
    if title:
        return title
    else:
        tit = ""
        for t in item.find('li','title_li').find_all('a')[1].strings:
            tit += t
        return tit

def getJournal(item):
    """获取文章期刊日期，传入 HTML ，获取其期刊日期并返回"""
    journal = item.find('li','greencolor').find_all('a')[1].string
    return journal

def getAuthor(item):
    """获取文章作者，传入 HTML，获取其作者并返回"""
    authors = item.find('li','greencolor').find_all('a')[2:]
    result = ""
    for author in authors:
        result += author.string + ','
    # authors1 = item.find('li','greencolor').find_all('span')[3:]
    # for author in authors1:
    #     result += author.string + ','
    return result

def getKey(item):
    """获取文章关键词，传入 HTML，获取其关键词并返回"""
    key = item.find('p','greencolor').get_text()
    return key

def setExcel(sheet,title, journal, author, key, x):
    """写入 Excel 单元格，传入 Excel表名，题目，期刊号，作者，关键词，行号"""
    # print title, journal, author, key, x
    for i in range(0,4):
        if i == 0:
            sheet.write(x,i,title)
        if i == 1:
            sheet.write(x,i,journal)
        if i == 2:
            sheet.write(x,i,author)
        if i == 3:
            sheet.write(x,i,key)
        
    


if __name__ == '__main__':
    # 设置 Excel
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('journals', cell_overwrite_ok=True)
    sheet.write(0,0,'论文题目')
    sheet.write(0,1,'期刊')
    sheet.write(0,2,'作者')
    sheet.write(0,3,'关键词')

    print "开始下载数据"
    for x in range(5,6):
        # url = """http://librarian.wanfangdata.com.cn/SearchResult.aspx?dbhit=wf_qk%3a2438|wf_xw%3a0|wf_hy%3a0|nstl_qk%3a0|nstl_hy%3a0&q=%E6%9C%9F%E5%88%8A%E2%80%94%E5%88%8A%E5%90%8D%3a%28%E4%B8%AD%E5%8D%8E%E8%A1%8C%E4%B8%BA%E5%8C%BB%E5%AD%A6%E4%B8%8E%E8%84%91%E7%A7%91%E5%AD%A6%E6%9D%82%E5%BF%97%29+*+Date%3a-2015&db=wf_qk|wf_xw|wf_hy|nstl_qk|nstl_hy&p="""
        url = "http://librarian.wanfangdata.com.cn/SearchResult.aspx?dbhit=wf_qk%3a736%7cwf_xw%3a0%7cwf_hy%3a0%7cnstl_qk%3a0%7cnstl_hy%3a0&q=期刊—刊名%3a(中华行为医学与脑科学杂志)+*+Date%3a2013-2014&db=wf_qk%7cwf_xw%7cwf_hy%7cnstl_qk%7cnstl_hy&p="
        print "开始请求第" + str(x) + "页"
        html = urllib2.urlopen(url + str(x)) # 通过urllib2请求URL
        soup = BeautifulSoup(html)
        list_ul = soup.find_all('ul','list_ul')
        items = list()
        for i in range(0, len(list_ul),2):
            items.append(list_ul[i])
        for i in range(len(items)):
            setExcel(sheet,getTitle(items[i]),getJournal(items[i]),getAuthor(items[i]),getKey(items[i]),(x-1)*50+i+1)  
            print getTitle(items[i])
            print "第", (x-1)*50+i+2 , "行写入完毕"
            book.save('journals.xls')
    print "数据下载完毕！"







