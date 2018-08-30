import pickle
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
import nltk
from nltk.tree import Tree
import pandas as pd
import datetime
import pycountry

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

# returns all the countries it can find from a given text (in English)
def get_countries(en_text):
    countries = pycountry.countries
    country_names = []
    for country in countries:
        try:
            country_names.append([country.name, country.official_name])
        except:
            country_names.append([country.name])

    countries = []
    for names in country_names:
        if any(name.lower() in en_text.lower() for name in names):
            countries.append(names[0])

    string_of_countries = ' '
    for country in countries:
        string_of_countries += country + ', '

    if string_of_countries.endswith(', '):
        string_of_countries = string_of_countries[:-2]

    return string_of_countries

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

# does the actual chunking and all other heavy lifting of the text analysis
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
        
    
    years = [] # int array
    dividends_total = [] # float array
    dividends_per_share = [] # float array
    currencies = [] # string array
    countries = [] # string array
    the_dictionary = {'Periodas': years, 'Dividendai viso': dividends_total, 'Dividendai/akcija': dividends_per_share, 'Valiuta': currencies, 'Šalis': countries} # all of the above combined into one neat and tidy array

    for sent in sentences_with_dividend:
        # initialize some variables so that we can later use these initial values to detect wheter anything noteworthy was found or not
        div_per_share = 0
        div_total = 0
        year = 0
        currency = 'EUR' # euro is assumed as it is the most popular currency in lithuanian media

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

        currency_list = []
        for currency in pycountry.currencies:
            currency_list.append([currency.alpha_3, currency.name, currency.name.split(' ')[0]])
            
        for curr in currency_list:
            if any(c.lower() in sent.lower() for c in curr):
                currency = curr[0]


        if 'eur' in sent.lower():
            currency = 'EUR'
        elif 'ltl' in sent.lower():
            currency = 'LTL'
        elif 'dollar' in sent.lower():
            currency = 'USD'

        if currency == 'XXX' or len(str(currency)) != 3:
            currency = 'EUR'

        # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<
        # find country
        # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<
        
        if not(div_total == 0 and div_per_share == 0): # if the program failed to find any dividends there is no point in just adding year and (maybe) currency to the results
            dividends_total.append(div_total)
            dividends_per_share.append(div_per_share)
            years.append(year)
            currencies.append(currency)

    # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<
    # find country
    # ^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<^>v<

    countries = [get_countries(en_text)] * len(years)

    the_dictionary = {'Periodas': years, 'Dividendai viso': dividends_total, 'Dividendai/akcija': dividends_per_share, 'Valiuta': currencies, 'Šalis': countries}
    # if year not found:
    # -1 for this year, -2 for last year and so on
    # afterwards in main_analyze article date will be looked up and 'this year' as well as 'last year' will be deduced

    return the_dictionary

# compares two numbers if they are equal within the margin of error (defined inside the function)
def are_nums_equal(a, b):
    # a -> big integer
    # b -> string of a fractional number
    # assume a > 10**9 and 1 < b < 10

    original_a = a
    margin_of_error = 0.02
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

# finds every word that is in quotes (we assume that to be a possible candidate for the name of the company)
def get_company_name_quotes(sent):
    text = sent
    text = text.replace('„', '"')
    text = text.replace('“', '"')
    text = text.replace('”', '"')

    names = []
    while text.rfind('"') != -1:
        end = text.rfind('"')
        start = text[:end - 1].rfind('"')

        if start == -1 or end == -1:
            break

        if end - start < 35 and end > start and end - start > 2:
            name = text[start+1:end]
            names.append(name)
        text = text[:start]

    return names

# finds every company name from list_of_companies.txt that is present in a sentence
def get_company_name_list(sent):
    with open('list_of_companies.txt', 'r', encoding = 'utf-16') as f:
        companies = f.read()
        companies = companies.split('\n')

    bad_names = ['', ' ', '\n', '\t', '  ']
    for comp in companies:
        if any(name == comp for name in bad_names):
            companies.remove(comp)

    names = []
    for company in companies:
        if company.lower() in sent.lower():
            count = sent.count(company)

            for _ in range(count):
                names.append(company)

    return names

# finds sentences that have the already extracted numbers and looks for a name only in those sentences. main use is for one sentence headlines that somehow managed to get into the main text
def get_company_name_nums(sent, dict_data):
    new_dict = dict_data

    dividends = list(dict_data['Dividendai viso'] + dict_data['Dividendai/akcija'])
    for div in dividends:
        if div == 0:
            dividends.remove(div)

    nums = []
    for s in sent.split():
        try:
            if s.isdigit():
                nums.append(float(s))
        except:
            pass

    for num in nums:
        for div in dividends:
            names = []
            if are_nums_equal(div, num):
                try:
                    names.append(get_company_name_ab(sent))
                except:
                    pass

                try:
                    quoted_companies = get_company_name_quotes(sent)
                    for comp in quoted_companies:
                        names.append(comp)
                except:
                    pass

                try:
                    listed_companies = get_company_name_list(sent)
                    for comp in listed_companies:
                        names.append(comp)
                except:
                    pass

                try:
                    with open('blacklisted_companies.txt', 'r', encoding = 'utf-16') as f:
                        blacklisted = f.read()
                        blacklisted = blacklisted.split('\n')

                    for comp in blacklisted:
                        while comp in names:
                            names.remove(comp)
                except:
                    pass

                try:
                    names.remove(None)
                except:
                    pass

                for n, dividend in enumerate(new_dict['Dividendai viso']):
                    if div == dividend:
                        try:
                            new_dict['Kompanija'][n] = names[0]
                        except Exception as e:
                            print('get_company_name_nums() exception 1: ', e)

                for n, dividend in enumerate(new_dict['Dividendai/akcija']):
                    if div == dividend:
                        try:
                            new_dict['Kompanija'][n] = names[0]
                        except Exception as e:
                            print('get_company_name_nums() exception 2: ', e)

    return new_dict

# finds AB (akcinė bendrovė in Lithuanian, public limited liability company in English) in a sentence and extracts the name that goes with it
def get_company_name_ab(sent):
    if 'AB ' in sent:
        sent = sent.replace('„', '"')
        sent = sent.replace('“', '"')

        end = sent.rfind('"')
        start = sent[:end].rfind('"')
        while sent.find('"') != -1 and (end != -1 and start != -1):
            sent = sent[:start] + sent[start+1:end].upper() + sent[end:]
            end = sent.rfind('"')
            start = sent[:end].rfind('"')


        sent = sent.replace(',', '')
        sent = sent.replace('``', '')
        sent = sent.replace("''", '')
        sent = sent.replace('"', '')
        words = word_tokenize(sent)

        name = ''
        for x, word in enumerate(words):
            a = 1
            if 'AB' in word:
                try:
                    while words[x + a][0].isupper():
                        name += words[x + a] + ' '
                        a += 1
                except Exception as e:
                    print('get_company_name_ab exception 1: ', e)

                if name == '':
                    names = []
                    a = -1
                    try:
                        while words[x + a][0].isupper():
                            names.append(words[x + a])
                            a -= 1
                    except Exception as e:
                        print('get_company_name_ab exception 2: ', e)

                    for x in range(len(names), 0):
                        name += names[x] + ' '
        try:
            name = name[0].upper() + name[1:].lower()
        except Exception as e:
            print('get_company_name_ab exception 3: ', e)

        return name
    return None

# function that encapsules all the name finding functions
def get_company_name(title, lt_text, dict_data):
    sents = sent_tokenize(title + '\n.' + lt_text)
    names = []
    new_dict = dict_data
    new_dict['Kompanija'] = [''] * len(dict_data['Periodas'])

    names = []
    for n, sent in enumerate(sents):
        new_dict = get_company_name_nums(sent, new_dict)
        name = get_company_name_ab(sent)
        if name != None and name != '':
            names.append(name)

        quoted_names = get_company_name_quotes(sent)
        for name in quoted_names:
            names.append(name)

        listed_names = get_company_name_list(sent)
        for name in listed_names:
            names.append(name)

    try:
        with open('blacklisted_companies.txt', 'r', encoding = 'utf-16') as f:
            blacklisted = f.read()
            blacklisted = blacklisted.split('\n')

        for comp in blacklisted:
            while comp in names:
                names.remove(comp)
    except:
        pass

    title_names = []
    try:
        for name in get_company_name_list(title):
            title_names.append(name)
        for name in get_company_name_quotes(title):
            title_names.append(name)
        for name in get_company_name_ab(title):
            title_names.append(name)
    except:
        pass

    title_name = ''

    try:
        title_name, _ = nltk.FreqDist(title_names).most_common(1)[0]
    except Exception as e:
        print(e)

    if title_name != '':
        weight = 0.3
        weighted_num = int(len(names) * weight)
        for _ in range(weighted_num):
            names.append(title_name)

    most_popular_name = ''
    
    try:
        most_popular_name = max(set(names), key = names.count)
        
        while most_popular_name[0] == ' ':
            most_popular_name = most_popular_name[1:]
        while most_popular_name[-1] == ' ':
            most_popular_name = most_popular_name[:-1]

    except Exception as e:
        print('get_company_name() exception:', e)

    for x, _ in enumerate(new_dict['Kompanija']):
        if new_dict['Kompanija'][x] == '':
            new_dict['Kompanija'][x] = most_popular_name

    return new_dict