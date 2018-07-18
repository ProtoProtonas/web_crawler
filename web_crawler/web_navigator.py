from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import random
import os

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
            print(link) # printina visas nuorodas, kad zmogus galetu matyti, kaip viskas vyksta
        print(len(links))

        for link in links:
            all_the_links_collected.append(link)

        # bent kiek simuliuoja zmogaus narsyma
        time_to_wait = random.randint(100, 500) / 100
        print('Time to wait:', time_to_wait)
        time.sleep(time_to_wait)
        
    print(len(all_the_links_collected))



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

        for link in links:
            print(link)
        print(len(links))

        if links == all_the_links_collected[-len(links):] and len(links) != len(all_the_links_collected):
            print('Nuorodos kartojasi')
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
        print('Time to wait:', time_to_wait)
        time.sleep(time_to_wait)

    print(len(all_the_links_collected))




#get_bing_search_links('dividendai')
#get_google_search_links('lenovo')
