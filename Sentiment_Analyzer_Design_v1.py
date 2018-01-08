import nltk, random;
from nltk.corpus import nps_chat;
from nltk.corpus import brown;
from nltk import word_tokenize;

posts = nltk.corpus.nps_chat.xml_posts();
featuresets = [nltk.pos_tag(word_tokenize(post.text)) for post in posts];
t0= nltk.DefaultTagger('NN');
t1= nltk.UnigramTagger(featuresets, backoff=t0);
t2= nltk.BigramTagger(featuresets, backoff= t1);

##text = word_tokenize("I am good");
##print(t2.tag(text));
##print(text);

from nltk.corpus import movie_reviews as movies
pos_docs = movies.fileids('pos');
neg_docs = movies.fileids('neg');
classifier_training=[];
sentence={};
for doc in pos_docs[:1]:
    sents = movies.sents(doc);
    for sent in sents:
        sentence['sentence']=t2.tag(sent);
##        tagged_sent = t2.tag(sent);
##        sentence['contains({})'.format((word,tag))] \
##        = ((word,tag) for (word,tag) in tagged_sent)
        temp = (sentence, 'pos');
        classifier_training.append(temp);

##for doc in neg_docs:
##    sents = movies.sents(doc);
##    for sent in sents:
##        temp = (t2.tag(sent), 'neg');
##        classifier_training.append(temp);

train_set, test_set = classifier_training[20000:], classifier_training[:20000];
print(train_set[:100])
classifier = nltk.NaiveBayesClassifier.train(train_set);
print(nltk.classify.accuracy(classifier, test_set));

        
    
    
