import requests
import time
from bs4 import BeautifulSoup as bs
import random
from html_processor import delete_comments
import duckpy
import http.client
import json
import urllib.parse
import ddg3

def get_duckduckgo_search_links(keyword):
    r = ddg3.query(keyword)
    print(type(r))
    print(r.results[1].url)
    links = []
    # search = duckpy.search(keyword)
    # print(search)
    # links = []
    # results = search['results']
    # for result in results:
    #     links.append(result['url'])

    return links


def main():
    urls = get_duckduckgo_search_links('microsoft')
    print(len(urls), 'URLs collected')

main()