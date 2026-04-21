import scrapy
import json
import re
from typing import Any, Generator, Optional
from src.crawlers.bmw_co_uk.items import BmwCarItem
from src.crawlers.bmw_co_uk.consts import (
    API_URL,
    DEFAULT_PAGE,
    DEFAULT_SIZE,
    MAX_PAGES,
    UVL_REGEX,
    HEADERS,
    COOKIES_TEMPLATE,
)


class BmwSpider(scrapy.Spider):
    name: str = 'bmw'
    headers: dict[str, str] = HEADERS.copy()
    cookies: dict[str, str] = COOKIES_TEMPLATE.copy()
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.total_pages: int = 0

    def start_requests(self) -> Generator[scrapy.Request, None, None]:
        url: str = f'{API_URL}?page={DEFAULT_PAGE}&size={DEFAULT_SIZE}'
        yield scrapy.Request(
            url=url,
            headers=self.headers,
            cookies=self.cookies,
            callback=self.parse_list
        )

    def parse_list(self, response: scrapy.http.Response) -> Generator[scrapy.Request, None, None]:
        if response.status != 200:
            self.logger.error(f"Failed: {response.status}")
            return

        data: dict[str, Any] = response.json()
        results: list[dict[str, Any]] = data.get('results', [])

        for car in results:
            advert_id: Optional[str] = car.get('advert_id')
            if advert_id:
                detail_url: str = f'https://usedcars.bmw.co.uk/vehicle/{advert_id}'
                yield scrapy.Request(
                    url=detail_url,
                    headers=self.headers,
                    cookies=self.cookies,
                    callback=self.parse_detail
                )

        pagination: dict[str, Any] = data.get('pagination', {})
        current_page: int = pagination.get('current', DEFAULT_PAGE)
        if not self.total_pages:
            self.total_pages = pagination.get('total', DEFAULT_PAGE)

        if current_page < self.total_pages and current_page < MAX_PAGES:
            next_page: int = current_page + 1
            next_url: str = f'{API_URL}?page={next_page}&size={DEFAULT_SIZE}'
            yield scrapy.Request(
                url=next_url,
                headers=self.headers,
                cookies=self.cookies,
                callback=self.parse_list
            )

    def parse_detail(self, response: scrapy.http.Response) -> Generator[BmwCarItem, None, None]:
        match: Optional[re.Match] = re.search(UVL_REGEX, response.text, re.DOTALL)
        if match:
            ad_data: dict[str, Any] = json.loads(match.group(1))

            item: BmwCarItem = BmwCarItem()
            item['model'] = ad_data.get('title')
            item['name'] = ad_data.get('specification', {}).get('derivative')
            item['mileage'] = ad_data.get('condition_and_state', {}).get('mileage')
            item['registered'] = ad_data.get('dates', {}).get('registration')
            item['range_value'] = ad_data.get('battery', {}).get('range', {}).get('value')
            item['exterior'] = (ad_data.get('colour', {}).get('manufacturer_colour') or
                                ad_data.get('colour', {}).get('colour'))
            item['fuel'] = ad_data.get('specification', {}).get('raw_fuel_type')
            item['transmission'] = ad_data.get('specification', {}).get('transmission')
            item['registration'] = ad_data.get('identification', {}).get('registration')
            item['upholstery'] = ad_data.get('specification', {}).get('interior')

            self.logger.info(f"Parsed: {item['model']} - {item['registration']}")

            yield item
