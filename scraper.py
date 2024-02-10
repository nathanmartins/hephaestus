from scraper_types import *
import requests
import uuid


def scrap(articles, sessionKey):
    url = 'https://w9ea975b8.api.esales.apptus.cloud/api/v2/panels/slp'
    params = {
        'esales.sessionKey': sessionKey,
        'esales.customerKey': sessionKey,
        'esales.market': 'MX',
        'market_locale': 'es_mx',
        'search_prefix': articles,
        'search_phrase': articles
    }
    headers = {
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'referer': 'https://www2.hm.com/'
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return welcome_from_dict(data)
    else:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return None


if __name__ == "__main__":

    # session_key is just a uuid4
    session_key = str(uuid.uuid4())

    articles = 'zapatos'
    search_results = scrap(articles, session_key)

    if search_results is None:
        print("No search results found.")
        exit(-1)

    print(search_results)
    for suggestion in search_results.product_suggestions:
        for product in suggestion.products:
            print(product.to_dict())