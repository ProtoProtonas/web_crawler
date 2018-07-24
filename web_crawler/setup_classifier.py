import random
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
import nltk
import pandas as pd
from sklearn.utils import shuffle
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from web_navigator import download_article, translate_article, setup_chrome_translator
from text_processor import find_features, get_wordnet_pos
import pickle



def download_test_articles():

    if not os.path.isdir('tekstai_classifieriui/'):
        os.mkdir('tekstai_classifieriui/')

    df = pd.read_csv('su_dividendais.txt', sep = '\t', encoding = 'utf-16')
    df = shuffle(df)
    df = df.reset_index(drop = True)
    urls = df['Nuoroda']
    about_dividends = df['Ar apie dividendus?']

    datafile = open(r'tekstai_classifieriui/0.txt', 'w', encoding = 'utf-16')

    binary = FirefoxBinary(r'C:\Users\asereika\AppData\Local\Mozilla Firefox\firefox.exe')
    browser = webdriver.Firefox(firefox_binary = binary)

    for x, url in enumerate(urls):
        try:
            text, _ = download_article(url, browser)
            text = str(about_dividends[x]) + '\n' + text

            with open(r'tekstai_classifieriui/%s.txt' % str(x+1), 'w', encoding = 'utf-16') as f:
                f.write(text)

            datafile.write(str(x+1) + '\n')
            print(x + 1, 'files written')
        except Exception as e:
            print(e)
            with open(r'tekstai_classifieriui/%s.txt' % str(x+1), 'w', encoding = 'utf-16') as f:
                f.write('Nepavyko parsiųsti straipsnio')
        

    browser.close()
    datafile.close()
    print('Done downloading!')


def translate_articles():  # nereikia API, nes tekstui irasyti ir nuskaityti naudojamas headless browser
    amount_of_articles = 0
    with open(r'tekstai_classifieriui/0.txt', 'r', encoding = 'utf-16') as f:
        datafile = f.readlines()
        amount_of_articles = int(datafile[-1])

    browser = setup_chrome_translator()

    for x in range(1, amount_of_articles + 1):
        with open(r'tekstai_classifieriui/%s.txt'%x, 'r', encoding = 'utf-16') as f:
            text_to_translate = f.read()

        while 'mln.' in text_to_translate:
            text_to_translate = text_to_translate.replace('mln.', 'mln')
        while 'mlrd.' in text_to_translate:
            text_to_translate = text_to_translate.replace('mlrd.', 'mlrd')
        while 'tūkst.' in text_to_translate:
            text_to_translate = text_to_translate.replace('tūkst.', 'tūkst')

        category = text_to_translate[:text_to_translate.find('\n')]
        text_to_translate = text_to_translate[text_to_translate.find('\n')+1:]

        translated_text = translate_article(browser, text_to_translate)

        with open(r'tekstai_classifieriui/%s_en.txt'%x, 'w', encoding = 'utf-16') as f:
            f.write(category + '\n' + translated_text)        
        print(x, 'articles translated')


def get_featuresets():

    if not os.path.isdir('tekstai_classifieriui/'):
        os.mkdir('tekstai_classifieriui/')
    
    with open(r'tekstai_classifieriui/0.txt', 'r', encoding = 'utf-16') as f:
        datafile = f.readlines()
        amount_of_articles = int(datafile[-1])

    documents = []
    all_words = []
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    for x in range(1, amount_of_articles + 1):
        with open(r'tekstai_classifieriui/%s_en.txt' % x, 'r', encoding = 'utf-16') as f:
            text = f.read()
        #print('Reading file no.', x)
        
        category = text[:text.find('\n')]
        text = text[text.find('\n')+1:]

        if category == '1':
            category = 'div' # for dividends
        else:
            category = 'nodiv' # for no dividends

        words = word_tokenize(text)
        tagged = nltk.pos_tag(words)

        for m, tuple in enumerate(tagged):
            word = tuple[0]
            part_of_speech = tuple[1]

            # atskiras atvejis, kazkodel neatpazista, kad thousand yra skaicius (pvz million atpazista be problemu)
            if word == 'thousand':
                part_of_speech = 'CD'

            w = lemmatizer.lemmatize(word, get_wordnet_pos(part_of_speech))
            if w not in stop_words:
                if w not in """,...()'":-;''s``""":
                    words[m] = w
                    all_words.append(w.lower())

        documents.append((list(words), category))

    random.shuffle(documents)

    all_words = nltk.FreqDist(all_words)
    all_words = all_words.most_common(1000)

    word_features = []
    for w in all_words:
        word_features.append(w[0])

    pickle_out = open('word_features.pickle', 'wb')
    pickle.dump(word_features, pickle_out)
    pickle_out.close()
    print('word features has been saved')

    featuresets = []
    for rev, category in documents:
        featuresets.append((find_features(rev, word_features), category))

    return featuresets


def train_classfier(sets_of_features):

    length = len(sets_of_features)
    train_test_split = 0.75
    split = int(train_test_split * length)

    train_set = sets_of_features[:split]
    test_set = sets_of_features[split + 1:]
    
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    print("Classifier accuracy percent:", (nltk.classify.accuracy(classifier, test_set)) * 100)
    classifier.show_most_informative_features(30)
    accuracy = (nltk.classify.accuracy(classifier, test_set)) * 100

    # classifier.classify(featureset)
    return classifier


def main():
    download_test_articles()
    translate_articles()
    featuresets = get_featuresets()
    classifier = train_classfier(featuresets)
    pickle_out = open('classifier.pickle', 'wb')
    pickle.dump(classifier, pickle_out)
    pickle_out.close()
    

main()


