import requests
from datetime import datetime
from lxml import etree
from time import sleep

class Crawler(object):
    def __init__(self,
                 base_url='https://www.csie.ntu.edu.tw/news/',
                 rel_url='news.php?class=106'):
        self.base_url = base_url
        self.rel_url = rel_url

    def crawl(self, start_date, end_date,
              date_thres = datetime(2012, 1, 1)):
        """Main crawl API

        1. Note that you need to sleep 0.1 seconds for any request.
        2. It is welcome to modify TA's template.
        """
        if end_date < date_thres:
            end_date = date_thres
        contents = list()
        page_num = 0
        while True:
            rets, last_date = self.crawl_page(
                start_date, end_date, page=f'&no={page_num}')
            page_num += 10
            if rets:
                contents += rets
            if last_date < start_date:
                break
        return contents

    def crawl_page(self, start_date, end_date, page=''):
        """Parse ten rows of the given page

        Parameters:
            start_date (datetime): the start date (included)
            end_date (datetime): the end date (included)
            page (str): the relative url specified page num

        Returns:
            content (list): a list of date, title, and content
            last_date (datetime): the smallest date in the page
        """
        res = requests.get(
            self.base_url + self.rel_url + page,
            headers={'Accept-Language':'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'}
        ).content.decode()
        sleep(0.1)

        # parse the response and get dates, titles and relative url with etree
        root = etree.HTML(res)	
        dates = root.xpath("//div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[1]/text()")
        titles = root.xpath("//div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]/a/text()")
        pageviews = root.xpath("/html/body/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[3]/text()")
        rel_urls = root.xpath("//div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]/a/@href")

        contents = list()
        last_date = dates[0].split('-')
        last_date = datetime(int(last_date[0]), int(last_date[1]), int(last_date[2]))
        
        for date, title, pageview, rel_url in zip(dates, titles, pageviews, rel_urls):
            # 1. concatenate relative url to full url
            # 2. for each url call self.crawl_content
            #    to crawl the content
            # 3. append the date, title and content to
            #    contents
            curr_date = date.split('-')
            curr_date = datetime(int(curr_date[0]), int(curr_date[1]), int(curr_date[2]))
            if (curr_date < last_date):
                last_date = curr_date
            if (curr_date >= start_date and curr_date <= end_date):
                title = title.replace(' ', '')
                content = (date, title, pageview, self.crawl_content(self.base_url + rel_url))
                contents.append(content)

        return contents, last_date

    def crawl_content(self, url):
        """Crawl the content of given url and return a string

        For example, if the url is
        https://www.csie.ntu.edu.tw/news/news.php?Sn=15216 then you are to crawl contents of
                ``Title : 我與DeepMind的A.I.研究之路, My A.I. Journey with DeepMind Date : 2019-12-27 2:20pm-3:30pm Location : R103, CSIE Speaker : 黃士傑博士, DeepMind Hosted by : Prof. 
                Shou-De LinAbstract: 我將與同學們分享，我博士班研究到加入DeepMind所參與的projects (AlphaGo, AlphaStar與AlphaZero)，以及從我個人與DeepMind的視角對未來AI發展的展望。 Biogr
                aphy: 黃士傑, Aja Huang 台灣人，國立臺灣師範大學資訊工程研究所博士，現為DeepMind Staff Research Scientist。``
        """
        if (url):
            response = requests.get(url)
            html_text = response.content.decode('utf-8')
            root = etree.HTML(html_text)
            contentlist = root.xpath("//div[1]/div/div[2]/div/div/div[2]//div[@class='editor content']//text()")
            content = str()
            for string in contentlist:
                content += string
            content = content.replace('\r\n', ' ')
            return content
