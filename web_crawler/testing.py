import nltk
from nltk.tokenize import word_tokenize, PunktSentenceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
from nltk.corpus import movie_reviews as mr
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


def test_tokenizer():
    with open(r'tekstai/4_en.txt', 'r', encoding = 'utf-16') as f:
        sample_text = f.read()

    with open(r'tekstai/25_en.txt', 'r', encoding = 'utf-16') as f:
        train_text = f.read()


    custom_sent_tokenizer = PunktSentenceTokenizer(train_text)

    tokenized = custom_sent_tokenizer.tokenize(sample_text)

    try:
        for i in tokenized[5:]:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            namedEnt = nltk.ne_chunk(tagged, binary = True)
            namedEnt.draw()
    except Exception as e:
        print(str(e))

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
    print(mr, '\n\n\n\n\n\n\n\n\n')
    
    #mr.category

    documents = [(list(mr.words(fileid)), category) for category in mr.categories for fileid in mr.fileids(category)]

    random.shuffle(documents)

    print(documents[1])

    all_words = []
    for w in mr.words():
        all_words.append(w.lower())

    all_words = nltk.FreqDist(all_words)
    print(all_words.most_common(15))
    print(all_words["stupid"])





movie_reviews()
    
#main()
#synonyms('word')