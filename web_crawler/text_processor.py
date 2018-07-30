import pickle
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
import nltk
from nltk.tree import Tree


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

    #chunked.draw()

def get_dividend_amount_per_share(en_text):
    tokenized = word_tokenize(en_text)
    tagged_text = nltk.pos_tag(tokenized)
    print(tagged_text)

    # change '7 cents per share' to '0.07 euro per share'
    chunk_gram = r"""Cents: {<CD><NN?>}"""  # catches x cent(s)
    chunk_parser = nltk.RegexpParser(chunk_gram)
    chunked = chunk_parser.parse(tagged_text)
    chunked.draw()

    chunk_gram = r"""per share: {<IN><NN>}""" # catches 'per share'
    chunk_parser = nltk.RegexpParser(chunk_gram)
    chunked = chunk_parser.parse(tagged_text)
    chunked.draw()

    # split up in sentences and check which sentence has both cents and per share chunks


def get_company_name(lt_text):
    pass

def main():
    with open(r'tekstai_classifieriui/15_en.txt', 'r', encoding = 'utf-16') as f:
        en_text = f.read()
    #lt_text, en_text = text.split('\n#####\n')

    while en_text.find('EUR') != -1:
        en_text = en_text.replace('EUR', 'euro')
    while en_text.find('LTL') != -1:
        en_text = en_text.replace('LTL', 'litas')

    print(en_text)
    get_dividend_amount_per_share(en_text)


main()