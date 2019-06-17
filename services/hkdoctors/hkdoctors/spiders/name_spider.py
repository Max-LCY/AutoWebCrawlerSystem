import scrapy
import boto3

class NameSpider(scrapy.Spider):
    name = "names"

    def start_requests(self):
        params = {"district": "00", "practice": '01', "specialty": '00', "x": '14', "y": '23'}
        yield scrapy.FormRequest(url="http://www.hkdoctor.org/english/docsearch1.asp", callback=self.parse,
                                 formdata=params)

    def parse(self, response):
        hxs = scrapy.Selector(response)
        # extract all links from page
        all_links = hxs.xpath('*//a/@href').extract()
        filename = '/tmp/name_list.txt'
        with open(filename, 'w') as f:
            f.write('\n'.join(all_links) + '\n')
        self.log('Saved file %s' % filename)
