###!/usr/bin/python3

import httplib2;
import os;
import sys;
from CommentsTest_v10 import ProcessVideoID;
from apiclient.discovery import build;
from apiclient.errors import HttpError;
from oauth2client.tools import argparser;
 
#DEVELOPER_KEY = 'AIzaSyDHHWxvvvt6eojYOW0Y9O8h6JF7ScXRGi0';
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

def bubble(bad_list,key):
    length = len(bad_list) - 1
    sorted = False

    while not sorted:
        sorted = True
        for i in range(length):
            if bad_list[i][key] < bad_list[i+1][key]:
                sorted = False
                bad_list[i], bad_list[i+1] = bad_list[i+1], bad_list[i]

    return bad_list


#################################################################################################################
  
if __name__ == "__main__":
  input_keyword = input('Enter a keyword to seearch videos : ');
  ar = input_keyword;
  #argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--q", help="Search term", default=ar)
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()

  video_Table = {'Video ID' : [],'compound' : [],'neg' : [],'neu' : [],'pos' : []}
  video_Table2 = []
  try:
    video_ids = youtube_search(args);
    for x in video_ids:
        print('The video is :',x)
        video_Score = ProcessVideoID(x)
        
        video_Table['Video ID'].append(x)

        temp = [x]
        
        for x in sorted(video_Score.keys()):
          video_Table[x].append(video_Score[x])
          temp.append(video_Score[x])

        video_Table2.append(temp)
        
  except HttpError as e:
    print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

##  print(video_Table)

  print ("{:<20} {:<20} {:<20} {:<20} {:<20}".format('Video ID','Compound','Positive','Negative','Neutral'))
  for x in zip(video_Table['Video ID'],video_Table['compound'],
                          video_Table['neg'],video_Table['neu'],video_Table['pos']):
    print ("{:<5} {:<5} {:<5} {:<5} {:<5}".format(x[0],x[1],x[2],x[3],x[4]))

  #print(video_Table2)
  print()
  print()
## sorting the table
  bubble(video_Table2,2)

  print ("{:<20} {:<20} {:<20} {:<20} {:<20}".format('Video ID','Compound','Positive','Negative','Neutral'))
  for x in video_Table2:
    print ("{:<5} {:<5} {:<5} {:<5} {:<5}".format(x[0],x[1],x[2],x[3],x[4]))

    
  #print(video_Table2)
  print()
  print()
## sorting the table
  bubble(video_Table2,1)

  print ("{:<20} {:<20} {:<20} {:<20} {:<20}".format('Video ID','Compound','Positive','Negative','Neutral'))
  for x in video_Table2:
    print ("{:<5} {:<5} {:<5} {:<5} {:<5}".format(x[0],x[1],x[2],x[3],x[4]))

