from web_navigator import get_google_search_links, get_bing_search_links, setup_chrome_translator, setup_firefox_for_article_download, download_article, translate_article, wait
from html_processor import get_domain_name, html_comment, extract_html_comment
from text_processor import get_featureset, get_dividends, get_company_name
from metadata_collector import get_title, get_date
from link_collector import get_links_from_html
import pickle
import os
import time
import random
import pandas as pd
import datetime

# main function designed for article download. Does not return anything
def main_download(keyword):

    page_load_timetout = 10 # in seconds
    url_blacklist = []
    with open('url_blacklist.txt', 'r') as f:
        url_blacklist = f.readlines()
    maximum_text_length = 15000 # maximum text length in characters (if article is longer exception is thrown). Necessary because long articles take a lot of time to translate (and are probably not what we are looking for)


    # checks whether directory exists
    if not os.path.isdir('straipsniai/'):
        os.mkdir('straipsniai/')

    if not os.path.isdir('nuorodos/'):
        os.mkdir('nuorodos/')


    links = []
    links += get_google_search_links(keyword) # pick up urls from google search
    links += get_bing_search_links(keyword) # pick up urls form bing search
    links = list(links) # make them in a single dimension array (list). Just to be sure that this is one-dimensional
    
    with open(r'nuorodos/links_from_web_search.txt', 'w', encoding = 'utf-16') as f:
        for link in links:
            f.write(link + '\n')

    print(len(links))


    #links = list(['https://www.15min.lt/verslas/naujiena/energetika/finansu-analitikai-dividendus-apranga-mokes-o-del-teo-lt-neaisku-664-591077', 'https://www.delfi.lt/auto/patarimai/siulo-baudas-uz-ket-pazeidimus-israsyti-automatiskai.d?id=78664537', 'https://www.delfi.lt/verslas/verslas/prasidejo-dvidesimtmecio-statybos-kaune-iskils-continental-gamykla.d?id=78623223', 'https://www.vmi.lt/cms/web/kmdb/1.4.8.5', 'https://www.15min.lt/verslas/naujiena/bendroves/rokiskio-suris-ismokes-3-2-mln-euru-dividendu-663-790246', 'https://www.vz.lt/agroverslas/maisto-pramone/2018/06/18/mars-lietuva-dividendams-skyre-40-mlneur'])  # just a small sample for quick testing

    browser_chrome = setup_chrome_translator()
    browser_firefox = setup_firefox_for_article_download()
    browser_firefox.set_page_load_timeout(page_load_timetout)

    how_many_articles_downloaded = 0
    urls_to_save = []

    random.shuffle(links)

    # performance measurements

    time_start = time.time()  # unix time in seconds (floating point)
    links_collected = len(links)
    how_many_urls_failed_to_open = 0

    # remove blacklisted urls
    no_of_blacklisted_urls = 0
    for url in links:
        for blacked_url in url_blacklist:
            if blacked_url in url:
                # try statement just because my blacklist includes domain names as well as filetypes (you can put literally anything there, as long as it is a string) so a single url may have blacklisted domain name and blacklisted filetype
                try:  
                    links.remove(url)
                    no_of_blacklisted_urls += 1
                except:
                    pass
    print(no_of_blacklisted_urls, 'blacklisted URLs removed')
    # main loop

    for x, url in enumerate(links):
        print(x + 1, '/', links_collected - no_of_blacklisted_urls)
        try:
            text_lt, html = download_article(url, browser_firefox)  # text - just plain article text ||| html - webpage source code
            if len(text_lt) > maximum_text_length:
                raise Exception('Article too long') # protection against webpages that fail to utilize reader mode (otherwise the whole webapge is translated)
            urls_from_page = get_links_from_html(html, get_domain_name(url))

            for link in urls_from_page:  
                for blacked_url in url_blacklist:  
                    if blacked_url not in link:
                        urls_to_save.append(link)
                        break

            text_en = translate_article(browser_chrome, text_lt) # text is translated to english

            pickle_in = open('classifier.pickle','rb')  # pre-trained classifier
            classifier = pickle.load(pickle_in)
            featureset = get_featureset(text_en)

            # actual prediction happens here based on the featureset of the article
            category = classifier.classify(featureset)
            print('Classified: ', category)

            # if the article matches the criteria that we are looking for we download it
            if category == 'div':
                # download
                how_many_articles_downloaded += 1
                with open(r'straipsniai/%s.txt' % how_many_articles_downloaded, 'w', encoding = 'utf-16') as f:
                    try:
                        date = str(get_date(html)) # try to make up date from page source
                    except Exception as e:
                        date = 'Date not found'
                        print('Date not found: ', e)

                    try:
                        title = get_title(html) # as well as the title
                    except Exception as e:
                        title = 'Title not found'
                        print('Title not found: ', e)

                    metadata = url + '\n#####\n' + title + '\n#####\n' + date  # some metadata as well since it will be needed later
                    f.write(text_lt + '\n#####\n' + text_en + '\n#####\n' + metadata)
                with open(r'straipsniai/%s.html' % how_many_articles_downloaded, 'w', encoding = 'utf-16') as f:
                    f.write(html)
        except Exception as e:
            print('main.py exception 1: ', e)
            print(url)
            how_many_urls_failed_to_open += 1

    try:
        browser_chrome.close()
        browser_firefox.close() # usually raises exception
    except Exception as e:
        print('Failed to close browser: ', e)


    time_end = time.time() # just some timing for performance stats



    total_time = time_end - time_start
    avg_time_per_article = total_time / links_collected
    with open('performance.txt', 'w', encoding = 'utf-16') as f:
        to_write = 'Total time: ' + str(total_time) + ' seconds\nAverage time per article: ' + str(avg_time_per_article) + ' seconds\nTotal articles checked: ' + str(links_collected) + '\nTotal articles downloaded: ' + str(how_many_articles_downloaded) + '\nTotal urls collected: ' + str(len(urls_to_save)) + '\nBlacklisted URLs removed: ' + str(no_of_blacklisted_urls) + '\nURLs failed to open: ' + str(how_many_urls_failed_to_open)
        f.write(to_write)

    with open(r'nuorodos/links_collected_from_scraping.txt', 'a', encoding = 'utf-16') as f:
        for link in urls_to_save:
            f.write(link + '\n')


def main_analyze():
    # initialize pandas dataframe for relatively easy data manipulation
    columns = ['Pavadinimas', 'Straipsnio data', 'Nuoroda', 'Dividendai viso', 'Dividendai/akcija', 'Periodas', 'Valiuta', 'Kompanija']
    df = pd.DataFrame()

    # get file list of the 'straipsniai/' directory
    path = 'straipsniai/'
    filenames = os.listdir(path)
    filenames = [s.split('.')[0] for s in filenames]
    filenames = list(set(filenames)) # remove duplicate file names

    a = 0
    for article in filenames:
        a += 1
        print(a, '/%s' % len(filenames))

        with open(path + article + '.txt', 'r', encoding = 'utf-16') as f:
            text = f.read()

            lt_text, en_text, url, name, date = text.split('\n#####\n')

            # tidy up the text a bit, also this helps the algorithm to find names a whole lot
            en_text = en_text.replace('euros', 'EUR')
            en_text = en_text.replace('euro', 'EUR')
            en_text = en_text.replace('litas', 'LTL')
            en_text = en_text.replace('Lt', 'LTL')
            en_text = en_text.replace('LT', 'LTL')

            while lt_text.find('\n') != -1:
                lt_text = lt_text.replace('\n', '. ')
            while lt_text.find('..') != -1:
                lt_text = lt_text.replace('..', '.')
            while lt_text.find('  ') != -1:
                lt_text = lt_text.replace('  ', ' ')

            lt_text = lt_text.replace('tūkst.', 'tūkst')
            lt_text = lt_text.replace('mln.', 'mln')
            lt_text = lt_text.replace('mlrd.', 'mlrd')

            
            dividends = get_dividends(en_text)

            if dividends['Periodas'] != []: # if at least some form of dividend was found, otherwise there is no point in looking for a company name if we have no dividends that could go with it
                dividends = get_company_name(lt_text, dividends)

            periods = dividends['Periodas']
            div_total = dividends['Dividendai viso']
            div_per_share = dividends['Dividendai/akcija']
            currency = dividends['Valiuta']
            try:
                company = dividends['Kompanija']
            except:
                pass

        try:
            date = date.split('-')
            date = datetime.date(year = int(date[0]), month = int(date[1]), day = int(date[2]))
        except:
            date = datetime.date(7777, 11, 11)

        for x in range(len(periods)): # all of the arrays in the new_dict hastable have exactly the same length so we just need to choose one
            period = periods[x]
            if period < 0:
                period = date.year + period

            s = pd.Series([name, date, url, int(div_total[x]), float(div_per_share[x]), int(period), currency[x], company[x]], index = columns)
            df = df.append(s, ignore_index = True)

    df[['Dividendai viso', 'Periodas']] = df[['Dividendai viso', 'Periodas']].astype(int)
    df['Dividendai/akcija'] = df['Dividendai/akcija'].astype(float)
    df = df.reset_index(drop = True)
    df = df.drop_duplicates()
    df.to_csv('maindataframe.csv', encoding = 'utf-16', sep = '\t')
    print('The output data has been saved to a file succesfully.')

#main_download('dividendai 2018')
main_analyze()