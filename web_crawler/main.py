from html_processor import get_domain_name, html_comment, extract_text
from link_collector import get_links_from_html
from metadata_collector import get_title, get_date
from text_processor import get_featureset, get_dividends, get_company_name, normalize_text
from web_navigator import get_google_search_links, get_bing_search_links, download_article, translate_article, wait
import numpy as np
import pickle
import os
import time
import random
import pandas as pd
import datetime

# main function designed for article download. Does not return anything
def main_download(keyword):

    url_blacklist = []
    with open('url_blacklist.txt', 'r') as f:
        url_blacklist = f.read()
        url_blacklist = url_blacklist.split('\n')

    # checks whether directory exists
    if not os.path.isdir('straipsniai/'):
        os.mkdir('straipsniai/')

    if not os.path.isdir('nuorodos/'):
        os.mkdir('nuorodos/')

    # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<
    # select whether URLs are already collected from web search
    already_collected = 1
    # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<
    if already_collected == 0:
        links = []
        print('Fetching Google Search results...')
        links += get_google_search_links(keyword) # pick up urls from google search
        print('Total URLs collected: ', len(links))
        print('Fetching Bing Search results...')
        links += get_bing_search_links(keyword) # pick up urls form bing search
        print('Total URLs collected: ', len(links))
        time.sleep(1)
        links = list(links) # make them in a single dimension array (list). Just to be sure that this is one-dimensional
        
        with open(r'nuorodos/links_from_web_search.txt', 'w', encoding = 'utf-16') as f:
            for link in links:
                f.write(link + '\n')
    
    else:
        with open(os.path.join('nuorodos', 'links_from_web_search.txt'), 'r', encoding = 'utf-16') as f:
            links = f.read()
            links = links.split('\n')

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
        for blacklisted_url in url_blacklist:
            if blacklisted_url in url:
                links.remove(url)
                no_of_blacklisted_urls += 1
                break

    print(no_of_blacklisted_urls, 'blacklisted URLs removed')
    # main loop

    pickle_in = open('classifier.pickle','rb')  # pre-trained classifier
    classifier = pickle.load(pickle_in)
    print('Classifier loaded succesfully')

    for x, url in enumerate(links):
        print(x + 1, '/', len(links))

        try:
            text_lt, html = download_article(url)  # text - just plain article text ||| html - webpage source code

            urls_from_page = get_links_from_html(html, get_domain_name(url))

            for link in urls_from_page:  
                for blacked_url in url_blacklist:  
                    if blacked_url not in link:
                        urls_to_save.append(link)
                        break

            text_en = translate_article(text_lt) # text is translated to english
            featureset = get_featureset(text_en)

            # actual prediction happens here based on the featureset of the article
            category = classifier.classify(featureset)
            print('Classified: ', category)
            del(featureset)

            # if the article matches the criteria that we are looking for we download it
            if category == 'div':
                # download
                how_many_articles_downloaded += 1

                with open(os.path.join('straipsniai', '%s.html' % how_many_articles_downloaded), 'wb') as f:
                    f.write(html)

                with open(os.path.join('straipsniai', '%s.txt' % how_many_articles_downloaded), 'w', encoding = 'utf-16') as f:
                    try:
                        date = get_date(str(html)) # try to retrieve date from page source
                    except Exception as e:
                        date = '7777-11-11'
                        print('main.py exception 3: Date not found: ', e)

                    try:
                        title = get_title(html) # as well as the title
                    except Exception as e:
                        title = 'Title not found'
                        print('main.py exception 4: Title not found: ', e)

                    metadata = url + '\n#####\n' + title + '\n#####\n' + date  # some metadata as well since it will be needed later
                    f.write(text_lt + '\n#####\n' + text_en + '\n#####\n' + metadata)

            
            del(text_en)
            del(text_lt)
            del(html)
                    

        except Exception as e:
            print('main.py exception 5: ', e)
            # print(url)
            how_many_urls_failed_to_open += 1

        time.sleep(2) # pay respect to servers

    time_end = time.time() # just some timing for performance stats


    total_time = time_end - time_start
    avg_time_per_article = total_time / links_collected
    with open('performance.txt', 'w', encoding = 'utf-16') as f:
        # write performance measurements for later inspection
        to_write = 'Total time: ' + str(total_time) + ' seconds\nAverage time per article: ' + str(avg_time_per_article) + ' seconds\nTotal articles checked: ' + str(links_collected) + '\nTotal articles downloaded: ' + str(how_many_articles_downloaded) + '\nTotal urls collected: ' + str(len(urls_to_save)) + '\nBlacklisted URLs removed: ' + str(no_of_blacklisted_urls) + '\nURLs failed to open: ' + str(how_many_urls_failed_to_open)
        f.write(to_write)

    with open(os.path.join('nuorodos', 'links_collected_from_scraping.txt'), 'a', encoding = 'utf-16') as f:
        for link in urls_to_save:
            f.write(str(link) + '\n')


def main_analyze():
    # initialize pandas dataframe for relatively easy data manipulation
    columns = ['Pavadinimas', 'Straipsnio data', 'Nuoroda', 'Dividendai viso', 'Dividendai/akcija', 'Periodas', 'Valiuta', 'Kompanija', 'Šalis', 'Kada pasiektas straipsnis', 'Straipsnio numeris']
    df = pd.DataFrame(index = columns)

    # get file list of the 'straipsniai/' directory
    path = 'straipsniai/'
    filenames = os.listdir(path)
    filenames = [s if 'txt' in s else '0' for s in filenames]
    filenames = list(set(filenames)) # remove duplicate file names
    filenames.remove('0')

    a = 0
    for article in filenames:
        a += 1
        print(a, '/ %s' % len(filenames))

        path_to_the_file = os.path.join(path, article)

        with open(path_to_the_file, 'r', encoding = 'utf-16') as f:
            text = f.read()

            lt_text, en_text, url, name, date = text.split('\n#####\n')

            # tidy up the text a bit, also this helps the algorithm to find names a whole lot easier
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
                dividends = get_company_name(name, lt_text, dividends)

            periods = dividends['Periodas']
            div_total = dividends['Dividendai viso']
            div_per_share = dividends['Dividendai/akcija']
            currency = dividends['Valiuta']
            country = dividends['Šalis']

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

            if period <= datetime.datetime.now().year:
                access_date_of_the_article = os.path.getmtime(path_to_the_file) # article was accessed exactly when the file was created (+- a few minutes which is not a significant difference in this case)
                access_date_of_the_article = datetime.datetime.utcfromtimestamp(access_date_of_the_article).strftime('%Y-%m-%d %H:%M:%S')
                s = pd.Series([name, date, url, int(div_total[x]), float(div_per_share[x]), int(period), currency[x], company[x], country[x], access_date_of_the_article, article], index = columns)
                df = df.append(s, ignore_index = True)

    df = df.dropna(how = 'all')
    df['Dividendai viso'] = df['Dividendai viso'].astype(int)
    df['Periodas'] = df['Periodas'].astype(int)
    df['Dividendai/akcija'] = df['Dividendai/akcija'].astype(float)
    df = df.reset_index(drop = True)
    #df = df.drop_duplicates(subset = ['Dividendai viso', 'Periodas', 'Dividendai/akcija', 'Kompanija', 'Valiuta']) # drops rows that are duplicates in these columns alone and not in the whole dataframe
    #df = df.drop_duplicates()
    df.to_csv('maindataframe.csv', encoding = 'utf-16', sep = '\t', index = False)
    print('Duomenys išsaugoti sėkmingai.')

main_download('dividendai 2019')
main_analyze()
