from googlesearch import search

from common.constants import MARKET_APP_URL_REGEX, MARKET_URL_MATCH_PROCESSOR

GOOGLE_SEARCH_QUERY = (
    "{name} {developer} app install site:play.google.com OR site:apps.apple.com"
)


def search_app(name, developer, market):
    query = GOOGLE_SEARCH_QUERY.format(name=name, developer=developer)
    result = search(query, num_results=5)

    regex = MARKET_APP_URL_REGEX[market]
    for url in result:
        if match := regex.match(url):
            return MARKET_URL_MATCH_PROCESSOR[market](match)
    return {}
