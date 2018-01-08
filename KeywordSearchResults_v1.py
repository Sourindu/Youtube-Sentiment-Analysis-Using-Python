###!/usr/bin/python3

import httplib2;
import os;
import sys;
from CommentsTest_v9 import ProcessVideoID;
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

  try:
    video_ids = youtube_search(args);
    for x in video_ids:
        ProcessVideoID(x)
##    test = video_ids[0];
##    ProcessVideoID(test); 
##    ProcessVideoID('-8N9UR6OTCs'); 
  except HttpError as e:
    print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
