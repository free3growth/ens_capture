'''
2021年500强财富爬取
QQ：28928247
# '''
# -*- coding: UTF-8 -*-
import requests, random
import os
from lxml import etree
import xlsxwriter


class Httprequest(object):
    ua_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36Chrome 17.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0Firefox 4.0.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    ]

    @property  # 把方法变成属性的装饰器
    def random_headers(self):
        return {
            'User-Agent': random.choice(self.ua_list)
        }


class Get_data(Httprequest):
    def __init__(self):
        self.murl = "http://www.fortunechina.com/fortune500/c/2021-08/02/content_394571.htm"

    def get_data(self, url):
        html = requests.get(url, headers=self.random_headers, timeout=5).content.decode('utf-8')
        req = etree.HTML(html)
        data = []
        zc = req.xpath('//div[@class="top"]/div[@class="table"]/table/tr[4]/td[2]/text()')
        gdqy = req.xpath('//div[@class="top"]/div[@class="table"]/table/tr[5]/td[2]/text()')
        jlr = req.xpath('//div[@class="top"]/div[@class="table"]/table/tr[7]/td[3]/text()')
        zcsyl = req.xpath('//div[@class="top"]/div[@class="table"]/table/tr[8]/td[3]/text()')
        #data.extend(zc)
        #data.extend(gdqy)
        #data.extend(jlr)
        #data.extend(zcsyl)
        #print(data)
        return data

    def get_mdata(self):
        html = requests.get(self.murl, headers=self.random_headers, timeout=5).content.decode('utf-8')
        # print(html)
        req = etree.HTML(html)
        rankings = req.xpath('//table[@class="wt-table"]/tbody/tr/td[1]/text()')
        companys = req.xpath('//table[@class="wt-table"]/tbody/tr/td[2]/a/text()')
        incomes = req.xpath('//table[@class="wt-table"]/tbody/tr/td[3]/text()')
        profits = req.xpath('//table[@class="wt-table"]/tbody/tr/td[4]/text()')
        hrefs = req.xpath('//table[@class="wt-table"]/tbody/tr/td[2]/a/@href')
        data_list = []
        for ranking, company, income, profit, href in zip(
                rankings, companys, incomes, profits, hrefs
        ):
            data = [
             company
            ]
            href = href.replace('../', '')
            href = "http://www.fortunechina.com/{}".format(href)
            data.extend(self.get_data(href))

            print(data)
            data_list.append(data)
        print('\n')
        print(data_list)
        #self.write_to_mxlsx(data_list)

    def write_to_mxlsx(self, data_list):
        mypath = os.path.dirname((os.path.abspath(__file__)))
        workbook = xlsxwriter.Workbook(mypath + '\{}.xlsx'.format("2021年《财富》美国500强排行榜"))
        worksheet = workbook.add_worksheet("2020年《财富》美国500强排行榜")
        # title = ['排名', '公司名称（中文）', '营业收入（百万美元）', '利润（百万美元）', '资产', '股东权益', '净利率', '资产收益率']
        title = ['排名']
        worksheet.write_row('A1', title)
        for index, data in enumerate(data_list):
            num0 = str(index + 2)
            row = 'A' + num0
            worksheet.write_row(row, data)
        workbook.close()


if __name__ == "__main__":
    spider = Get_data()
    spider.get_mdata()
