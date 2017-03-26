import nltk, random, getpass, os, pickle;
from nltk.corpus import nps_chat;
from nltk.corpus import brown;
from nltk import word_tokenize;
from nltk.corpus import movie_reviews as movies

default_sentence_set = [];
new_sentence_set = [];
Is_Classifier_TrainingRequired = "N";
classifier_training=[]; 

posts = nltk.corpus.nps_chat.xml_posts();
featuresets = [nltk.pos_tag(word_tokenize(post.text)) for post in posts];
t0= nltk.DefaultTagger('NN');
t1= nltk.UnigramTagger(featuresets, backoff=t0);
t2= nltk.BigramTagger(featuresets, backoff= t1);

print('global execution')

##text = word_tokenize("I am good");
##print(t2.tag(text));
##print(text);

def Get_BigramTagging(text):
    tagged_text = t2.tag(text);
    return tagged_text;
    
def Initialize_SentimentAnalyzer(flag=0):
    global Is_Classifier_TrainingRequired;
    if flag == 0:
        Default_Dataset();
        default_dataset = default_sentence_set;
        for i in range(len(default_dataset)):
            label = default_dataset[i][0];
            sent = default_dataset[i][1];
            tagged = t2.tag(sent);
            pairs = [(w,k) for w,k in tagged];        
            feature={};
            for i in range(len(pairs)-1):
                feature[pairs[i][0]+ ' ' + pairs[i+1][0]] = pairs[i][1]+ ' ' + pairs[i+1][1];
            
            temp = (feature, label);
            classifier_training.append(temp);
            
        Is_Classifier_TrainingRequired = "Y";
        
    elif flag == 1:
        usrname = getpass.getuser();
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        filepath = os.path.join(fileDir, '../naivebayes.pickle')
        #filepath = "C:/Users/"+usrname+"/OneDrive/Project/naivebayes.pickle";
        if os.path.exists(filepath):
            classifier_f = open("naivebayes.pickle", "rb");
            classifier = pickle.load(classifier_f);
            classifier_f.close();
            print('Classifier Loading')
            Is_Classifier_TrainingRequired = "N";
        else:
            Initialize_SentimentAnalyzer(0);
            
    elif flag == 2:
        New_Dataset();
        new_dataset = new_sentence_set;
        for i in range(len(new_dataset)):
            label = new_dataset[i][0];
            sent = new_dataset[i][1];
            tagged = t2.tag(sent);
            pairs = [(w,k) for w,k in tagged];        
            feature={};
            for i in range(len(pairs)-1):
                feature[pairs[i][0]+ ' ' + pairs[i+1][0]] = pairs[i][1]+ ' ' + pairs[i+1][1];
            
            temp = (feature, label);
            classifier_training.append(temp);
            
        Is_Classifier_TrainingRequired = "Y";

    print('local execution')
    
    if Is_Classifier_TrainingRequired == "Y":
        random.shuffle(classifier_training);
        classifier = nltk.NaiveBayesClassifier.train(classifier_training);
        save_classifier = open("naivebayes.pickle","wb");
        pickle.dump(classifier, save_classifier);
        save_classifier.close();
    else:
        None;
    print('after class execution')
    return classifier;

def Default_Dataset():
    documents = movies.fileids();
    for doc in documents:
        sents = movies.sents(doc);
        doc_label = doc[:3];
        for sent in sents:
            default_sentence_set.append((doc_label,sent));


def New_Dataset():
    documents = movies.fileids();
    for doc in documents:
        sents = movies.sents(doc);
        doc_label = doc[:3];
        for sent in sents:
            new_sentence_set.append((doc_label,sent));


####testing simple text
##a = Initialize_SentimentAnalyzer(0);
##text = word_tokenize("I am good");
##tgd = Get_BigramTagging(text);
##t=[(w,k) for w,k in tgd];
##f={};
##for i in range(len(t)-1):    
##    f[t[i][0]+ ' ' + t[i+1][0]] = t[i][1]+ ' ' + t[i+1][1];
##
##print(f);
##print('input : ',text,'classification : ',a.classify(f))
##
##b = Initialize_SentimentAnalyzer(1);
##text = word_tokenize("I am not good");
##tgd = Get_BigramTagging(text);
##t=[(w,k) for w,k in tgd];
##f={};
##for i in range(len(t)-1):    
##    f[t[i][0]+ ' ' + t[i+1][0]] = t[i][1]+ ' ' + t[i+1][1];
##
##print(f);
##print('input : ',text,'classification : ',b.classify(f))

    
    
