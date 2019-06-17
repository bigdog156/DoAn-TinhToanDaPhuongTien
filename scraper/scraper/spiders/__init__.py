# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
from scrapy.selector import Selector

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        #Crawler các pages tiếp theo của website 
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
#Done
class Viettourist(scrapy.Spider):
    name = "viettourist"
    start_urls = [
        'https://viettourist.com/tour/du-lich-trong-nuoc-cid-198-0.html',
    ]

    def parse(self, response):
        for element in response.css('li.col-md-4.col-sm-6'):
            yield{
                'text': element.css('div.item div.name a::text').get(),
                'address':"https://viettourist.com"+ element.css('div.item div.name a::attr(href)').get()[1:],
                'time': element.css('div.item div.xinfo.clearfix div span span::text').get(),
                'link': element.css('div.item div.image a img::attr(src)').get(),
                'price': element.css('div.item div.price::text').get(),
            }

#Done Vinatourist.net
class Vinatourist(scrapy.Spider):
    name = "vinatourist"
    start_urls = [
        'http://www.vinatourist.net/tour-trong-nuoc/tour-mien-tay/',
        'http://www.vinatourist.net/tour-trong-nuoc/tour-da-nang/',
        'http://www.vinatourist.net/tour-trong-nuoc/tour-mien-bac/',
        'http://www.vinatourist.net/tour-trong-nuoc/tour-phu-quoc/',
    ]

    def parse(self, response):
        i = 0
        for element in response.xpath('//*[@class="items-tours "]'):
            
            yield{
                'text': element.xpath('div/h3/a/text()').get(),
                'address': element.xpath('div/h3/a/@href').get(),
                'time': element.xpath('div/p[2]/span/text()').get(),
                'link': "http://www.vinatourist.net/"+str(element.xpath('a/img/@src').get()),
                'price': element.xpath('div/p[@id="price"]/span/text()').get(),
            }
            i = i+1

# Done but just 17 item
class Travel(scrapy.Spider):
    name = "travel"

    start_urls = [
        'https://travel.com.vn/du-lich-viet-nam-p1.aspx',
    ]
    def parse(self, response):
        for element in response.xpath('//*[@id="grTours"]/div'):
            yield{
                'text': element.xpath('div[1]/div[2]/div[1]/div/div/a/text()').get(),
                'address':"https://travel.com.vn"+ str(element.xpath('div[1]/div[2]/div[1]/div/div/a/@href').get()),
                'time': element.xpath('div[1]/div[2]/div[2]/div[2]/div/div[2]/text()').getall()[1:],
                'link': element.xpath('div[1]/div[1]/div/a/img/@src').get(),
                'price': element.xpath('div[1]/div[2]/div[2]/div[3]/div/div/text()').get(),

            }
#Done Vivu
class Vivu(scrapy.Spider):
    name = "vivu"

    start_urls = [
        'https://www.ivivu.com/du-lich/trong-nuoc',
    ]
#div.row.v-margin-top-10
    def parse(self, response):
        for element in response.css('div.col-xs-12.col-sm-12.col-md-12.col-lg-12.tourItem'):
            
            yield{
                'text': element.css('div.col-xs-12.col-sm-8.col-md-8.col-lg-8 span.tourItemName a.linkDetail::text').get(),
                'address':"https://www.ivivu.com"+ str(element.css('div.col-xs-12.col-sm-8.col-md-8.col-lg-8 span.tourItemName a.linkDetail::attr(href)').get()),
                'time': element.css('div.col-xs-12.col-sm-4.col-md-4.col-lg-4.tourItemContentPrice.text-right span.tourItemDateTime::text').get(),
                'link': element.css('img.img-responsive::attr(src)').get(),
                'price': element.css('div.col-xs-12.col-sm-4.col-md-4.col-lg-4.tourItemContentPrice.text-right span.tourItemPrice::text').get(),
            }
           

        next_page = response.xpath('//*[@class="pagination pagination-flat"]/li[3]/a/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

class VietNamBooking(scrapy.Spider):
    name = "vietnambooking"

    start_urls = [
        'https://www.vietnambooking.com/du-lich?type=tour-trong-nuoc&page=1',
        'https://www.vietnambooking.com/du-lich?type=tour-trong-nuoc&page=2',
        'https://www.vietnambooking.com/du-lich?type=tour-trong-nuoc&page=3',
        'https://www.vietnambooking.com/du-lich?type=tour-trong-nuoc&page=4',
        'https://www.vietnambooking.com/du-lich?type=tour-trong-nuoc&page=5',
        'https://www.vietnambooking.com/du-lich?type=tour-trong-nuoc&page=6',
        'https://www.vietnambooking.com/du-lich?type=tour-trong-nuoc&page=7',
        'https://www.vietnambooking.com/du-lich?type=tour-trong-nuoc&page=8',
    ]

    def parse(self, response):
        for element in response.css('div.category-box-list-default-inner ul li'):
            yield{
                'text': element.css('h3.title-h3 a::text').get(),
                'address': element.css('a.btn.btn-success.btn-xs.btn-readmore::attr(href)').get(),
                'time': element.css('table.table.tlb-time-and-traffic-tour tr td::text').getall()[4:],
                'link': element.css('div.box-img a img::attr(src)').get(),
                'price': element.css('div.box-price-promotion-tour span::text').get(),
            }

    
class Mytour(scrapy.Spider):
    name = "mytour"

    start_urls = [
        'https://mytour.vn/tour/n1/tour-du-lich-viet-nam.html?page=1',
        'https://mytour.vn/tour/n1/tour-du-lich-viet-nam.html?page=2',
    ]

    def parse(self, response):
        for element in response.css('div.product-item.row'):
            yield{
                'text': element.css('a.product-name::text').get(),
                'address': "https://mytour.vn"+str(element.css('a.product-name::attr(href)').get()),
                'time': element.css('div.product-content ul li::text').get(),
                'link': element.css('div.product-image a img::attr(data-src)').get(),
                'price': element.css('div.item-price strong.price::text').get(),
            }

class Trippy(scrapy.Spider):
    name = "trippy"

    start_urls = [
        'https://trippy.vn/tour/tour-du-lich-trong-nuoc?page=1',
        'https://trippy.vn/tour/tour-du-lich-trong-nuoc?page=2',
        'https://trippy.vn/tour/tour-du-lich-trong-nuoc?page=3',
        'https://trippy.vn/tour/tour-du-lich-trong-nuoc?page=4',
        'https://trippy.vn/tour/tour-du-lich-trong-nuoc?page=5',
        'https://trippy.vn/tour/tour-du-lich-trong-nuoc?page=6',
        'https://trippy.vn/tour/tour-du-lich-trong-nuoc?page=7',
        'https://trippy.vn/tour/tour-du-lich-trong-nuoc?page=8',
        'https://trippy.vn/tour/tour-du-lich-trong-nuoc?page=9',
        'https://trippy.vn/tour/tour-du-lich-trong-nuoc?page=10',
    ]

    def parse(self, response):
        for element in response.css('a.product-thumb.item'):
            yield{
                'text': element.css('h3.product-name::text').get(),
                'address': element.css('a.product-thumb.item::attr(href)').get(),
                'time': element.css('li.khoi-hanh::text').get(),
                'link': None,
                'price': element.css('p.price.price-new::text').get(),
            }

class Travellife(scrapy.Spider):
    name = "travellifevn"

    start_urls = [
        'http://travellifevn.vn/tour-trong-nuoc.html',
    ]
    def parse(self, response):
        for element in response.css('div.spacer'):
            yield{
                'text': element.css('h3.product-thongtin-ten a::text').get(),
                'address': "http://travellifevn.vn/" + str(element.css('h3.product-thongtin-ten a::attr(href)').get()),
                'time': element.xpath('//*[@class="product-thongtin-mota"]/p[1]/span/text()').get(),
                'link': element.css('span.product-anh_1 img::attr(src)').get(),
                'price': element.css('div.product-thongtin-salesPrice::text').get(),
            }

class Vietfun(scrapy.Spider):
    name = "vietfun"

    start_urls = [
        'https://www.vietfuntravel.com.vn/tour-mien-nam?page=1',
        
    ]

    def parse(self, response):
        for element in response.xpath('//*[@id="content"]/div[1]/div[1]'):
            yield{
                'text': element.xpath('div[2]/h3/a/text()').get(),
                # 'address': element.css('h3.name a::attr(href)').get(),
                
            }