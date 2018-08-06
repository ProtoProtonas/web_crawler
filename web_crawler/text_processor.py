import pickle
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
import nltk
from nltk.tree import Tree
import pandas as pd
import datetime

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

# T/F whether a string is an integer or not
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return s == int(s)
    except (TypeError, ValueError):
        pass
 
    return False

# T/F whether a string is a floating point number or not
def is_float(s):
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

# T/F whether string contains floating point numbers or not
def has_floats(s):
    digs = s.split(' ')
    digs = [is_float(x) for x in digs]
    if True in digs:
        return True
    return False

# T/F whether string contains integers or not
def has_ints(s):
    digs = s.split(' ')
    digs = [is_int(x) for x in digs]
    if True in digs:
        return True
    return False

def get_countries(en_text):
    tokenized = word_tokenize(en_text)
    tagged_text = nltk.pos_tag(tokenized)

    namedEnt = nltk.ne_chunk(tagged_text, binary = False)
    namedEnt.draw()
    print(tagged_text)


def find_year_in_sentence(sent):
    if 'this year' in sent.lower():
            return -1
    if 'last year' in sent.lower():
            return -2

    sent_tokenized = word_tokenize(sent)
    tagged = nltk.pos_tag(sent_tokenized)
    this_year = datetime.datetime.today().year
    year_range = range(1990, this_year + 1)

    # look for the date of Annual General Meeting
    agm_date = ''
    if 'general meeting' in sent.lower() or 'shareholder' in sent.lower():
        chunk_gram_agm = r"""AGM: {(<IN>?<CD>+<IN>?<NNP><CD>)|(<NNP><CD><,>?<CD>)}"""
        chunk_parser = nltk.RegexpParser(chunk_gram_agm)
        chunked = chunk_parser.parse(tagged)
        for subtree in chunked.subtrees(filter = lambda t: t.label() == 'AGM'):
            extracted_info = ''
            for word, _ in subtree.leaves():
                extracted_info += word + ' '
            nums = []
            [nums.append(int(s)) for s in extracted_info.split(' ') if is_int(s)] # collect all the numbers from extracted_info string
            if any(num in year_range for num in nums) and not any(s in extracted_info.lower() for s in ['of', 'for', 'in']):
                #print('AGM: ' + extracted_info)
                agm_date = extracted_info
                agm_date = agm_date.split(' ')
                for s in agm_date:
                    if is_int(s):
                        if int(s) in year_range:
                            return int(s) - 1

    # find actual date

    chunk_gram = r"""Year: {<IN>(<DT>?<JJ.?>?<NN.?>)?<CD>+}"""  # 'for/in/of (the year) 2017
    chunk_parser = nltk.RegexpParser(chunk_gram)
    chunked = chunk_parser.parse(tagged)

    for subtree in chunked.subtrees(filter = lambda t: t.label() == 'Year'):
        extracted_info = ''
        for word, _ in subtree.leaves():
            extracted_info += word.replace('.', '') + ' '

        nums = []
        [nums.append(int(s)) for s in extracted_info.split(' ') if is_int(s)] # collect all the numbers from extracted_info string
        if any(num in year_range for num in nums):
            #print('_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_- Actual date: ' + extracted_info)
            for s in extracted_info.split(' '):
                if is_int(s):
                    if int(s) in year_range:
                        return int(s)

    # if no date was found:
    
    if 'last year' in sent.lower():
        if 'profit' not in sent.lower():
            return -2
    if 'this year' in sent.lower():
        if 'profit' not in sent.lower():
            return -1

    return -1



def get_dividends(en_text):

    sents = en_text

    while '\n' in sents:
        sents = sents.replace('\n', '. ') # some articles are not in a great format so that should be fixed up (or it may have some irrelevant data in some of its lines)
    while '..' in sents:
        sents = sents.replace('..', '.')  # for every case where sentence and line end in the same place

    tokenized = sent_tokenize(sents) # split up the article into sentences
    sentences_with_dividend = []
    for sent in tokenized:
        if 'dividend' in sent and (has_ints(sent) or has_floats(sent)): # since we are looking for dividend amount which is a number
            sentences_with_dividend.append(sent)
        
    for x, _ in enumerate(sentences_with_dividend):  # just some tidying up (and capitalize money codes as it is easier for the part of speech tagger to recognize them correctly)
        while sentences_with_dividend[x].find('*') != -1:
            sentences_with_dividend[x] = sentences_with_dividend[x].replace('*', '')
        while sentences_with_dividend[x].find('eur') != -1:
            sentences_with_dividend[x] = sentences_with_dividend[x].replace('eur', 'EUR')
        while sentences_with_dividend[x].find('litas') != -1:
            sentences_with_dividend[x] = sentences_with_dividend[x].replace('litas', 'LTL')
        while sentences_with_dividend[x].find('ltl') != -1:
            sentences_with_dividend[x] = sentences_with_dividend[x].replace('ltl', 'LTL')
        while sentences_with_dividend[x].find('sek') != -1:
            sentences_with_dividend[x] = sentences_with_dividend[x].replace('sek', 'SEK')
    
    years = [] # int array
    dividends_total = [] # float array
    dividends_per_share = [] # float array
    currencies = [] # string array
    #the_dictionary = {'Year': years, 'Dividends total': dividends_total, 'Dividends per share': dividends_per_share, 'Currency': currencies} # all of the above combined into one neat and tidy array

    for sent in sentences_with_dividend:
        print(sent)
        sent_tokenized = word_tokenize(sent)
        tagged = nltk.pos_tag(sent_tokenized)
        print(tagged)

        if ('thousand', 'NN') in tagged:
            i = tagged.index(('thousand', 'NN'))
            tagged.insert(i, ('thousand', 'CD'))

        # pre-initialize so there are no missing values in the_dictionary
        div_per_share = 0
        div_total = 0
        year = 0
        currency = 0

        # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<
        # find dividends per share
        # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<

        chunk_gram = r"""Per share: {<NN.?>?<CD>+<NN.?>*(<IN><NN.?>)?((<IN><NN>)|(<DT><NN>))?}"""  # basically the main brains of this function (actually a template of how a sentence should look). Testing proved this to be good enough template
        chunk_parser = nltk.RegexpParser(chunk_gram)
        chunked = chunk_parser.parse(tagged) # find relevant chunks that fit the 'main brains' template

        for subtree in chunked.subtrees(filter = lambda t: t.label() == 'Per share'):
            extracted_info = ''
            for word, _ in subtree.leaves():
                extracted_info += word.replace(',', '.') + ' '



            if ('a share' in extracted_info or 'per share' in extracted_info) and has_floats(extracted_info):  # look for '0.07 EUR per share' or something with similar criteria

                nums = []
                [nums.append(float(s)) for s in extracted_info.split(' ') if is_float(s)] # collect all the numbers from extracted_info string
                div_per_share = nums[0] # we assume the first number is the only number in the chunk

                if 'cent' in extracted_info.lower(): # if the amount is expressed in cents - amount in euros (or other currencies) is wanted
                    div_per_share /= 100 

                dividends_per_share.append(div_per_share)
                print('Dividens per share: ', div_per_share)
                break

            
        # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<
        # find dividends per share
        # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<

        #chunk_gram = r"""Total: {<VB.?>(<DT><RB>?)?<NN.?>?<IN>?<RP>?<CD>+<NNP>?<NN.?>?}"""  # basically the main brains of this function (actually a template of how a sentence should look). Testing proved this to be good enough template
        chunk_gram = r"""Total: {<V.*>+(<N.*>?<DT><N.*><IN>?)?<R.?>?(<N.*><IN>?)?<NNP>?<CD>+<NNP>?}"""
        chunk_parser = nltk.RegexpParser(chunk_gram)
        chunked = chunk_parser.parse(tagged) # find relevant chunks of text that fit the chunk_gram template

        for subtree in chunked.subtrees(filter = lambda t: t.label() == 'Total'):
            extracted_info = ''
            for word, _ in subtree.leaves():
                extracted_info += word.replace(',', '.') + ' '
            print('Dividends total: ', extracted_info, '\n\n\n\n')



        # if year not found:
        # -1 for this year, -2 for last year and so on
        # afterwards in main_analyze article date will be looked up and 'this year' as well as 'last year' will be deduced

    #print('Dictionary: ', the_dictionary)
    print('\n')
    return 0 #the_dictionary

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
        
    for x, _ in enumerate(sentences_with_share):  # just some tidying up (and capitalize money codes as it is easier for the part of speech tagger to recognize them correctly)
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
    
    years = [] # int array
    dividends = [] # float array
    currencies = [] # string array
    the_dictionary = {'Year': years, 'Dividend per share': dividends, 'Currency': currencies} # all of the above combined into one neat and tidy array

    for sent in sentences_with_share:
        print(sent)
        sent_tokenized = word_tokenize(sent)
        tagged = nltk.pos_tag(sent_tokenized)
        #print(tagged)

        chunk_gram = r"""Per share: {<NN.?>?<CD>+<NN.?>*(<IN><NN.?>)?((<IN><NN>)|(<DT><NN>))?}"""  # basically the main brains of this function (actually a template of how a sentence should look). Testing proved this to be good enough template
        chunk_parser = nltk.RegexpParser(chunk_gram)
        chunked = chunk_parser.parse(tagged) # find relevant chunks that fit the 'main brains' template

        for subtree in chunked.subtrees(filter = lambda t: t.label() == 'Per share'):
            extracted_info = ''
            for word, _ in subtree.leaves():
                extracted_info += word.replace(',', '.') + ' '



            if 'share' in extracted_info and has_floats(extracted_info):  # look for '0.07 EUR per share' or something with similar criteria

                nums = []
                [nums.append(float(s)) for s in extracted_info.split(' ') if is_float(s)] # collect all the numbers from extracted_info string
                dividends_per_share = nums[0] # we assume the first number is the only number in the chunk

                if 'cent' in extracted_info.lower(): # if the amount is expressed in cents - amount in euros (or other currencies) is wanted
                    dividends_per_share /= 100 

                dividends.append(dividends_per_share)
                break
                

        # find year
        year = find_year_in_sentence(sent)

        if len(dividends_per_share) > len(currencies):
            if 'eur' in sent.lower():
                currencies.append('EUR')
            elif 'ltl' in sent.lower():
                 currencies.append('LTL')
            elif 'sek' in sent.lower():
                currencies.append('SEK')


        if len(dividends_per_share) > len(years):
            years.append(year)

    print('Dictionary: ', the_dictionary)
    return the_dictionary



def get_company_name(lt_text):
    pass

def main():
    #with_shares = [4, 12, 15, 18, 22, 27, 36, 42, 48, 51, 55, 62]
    for num in range(1, 302):


        #with open(r'tekstai_classifieriui/27_en.txt', 'r', encoding = 'utf-16') as f: # 4, 12, 15, 18, 22, 27, 36, 42?, 48, 51, 55, 62, 
        with open(r'straipsniai/%s.txt' % num, 'r', encoding = 'utf-16') as f:
            text = f.read()
        lt_text, en_text = text.split('\n#####\n')

        while en_text.find('euros') != -1:
            en_text = en_text.replace('euros', 'EUR')
        while en_text.find('euro') != -1:
            en_text = en_text.replace('euro', 'EUR')
        while en_text.find('litas') != -1:
            en_text = en_text.replace('litas', 'LTL')

        #print(en_text)
        print('\n\n\n', num)
        get_dividends(en_text)

    #df = pd.read_csv('su_dividendais.txt', sep = '\t', encoding = 'utf-16')
    #urls = df['Nuoroda']
    #df['Tekstas'] = []



main()