from web_navigator import get_google_search_links, get_bing_search_links, setup_chrome_translator, setup_firefox_for_article_download, download_article, translate_article
from html_processor import get_domain_name
from text_processor import get_featureset
from metadata_collector import get_title, get_date
from html_processor import html_comment
import pickle
import os
from link_collector import get_links_from_html


# main function designed for article download. Does not return anything
def main_download(keyword):
    # checks whether directory exists
    if not os.path.isdir('straipsniai/'):
        os.mkdir('straipsniai/')


    links = []
    links += get_google_search_links(keyword) # pick up urls from google search
    links += get_bing_search_links(keyword) # pick up urls form bing search
    links = list(links) # make them in a single dimension array (list). Just to be sure that this is one-dimensional
    print(len(links))

    # save urls for later use (i.e. fact checking or whatever else may come our way)
    with open('links.txt', 'w', encoding = 'utf-16') as f:
        for link in links:
            f.write(link + '\n')


    # links = list(['https://www.15min.lt/verslas/naujiena/energetika/finansu-analitikai-dividendus-apranga-mokes-o-del-teo-lt-neaisku-664-591077', 'https://www.delfi.lt/verslas/verslas/prasidejo-dvidesimtmecio-statybos-kaune-iskils-continental-gamykla.d?id=78623223'])

    browser_chrome = setup_chrome_translator()
    browser_firefox = setup_firefox_for_article_download()

    how_many_articles_downloaded = 0
    urls_to_save = []

    for x, url in enumerate(links):
        print(x)
        try:
            text, html = download_article(url, browser_firefox)  # text - just plain article text ||| html - webpage source code
            urls_from_page = get_links_from_html(html, '')
            url_blacklist = ['vmi.lt']

            for link in urls_from_page:
                if link not in url_blacklist:
                    urls_to_save.append(link)

            text = translate_article(browser_chrome, text) # text is translated to english

            pickle_in = open('classifier.pickle','rb')  # pre-trained classifier
            classifier = pickle.load(pickle_in)
            featureset = get_featureset(text)

            # actual prediction happens here based on the featureset of the article
            category = classifier.classify(featureset)
            print('Classified: ', category)

            # if the article matches the criteria that we are looking for we download it
            if category == 'div':
                # download
                how_many_articles_downloaded += 1
                with open(r'straipsniai/%s.txt' % how_many_articles_downloaded, 'w', encoding = 'utf-16') as f:
                    f.write(text)
                with open(r'straipsniai/%s.html' % how_many_articles_downloaded, 'w', encoding = 'utf-16') as f:
                    try:
                        date = html_comment(str(get_date(html)))
                    except Exception as e:
                        date = html_comment('Date not found')
                        print(e)

                    try:
                        title = html_comment(get_title(html))
                    except Exception as e:
                        title = html_comment('Title not found')
                        print(e)

                    metadata = html_comment(url) + '\n' + title + '\n' + date + '\n'  # some metadata as well since it will be needed later
                    f.write(metadata + html)
        except Exception as e:
            print(e)

    browser_chrome.close()
    browser_firefox.close()

    print(len(urls_to_save))

    if not os.path.isdir('nuorodos/'):
        os.mkdir('nuorodos/')

    # write urls_to_save to a file here




main_download('dividendai 2018')
