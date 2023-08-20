BDTD_API_URL = "https://bdtd.ibict.br/vufind/api/v1"
BDTD_LIMIT = 1000
ENDPOINTS = {
    "search": {
        "url": BDTD_API_URL + "/search",
        "params": {
            "limit": BDTD_LIMIT,
            "sort": "year",
            "lng": "pt-br",
            "type": "AllFields",
        },
    },
    "record": {
        "url": BDTD_API_URL + "/record",
        "params": {
            "lng": "pt-br",
        },
    },
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
    "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}
