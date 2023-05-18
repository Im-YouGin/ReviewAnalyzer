from googlesearch import search

from common.constants import MARKET_APP_URL_REGEX, MARKET_URL_MATCH_PROCESSOR


def search_app(name, developer, market):
    query = f"{name} {developer} {market.replace('_', ' ')} install"
    result = search(query, num_results=5)

    regex = MARKET_APP_URL_REGEX[market]
    for url in result:
        if match := regex.match(url):
            return MARKET_URL_MATCH_PROCESSOR[market](match)
    return {}
