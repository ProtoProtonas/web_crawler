#import urllib.request
#from bs4 import BeautifulSoup as bs
import scrapy
from scrapy.crawler import CrawlerProcess
from html_processor import extract_text

class LBspider(scrapy.Spider):
    name = 'lb_voras'
    urls =  ['https://www.vz.lt/agroverslas/maisto-pramone/2018/06/18/mars-lietuva-dividendams-skyre-40-mlneur', 'https://www.vz.lt/rinkos/akcijos-ir-obligacijos/2018/03/28/telia-lietuva-uz-2017-m-siulo-ismoketi-408mlneur-dividendu']
    #urls = ['https://textminingonline.com/dive-into-tensorflow-part-iii-gtx-1080-ubuntu16-04-cuda8-0-cudnn5-0-tensorflow']

    def start_requests(self):
        
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = r'skreip/%s.txt' % response.url.split('/')[-1]
        with open(filename, 'wb', encoding = 'utf-16') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)




def main():
    process = CrawlerProcess({'USER_AGENT':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'})
    process.crawl(LBspider)
    process.start()

    #filenames = [r'verslozinios/mars-lietuva-dividendams-skyre-40-mlneur.html', r'verslozinios/telia-lietuva-uz-2017-m-siulo-ismoketi-408mlneur-dividendu.html']
    #for name in filenames:
    #    with open(name, 'r') as f:
    #        with open(name.split('/')[1] + '.txt', 'w', encoding = 'utf-16') as file:
    #            html = f.read()
    #            file.write(extract_text(html))
    #            print('succesfully written')

    #names = ['mars-lietuva.html', 'telia-lietuva.html']

    #for name in names:
    #    html = 0
    #    with open(name, 'r', encoding = 'utf-16') as f:
    #        print(f.read())



main()