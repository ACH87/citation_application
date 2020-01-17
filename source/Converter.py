import requests
import re
from bs4 import BeautifulSoup
import json
from dateutil import parser

# FORMAT = '%s, (%s). %s%s %s [Accessed 20 Aug. 2019]'
# FORMAT = ['website', ', (', 'published year', ').', 'page title', '. [online] available at: ', 'url'
#           + ' [Accessed 20 Aug. 2019]']
WEBSITE_NAME = '%s, ('
DATE = '%s). '
PAGE_TITLE = '%s'
SRC = '%s'
URL = '%s [Accessed 20 Aug. 2019]'
REGEX = '>(.+?)<'

"""
Converts a website url to a harvard style citation

@:param url
   url to convert
"""
def website(url):
    page_source = requests.get(url).content
    soup = BeautifulSoup(page_source, "html.parser")
    soup_str = re.search(REGEX, str(soup.find(type='application/ld+json')))
    website_name = None
    date = DATE % 'n.d.'

    if soup_str:
        found = soup_str.group(1)
        j = json.loads(found)
        try:
            date = DATE % str(parser.parse(j['datePublished']).year)
        except AttributeError:
            # TODO find more ways to retrieve date
            pass
        try:
            website_name = j['author']['name']
        except AttributeError:
            pass

    website_title = re.search(REGEX, str(soup.title)).group(1).split(' - ')
    print('website title%s' % str(website_title))
    # TODO cheat for situations such as 'the contributors to wikipiedia', can have people with 4 names
    if not website_name or website_name.count(' ') > 2:
        website_name = WEBSITE_NAME % website_title[1]
    else:
        website_name = WEBSITE_NAME % website_name

    page_title = PAGE_TITLE % website_title[0]

    src = SRC % '. [online] available at: '

    result = (website_name, date, page_title, src, URL % url)
    final_string = ''.join(result)
    print(final_string)

    return result


if __name__ == '__main__':
    website('https://en.wikipedia.org/wiki/Suillus_bovinus')
