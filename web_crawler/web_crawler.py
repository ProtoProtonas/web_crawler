import scrapy
from scrapy.crawler import CrawlerProcess
# tried to get this to work but it is very slow and does not even support javascript

class LBspider(scrapy.Spider):
    name = 'lb_voras'
    urls =  ['https://www.vz.lt/agroverslas/maisto-pramone/2018/06/18/mars-lietuva-dividendams-skyre-40-mlneur', 'https://www.vz.lt/rinkos/akcijos-ir-obligacijos/2018/03/28/telia-lietuva-uz-2017-m-siulo-ismoketi-408mlneur-dividendu']

    def start_requests(self):
        
        for url in self.urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        filename = r'skreip/%s.txt' % response.url.split('/')[-1]
        with open(filename, 'wb', encoding = 'utf-16') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


def main():
    process = CrawlerProcess({'USER_AGENT':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'})
    process.crawl(LBspider)
    process.start()

main()