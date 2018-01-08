import bs4, re
from urllib import request
#grab the page source for vide
t = request.urlopen(r'http://www.youtube.com/all_comments?v=i7wveOu5hkQ').read()
#data = urllib.request.urlopen(r'http://www.youtube.com/all_comments?v=wf_IIbT8HGk') #example XhFtHW4YB7M
#pull out comments
soup = bs4.BeautifulSoup(t)
cmnts = soup.findAll(attrs={'class': 'comment yt-tile-default'})
#do something with them, ie count them
print (len(cmnts))
