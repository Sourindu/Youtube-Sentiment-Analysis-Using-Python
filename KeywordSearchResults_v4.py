###!/usr/bin/python3

import httplib2;
import os;
import sys;
from CommentsTest_v10 import ProcessVideoID;
from apiclient.discovery import build;
from apiclient.errors import HttpError;
from oauth2client.tools import argparser;
 
DEVELOPER_KEY = 'AIzaSyDz8_XTYvc-7e_VwkJEZqfHbQQEv5WYCOU';
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

#################################################################################################################
  
if __name__ == "__main__":
  input_keyword = input('Enter a keyword to seearch videos : ');
  ar = input_keyword;
  #argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--q", help="Search term", default=ar)
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()

  video_Table = {'Video ID' : [],'compound' : [],'neg' : [],'neu' : [],'pos' : []}

  try:
    video_ids = youtube_search(args);
    for x in video_ids:
        print('The video is :',x)
        video_Score = ProcessVideoID(x)
        
        video_Table['Video ID'].append(x)
        
        for x in video_Score.keys():
          video_Table[x].append(video_Score[x])
  except HttpError as e:
    print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

  print "{:<8} {:<15} {:<10}".format('Key','Label','Number')
  for k, v in d.iteritems():
    label, num = v
    print "{:<8} {:<15} {:<10}".format(k, label, num)
