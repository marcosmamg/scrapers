import scrapy


class TalksSpider(scrapy.Spider):
    name = "talks"

    def start_requests(self):
        urls = [
            'https://us.pycon.org/2018/schedule/talks/list/',
            #'https://us.pycon.org/2018/schedule/talks/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'USPyconTalks2018.html'
        with open(filename, 'w') as f:
            for talk in response.selector.xpath('//h2//a/text()').extract():
                f.write('Title: %s' % talk.strip() + '\n')

            for description in response.css('.presentation-description::text').extract():
                f.write('Description: %s' % description.strip() + '\n')

            for date_location in response.selector.xpath('//b/following-sibling::*//text()').extract():
                    f.write('date_location: %s' % date_location.strip() + '\n')

            for speaker in response.selector.xpath('//b[1]/text()').extract():
                    f.write('speaker: %s' % speaker.strip() + '\n')
