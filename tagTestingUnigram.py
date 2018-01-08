import nltk;
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sentence = ''.join(open('output.txt').read())
sid = SentimentIntensityAnalyzer()
print(sentence)
ss = sid.polarity_scores(sentence)
for k in sorted(ss):
 print('{0}: {1}, '.format(k, ss[k]), end='')
print()

