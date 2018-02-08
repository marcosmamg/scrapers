from grab import Grab
from grab.spider import Spider, Task
from urllib.parse import urljoin
import re


class OoqiaSpider(Spider):
    def prepare(self):
        self.initial_urls = ['https://attorneys.superlawyers.com/divorce/new-york-metro/new-york/']
        self.attorneys = []
        self.current_page = 1
        self.current_att = 1
        super(OoqiaSpider, self).prepare()

    def task_initial(self, grab, task):
        print('Current page: %s' % self.current_page)
        container = grab.doc.select('//*[@id="browse_view"]')
        selector = './/*[contains(@class,"search_result")]'
        for attorney in container.select(selector):
            att = dict()
            img_tag = attorney.select('.//*[@class="image"]//img')
            if img_tag:
                att['picture'] = img_tag.attr('src')
            card = attorney.select('.//*[@class="text_container"]')
            att['name'] = card.select('.//h2').text()
            print('    (%s) Current attorney: %s' % (self.current_att, att['name']))
            self.current_att += 1
            self.attorneys.append(att)


        pagination = grab.doc.select('//*[@class="pagination"]')
        next_page = pagination.select('.//a[@rel="next"]')
        if next_page:
            url = next_page.attr('href')
            self.current_page += 1
            yield Task('initial', grab.make_url_absolute(url))

    def make_url_absolute(grab, href, force_https=False):
        if grab.config['url']:
            base_url = grab.response.url
            url = urljoin(base_url, href)
        else:
            url = href
        if force_https and url.startswith('http://'):
            url = re.sub('^http:\/\/', 'https://', url)
        return url
