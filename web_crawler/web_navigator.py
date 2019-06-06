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

    capabilities = { 'chromeOptions':  { 'useAutomationExtension': False, 'args': ['--disable-extensions']}}
    browser = webdriver.Chrome(executable_path = 'chromedriver.exe', desired_capabilities = capabilities)

    # go to google main page
    browser.get('https://www.google.com/')
    search_bar = browser.find_element_by_name('q') # finds search bar according to the name of the element

    search_bar.send_keys(google_keyword)
    search_bar.submit() # same as pressing Enter
    time.sleep(1)
    all_the_links_collected = []

    while True:
        html = browser.page_source
        links = html.split('<div class="g"')[1:] # splits the entire page source according to the name of the class

        for x, link in enumerate(links):
            start = link.find('<a href="') + 9  # the beginning of the url to one of the search results
            end = link[start:].find('"')  # url starts as well as ends with quotation mark
            links[x] = link[start:start + end]  # only the actual url is supposed to be stored in links array now

        try:
             next_page_button = browser.find_element_by_id('pnnext') # finds the next page button according to the id of it
             next_page_button.click()
        except Exception as e:  # if the button is not found
            print(e)
            try:
                add_more_results = browser.find_element_by_xpath('//*[@id="ofr"]/i/a') # google likes to skip some results so we press a button to add them back
                add_more_results.click()
            except:
                break  # neither next page button nor more results link is found, so the search is over (usually 40-60 pages but it might differ for each case)

        for link in links:
            all_the_links_collected.append(link)

        # adding at least some randomness to simulate human browsing (but this is nowhere near enough)
        time_to_wait = random.randint(100, 250) / 100
        time.sleep(time_to_wait)

    browser.close()
        
    return all_the_links_collected


def get_bing_search_links(bing_keyword):
    # working principle is basically the same as the get_google_search_links function, so please look above ;)
    capabilities = { 'chromeOptions':  { 'useAutomationExtension': False, 'args': ['--disable-extensions']}}
    browser = webdriver.Chrome(executable_path = 'chromedriver.exe', desired_capabilities = capabilities)
    browser.get('https://www.bing.com/')

    search_bar = browser.find_element_by_name('q')
    search_bar.send_keys(bing_keyword)
    search_bar.submit()
    time.sleep(0.8)
    all_the_links_collected = []

    while True:
        html = browser.page_source
        links = html.split('<li class="b_algo"')[1:]

        for x, link in enumerate(links):
            start = link.find('<a href="') + 9
            end = link[start:].find('"')
            links[x] = link[start:start + end]

        if links == all_the_links_collected[-len(links):] and len(links) != len(all_the_links_collected):  # when the end is reached bing still has a next page button that redirects to the same page that it is already in (leads to an infinite loop)
            break

        for link in links:
            all_the_links_collected.append(link)
        
        try:
            next_page_button = browser.find_element_by_class_name('sb_pagN')
            next_page_button.click()
        except Exception as e:
            print(e)
            break

        time_to_wait = random.randint(150, 250) / 100
        time.sleep(time_to_wait)

    browser.close()

    return all_the_links_collected


# utilizes firefox reader mode to extract only the important text
def download_article(url):

    resp = requests.get(url)

    if resp.status_code != 200:
        print('Unable to fetch page')
        return None, None

    else:
        html = resp.content

    text = reader_mode(html)

    return text, html



def translate_article(txt_to_translate):

    try:
        translator = Translator()
        translation = translator.translate(txt_to_translate, dest = 'en')
    except Exception as e:
        print('Unable to translate text because:')
        print(e)
        return '.'

    return translation.text


def get_clear_browsing_button(driver):
    return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')

def clear_cache(driver, timeout = 60):
    driver.get('chrome://settings/clearBrowserData')

    # wait for the button to appear
    wait = WebDriverWait(driver, timeout)
    wait.until(get_clear_browsing_button)

    # click the button to clear the cache
    get_clear_browsing_button(driver).click()

    # wait for the button to be gone before returning
    wait.until_not(get_clear_browsing_button)

def most_common(lst):
    return max(set(lst), key = lst.count)
