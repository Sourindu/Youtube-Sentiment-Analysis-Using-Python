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

def Get_BigramTagging(text):
    tagged_text = t2.tag(text);
    return tagged_text;
    
def Initialize_SentimentAnalyzer():
    documents = movies.fileids();
    classifier_training=[];

    for doc in documents:
        sents = movies.sents(doc);
        doc_label = doc[:3];
        for sent in sents:
            tagged = t2.tag(sent);
            pairs = [(w,k) for w,k in tagged];        
            feature={};
            for i in range(len(pairs)-1):
                feature[pairs[i][0]+ ' ' + pairs[i+1][0]] = pairs[i][1]+ ' ' + pairs[i+1][1];
            
            temp = (feature, doc_label);
            classifier_training.append(temp);

    random.shuffle(classifier_training);
    train_set = classifier_training;
    classifier = nltk.NaiveBayesClassifier.train(train_set);

    return classifier;

####testing simple text
####a = Initialize_SentimentAnalyzer();
####text = word_tokenize("I am good");
####tgd = Get_BigramTagging(text);
####t=[(w,k) for w,k in tgd];
####f={};
####for i in range(len(t)-1):    
####    f[t[i][0]+ ' ' + t[i+1][0]] = t[i][1]+ ' ' + t[i+1][1];
####
####print(f);
####print('input : ',text,'classification : ',a.classify(f))
####
####text = word_tokenize("I am not good");
####tgd = Get_BigramTagging(text);
####t=[(w,k) for w,k in tgd];
####f={};
####for i in range(len(t)-1):    
####    f[t[i][0]+ ' ' + t[i+1][0]] = t[i][1]+ ' ' + t[i+1][1];
####
####print(f);
####print('input : ',text,'classification : ',a.classify(f))

    
    
