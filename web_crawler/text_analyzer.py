from bs4 import BeautifulSoup as bs
from html_processor import extract_text, get_domain_name
from link_collector import get_whole_html, get_links
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
import random
import time
import pandas as pd
#import numpy as np
from sklearn.utils import shuffle


def wait(min, max = 0): # kiek laukti milisekundemis 
    if min > max:
        max = min
    time_to_wait = random.randint(min, max) / 1000
    time.sleep(time_to_wait)

def remove_duplicate_text(actual_text, supporting_text):
    start = 0
    end = -1
    while actual_text[start] == supporting_text[start]:
        start += 1

    while actual_text[end] == supporting_text[end]:
        end -= 1

    return actual_text[start:end]



def extract_text_cross_comparision_with_another_site(url):
    text_to_extract = 'text1'
    another_text = 'text2'

    html_to_extract = get_whole_html(url)
    domain = get_domain_name(url)
    links = get_links(url)

    url_to_check = url

    while True:
        url_to_check = links[random.randint(0, len(links))]
        if domain == get_domain_name(url_to_check):
            if url != url_to_check:
                break

    html_to_match = get_whole_html(url_to_check)

    text_to_extract = html_to_extract #extract_text(html_to_extract)
    text_to_match = html_to_match #extract_text(html_to_match)

    actual_text = remove_duplicate_text(text_to_extract, text_to_match)
    return actual_text


def is_worth_downloading(text):

    return False



# pasinaudoja firefox reader mode ir nuskaito tik straipsnio teksta (idealiu atveju)
def download_article(url, browser):
    browser.get('about:reader?url=' + url)  # einama i specialu reader mode, kuriuo naudojantis yra lengviau straipsnio teksta atskirti nuo viso kito teksto, esancio tame paciame puslapyje
    text = browser.find_element_by_tag_name('body').text
    # laukiama, kol uzsikraus puslapis
    a = 0
    while len(text) < 500:  
        text = browser.find_element_by_tag_name('body').text
        time.sleep(0.5)
        a += 1
        if a > 12: 
            return 'Nepavyko atidaryti puslapio'

    cut_here = text.find('minutes')
    if cut_here > 0:
        text = text[cut_here:]
        cut_here = text.find('\n')
        text = text[cut_here + 1:]

    return text

# naudoja firefox reader mode atskirti straipsnio teksta nuo viso kito slamsto (reklamu, nuorodu i kitus straipsnius ir pan.)
def download_articles():
    df = pd.read_csv('su_dividendais.txt', sep = '\t', encoding = 'utf-16')
    df = shuffle(df)
    df = df.reset_index(drop = True)

    datafile = open(r'tekstai/0.txt', 'w', encoding = 'utf-16')

    binary = FirefoxBinary(r'C:\Users\asereika\AppData\Local\Mozilla Firefox\firefox.exe')
    browser = webdriver.Firefox(firefox_binary = binary)
    urls = df['Nuoroda']

    for x, url in enumerate(urls):
        try:
            text = download_article(url, browser)

            with open(r'tekstai/%s.txt'%str(x+1), 'w', encoding = 'utf-16') as f:
                f.write(text)

            datafile.write(str(x+1) + '\n')
            print(x + 1, 'files written')
        except:
            print('Something happened')
        

    browser.close()
    datafile.close()
    print('Done!')
    

def translate_articles():
    amount_of_articles = 0
    with open(r'tekstai/0.txt', 'r', encoding = 'utf-16') as f:
        datafile = f.readlines()
        amount_of_articles = int(datafile[-1])

    capabilities = { 'chromeOptions':  { 'useAutomationExtension': False, 'args': ['--disable-extensions']}}
    browser = webdriver.Chrome(desired_capabilities = capabilities)
    browser.get('https://translate.google.com/')
    
    # originali teksto kalba
    language_selector = browser.find_element_by_id('gt-sl-gms')
    language_selector.click()
    time.sleep(0.1)
    language_selector = browser.find_element_by_xpath('//*[@id=":1l"]/div')  # pasirenka lietuviu
    language_selector.click()
    time.sleep(0.1)
    # kalba i kuria norima isversti
    language_selector = browser.find_element_by_id('gt-tl-gms')
    language_selector.click()
    time.sleep(0.1)
    language_selector = browser.find_element_by_xpath('//*[@id=":3j"]/div')  # pasirenka anglu
    language_selector.click()
    time.sleep(0.1)


    for x in range(1, amount_of_articles + 1):
        with open(r'tekstai/%s.txt'%x, 'r', encoding = 'utf-16') as f:
            text_to_translate = f.read()

        while 'mln.' in text_to_translate:
            text_to_translate = text_to_translate.replace('mln.', 'mln')
        while 'mlrd.' in text_to_translate:
            text_to_translate = text_to_translate.replace('mlrd.', 'mlrd')
        while 'tūkst.' in text_to_translate:
            text_to_translate = text_to_translate.replace('tūkst.', 'tūkst')

        translated_text = translate_article(browser, text_to_translate)

        with open(r'tekstai/%s_en.txt'%x, 'w', encoding = 'utf-16') as f:
            f.write(translated_text)        
        print(x, 'articles translated')


def translate_article(browser, text_to_translate):
    # isvalyti isversta teksta is anksciau
    while len(browser.find_element_by_id('result_box').text) > 5:
        try: 
            translate_button = browser.find_element_by_id('gt-submit')
            translate_button.click()
        except Exception as e:
            print('Could not locate the "Translate" button')
            print(e)
        wait(100)


    text_field = browser.find_element_by_id('source')
    translated_text = ''

    while len(text_to_translate) > 2:
        if len(text_to_translate) > 4999:
            cut_here = text_to_translate.rfind('\n', 0, 4999)
            text_field.send_keys(text_to_translate[:cut_here])
        else: 
            cut_here = len(text_to_translate)
            text_field.send_keys(text_to_translate)

        translate_click_counter = 0
        translate_button = browser.find_element_by_id('gt-submit')
        translate_button.click()
        wait(300, 200)

        while len(browser.find_element_by_id('result_box').text) < 5:
            #try: 
            translate_button.click()
            translate_click_counter += 1
            if translate_click_counter > 5:
                break
            wait(200)

        translated_text += browser.find_element_by_id('result_box').text

        text_to_translate = text_to_translate[cut_here:]
        text_field.clear()
        wait(50)
        translate_button = browser.find_element_by_id('gt-submit')
        translate_button.click()

    return translated_text


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
