class YoutubeSentiment:
    from apiclient.errors import HttpError
    from apiclient.discovery import build
    from nltk.sentiment.vader import SentimentIntensityAnalyzer


    def __init__(self, SearchWord):
        self.Keyword = SearchWord

    
