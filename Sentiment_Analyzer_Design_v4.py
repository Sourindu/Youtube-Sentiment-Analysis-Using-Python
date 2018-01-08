import nltk, random;
from nltk.corpus import nps_chat;
from nltk.corpus import brown;
from nltk import word_tokenize;
from nltk.corpus import movie_reviews as movies

posts = nltk.corpus.nps_chat.xml_posts();
featuresets = [nltk.pos_tag(word_tokenize(post.text)) for post in posts];
t0= nltk.DefaultTagger('NN');
t1= nltk.UnigramTagger(featuresets, backoff=t0);
t2= nltk.BigramTagger(featuresets, backoff= t1);

##text = word_tokenize("I am good");
##print(t2.tag(text));
##print(text);

pos_docs = movies.fileids('pos');
neg_docs = movies.fileids('neg');
classifier_training=[];

for doc in pos_docs:
    sents = movies.sents(doc);
    for sent in sents:
        tagged = t2.tag(sent);
        words = [w for w,k in tagged];        
        tags = [k for w,k in tagged];
        feature={};
        for i in range(len(words)-1):
            feature[words[i]+ ' ' + words[i+1]] = tags[i]+ ' ' + tags[i+1];
        
        temp = (feature, 'pos');
        classifier_training.append(temp);

##print('pos data acquired !');

for doc in neg_docs:
    sents = movies.sents(doc);
    for sent in sents:
        tagged = t2.tag(sent);
        words = [w for w,k in tagged];        
        tags = [k for w,k in tagged];
        feature={};
        for i in range(len(words)-1):
            feature[words[i]+ ' ' + words[i+1]] = tags[i]+ ' ' + tags[i+1];
        
        temp = (feature, 'neg');
        classifier_training.append(temp);

##print(' neg data acquired !');

random.shuffle(classifier_training);

##print(' random data acquired !');

train_set = classifier_training;
classifier = nltk.NaiveBayesClassifier.train(train_set);

##testing simple text
a=Initialize_SentmentAnalyzer();
text = word_tokenize("I am good");
tgd = t2.tag(text);
t=[w for w,k in tgd];
v=[k for w,k in tgd];
arr=[];
f={};
for i in range(len(t)-1):    
    f[t[i]+ ' ' + t[i+1]] = v[i]+ ' ' + v[i+1];

print('input : ',text,'classification : ',a.classify(f))

text = word_tokenize("I am not good");
tgd = t2.tag(text);
t=[w for w,k in tgd];
v=[k for w,k in tgd];
arr=[];
f={};
for i in range(len(t)-1):    
    f[t[i]+ ' ' + t[i+1]] = v[i]+ ' ' + v[i+1];

print('input : ',text,'classification : ',a.classify(f))

##train_set, test_set = classifier_training[20000:], classifier_training[:20000];
##train_set = classifier_training;
##classifier = nltk.NaiveBayesClassifier.train(train_set);
##print(nltk.classify.accuracy(classifier, test_set));

##train_set, test_set = classifier_training[100:1000], classifier_training[:100];
    
    
