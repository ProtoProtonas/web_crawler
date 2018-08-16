from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time
import random
import pyautogui


def wait(min, max = 0): # milliseconds to wait
    if min > max: 
        max = min
    time_to_wait = random.randint(min, max) / 1000
    time.sleep(time_to_wait)

def get_google_search_links(google_keyword):

    # setup of headless chrome. Capabilities are changed because otherwise error "failed to load extension" is thrown
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
        time_to_wait = random.randint(100, 500) / 100
        time.sleep(time_to_wait)

    browser.close()
        
    return all_the_links_collected


def get_bing_search_links(bing_keyword):
    #capabilities = webdriver.DesiredCapabilities().FIREFOX
    #capabilities["marionette"] = False
    #binary = FirefoxBinary(r'C:\Users\asereika\AppData\Local\Mozilla Firefox\firefox.exe')
    #browser = webdriver.Firefox(firefox_binary = binary) #, desired_capabilities = capabilities)
    #browser = webdriver.Firefox()

    #binary = FirefoxBinary(r'C:\Users\asereika\AppData\Local\Mozilla Firefox\firefox.exe')
    #browser = webdriver.Firefox(firefox_binary = binary)


    # working princilpe is basically the same as the get_google_search_links function, so please look above ;)
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

        time_to_wait = random.randint(200, 350) / 100
        time.sleep(time_to_wait)

    browser.close()

    return all_the_links_collected


# utilizes firefox reader mode to extract only the important text
def download_article(url, browser):

    # browser.get(url)
    # browser.set_page_load_timeout(10)
    # html = browser.page_source
    # browser.get('about:reader?url=' + url)  # this works nowhere near as often as the other way of triggering reader mode
    try:
        browser.get(url) # this line often raises Remote end closed connection without response error
    except:
        wait(100)
        try:
            browser.get(url) # simple workaround against remote end closed... error
        except Exception as e:
            print(e)

    html = browser.page_source

    # pressing F9 triggers reader mode
    pyautogui.keyDown('F9')
    time.sleep(0.05)
    pyautogui.keyUp('F9')
    time.sleep(0.15)

    text = ' '

    # waiting until the page loads up
    a = 0
    while len(text) < 500:  
        text = browser.find_element_by_tag_name('body').text
        time.sleep(0.25)
        a += 1
        if a > 20:
            return 'Unable to open page' # kind of a 5 second timeout

    cut_here = text.find('minute') # reader mode adds estimated reading time so that is simply chopped off
    if cut_here > 0:
        text = text[cut_here:]
        cut_here = text.find('\n')
        text = text[cut_here + 1:]

    return text, html


def setup_firefox_for_article_download():
    extension_path = r'C:\Users\asereika\AppData\Roaming\Mozilla\Firefox\Profiles\f2yud58z.dev-edition-default\extensions\uBlock0@raymondhill.net.xpi' # path to adblocker extension (any adblocker should work)
    binary = FirefoxBinary(r'C:\Users\asereika\AppData\Local\Firefox Developer Edition\firefox.exe')
    browser_firefox = webdriver.Firefox(firefox_binary = binary)
    browser_firefox.install_addon(extension_path, temporary = False)
    print('Firefox browser is set up and ready to go')

    #binary = FirefoxBinary(r'C:\Users\asereika\AppData\Local\Mozilla Firefox\firefox.exe')
    #browser_firefox = webdriver.Firefox(firefox_binary = binary)
    #print('Firefox browser is set up and ready to go')
    return browser_firefox
    

def setup_chrome_translator():  # nereikia API, nes tekstui irasyti ir nuskaityti naudojamas headless browser
    capabilities = { 'chromeOptions':  { 'useAutomationExtension': False, 'args': ['--disable-extensions']}}  # be sito meta error
    browser = webdriver.Chrome(desired_capabilities = capabilities)
    browser.get('https://translate.google.com/')
    
    # original language of the text (in this case it is Lithuanian)
    language_selector = browser.find_element_by_id('gt-sl-gms')
    language_selector.click()
    time.sleep(0.1)
    language_selector = browser.find_element_by_xpath('//*[@id=":1l"]/div')  # Lithuanian is chosen
    language_selector.click()
    time.sleep(0.1)
    # destination language (English in this case)
    language_selector = browser.find_element_by_id('gt-tl-gms')
    language_selector.click()
    time.sleep(0.1)
    language_selector = browser.find_element_by_xpath('//*[@id=":3j"]/div')  # English is chosen
    language_selector.click()
    time.sleep(0.1)

    print('Chrome for translation is set up and ready to go')
    return browser


def translate_article(browser, txt_to_translate):
    # to realy clean up text field (may have some text in it from earlier)
    while len(browser.find_element_by_id('result_box').text) > 5:
        try: 
            translate_button = browser.find_element_by_id('gt-submit')
            translate_button.click()
        except Exception as e:
            print('Could not locate the "Translate" button: ', e)
            break
        wait(100)

    text_to_translate = txt_to_translate
    while 'mln.' in text_to_translate: # removing dots as Google Translate might think that they mark the end of the sentence (which they actually don't)
        text_to_translate = text_to_translate.replace('mln.', 'mln')
    while 'mlrd.' in text_to_translate:
        text_to_translate = text_to_translate.replace('mlrd.', 'mlrd')
    while 'tūkst.' in text_to_translate:
        text_to_translate = text_to_translate.replace('tūkst.', 'tūkst')

    text_field = browser.find_element_by_id('source')
    translated_text = ''

    while len(text_to_translate) > 2:
        if len(text_to_translate) > 4999:  # text field does not accept more than 5000 symbols
            cut_here = text_to_translate.rfind('\n', 0, 4999)  # last new line among the first 5000 symbols (to lose as little text meaning as possible
            text_field.send_keys(text_to_translate[:cut_here])
        else: 
            cut_here = len(text_to_translate)
            text_field.send_keys(text_to_translate)

        translate_click_counter = 0
        translate_button = browser.find_element_by_id('gt-submit')
        translate_button.click()
        wait(300, 200)

        while len(browser.find_element_by_id('result_box').text) < 5:
            translate_button.click()
            translate_click_counter += 1
            if translate_click_counter > 10: # 2 second timeout
                break
            wait(200)

        translated_text += browser.find_element_by_id('result_box').text

        text_to_translate = text_to_translate[cut_here:]
        text_field.clear()
        wait(50)
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

def most_common(lst):
    return max(set(lst), key = lst.count)
