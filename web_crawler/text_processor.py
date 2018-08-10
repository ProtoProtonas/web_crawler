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

# gets featureset of a text
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

# finds year mentions in a sentence
def find_year_in_sentence(sent):

    sent_tokenized = word_tokenize(sent) # split sentences into words
    tagged = nltk.pos_tag(sent_tokenized) # tag each word with part of speech
    this_year = datetime.datetime.today().year
    year_range = range(1990, this_year + 1) # look for one year period only between 1990 and the current year, as in Lithuania there were no (or very little, can neither confirm nor deny) privately owned companies under the soviet occupation. And dividends will not be paid in advance (most likely) so there is no point in looking for them in a year that has not even started

    # look for the date of Annual General Meeting and then subtract one to get the year we are looking for
    agm_date = ''
    if 'general meeting' in sent.lower() or 'shareholder' in sent.lower():
        chunk_gram_agm = r"""AGM: {(<IN>?<CD>+<IN>?<NNP><CD>)|(<NNP><CD><,>?<CD>)}""" # template of what a description of a AGM should look like
        chunk_parser = nltk.RegexpParser(chunk_gram_agm)
        chunked = chunk_parser.parse(tagged)
        for subtree in chunked.subtrees(filter = lambda t: t.label() == 'AGM'): # subtree -> one chunk of words that matches the template above
            extracted_info = ''
            for word, _ in subtree.leaves():
                extracted_info += word + ' ' # put the words back to a text with some meaning
            nums = []
            [nums.append(int(s)) for s in extracted_info.split(' ') if is_int(s)] # collect all the numbers from extracted_info string
            if any(num in year_range for num in nums) and not any(s in extracted_info.lower() for s in ['of', 'for', 'in']): # of, for, in -> bad words that do not mean the date of the AGM
                agm_date = extracted_info
                agm_date = agm_date.split(' ')
                for s in agm_date:
                    if is_int(s):
                        if int(s) in year_range:
                            return int(s) - 1 # if any of the numbers is within the year range that we are interested in we return that

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
            for s in extracted_info.split(' '):
                if is_int(s):
                    if int(s) in year_range:
                        return int(s)

    # if no date was found:
    
    if 'last year' in sent.lower(): # last year for an article written in 2016 will be 2015 so later we will look up the date of the article but for now this should do the job
        if 'profit' not in sent.lower():
            return -2
    if 'this year' in sent.lower():
        if 'profit' not in sent.lower():
            return -1 

    return -1 # if nothing works it is assumed that article talks about last year period

# extracts total dividend amounts from pre-processed chunk of text
def get_total_dividends(chunk):
    nums = []
    [nums.append(float(s)) for s in chunk.split(' ') if (is_float(s) or is_int(s))] # collect all the numbers from extracted_info string

    div_total = 0 # in case the function fails to find anything

    if len(nums) > 0:
        div_total = nums[0]
        if 'million' in chunk:
            div_total *= 1000000
        elif 'thousand' in chunk:
            div_total *= 1000
        elif 'billion' in chunk:
            div_total *= 1000000000

        if div_total > 5000 and not any(s in chunk for s in ['propose', 'suggest']): # as many articles as I have seen none of the dividends were smaller than 10k euros, so we are not interested in any amount smaller than 5k
            pass 
        else:
            div_total = 0

    return div_total

# extracts dividend per share amounts from pre-processed chunk of text
def get_dividends_per_share(chunk):
    nums = []
    [nums.append(float(s)) for s in chunk.split(' ') if is_float(s)] # collect all the numbers from extracted_info string
    div_per_share = nums[0] # we assume the first number is the only number in the chunk

    if 'cent' in chunk.lower(): # if the amount is expressed in cents - amount in euros (or other currencies) is wanted
        div_per_share /= 100 

    return div_per_share

# does the actual chunking and all other heavy lifting of the text  analysis
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
    the_dictionary = {'Periodas': years, 'Dividendai viso': dividends_total, 'Dividendai/akcija': dividends_per_share, 'Valiuta': currencies} # all of the above combined into one neat and tidy array

    for sent in sentences_with_dividend:
        # initialize some variables so that we can later use these initial values to detect wheter anything noteworthy was found or not
        div_per_share = 0
        div_total = 0
        year = 0
        currency = 'EUR' # euro is assumed as it is the most popular currency in lithuanian media

        #print(sent)
        sent_tokenized = word_tokenize(sent)
        tagged = nltk.pos_tag(sent_tokenized)

        if ('thousand', 'NN') in tagged: # for no apparent reason whatsoever thhe word 'thousand' is not recognized as a cardinal digit, so this is where we fix it manually
            i = tagged.index(('thousand', 'NN'))
            tagged.insert(i, ('thousand', 'CD'))

        # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<
        # find dividends per share
        # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<

        chunk_gram = r"""Per share: {<NN.?>?<CD>+<NN.?>*(<IN><NN.?>)?((<IN><CD>?<NN>)|(<DT><NN>))?}"""  # basically the main brains of this function (actually a template of how a sentence should look). Testing proved this to be good enough template
        chunk_parser = nltk.RegexpParser(chunk_gram)
        chunked = chunk_parser.parse(tagged) # find relevant chunks that fit the 'main brains' template

        for subtree in chunked.subtrees(filter = lambda t: t.label() == 'Per share'):
            extracted_info = ''
            for word, _ in subtree.leaves():
                extracted_info += word.replace(',', '.') + ' '



            if ('a share' in extracted_info or 'per share' in extracted_info) and (has_floats(extracted_info) or has_ints(extracted_info)):  # look for '0.07 EUR per share' or something with similar criteria
                div_per_share = get_dividends_per_share(extracted_info)
            
        # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<
        # find total dividends
        # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<
        chunk_gram = r"""Total: {<V.*>+(<N.*>?<DT><N.*><IN>?)?<R.?>?(<N.*><IN>?)?<NNP>?<CD>+<NNP>?}"""
        chunk_parser = nltk.RegexpParser(chunk_gram)
        chunked = chunk_parser.parse(tagged) # find relevant chunks of text that fit the chunk_gram template

        for subtree in chunked.subtrees(filter = lambda t: t.label() == 'Total'):
            extracted_info = ''
            for word, _ in subtree.leaves():
                extracted_info += word.replace(',', '.') + ' '

            div_total = get_total_dividends(extracted_info)

        # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<
        # find year
        # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<

        year = find_year_in_sentence(sent)

        # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<
        # find currency
        # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<
        if 'eur' in sent.lower():
            currency = 'EUR'
        elif 'ltl' in sent.lower():
            currency = 'LTL'
        elif 'sek' in sent.lower():
            currency = 'SEK'
        # ^ this is rather dodgy solution but works surprisingly well


        if not(div_total == 0 and div_per_share == 0): # if the program failed to find any dividends there is no point in just adding year and (maybe) currency to the results
            dividends_total.append(div_total)
            dividends_per_share.append(div_per_share)
            years.append(year)
            currencies.append(currency)

    the_dictionary = {'Periodas': years, 'Dividendai viso': dividends_total, 'Dividendai/akcija': dividends_per_share, 'Valiuta': currencies}
    # if year not found:
    # -1 for this year, -2 for last year and so on
    # afterwards in main_analyze article date will be looked up and 'this year' as well as 'last year' will be deduced

    #print('Dictionary: ', the_dictionary)
    #print('\n\n\n')
    return the_dictionary

def are_nums_equal(a, b):
    # a -> big integer
    # b -> string of a fractional number
    # assume a > 10**9 and 1 < b < 10

    original_a = a
    margin_of_error = 0.05
    try:
        b = b.replace(',', '.')
    except:
        pass
    
    if float(b) == 0:
        return False

    for _ in range(4):
        frac = a/float(b)
        if frac < 1 + margin_of_error and frac > 1 - margin_of_error:
            return True
        a = a / 1000

    for _ in range(2):
        frac = original_a / float(b)
        if frac < 1 + margin_of_error and frac > 1 - margin_of_error:
            return True
        original_a = original_a * 100

    return False
        



def get_company_name_quotes(sent):
    text = sent
    text = text.replace('„', '"')
    text = text.replace('“', '"')

    names = []
    while text.rfind('"') != -1:
        end = text.rfind('"')
        start = text[:end - 1].rfind('"')

        if end - start < 35 and end > start:
            name = text[start+1:end]
            print('Pavadinimas: ', name)
            names.append(name)
        text = text[:start]

    return names

    #print(end - start)

def get_company_name_nums(sent, dict_data):
    dividends = list(dict_data['Dividendai viso'] + dict_data['Dividendai/akcija'])
    for div in dividends:
        if div == 0:
            dividends.remove(div)
    #print('Nums: ', dividends)

    nums = []
    for s in sent.split():
        try:
            if s.isdigit():
                nums.append(float(s))
        except:
            pass

    #[nums.append(float(s)) for s in sent.split() if s.isdigit()]
    #print(nums)

    for num in nums:
        if any(are_nums_equal(div, num) for div in dividends):
            # sent with the supposed company is right here
            print(sent)

    # isrinkti zodzius tarp kabuciu
    # palyginti skaicius is dividendu ir is sakinio. jei sutampa - paimti zodi is kabuciu arba nuo AB


def get_company_name_uab(sent):
    if 'AB ' in sent:
        return sent
    return ''

def get_company_name(lt_text, dict_data):
    sents = sent_tokenize(lt_text)
    for n, sent in enumerate(sents):
        get_company_name_nums(sent, dict_data)

    #get_company_name_quotes(lt_text)
    #get_company_name_nums(lt_text, dict_data)
    #if dict_data['Periodas'] != []:
    #    print(dict_data)
    #    sents = sent_tokenize(lt_text)
    #    for sent in sents:
    #        print(get_company_name_uab(sent))




def main():

    #print(are_nums_equal(7700000, '7,713'))

    #x = 25
    for num in range(1, 286):
    #for num in range(x, x + 10):
        
        with open(r'straipsniai/%s.txt' % num, 'r', encoding = 'utf-16') as f:
            text = f.read()
        lt_text, en_text, _, _, _ = text.split('\n#####\n')

        while en_text.find('euros') != -1:
            en_text = en_text.replace('euros', 'EUR')
        while en_text.find('euro') != -1:
            en_text = en_text.replace('euro', 'EUR')
        while en_text.find('litas') != -1:
            en_text = en_text.replace('litas', 'LTL')

        while lt_text.find('\n') != -1:
            lt_text = lt_text.replace('\n', '. ')
        while lt_text.find('..') != -1:
            lt_text = lt_text.replace('..', '.')
        while lt_text.find('  ') != -1:
            lt_text = lt_text.replace('  ', ' ')

        lt_text = lt_text.replace('tūkst.', 'tūkst')
        lt_text = lt_text.replace('mln.', 'mln')
        lt_text = lt_text.replace('mlrd.', 'mlrd')

        print('\n\n', num)
        dict_data = get_dividends(en_text)
        print(dict_data)
        get_company_name(lt_text, dict_data)


main()