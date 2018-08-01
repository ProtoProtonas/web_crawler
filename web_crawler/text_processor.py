import pickle
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
import nltk
from nltk.tree import Tree
import pandas as pd

#CC	    coordinating conjunction
#CD	    cardinal digit
#DT	    determiner
#EX	    existential there (like: "there is" ... think of it like "there exists")
#FW	    foreign word
#IN	    preposition/subordinating conjunction
#JJ	    adjective	'big'
#JJR	adjective, comparative	'bigger'
#JJS	adjective, superlative	'biggest'
#LS	    list marker	1)
#MD	    modal	could, will
#NN	    noun, singular 'desk'
#NNS	noun plural	'desks'
#NNP	proper noun, singular	'Harrison'
#NNPS	proper noun, plural	'Americans'
#PDT	predeterminer	'all the kids'
#POS	possessive ending	parent\'s
#PRP	personal pronoun	I, he, she
#PRP$	possessive pronoun	my, his, hers
#RB	    adverb	very, silently,
#RBR	adverb, comparative	better
#RBS	adverb, superlative	best
#RP	    particle	give up
#TO	    to	go 'to' the store.
#UH	    interjection	errrrrrrrm
#VB	    verb, base form	take
#VBD	verb, past tense	took
#VBG	verb, gerund/present participle	taking
#VBN	verb, past participle	taken
#VBP	verb, sing. present, non-3d	take
#VBZ	verb, 3rd person sing. present	takes
#WDT	wh-determiner	which
#WP	    wh-pronoun	who, what
#WP$	possessive wh-pronoun	whose
#WRB	wh-abverb	where, when

#+ = match 1 or more
#? = match 0 or 1 repetitions.
#* = match 0 or MORE repetitions	  
#. = Any character except a new line



def get_featureset(text): # returns featureset (dictionary with most popular words and T/F if the word is in article or not)
    lemmatizer = WordNetLemmatizer()  # initialize lemmatizer object
    words = word_tokenize(text) # one long text string is separated into array of words
    tagged = nltk.pos_tag(words) # parts of speech are identified for lemmatization
    stop_words = set(stopwords.words('english'))  # array of words that have no useful meaning and are there just to make speech sound more natural (computer does not care about them at all)

    for m, word_and_tag in enumerate(tagged):
        word, part_of_speech = word_and_tag

        # for some reason the word 'thousand' is not recognized as cardinal digit (unlike 'million' or 'billion') by the algorithm, so we help it a little bit
        if word == 'thousand':
            part_of_speech = 'CD'

        w = lemmatizer.lemmatize(word, get_wordnet_pos(part_of_speech)) # a single word is lemmatized (turned back into it's initial form)
        # check if the word has any meaning
        if w not in stop_words:
            if w not in """,...()'":-;''s``""":
                words[m] = w

    pickle_in = open('word_features.pickle', 'rb')  # most popular words from a small dataset that we use as features
    features = pickle.load(pickle_in)
    pickle_in.close()

    return find_features(list(words), features)

# featureset of the specific article is made up
def find_features(document, word_features):
    words = set(document)
    features = {} # empty dictionary is initialized
    for w in word_features:
        features[w] = int(w in words) # dictionary entries are added

    return features

# returns part of speech (given a tag)
def get_wordnet_pos(treebank_tag): # returns part of speech

    if treebank_tag.startswith('J'):
        return wordnet.ADJ  # adjective
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV # adverb
    else:
        return wordnet.NOUN

def get_countries(en_text):
    tokenized = word_tokenize(en_text)
    tagged_text = nltk.pos_tag(tokenized)

    namedEnt = nltk.ne_chunk(tagged_text, binary = False)
    namedEnt.draw()
    print(tagged_text)

def get_dividend_amount_total(en_text):   # kind of working but has plenty of its own quirks
    tokenized = word_tokenize(en_text)
    tagged_text = nltk.pos_tag(tokenized)

    chunk_gram = r"""Chunk: {<VB?>*<RP>?<CD>+<NN?>}"""
    chunk_parser = nltk.RegexpParser(chunk_gram)
    chunked = chunk_parser.parse(tagged_text)

    money = []
    for subtree in chunked.subtrees(filter = lambda t: t.label() == 'Chunk'):
        #subtree = Tree(subtree)
        #print('sldgsdf', subtree.leaves())
        try:
            numbers_from_text = []
            for word, _ in subtree.leaves():
                if 'percent' in word:
                    raise Exception
                numbers_from_text.append(word)
            print(subtree, '\n', numbers_from_text)
            money.append(numbers_from_text)

        except:
            pass
    print(money)

# T/F whether a string is a number or not
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

# T/F whether string contains numbers or not
def has_digits(s):
    digs = s.split(' ')
    digs = [is_number(x) for x in digs]
    if True in digs:
        return True
    return False

# returns dividend amount per single share (if able to find it)
def get_dividend_amount_per_share(en_text):
    sents = en_text
    while '\n' in sents:
        sents = sents.replace('\n', '. ') # some articles are not in a great format so that should be fixed up (or it may have some irrelevant data in some of its lines)
    while '..' in sents:
        sents = sents.replace('..', '.')  # for every case where sentence and line end in the same place

    tokenized = sent_tokenize(sents) # split up the article into sentences
    sentences_with_share = []
    for sent in tokenized:
        if 'per share' in sent or ' a share' in sent: # since we are looking for dividends/share
            if 'equity' not in sent: # noticed from testing that most of sentences that have the word 'equity' tell nothing about dividends
                sentences_with_share.append(sent)
        
    for x, _ in enumerate(sentences_with_share):  # just some tidying up (and capitalize money codes as it is easier for part of speech tagger to recognize them correctly)
        while sentences_with_share[x].find('*') != -1:
            sentences_with_share[x] = sentences_with_share[x].replace('*', '')
        while sentences_with_share[x].find('eur') != -1:
            sentences_with_share[x] = sentences_with_share[x].replace('eur', 'EUR')
        while sentences_with_share[x].find('litas') != -1:
            sentences_with_share[x] = sentences_with_share[x].replace('litas', 'LTL')
        while sentences_with_share[x].find('ltl') != -1:
            sentences_with_share[x] = sentences_with_share[x].replace('ltl', 'LTL')
        while sentences_with_share[x].find('sek') != -1:
            sentences_with_share[x] = sentences_with_share[x].replace('sek', 'SEK')

    for sent in sentences_with_share:
        sent_tokenized = word_tokenize(sent)
        tagged = nltk.pos_tag(sent_tokenized)

        chunk_gram = r"""Per share: {<NN.?>?<CD>+<NN.?>*(<IN><NN.?>)?((<IN><NN>)|(<DT><NN>))?}"""  # basically the main brains of this function (actually a template of how a sentence should look). Testing proved this to be good enough template
        chunk_parser = nltk.RegexpParser(chunk_gram)
        chunked = chunk_parser.parse(tagged) # find relevant chunks that fit the 'main brains' template

        for subtree in chunked.subtrees(filter = lambda t: t.label() == 'Per share'):
            extracted_info = ''
            for word, _ in subtree.leaves():
                extracted_info += word.replace(',', '.') + ' '

            if 'share' in extracted_info and has_digits(extracted_info):  # look for '0.07 EUR per share' or something with similar criteria

                nums = []
                [nums.append(float(s)) for s in extracted_info.split(' ') if is_number(s)] # collect all the numbers from extracted_info string
                dividends_per_share = nums[0] # we assume the first digit is the only digit in the chunk
                if 'cent' in extracted_info: # if the amount is expressed in cents - amount in euros (or other currencies) is wanted
                    dividends_per_share /= 100 
                print('Actual dividends: ', dividends_per_share, '\n')
            
    return 0



def get_company_name(lt_text):
    pass

def main():
    #with_shares = [4, 12, 15, 18, 22, 27, 36, 42, 48, 51, 55, 62]
    for num in range(1, 302):


        #with open(r'tekstai_classifieriui/27_en.txt', 'r', encoding = 'utf-16') as f: # 4, 12, 15, 18, 22, 27, 36, 42?, 48, 51, 55, 62, 
        with open(r'straipsniai/%s.txt' % num, 'r', encoding = 'utf-16') as f: # 4, 12, 15, 18, 22, 27, 36, 42?, 48, 51, 55, 62
            #en_text = f.read()
            text = f.read()
        lt_text, en_text = text.split('\n#####\n')

        while en_text.find('euros') != -1:
            en_text = en_text.replace('euros', 'EUR')
        while en_text.find('euro') != -1:
            en_text = en_text.replace('euro', 'EUR')
        while en_text.find('litas') != -1:
            en_text = en_text.replace('litas', 'LTL')

        #print(en_text)
        print(num)
        get_dividend_amount_per_share(en_text)

    #df = pd.read_csv('su_dividendais.txt', sep = '\t', encoding = 'utf-16')
    #urls = df['Nuoroda']
    #df['Tekstas'] = []



main()