from bs4 import BeautifulSoup as bs
from googletrans import Translator
from reader_mode import reader_mode
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time
import random
import requests


def wait(min, max = 0): # milliseconds to wait
    if min > max: 
        max = min
    time_to_wait = random.randint(min, max) / 1000
    time.sleep(time_to_wait)

def get_google_search_links(google_keyword):

    keywd = google_keyword.replace(' ', '+')
    resp = requests.get('https://www.google.com/search?q=%s&filter=0&start=%d' % (keywd, 1))
    time.sleep(2.5)

    if resp.status_code != 200:
        print('Unable to fetch Google results. Status code %d.Trying again...' % resp.status_code)
        time.sleep(2)
        resp = requests.get('https://www.google.com/search?q=%s&filter=0&start=%d' % (keywd, 1))
            
        if resp.status_code != 200:
            print('Unable to fetch Google results again. Exiting with status code %d' % resp.status_code)
            return []

    time.sleep(1)
    all_the_links_collected = []

    no_of_results_fetched = 0

    while True:
        soup = bs(resp.content, 'lxml')

        links = soup.find_all('div', {'class':'jfp3ef'})

        for link in links:
            try:
                href = link.find('a')['href']
                href = href.replace('/url?q=', '')
                place = href.find('&sa=U&ved=')
                if place != -1:
                    href = href[:place]
                all_the_links_collected.append(href)
            except:
                pass
        # print('links: ', len(all_the_links_collected))

        no_of_results_fetched += len(links)

        try:
             resp = requests.get('https://www.google.com/search?q=%s&filter=0&start=%s' % (keywd, no_of_results_fetched + 1))
        except Exception as e:  
            print(e)
            return all_the_links_collected
            
        if len(links) < 3:
            break

        # adding at least some randomness to simulate human browsing (but this is nowhere near enough)
        time_to_wait = random.randint(200, 350) / 100
        time.sleep(time_to_wait)

    for l in all_the_links_collected:
        print(l)

        
    return all_the_links_collected


def get_bing_search_links(bing_keyword):

    keywd = bing_keyword.replace(' ', '+')
    url = 'https://www.bing.com/search?q=%s&first=%d' % (keywd, 1)
    resp = requests.get(url)
    time.sleep(2.5)

    
    if resp.status_code != 200:
        print('Unable to fetch Bing results. Status code %d.Trying again...' % resp.status_code)
        time.sleep(2)
        resp = requests.get('https://www.bing.com/search?q=%s&first=%d' % (keywd, 1))
            
        if resp.status_code != 200:
            print('Unable to fetch Bing results again. Exiting with status code %d' % resp.status_code)
            return []

    time.sleep(1)
    all_the_links_collected = []

    no_of_results_fetched = 0

    while True:
        soup = bs(resp.content, 'lxml')

        links = soup.find_all('li', {'class':'b_algo'})
        no_new_links = 1

        for link in links:
            try:
                href = link.find('a')['href']
                # print(href)
                if href not in all_the_links_collected:
                    all_the_links_collected.append(href)
                    no_of_results_fetched += 1
                    no_new_links = 0
            except:
                pass

        try:
            url = 'https://www.bing.com/search?q=%s&first=%d' % (keywd, no_of_results_fetched + 1)
            resp = requests.get(url)
            # print(url)
        except Exception as e:  
            print(e)
            return all_the_links_collected
            
        if no_new_links == 1:
            # print('Breaking news')
            break

        # adding at least some randomness to simulate human browsing (but this is nowhere near enough)
        time_to_wait = random.randint(200, 350) / 100
        time.sleep(time_to_wait)
        
    return all_the_links_collected


# utilizes firefox reader mode to extract only the important text
def download_article(url):
    resp = requests.get(url)
    if resp.status_code > 399:
        raise Exception('Unable to fetch page')
    else:
        html = resp.content

    # text = reader_mode(html)
    soup = bs(html, 'lxml')
    text = soup.get_text()
    return text, html


def translate_article(txt_to_translate):

    try:
        translator = Translator()
        translation = translator.translate(txt_to_translate, dest = 'en')
    except Exception as e:
        print('web_navigator.py exception 2: Unable to translate text because: ', e)
        return '.'

    return translation.text

def most_common(lst):
    return max(set(lst), key = lst.count)
