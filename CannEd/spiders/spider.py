import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup

# --- Run docker for scrapy splash ---
# docker run -p 8050:8050 scrapinghub/splash

# --- Start spider ---
# scrapy runspider spider.py

class InvnentorySpider(scrapy.Spider):
    name = "Inventory"


    def start_requests(self):
        url = 'https://www.greenrush.com/dispensary/cannabis-express'

        yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        url = response.url
        # Get the names of different categories
        category_names = response.css('.product-group__category-title::text').extract()
        # Get name of each link
        category_links = response.css('.product-group__category-link::attr(href)').extract()

        # Create dictionary mapping names to links for naming html files later
        self.category_dict = {}
        for i in range(len(category_links)):
            self.category_dict[category_links[i].split("?")[1]] = category_names[i]

        #print category_names
        #print len(category_names)
        #print category_links
        #print len(category_links)
        print self.category_dict


        for links in category_links:
            next_page = links
            if next_page is not None:
                next_page = response.urljoin(next_page)
                #yield scrapy.Request(next_page, callback=self.parse_product)
                # yield scrapy.Request(next_page, callback=self.parse_product, meta={
                #     'splash': {
                #         'args': {'wait': 0.5}
                #     }
                # })

                yield SplashRequest(next_page, callback=self.parse_product)


    def parse_product(self, response):
        url = response.url
        print "-----------"
        print url

        # Get name/description of cannabis
        canna_name = response.css('article.product-preview div.product-preview__description h3.product-preview__title .product-preview__title-link::text').extract()
        # canna_name = response.selector.xpath('//article//div//h3//a/text()').extract()
        print canna_name
        print len(canna_name)

        # Get type of cannabis (sativa, indica, hybrid)
        canna_type = response.css('.product-preview__category::text').extract()
        print canna_type
        print len(canna_type)


        '''
        # Get the name of the category to save
        url_id = url.split("?")[1]
        category_name = self.category_dict[url_id]

        # Save category page as html file
        filename = "cannabis-express-" + category_name + ".html"
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file' + filename)
        '''
