from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from itemloaders.processors import MapCompose as mc
from itemloaders.processors import TakeFirst as tf # toma el primer elemento no nulo
from itemloaders.processors import Join

import os
import re