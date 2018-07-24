from web_navigator import get_google_search_links, get_bing_search_links, setup_chrome_translator, setup_firefox_for_article_download, download_article, translate_article
from html_processor import get_domain_name
from text_processor import get_featureset
from metadata_collector import get_title, get_date
from html_processor import html_comment
import pickle
import os



def main_download(keyword):
    # checks whether directory exists
    if not os.path.isdir('straipsniai/'):
        os.mkdir('straipsniai/')


    links = []
    links += get_google_search_links(keyword)
    links += get_bing_search_links(keyword)
    links = list(links)
    print(len(links))


    with open('links.txt', 'w', encoding = 'utf-16') as f:
        for link in links:
            f.write(link + '\n')


    # links = list(['https://www.15min.lt/verslas/naujiena/energetika/finansu-analitikai-dividendus-apranga-mokes-o-del-teo-lt-neaisku-664-591077', 'https://www.delfi.lt/verslas/verslas/prasidejo-dvidesimtmecio-statybos-kaune-iskils-continental-gamykla.d?id=78623223'])

    browser_chrome = setup_chrome_translator()
    browser_firefox = setup_firefox_for_article_download()

    a = 0

    for x, url in enumerate(links):
        print(x)
        try:
            text, html = download_article(url, browser_firefox)
            text = translate_article(browser_chrome, text)

            pickle_in = open('classifier.pickle','rb')
            classifier = pickle.load(pickle_in)
            featureset = get_featureset(text)
            # print(featureset, '\n\n\n')

            category = classifier.classify(featureset)
            print('Classified: ', category)

            if category == 'div':
                # download
                a += 1
                print(a)
                with open(r'straipsniai/%s.txt' % a, 'w', encoding = 'utf-16') as f:
                    f.write(text)
                with open(r'straipsniai/%s.html' % a, 'w', encoding = 'utf-16') as f:

                    try:
                        date = html_comment(str(get_date(html)))
                    except:
                        date = html_comment('Date not found')

                    try:
                        title = html_comment(get_title(html))
                    except:
                        title = html_comment('Title not found')

                    metadata = html_comment(url) + '\n' + title + '\n' + date + '\n'
                    f.write(metadata + html)
        except Exception as e:
            print(e)

    browser_chrome.close()
    browser_firefox.close()


main_download('dividendai 2018')
