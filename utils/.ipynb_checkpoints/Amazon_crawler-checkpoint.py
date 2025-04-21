from imports import *

## set setting and configs to module to scraper.
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'config.settings')

def extract_score(s):
    match = re.search(r"(\d+.\d+)", s)
    return match.group(1) if match else None

def extract_price(p):
    match = re.search(r"(\d+.\d+)", p)
    return match.group(1) if match else None

class Product(Item):
    title = Field()
    description = Field()
    price = Field()
    amount_reviews = Field()

    score = Field()
    review_body = Field()
    review_title = Field()


class Amazon(CrawlSpider):
    name = "Beauty Products"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "CLOSESPIDER_ITEMCOUNT": 4,
        "CLOSESPIDER_COUNTPAGE": 1,
    }

    allowed_domains = ["www.amazon.com"]

    start_urls = ["https://www.amazon.com/s?k=beauty+products"]

    download_delay = 2

    visited_urls = set()

    rules = (
        # product details
        Rule(
            LinkExtractor(
                allow=r"/dp/B0\w+"
            ), follow=True, callback="to_get_products"
        ),
        # Product pagination
        Rule(
            LinkExtractor(
                allow=r"&page=\d+&"
            )
        )
    )


    def to_get_products(self, response):
        # verificar si la url ya fue visitada
        if response.url in self.visited_urls:
            self.logger.warning(f"Loop Dectectado: {response.url}")
            return # no procesar si es recursiva

        # registrar la url como visitada
        self.visited_urls.add(response.url)

        item = ItemLoader(Product(), response)

        item.add_xpath('title', '//div[@id="ppd"]//h1//span[@id="productTitle"]/text()')
        item.add_xpath('description', '//ul[@class="a-unordered-list a-vertical a-spacing-mini"]//text()', Join("\n"))
        item.add_xpath('price', '//div[@class="a-section a-spacing-none aok-align-center aok-relative"]/span[1]/text()', mc(lambda x: re.search(r"(\$[0-9\W]+)", x).group(1).strip() if re.search(r"(\$[0-9\W]+)", x) else None), tf()) #(\$[0-9\W]+)
        item.add_xpath('amount_reviews', '//div[@id="averageCustomerReviews"]//span[@id="acrCustomerReviewText"]/text()', mc(lambda x: re.match(r"([0-9\W]+)", x).group(1).strip() if x else None))

        reviews = response.xpath("//li[@data-hook='review']")
        title = reviews.xpath('.//a[@data-hook="review-title"]/span[2]/text()').getall()
        body = reviews.xpath('.//*[@data-hook="review-body"]//span/text()').getall()
        score = reviews.xpath('.//i[@data-hook="review-star-rating"]//text()').getall()


        item.add_value('score', [extract_score(s) for s in score if s])
        item.add_value('review_body', [b for b in body])
        item.add_value('review_title', [t for t in title if t])

        yield item.load_item()        