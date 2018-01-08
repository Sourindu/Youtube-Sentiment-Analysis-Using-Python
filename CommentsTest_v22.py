from apiclient.errors import HttpError;
from apiclient.discovery import build;

import nltk;

from textblob import TextBlob;
from nltk.corpus import opinion_lexicon;
from nltk.tokenize import treebank;

from nltk.sentiment.vader import SentimentIntensityAnalyzer;
sid = SentimentIntensityAnalyzer();

#from Sentiment_Analyzer_Design_v9 import Get_BigramTagging, Initialize_SentimentAnalyzer;
import Sentiment_Analyzer_Design_v9 as custom
from nltk import word_tokenize;
classifier = custom.Initialize_SentimentAnalyzer(1);

import pickle;

YOUTUBE_API_SERVICE_NAME = "youtube";
YOUTUBE_API_VERSION = "v3";
##DEVELOPER_KEY = 'AIzaSyBS5zcC0yuhCfVP5mihP-Io5PfGOgNExo4';
DEVELOPER_KEY = 'AIzaSyDz8_XTYvc-7e_VwkJEZqfHbQQEv5WYCOU';

def get_comment_threads(youtube, video_id, comments):
    threads = [];
    results = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    textFormat="plainText"
    ).execute();
    #Get the first set of comments
    for item in results["items"]:
        threads.append(item)
        comment = item["snippet"]["topLevelComment"]
        text = comment["snippet"]["textDisplay"]
        comments.append(text)    
    
    #Keep getting comments from the following pages
    while ("nextPageToken" in results):
        results = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        pageToken=results["nextPageToken"],
        textFormat="plainText"
        ).execute()
        if len(threads) > 10:
            break;        
        for item in results["items"]:
            threads.append(item)
            comment = item["snippet"]["topLevelComment"]
            text = comment["snippet"]["textDisplay"]
            comments.append(text)

    return threads;

###################################################################################

def check_lexicon(sentence):
    """
    Basic example of sentiment classification using Liu and Hu opinion lexicon.
    This function simply counts the number of positive, negative and neutral words
    in the sentence and classifies it depending on which polarity is more represented.
    Words that do not appear in the lexicon are considered as neutral.

    :param sentence: a sentence whose polarity has to be classified.
    :param plot: if True, plot a visual representation of the sentence polarity.
    """
    tokenizer = treebank.TreebankWordTokenizer()
    pos_words = 0
    neg_words = 0
    tokenized_sent = [word.lower() for word in tokenizer.tokenize(sentence)]

    x = list(range(len(tokenized_sent))) # x axis for the plot
    y = []

    for word in tokenized_sent:
        if word in opinion_lexicon.positive():
            pos_words += 1
            y.append(1) # positive
        elif word in opinion_lexicon.negative():
            neg_words += 1
            y.append(-1) # negative
        else:
            y.append(0) # neutral

    if pos_words > neg_words:
        return 'Positive'
    elif pos_words < neg_words:
        return 'Negative'
    elif pos_words == neg_words:
        return 'Neutral'

    if plot == True:
        _show_plot(x, y, x_labels=tokenized_sent, y_labels=['Negative', 'Neutral', 'Positive'])

###################################################################################
##if __name__ == "__main__":
def ProcessVideoID(video_id):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
  
  try:
    comments = [];
    Total_textblob_polarity = 0;
    classifier_score = 0;
    com_Lex_Score = 0
    video_comment_threads = get_comment_threads(youtube, video_id, comments);
    comlen = len(comments);
    
    print("Total Threads: %d" % len(video_comment_threads));
##  video_comment_threads = get_comment_threads(youtube, '-8N9UR6OTCs', comments);
    
    total_video_score = {'compound':0.0,'neg':0.0,'neu':0.0,'pos':0.0,'textblob_polarity':0.0,'lexicon_score':0.0,'classifier_score':0.0};
    
    
    
    for thread in video_comment_threads:
        try:
            comment = thread["snippet"]["topLevelComment"];
            text = comment["snippet"]["textDisplay"];
##          print(text);
########################################### textblob ######################################################
            
            textblob_polarity = ((TextBlob(text)).sentiment).polarity;
            #print(textblob_polarity);
            if(textblob_polarity < 0):
                if(textblob_polarity == -1):
                    textblob_polarity = -1*(abs(textblob_polarity+0.1)**2)/comlen
                else:
                    textblob_polarity = -1*(abs(textblob_polarity)**2)/comlen
            else:
                if(textblob_polarity == 1):
                    textblob_polarity = ((textblob_polarity-0.1)**2)/comlen
                else:
                    textblob_polarity = (textblob_polarity**2)/comlen
                    
            Total_textblob_polarity = Total_textblob_polarity + textblob_polarity;


########################################### nltk lexicon ###################################################
            lexicon_result = check_lexicon(text)
            if lexicon_result == 'Positive':
                com_Lex_Score = com_Lex_Score+(1/len(text))
            elif lexicon_result == 'Negative':
                com_Lex_Score = com_Lex_Score-(1/len(text))
            else:
                None
            #print(com_Lex_Score);


########################################### vader #########################################################
            
            ss = sid.polarity_scores(str(text));
##          print(ss);
            for k in sorted(ss):

                if(ss[k] == 1):
                    ss[k] = 0;                

                if(ss[k] < 0):
                    total_video_score[k] = total_video_score[k]-(ss[k]**2)/comlen
                else:
                    total_video_score[k] = total_video_score[k]+(ss[k]**2)/comlen
                    
########################################### custom classifer #########################################################

            tokenized_comment = word_tokenize(text);
            tgd = custom.Get_BigramTagging(tokenized_comment);
            t=[(w,k) for w,k in tgd];
            
            f={};
            for i in range(len(t)-1):    
                f[t[i][0]+ ' ' + t[i+1][0]] = t[i][1]+ ' ' + t[i+1][1];    
            classifier_result = classifier.classify(f);
            if classifier_result =='pos':
                classifier_score = classifier_score + 1;
            else:
                classifier_score = classifier_score - 1;
                
            
        except UnicodeEncodeError as e2:
            None;

    #print ("Total comments: %d" % comlen);
    #print('The total video score is : ',end='');
##    for k in sorted(total_video_score):
##        if(total_video_score[k] < 0):
##            total_video_score[k] = -1*(abs(total_video_score[k])**(1/2));
##        else:
##            total_video_score[k] = (abs(total_video_score[k])**(1/2));
##        print('{0}: {1}, '.format(k, total_video_score[k]), end='')

    total_video_score['textblob_polarity']=Total_textblob_polarity;

    if(com_Lex_Score < 0):
        total_video_score['lexicon_score'] = -1*(abs(com_Lex_Score)**2)/comlen
    else:
        total_video_score['lexicon_score'] = (com_Lex_Score)**2/comlen



        

                total_video_score['classifier_score']=classifier_score;





    total_video_score['lexicon_score']= com_Lex_Score;   

    for k in ['compound','neg','neu','pos','textblob_polarity']:
        if(total_video_score[k] < 0):
            total_video_score[k] = -1*(abs(total_video_score[k])**(1/2));
        else:
            total_video_score[k] = (abs(total_video_score[k])**(1/2));
        print('{0}: {1}, '.format(k, total_video_score[k]), end='')
        
    print('{0}: {1}, '.format('lexicon_score', total_video_score['lexicon_score']), end='')   
    print()
    return total_video_score

##  print(total_video_score);

  except HttpError as e:
    print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content));

##ProcessVideoID('cYVL3LkPBXA');
