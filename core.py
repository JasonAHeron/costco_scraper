from data_models import (
    Base,
    Item,
)
from decimal import Decimal
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import (
    CrawlSpider,
    Rule,
)
from settings import ITEM_DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(ITEM_DB)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def clean_extract(selector_result, func=lambda x:x):
    return func(selector_result.extract()[0]) if selector_result else None


class CostcoSpider(CrawlSpider):
    name = 'costco'
    allowed_domains = ['costco.com']
    start_urls = ['http://www.costco.com/']

    rules = (
        Rule(
            LxmlLinkExtractor(allow_domains=allowed_domains),
            follow=True,
            callback='find_items'
        ),
    )

    def find_items(self, response):
        if response.css('.product-tile').xpath('@itemid'):
            session = Session()
            for item in response.css('.product-tile'):
                payload = {
                    'id': item.xpath('@itemid').extract()[0],
                    'description': clean_extract(item.css('.description::text')),
                    'name': clean_extract(item.css('.short-desc::text')),
                    'price': clean_extract(item.css(
                        '.currency [data-regionnav=DEFAULT]::text'),
                        func=lambda x:Decimal(x[1:].replace(',', ''))
                    ),
                    'promotion': clean_extract(item.css('.promotion::text'))
                }
                session.merge(Item(**payload))
            session.commit()
