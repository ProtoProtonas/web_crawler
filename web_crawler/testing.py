import datetime
import random
from link_collector import get_whole_html
from metadata_collector import get_date
from html_processor import extract_text
import time
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs


def check_date(actual_date, html_date):
    return actual_date == html_date

def get_html_date(html):
    return get_date(html)

def main():
    correct = 0
    total = 0
    date = 0
    url = 0
    with open('su_dividendais.csv', 'r') as f:
        entries = f.readlines()
        #dataframe_head = entries[0]
        entries = entries[1:]
        random.shuffle(entries)
        #print(entries)
        for line in entries:
            try:
                line = line.replace('\n', '')
                url = line.split(';')[0]
                actual_date = line.split(';')[-1]
                actual_date = actual_date.split('-')
                actual_date = datetime.date(int(actual_date[0]), int(actual_date[1]), int(actual_date[2]))

                html = get_whole_html(url)
                html_date = get_html_date(html)

                print(url)
                print('\n', actual_date, '   ', html_date, '\n\n\n')
                if actual_date == html_date:
                    correct += 1
                total += 1
                time.sleep(1)

            except Exception:
                pass
    print(correct, total)
#main()

def get_article_text(url):
    binary = FirefoxBinary(r'C:\Users\asereika\AppData\Local\Mozilla Firefox\firefox.exe')
    browser = webdriver.Firefox(firefox_binary = binary)
    browser.get('about:reader?url=' + url)  # einama i specialu reader mode, kuriuo naudojantis yra lengviau straipsnio teksta atskirti nuo viso kito teksto, esancio tame paciame puslapyje

    body = browser.find_element_by_tag_name('body').text
    # laukiama, kol uzsikraus puslapis
    while len(body) < 500:  
        body = browser.find_element_by_tag_name('body').text
        time.sleep(0.5)

    return body


#html = get_article_text('http://www.rokiskio.com/lt/suris/pagrindinis-meniu/investuotojams/Visuotiniai-akcininku-susirinkimai/priskaiciuoti-dividendai-2.html')
#html = get_article_text('https://www.delfi.lt/verslas/verslas/es-pinigu-paradoksas-lietuva-ne-turtinga-o-pigi-todel-gaus-maziau.d?id=78535919')

#with open('vz.txt', 'w', encoding = 'utf-16') as f:
#    f.write(html)
#    print('html saved')
    
