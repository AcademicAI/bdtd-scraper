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
