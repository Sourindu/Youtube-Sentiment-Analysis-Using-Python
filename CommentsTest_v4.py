from apiclient.errors import HttpError
from apiclient.discovery import build

import nltk;
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
DEVELOPER_KEY = 'AIzaSyDz8_XTYvc-7e_VwkJEZqfHbQQEv5WYCOU'

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
        for item in results["items"]:
              threads.append(item)
              comment = item["snippet"]["topLevelComment"]
              text = comment["snippet"]["textDisplay"]
              comments.append(text)
        if len(threads) > 100:
            break;

    return threads[:100];

###################################################################################

##if __name__ == "__main__":
def ProcessVideoID(video_id):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
  
  try:
    comments = [];
    video_comment_threads = get_comment_threads(youtube, video_id, comments);
    print("Total Threads: %d" % len(video_comment_threads));
##    video_comment_threads = get_comment_threads(youtube, '-8N9UR6OTCs', comments);
    total_video_score = {'compound':0.0,'neg':0.0,'neu':0.0,'pos':0.0};
    for thread in video_comment_threads:
        try:
            comment = thread["snippet"]["topLevelComment"];
            text = comment["snippet"]["textDisplay"];
            #print(text);
            #print();
            ss = sid.polarity_scores(str(text));
            for k in sorted(ss):

                if(ss[k] < 0):
                    total_video_score[k] = total_video_score[k]-(ss[k]**10)
                elif(ss[k] < 1):
                    total_video_score[k] = total_video_score[k]+(ss[k]**10)
                else:
                    ss[k] = 0
                
                #print('{0}: {1}, '.format(k, ss[k]), end='')

##            print()
##            print()
##            print(text)
        except UnicodeEncodeError as e2:
            None;

    print ("Total comments: %d" % len(comments));
    print('The total video score is : ',end='');
    for k in sorted(total_video_score):
        total_video_score[k] = (total_video_score[k]**(0.1))/len(comments);
        print('{0}: {1}, '.format(k, total_video_score[k]), end='')
    print()

  except HttpError as e:
    print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content));
