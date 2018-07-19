import nltk
from nltk.tokenize import word_tokenize, PunktSentenceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
#from nltk.corpus import movie_reviews as mr
import random


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


def lemmatize(text):

    lemmatizer = WordNetLemmatizer()

    tokenized = word_tokenize(text)

    tagged = nltk.pos_tag(tokenized)

    for x, tuple in enumerate(tagged):
        word = tuple[0]
        part_of_speech = tuple[1]

        # atskiras atvejis, kazkodel neatpazista, kad thousand yra skaicius (million atpazista be problemu)
        if word == 'thousand':
            part_of_speech = 'CD'

        tokenized[x] = lemmatizer.lemmatize(word, get_wordnet_pos(part_of_speech))

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

def main():
    with open(r'tekstai/10_en.txt', 'r', encoding = 'utf-16') as f:
        text = f.read()
    print(lemmatize(text))

def synonyms(word):

    synonyms = []

    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())


    #w1 = wordnet.synset('%s.n.01' % 'watch')
    #w2 = wordnet.synset('boat.n.01')

    #print(w1.wup_similarity(w2))
    return set(synonyms)
    
def movie_reviews():
    
    mr._LazyCorpusLoader__load()

    documents = []

    for category in mr.categories():
        for fileid in mr.fileids(category):
            documents.append((list(mr.words(fileid)), category))
        print(len(documents))

    #documents = [(list(mr.words(fileid)), category) for category in mr.categories for fileid in mr.fileids(category)]

    random.shuffle(documents)

    print(documents[1], '\n\n\n\n', documents[5])

    all_words = []
    for w in mr.words():
        all_words.append(w.lower())

    all_words = nltk.FreqDist(all_words)
    print(all_words.most_common(35))
    print(all_words["nice"])


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
        #if features[w] == 1:
        #    print(w)

    return features


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

def main(x):
    high = 0
    low = 100
    avg_accuracy = 0
    for _ in range(x):
        accuracy = train_classfier(get_featuresets())
        avg_accuracy += accuracy
        if accuracy > high:
            high = accuracy
        elif accuracy < low:
            low = accuracy

    print(avg_accuracy / x)
    print('Low: ', low)
    print('High: ', high)


main(50)
