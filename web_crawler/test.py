# from web_navigator import get_duckduckgo_search_links
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




def BingWebSearch(search):

    a = 0

    if a == 0:
        host = "api.cognitive.microsoft.com"
        path = "/bing/v7.0/search"

        subscription_key = '6346c6f99c0240cdab53c73f5a631bbc'
        assert subscription_key

        headers = {'Ocp-Apim-Subscription-Key': subscription_key}
        conn = http.client.HTTPSConnection(host)
        query = urllib.parse.quote(search)
        conn.request("GET", path + "?q=" + query, headers = headers)
        response = conn.getresponse()
        headers = [k + ": " + v for (k, v) in response.getheaders() if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
                    
        return headers #response.read().decode("utf8")

    if a == 1:
    
        bing_web = PyBingWebSearch('e341f7008c604dc2b51d0df36a0ffbae', search, web_only = True) # web_only is optional, but should be true to use your web only quota instead of your all purpose quota
        first_fifty_result = bing_web.search(limit = 50, format = 'json') #1-50
        # second_fifty_result = bing_web.search(limit=50, format='json') #51-100
        return first_fifty_result

    if a == 2:
        url = 'https://northeurope.api.cognitive.microsoft.com'
        # query string parameters
        payload = {'q': search}
        # custom headers
        headers = {'Ocp-Apim-Subscription-Key': '49965ae339ad41e48b29dc0a0b633f0d'}
        # make GET request
        r = requests.get(url, params = payload, headers = headers)
        # get JSON response
        return r.json()

    else:
        web_bing = PyMsCognitiveWebSearch('49965ae339ad41e48b29dc0a0b633f0d', search)
        first_fity_results = web_bing.search(limit = 50)
        second_fifty_results = web_bing.search(limit=50)
        print(second_fifty_results[0].url)

        return first_fity_results







def get_bing_search_links(bing_keyword):

    subscription_key = ''
    assert subscription_key
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    search_term = urllib.parse.quote('dividendai 2019')
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}#, 'User-Agent': 'PC—Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko'}
    params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
    resp = requests.get(search_url, headers=headers, params=params)
    print(resp.status_code, resp.content)
    resp.raise_for_status()
    search_results = resp.json()

    print(search_results)

    return search_results




    # keywd = bing_keyword.replace(' ', '+')
    # url = 'https://www.bing.com/search?q=%s&first=%d&FORM=PORE' % (keywd, 1)
    # resp = requests.get(url)
    # print(resp.status_code)
    # time.sleep(2.5)

    
    # if resp.status_code != 200:
    #     print('Unable to fetch Bing results. Status code %d.Trying again...' % resp.status_code)
    #     time.sleep(2)
    #     resp = requests.get('https://www.bing.com/search?q=%s&first=%d&FORM=PORE' % (keywd, 1))
            
    #     if resp.status_code != 200:
    #         print('Unable to fetch Bing results again. Exiting with status code %d' % resp.status_code)
    #         return []

    # time.sleep(1)
    # all_the_links_collected = []

    # no_of_results_fetched = 0


    # while True:
    #     text = resp.content

    #     text = delete_comments(text)
    #     text = text.split(b'<body')[1]
    #     text = text[text.find(b'>')+1:]

    #     # delete text from <script to </script>
    #     script_start = 0
    #     while script_start != -1:
    #         script_start = text.find(b'<script')
    #         script_end = text.find(b'</script>') + 9
    #         text = text[:script_start] + text[script_end:]

    #     # delete text from <style to </style>
    #     style_start = 0
    #     while style_start != -1:
    #         style_start = text.find(b'<style')
    #         style_end = text.find(b'</style>') + 8
    #         text = text[:style_start] + text[style_end:]


    #     soup = bs(text, 'lxml')
    #     links = soup.find_all('li', {'class':'b_algo'})
    #     print('how many links: ', len(links))
    #     print(soup.prettify())
    #     no_new_links = 1

    #     for link in links:
    #         # try:
    #         href = link.find('a')['href']
    #         # print(href)
    #         if href not in all_the_links_collected:
    #             all_the_links_collected.append(href)
    #             no_of_results_fetched += 1
    #             no_new_links = 0
    #         # except:
    #         #     pass

    #     # try:
    #     url = 'https://www.bing.com/search?q=%s&first=%d&FORM=PORE' % (keywd, no_of_results_fetched + 1)
    #     resp = requests.get(url)
    #         # print(url)
    #     # except Exception as e:  
    #     #     print(e)
    #     #     return all_the_links_collected
            
    #     if no_new_links == 1:
    #         print('Breaking news')
    #         break

    #     # adding at least some randomness to simulate human browsing (but this is nowhere near enough)
    #     time_to_wait = random.randint(200, 350) / 100
    #     time.sleep(time_to_wait)
        
    # return all_the_links_collected

def get_duckduckgo_search_links(keyword):
    search = duckpy.search('keyword')
    print(search)
    links = []
    results = search['results']
    for result in results:
        links.append(result['url'])

    return links


def main():
    urls = BingWebSearch(r'samsung')
    print(len(urls), 'URLs collected')
    print(urls)

main()
