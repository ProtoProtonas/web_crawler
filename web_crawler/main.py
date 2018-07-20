from web_navigator import get_google_search_links, get_bing_search_links, setup_chrome_translator, setup_firefox_for_article_download, download_article, translate_article
from html_processor import get_domain_name
from text_processor import get_featureset
import pickle



def main_download(keyword):
    #links = []
    #links += get_google_search_links(keyword)
    #links += get_bing_search_links(keyword)
    #links = list(links)

    links = list(['https://www.15min.lt/verslas/naujiena/energetika/finansu-analitikai-dividendus-apranga-mokes-o-del-teo-lt-neaisku-664-591077'])#, 'https://www.delfi.lt/verslas/verslas/prasidejo-dvidesimtmecio-statybos-kaune-iskils-continental-gamykla.d?id=78623223'])

    browser_chrome = setup_chrome_translator()
    browser_firefox = setup_firefox_for_article_download()

    for url in links:
        text = download_article(url, browser_firefox)
        text = translate_article(browser_chrome, text)

        pickle_in = open('classifier.pickle','rb')
        classifier = pickle.load(pickle_in)
        featureset = get_featureset(text)
        print(featureset)
        
        # check if it is worth downloading
        # download / do not download
    browser_chrome.close()
    browser_firefox.close()


main_download('dividendai')