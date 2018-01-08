import nltk, random;
from nltk.corpus import nps_chat;
from nltk.corpus import brown;
from nltk import word_tokenize;
from nltk.corpus import movie_reviews as movies

posts = nltk.corpus.nps_chat.xml_posts();
featuresets = [nltk.pos_tag(word_tokenize(post.text)) for post in posts];

print(featuresets)

t0= nltk.DefaultTagger('NN');
t1= nltk.UnigramTagger(featuresets, backoff=t0);
t2= nltk.BigramTagger(featuresets, backoff= t1);

##text = word_tokenize("I am good");
##print(t2.tag(text));
##print(text);


pos_docs = movies.fileids('pos');
neg_docs = movies.fileids('neg');
classifier_training=[];
feature={};

for doc in pos_docs:
    sents = movies.sents(doc);
    for sent in sents:
        tagged = t2.tag(sent);
        words = [w for w,k in tagged];        
        tags = [k for w,k in tagged];
        for i in range(len(words)-1):
            feature[words[i]+ ' ' + words[i+1]] = tags[i]+ ' ' + tags[i+1];
        
        temp = (feature, 'pos');
        classifier_training.append(temp);

print('data acquired !');
##for doc in neg_docs:
##    sents = movies.sents(doc);
##    for sent in sents:
##        temp = (t2.tag(sent), 'neg');
##        classifier_training.append(temp);

##train_set, test_set = classifier_training[20000:], classifier_training[:20000];
##train_set = classifier_training;
##classifier = nltk.NaiveBayesClassifier.train(train_set);
##print(nltk.classify.accuracy(classifier, test_set));

train_set, test_set = classifier_training[100:1000], classifier_training[:100];

print(train_set)
    
    
