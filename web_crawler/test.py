
from py_ms_cognitive import PyMsCognitiveWebSearch
import requests
import time
from bs4 import BeautifulSoup as bs
import random
from html_processor import delete_comments
import duckpy
from py_bing_search import PyBingWebSearch
import http.client
import json
import urllib.parse


def get_bing_search_links(search):
    main_url = 'https://northeurope.api.cognitive.microsoft.com/bing/v7.0/search' # Bing API URL
    count = 20
    links = []
    for n in range(0, count):
        payload = {'q': search, 'count': 50, 'offset': 50 * n, 'responseFilter': ['Webpages']} # make request query and headers for the API
        headers = {'Ocp-Apim-Subscription-Key': '49965ae339ad41e48b29dc0a0b633f0d'}
        r = requests.get(main_url, params = payload, headers = headers)
        # parse the results
        urls = r.json()
        urls = urls['webPages']
        urls = urls['value']
        for url in urls:
            links.append(url['url'])

        time.sleep(2) # pay respect to servers
    return links

def get_duckduckgo_search_links(keyword):
    search = duckpy.search('keyword')
    print(search)
    links = []
    results = search['results']
    for result in results:
        links.append(result['url'])

    return links
