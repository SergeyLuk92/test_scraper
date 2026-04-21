DEFAULT_DOWNLOAD_DELAY: int = 2
DEFAULT_CONCURRENT_REQUESTS: int = 1
DEFAULT_RETRY_TIMES: int = 3
RETRY_HTTP_CODES: list[int] = [429, 500, 502, 503, 504]

API_URL: str = 'https://usedcars.bmw.co.uk/vehicle/api/list/'
DEFAULT_PAGE: int = 1
DEFAULT_SIZE: int = 23
MAX_PAGES: int = 5

UVL_REGEX: str = r'UVL\.AD\s*=\s*({.+?});'

HEADERS: dict[str, str] = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://usedcars.bmw.co.uk/result/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
    'x-csrftoken': 'L1ztUG3N592uZvuDlOlvkvMArMxs5VEu',
}

COOKIES_TEMPLATE: dict[str, str] = {
    'csrftoken': 'L1ztUG3N592uZvuDlOlvkvMArMxs5VEu',
    'django_language': 'en-gb',
}

DB_PATH: str = 'bmw_cars.db'
