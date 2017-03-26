###!/usr/bin/python3

import httplib2;
import os;
import sys;
from CommentsTest_v24 import ProcessVideoID;
from apiclient.discovery import build;
from apiclient.errors import HttpError;
from oauth2client.tools import argparser;
from openUrl import openURL;
 
##DEVELOPER_KEY = 'AIzaSyDHHWxvvvt6eojYOW0Y9O8h6JF7ScXRGi0';
DEVELOPER_KEY = 'AIzaSyDz8_XTYvc-7e_VwkJEZqfHbQQEv5WYCOU'
YOUTUBE_API_SERVICE_NAME = "youtube";
YOUTUBE_API_VERSION = "v3";

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute();

  videos = [];
  video_ids = [];
  
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"]));
      video_ids.append(search_result["id"]["videoId"]);
      
  return video_ids;

def bubble(bad_list,keyin):
  bad_list = sorted(bad_list,key=lambda x:x[keyin],reverse=True)
  return bad_list
           
#################################################################################################################
  
if __name__ == "__main__":
  input_keyword = input('Enter a keyword to seearch videos : ');
  ar = input_keyword;
  #argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--q", help="Search term", default=ar)
  argparser.add_argument("--max-results", help="Max results", default=10)
  args = argparser.parse_args()

  trial_if_error = 0
  
  video_Table = {'Video ID' : [],'classifier_score': [],'compound' : [],'neg' : [],'neu' : [],'pos' : [],'textblob_polarity': [],'lexicon_score': []}
  video_Table2 = []
  while(trial_if_error < 3):
    try:
      video_ids = youtube_search(args);
      for x in video_ids:
          print()
          print('The video is :',x)
          video_Score = ProcessVideoID(x)
          
          video_Table['Video ID'].append(x)

          temp = [x]
          
          for y in sorted(video_Score.keys()):
            video_Table[y].append(video_Score[y])
            temp.append(video_Score[y])

          video_Table2.append(temp)
          
      break
          
    except HttpError as e:
      print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
      trial_if_error = trial_if_error +1

##  print(video_Table)
  print()
  print()
  heading_print = "{:<10} {:<20} {:<22} {:<15} {:<26} {:<20} {:<20} {:<20}";
  
  value_print = "{:<10} {:<20} {:<22} {:<20} {:<24} {:<20} {:<20} {:<20}";
  #value_print = '{:20.5f} {:20.5f} {:20.5f} {:20.5f} {:20.5f} {:20.5f} {:20.5f} {:20.5f}'
  
  print (heading_print.format('Video ID','Compound','Positive','Negative','Neutral','textblob_polarity','lexicon_score','classifier_score'));
  
  for x in zip(video_Table['Video ID'],video_Table['compound'],video_Table['neg'],video_Table['neu'],video_Table['pos']
               ,video_Table['textblob_polarity'],video_Table['lexicon_score'],video_Table['classifier_score']):
    print (value_print.format(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]))

  #print(video_Table2)
  print()
  print()
## sorting the table on the basis of Compound
  video_Table2 = bubble(video_Table2,2)

  print (heading_print.format('Video ID','classifier_score','Compound','lexicon_score','Positive','Negative','Neutral','textblob_polarity'));
  for x in video_Table2:
    print (value_print.format(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]))

  openURL(video_Table2[0][0])
    
  #print(video_Table2)
  print()
  print()
## sorting the table on the basis of lexicon_score
  video_Table2 = bubble(video_Table2,4)

  print (heading_print.format('Video ID','classifier_score','Compound','lexicon_score','Positive','Negative','Neutral','textblob_polarity'));
  for x in video_Table2:
    print (value_print.format(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]))

  print()
  print()
## sorting the table on the basis of negativity
  video_Table2 = bubble(video_Table2,6)

  print (heading_print.format('Video ID','classifier_score','Compound','lexicon_score','Positive','Negative','Neutral','textblob_polarity'));
  for x in video_Table2:
    print (value_print.format(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]))

  

