from celery_app import app
import time,re
from urllib.parse import urljoin
from celery_app.downloader import send_request
from lxml.html import etree

baseUrl = 'http://www.xiachufang.com/category/104/'

def extract_first(dataList,default=None):
    if len(dataList) > 0:
        return dataList[0]
    else:
        return default

@app.task
def download1(url):
    html,url = send_request(url)
    return str(len(html))+'下载完毕1'


#ignore_result=True,忽略结果
@app.task(ignore_result=True)
def crawl_category_list(url):
    html, url = send_request(url=url)
    parse_category_data.delay(html)

@app.task
def parse_category_data(html):
    #解析分类的数据(名称，url地址，id)
    etree_html = etree.HTML(html)
    li_as = etree_html.xpath('//div[@class="cates-list-mini clearfix "]/ul/li/a')
    categorys = []
    for a in li_as:
        info = {}
        #标题
        info['title'] = extract_first(a.xpath('./text()'))
        #url地址
        info['url'] = extract_first(a.xpath('./@href'))
        #id
        info['id'] = re.search('\d+',info['url']).group()
        #full_url = 'http://www.xiachufang.com' + info['url']
        full_url = urljoin(baseUrl,info['url'])
        #根据分类url地址，发起请求
        print(full_url)
        crawl_caipu_list.delay(full_url,info['id'])

        categorys.append(info)

    return categorys

@app.task(ignore_result=True)
def crawl_caipu_list(url,categoryId):
    """
    根据分类的url地址，请求获取菜谱列表页面
    :param url:
    :param categoryId:
    :return:
    """
    html,url = send_request(url=url)
    etree_html = etree.HTML(html)
    #提取菜谱列表数据,获取菜谱详情url地址
    caipu_as = etree_html.xpath('//ul[@class="list"]/li//p[@class="name"]/a')
    print('===================',len(caipu_as))
    for a in caipu_as:
        caipu_url = urljoin(baseUrl,extract_first(a.xpath('./@href')))
        # 根据详情url请求，获取详情数据
        print('菜谱url地址',caipu_url)
        crawl_caipu_detail.delay(caipu_url,categoryId)
    #下一页
    next_url = extract_first(etree_html.xpath('//a[@class="next"]/@href'))
    if next_url:
        next_url = urljoin(baseUrl,next_url)
        crawl_caipu_list.delay(next_url,categoryId)



@app.task
def crawl_caipu_detail(url,categoryId):
    html,url = send_request(url=url)
    #解析菜谱详情数据
    etree_html = etree.HTML(html)
    detail = {}
    # 标题
    detail['title'] = extract_first(etree_html.xpath('//h1[@class="page-title"]/text()'),'')
    #categoryId
    detail['categoryId'] = categoryId
    return detail










