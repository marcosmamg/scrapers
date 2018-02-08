from grab import Grab
from grab.spider import Spider, Task
from urllib.parse import urljoin
import re
import requests
import json


def getData(url):
		req = requests.get(url)
		return req.json()

class OoqiaSpider(Spider):
    def prepare(self):
        self.initial_urls = ['https://attorneys.superlawyers.com/divorce/new-york-metro/new-york/']
        self.attorneys = []
        self.attorneys2 = []
        self.totalAttorneys = []
        self.getLawyerCentralAttorneys()
        super(OoqiaSpider, self).prepare()

    def task_initial(self, grab, task):
        container = grab.doc.select('//*[@id="browse_view"]')
        selector = './/*[contains(@class,"search_result")]'
        for attorney in container.select(selector):
            att = dict()
            att['source'] = 'superlawyers'
            img_tag = attorney.select('.//*[@class="image"]//img')

            if img_tag:
                att['picture'] = img_tag.attr('src')
            else:
                att['picture'] = ""
            card = attorney.select('.//*[@class="text_container"]')
            att['name'] = card.select('.//h2').text()

            self.attorneys.append(att)


        pagination = grab.doc.select('//*[@class="pagination"]')
        next_page = pagination.select('.//a[@rel="next"]')
        if next_page:
            url = next_page.attr('href')
            yield Task('initial', grab.make_url_absolute(url))
        else:
            self.test()

    def make_url_absolute(grab, href, force_https=False):
        if grab.config['url']:
            base_url = grab.response.url
            url = urljoin(base_url, href)
        else:
            url = href
        if force_https and url.startswith('http://'):
            url = re.sub('^http:\/\/', 'https://', url)
        return url

    def getLawyerCentralAttorneys(self):
        attorneys = getData(
            'https://www.lawyercentral.com/utils/maps.cfc?method=getAttorneysFromLatLng&lat=39.828185&lng=-98.57954&lawyerName=&stateAbb=&practiceareaID=89')

        for attorney in attorneys['markers']:
            lawyercentral_dict = dict()
            lawyercentral_dict['source'] = 'lawyercentral'
            lawyercentral_dict['name'] = attorney['name']
            lawyercentral_dict['picture'] = "https://www.lawyercentral.com" + attorney['picture']
            self.attorneys2.append(lawyercentral_dict)

    def test(self):

        for attorney in self.attorneys2:
            self.totalAttorneys.append(attorney)
            for _attorney in self.attorneys:
                if _attorney['name']==attorney['name']:
                    self.attorneys.remove(_attorney)
                    print('Attorney duplicated:' + _attorney['name'])

        for attorney in self.attorneys:
            self.totalAttorneys.append(attorney)

        f = open('workfile.csv', 'w')
        for attorney in self.totalAttorneys:
            f.write(attorney['source'])
            f.write(',')
            f.write('\t')
            f.write(attorney['name'])
            f.write(',')
            f.write('\t')
            f.write(attorney['picture'])
            f.write('\n')