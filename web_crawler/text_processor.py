#from bs4 import BeautifulSoup as bs
#from html_processor import extract_text, get_domain_name
#from selenium import webdriver
#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
import pickle
import random
import time
from nltk.tokenize import word_tokenize, PunktSentenceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
import nltk
import pyautogui


#CC	coordinating conjunction
#CD	cardinal digit
#DT	determiner
#EX	existential there (like: "there is" ... think of it like "there exists")
#FW	foreign word
#IN	preposition/subordinating conjunction
#JJ	adjective	'big'
#JJR	adjective, comparative	'bigger'
#JJS	adjective, superlative	'biggest'
#LS	list marker	1)
#MD	modal	could, will
#NN	noun, singular 'desk'
#NNS	noun plural	'desks'
#NNP	proper noun, singular	'Harrison'
#NNPS	proper noun, plural	'Americans'
#PDT	predeterminer	'all the kids'
#POS	possessive ending	parent\'s
#PRP	personal pronoun	I, he, she
#PRP$	possessive pronoun	my, his, hers
#RB	adverb	very, silently,
#RBR	adverb, comparative	better
#RBS	adverb, superlative	best
#RP	particle	give up
#TO	to	go 'to' the store.
#UH	interjection	errrrrrrrm
#VB	verb, base form	take
#VBD	verb, past tense	took
#VBG	verb, gerund/present participle	taking
#VBN	verb, past participle	taken
#VBP	verb, sing. present, non-3d	take
#VBZ	verb, 3rd person sing. present	takes
#WDT	wh-determiner	which
#WP	wh-pronoun	who, what
#WP$	possessive wh-pronoun	whose
#WRB	wh-abverb	where, when

#+ = match 1 or more
#? = match 0 or 1 repetitions.
#* = match 0 or MORE repetitions	  
#. = Any character except a new line


def is_worth_downloading(text):

    return False


def get_featureset(text):
    words = word_tokenize(text)
    tagged = nltk.pos_tag(words)

    for m, tuple in enumerate(tagged):
        word, part_of_speech = tuple

        # atskiras atvejis, kazkodel neatpazista, kad thousand yra skaicius (pvz million atpazista be problemu)
        if word == 'thousand':
            part_of_speech = 'CD'

        w = lemmatizer.lemmatize(word, get_wordnet_pos(part_of_speech))
        if w not in stop_words:
            if w not in """,...()'":-;''s``""":
                words[m] = w

    pickle_in = pickle.open('word_features.pickle')
    features = pickle.load(pickle_in)

    return find_features(list(words), features)


    



def get_featuresets():
    
    with open(r'tekstai/0.txt', 'r', encoding = 'utf-16') as f:
        datafile = f.readlines()
        amount_of_articles = int(datafile[-1])

    documents = []
    all_words = []
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    for x in range(1, amount_of_articles + 1):
        with open(r'tekstai/%s_en.txt' % x, 'r', encoding = 'utf-16') as f:
            text = f.read()
        #print('Reading file no.', x)
        
        category = text[:text.find('\n')]
        text = text[text.find('\n')+1:]

        url = text[:text.find('\n')]
        text = text[text.find('\n')+1:]

        if category == '1':
            category = 'div'
        else:
            category = 'nodiv'


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

    featuresets = []
    for rev, category in documents:
        featuresets.append((find_features(rev, word_features), category))

    return featuresets
    

def find_features(document, word_features):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = int(w in words)

    return features

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN    



def train_classfier(sets_of_features):
    length = len(sets_of_features)
    train_test_split = 0.75
    split = int(train_test_split * length)

    train_set = sets_of_features[:split]
    test_set = sets_of_features[split + 1:]
    
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    print("Classifier accuracy percent:", (nltk.classify.accuracy(classifier, test_set)) * 100)
    #classifier.show_most_informative_features(30)
    accuracy = (nltk.classify.accuracy(classifier, test_set)) * 100

    # classifier.classify(featureset)
    return accuracy, classifier





























#def wait(min, max = 0): # milliseconds to wait
#    if min > max: 
#        max = min
#    time_to_wait = random.randint(min, max) / 1000
#    time.sleep(time_to_wait)



## naudoja firefox reader mode atskirti straipsnio teksta nuo viso kito slamsto (reklamu, nuorodu i kitus straipsnius ir pan.)
#def download_article(url, browser):

#    #browser.get('about:reader?url=' + url)  # einama i specialu reader mode, kuriuo naudojantis yra lengviau straipsnio teksta atskirti nuo viso kito teksto, esancio tame paciame puslapyje

#    browser.get(url)
#    pyautogui.keyDown('F9')
#    time.sleep(0.05)
#    pyautogui.keyUp('F9')
#    time.sleep(0.5)

#    text = browser.find_element_by_tag_name('body').text
#    # laukiama, kol uzsikraus puslapis
#    a = 0
#    while len(text) < 500:  
#        text = browser.find_element_by_tag_name('body').text
#        time.sleep(0.5)
#        a += 1
#        if a > 12: 
#            return 'Nepavyko atidaryti puslapio'

#    cut_here = text.find('minute')
#    if cut_here > 0:
#        text = text[cut_here:]
#        cut_here = text.find('\n')
#        text = text[cut_here + 1:]

#    return url + '\n' + text


## isrenka nuorodas ir parsiuncia straipsnius, i kuriuos to nuorodos veda. Straipsnius suraso i atskirus sunumeruotus .txt failus 



#def setup_firefox_for_article_download():
#    binary = FirefoxBinary(r'C:\Users\asereika\AppData\Local\Mozilla Firefox\firefox.exe')
#    browser_firefox = webdriver.Firefox(firefox_binary = binary)
#    print('Firefox browser is set up and ready to go')
#    return browser_firefox
    

#def setup_chrome_translator():  # nereikia API, nes tekstui irasyti ir nuskaityti naudojamas headless browser
#    #amount_of_articles = 0
#    #with open(r'tekstai/0.txt', 'r', encoding = 'utf-16') as f:
#    #    datafile = f.readlines()
#    #    amount_of_articles = int(datafile[-1])

#    capabilities = { 'chromeOptions':  { 'useAutomationExtension': False, 'args': ['--disable-extensions']}}  # be sito meta error
#    browser = webdriver.Chrome(desired_capabilities = capabilities)
#    browser.get('https://translate.google.com/')
    
#    # originali teksto kalba
#    language_selector = browser.find_element_by_id('gt-sl-gms')
#    language_selector.click()
#    time.sleep(0.1)
#    language_selector = browser.find_element_by_xpath('//*[@id=":1l"]/div')  # pasirenka lietuviu
#    language_selector.click()
#    time.sleep(0.1)
#    # kalba i kuria norima isversti
#    language_selector = browser.find_element_by_id('gt-tl-gms')
#    language_selector.click()
#    time.sleep(0.1)
#    language_selector = browser.find_element_by_xpath('//*[@id=":3j"]/div')  # pasirenka anglu
#    language_selector.click()
#    time.sleep(0.1)

#    return browser


#def translate_article(browser, to_translate):
#    # isvalyti isversta teksta is anksciau
#    while len(browser.find_element_by_id('result_box').text) > 5:
#        try: 
#            translate_button = browser.find_element_by_id('gt-submit')
#            translate_button.click()
#        except Exception as e:
#            print('Could not locate the "Translate" button')
#            print(e)
#            break
#        wait(100)

#    text_to_translate = to_translate # kad nesipainiotu kintamasis, kuris ateina is kitos funkcijos (to_translate)

#    while 'mln.' in text_to_translate:
#        text_to_translate = text_to_translate.replace('mln.', 'mln')
#    while 'mlrd.' in text_to_translate:
#        text_to_translate = text_to_translate.replace('mlrd.', 'mlrd')
#    while 'tūkst.' in text_to_translate:
#        text_to_translate = text_to_translate.replace('tūkst.', 'tūkst')

#    #category = text_to_translate[:text_to_translate.find('\n')]
#    #text_to_translate = text_to_translate[text_to_translate.find('\n')+1:]

#    #url = text_to_translate[:text_to_translate.find('\n')]
#    #text_to_translate = text_to_translate[text_to_translate.find('\n')+1:]

#    text_field = browser.find_element_by_id('source')
#    translated_text = ''

#    while len(text_to_translate) > 2:
#        if len(text_to_translate) > 4999:  # google translate teksto laukelis nepriima daugiau, nei 5000 simboliu
#            cut_here = text_to_translate.rfind('\n', 0, 4999)  # paskutine nauja eilute tarp 5000 pirmuju simboliu. Eilute todel, kad tai butu pastraipos pabaiga ir kuo maziau pasikeistu teksto prasme verciant
#            text_field.send_keys(text_to_translate[:cut_here])
#        else: 
#            cut_here = len(text_to_translate)
#            text_field.send_keys(text_to_translate)

#        translate_click_counter = 0
#        translate_button = browser.find_element_by_id('gt-submit')
#        translate_button.click()
#        wait(300, 200)

#        while len(browser.find_element_by_id('result_box').text) < 5:
#            translate_button.click()
#            translate_click_counter += 1
#            if translate_click_counter > 5:
#                break
#            wait(200)

#        translated_text += browser.find_element_by_id('result_box').text

#        text_to_translate = text_to_translate[cut_here:]
#        text_field.clear()
#        wait(50)
#        translate_button.click()

#    return translated_text


#def get_clear_browsing_button(driver):
#    return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')

#def clear_cache(driver, timeout = 60):
#    driver.get('chrome://settings/clearBrowserData')

#    # wait for the button to appear
#    wait = WebDriverWait(driver, timeout)
#    wait.until(get_clear_browsing_button)

#    # click the button to clear the cache
#    get_clear_browsing_button(driver).click()

#    # wait for the button to be gone before returning
#    wait.until_not(get_clear_browsing_button)

#def most_common(lst):
#    return max(set(lst), key=lst.count)


#def create_lexicon(article):
#    lemmatizer = WordNetLemmatizer()

#    words = word_tokenize(article)
#    words = [lemmatizer.lemmatize(word) for word in words]

#    with open(r'tekstai/26_en.txt', 'r', encoding = 'utf-16') as f:
#        trained_tokenizer = PunktSentenceTokenizer(f.read())

#    tokenized_text = trained_tokenizer.tokenize(article)

#    try:
#        #for i in tokenized_text:
#        #    words = nltk.word_tokenize(i)
#        #    tagged = nltk.pos_tag(words)
#        #    print(tagged)
#        #    for word in tagged:
#        #        if 'NNP' in word: 
#        #            print(word)
        
#        for i in tokenized_text:
#            words = nltk.word_tokenize(i)
#            tagged = nltk.pos_tag(words)
#            #chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
#            chunkGram = r"""Chunk: {<NNP>+<VB.?>+}"""
#            #chunkGram = r"""Chunk: {<NNP>+}"""
#            chunkParser = nltk.RegexpParser(chunkGram)
#            chunked = chunkParser.parse(tagged)
#            #chunked.draw()
#            subtrees_of_interest = []
#            for subtree in chunked.subtrees(filter = lambda t: t.label() == 'Chunk'):
#                subtrees_of_interest.append(subtree)



#    except Exception as e:
#        print(str(e))

#    #print(subtrees_of_interest, '\n')
    #return most_common(list(subtrees_of_interest))

    #stop_words = set(stopwords.words('english'))
    #filtered_sentence = []

    #for w in words:
    #    if w not in stop_words:
    #        filtered_sentence.append(w)

    #return filtered_sentence

#def main():
#    binary = FirefoxBinary(r'C:\Users\asereika\AppData\Local\Mozilla Firefox\firefox.exe')
#    browser = webdriver.Firefox(firefox_binary = binary)
#    url = 'https://www.lrytas.lt/verslas/sekmes-istorijos/2018/07/18/news/kauno-sekme-be-cia-kuriamu-gaminiu-neissivercia-pasaulines-imones-6981729/'
#    print(download_article(url, browser, 0))
