import scrapy
from typing import Optional


class BmwCarItem(scrapy.Item):
    model: Optional[str] = scrapy.Field()
    name: Optional[str] = scrapy.Field()
    mileage: Optional[int] = scrapy.Field()
    registered: Optional[str] = scrapy.Field()
    engine: Optional[str] = scrapy.Field()
    range_value: Optional[int] = scrapy.Field()
    exterior: Optional[str] = scrapy.Field()
    fuel: Optional[str] = scrapy.Field()
    transmission: Optional[str] = scrapy.Field()
    registration: Optional[str] = scrapy.Field()
    upholstery: Optional[str] = scrapy.Field()
