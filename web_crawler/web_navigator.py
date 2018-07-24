from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
import pyautogui


def wait(min, max = 0): # milliseconds to wait
    if min > max: 
        max = min
    time_to_wait = random.randint(min, max) / 1000
    time.sleep(time_to_wait)

def get_google_search_links(google_keyword):

    #binary = FirefoxBinary(r'C:\Users\asereika\AppData\Local\Mozilla Firefox\firefox.exe')
    #browser = webdriver.Firefox(firefox_binary = binary)

    # susetupina chrome headless browser (capabilities keiciami, kad nemestu "failed to load extension" erroro)
    capabilities = { 'chromeOptions':  { 'useAutomationExtension': False, 'args': ['--disable-extensions']}}
    browser = webdriver.Chrome(executable_path = 'chromedriver.exe', desired_capabilities = capabilities)

    # eina i google pagrindini puslapi
    browser.get('https://www.google.com/')
    search_bar = browser.find_element_by_name('q') # randa search bar pagal elemento pavadinima

    #search_bar.send_keys(google_keyword)
    for c in google_keyword:
        search_bar.send_keys(c) # suveda paieskos zodzius. iveda raides po viena, kad simuliuotu zmogaus narsyma
    search_bar.submit() # tas pats, kas paspausti enter
    time.sleep(1)
    all_the_links_collected = []

    while True:  # ciklas, skirtas isrinkti nuorodas i paieskos rezultatus
        html = browser.page_source
        links = html.split('<div class="g"')[1:] # splitina visa page source pagal g klase

        for x, link in enumerate(links):
            start = link.find('<a href="') + 9  # iesko href atributu, kad is ju galetu paimti nuorodas i tai, ko reikia (paieskos rezultatus)
            end = link[start:].find('"')  # nuoroda prasideda ir baigiasi kabutemis
            links[x] = link[start:start + end]  # modifikuoja links masyva, kad kompiuteriui reiktu priziuret maziau kintamuju

        try:
             next_page_button = browser.find_element_by_id('pnnext') # pagal id randa mygtuka, vedanti i kita google puslapi
             next_page_button.click()
        except Exception as e:  # gali ir nerasti to mygtuko, kai pasibaigia google rezultatai
            print(e)
            try:
                add_more_results = browser.find_element_by_xpath('//*[@id="ofr"]/i/a') # pagal xpath suranda nuoroda, kad google rodytu daugiau rezultatu (be sito rodo tik +-11 puslapiu most relevant rezultatu)
                add_more_results.click()
            except:
                break  # kai neranda nei kito puslapio, nei paieskos prapletimo mygtuko baigia paieska

        for link in links:
            all_the_links_collected.append(link)

        # bent kiek simuliuoja zmogaus narsyma
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


    # kaip veikia dalykai - ziureti virsuje, i google funkcija, nes siu abieju funkciju veikimo principas yra lygiai toks pats
    capabilities = { 'chromeOptions':  { 'useAutomationExtension': False, 'args': ['--disable-extensions']}}
    browser = webdriver.Chrome(executable_path = 'chromedriver.exe', desired_capabilities = capabilities)
    browser.get('https://www.bing.com/')

    search_bar = browser.find_element_by_name('q')
    search_bar.send_keys(bing_keyword)
    search_bar.submit()
    time.sleep(1)
    all_the_links_collected = []

    while True:
        html = browser.page_source
        links = html.split('<li class="b_algo"')[1:]

        for x, link in enumerate(links):
            start = link.find('<a href="') + 9
            end = link[start:].find('"')
            links[x] = link[start:start + end]

        if links == all_the_links_collected[-len(links):] and len(links) != len(all_the_links_collected):
            break

        for link in links:
            all_the_links_collected.append(link)
        
        try:
            next_page_button = browser.find_element_by_class_name('sb_pagN')
            next_page_button.click()
        except Exception as e: # programa baigia darba nucrashindama (crashas yra handlinamas ir visos surinktos nuorodos laikomos links masyve)
            print(e)
            break

        time_to_wait = random.randint(200, 350) / 100
        #print('Time to wait:', time_to_wait)
        time.sleep(time_to_wait)

    browser.close()

    return all_the_links_collected


# naudoja firefox reader mode atskirti straipsnio teksta nuo viso kito slamsto (reklamu, nuorodu i kitus straipsnius ir pan.)
def download_article(url, browser):

    # browser.get(url)
    # browser.set_page_load_timeout(10)
    # html = browser.page_source
    # browser.get('about:reader?url=' + url)  # einama i specialu reader mode, kuriuo naudojantis yra lengviau straipsnio teksta atskirti nuo viso kito teksto, esancio tame paciame puslapyje

    browser.get(url)
    html = browser.page_source
    browser.set_page_load_timeout(10)
    pyautogui.keyDown('F9')
    time.sleep(0.05)
    pyautogui.keyUp('F9')
    time.sleep(0.05)

    text = browser.find_element_by_tag_name('body').text
    # laukiama, kol uzsikraus puslapis
    a = 0
    while len(text) < 500:  
        text = browser.find_element_by_tag_name('body').text
        time.sleep(0.5)
        a += 1
        if a > 12: 
            return 'Unable to open page'

    cut_here = text.find('minute')
    if cut_here > 0:
        text = text[cut_here:]
        cut_here = text.find('\n')
        text = text[cut_here + 1:]

    return text, html


# isrenka nuorodas ir parsiuncia straipsnius, i kuriuos to nuorodos veda. Straipsnius suraso i atskirus sunumeruotus .txt failus 
#def download_test_articles():
#    df = pd.read_csv('su_dividendais.txt', sep = '\t', encoding = 'utf-16')
#    df = shuffle(df)
#    df = df.reset_index(drop = True)
#    urls = df['Nuoroda']
#    about_dividends = df['Ar apie dividendus?']

#    datafile = open(r'tekstai/0.txt', 'w', encoding = 'utf-16')

#    binary = FirefoxBinary(r'C:\Users\asereika\AppData\Local\Mozilla Firefox\firefox.exe')
#    browser = webdriver.Firefox(firefox_binary = binary)

#    for x, url in enumerate(urls):
#        try:
#            text = about_dividends[x] + '\n' + download_article(url, browser)

#            with open(r'tekstai/%s.txt' % str(x+1), 'w', encoding = 'utf-16') as f:
#                f.write(text)

#            datafile.write(str(x+1) + '\n')
#            print(x + 1, 'files written')
#        except:
#            print('Unable to download article')
        

#    browser.close()
#    datafile.close()
#    print('Done!')


def setup_firefox_for_article_download():
    binary = FirefoxBinary(r'C:\Users\asereika\AppData\Local\Mozilla Firefox\firefox.exe')
    browser_firefox = webdriver.Firefox(firefox_binary = binary)
    print('Firefox browser is set up and ready to go')
    return browser_firefox
    

def setup_chrome_translator():  # nereikia API, nes tekstui irasyti ir nuskaityti naudojamas headless browser
    capabilities = { 'chromeOptions':  { 'useAutomationExtension': False, 'args': ['--disable-extensions']}}  # be sito meta error
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

    print('Chrome for translation is set up and ready to go')
    return browser


def translate_article(browser, txt_to_translate):
    # isvalyti isversta teksta is anksciau
    while len(browser.find_element_by_id('result_box').text) > 5:
        try: 
            translate_button = browser.find_element_by_id('gt-submit')
            translate_button.click()
        except Exception as e:
            print('Could not locate the "Translate" button')
            print(e)
            break
        wait(100)

    text_to_translate = txt_to_translate # kad nesipainiotu kintamasis, kuris ateina is kitos funkcijos (to_translate)

    while 'mln.' in text_to_translate:
        text_to_translate = text_to_translate.replace('mln.', 'mln')
    while 'mlrd.' in text_to_translate:
        text_to_translate = text_to_translate.replace('mlrd.', 'mlrd')
    while 'tūkst.' in text_to_translate:
        text_to_translate = text_to_translate.replace('tūkst.', 'tūkst')

    text_field = browser.find_element_by_id('source')
    translated_text = ''

    while len(text_to_translate) > 2:
        if len(text_to_translate) > 4999:  # google translate teksto laukelis nepriima daugiau, nei 5000 simboliu
            cut_here = text_to_translate.rfind('\n', 0, 4999)  # paskutine nauja eilute tarp 5000 pirmuju simboliu. Eilute todel, kad tai butu pastraipos pabaiga ir kuo maziau pasikeistu teksto prasme verciant
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
            if translate_click_counter > 5:
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
    return max(set(lst), key=lst.count)
