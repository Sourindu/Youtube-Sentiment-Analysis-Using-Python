import nltk
from nltk.corpus import brown as b
import re

tag_prefix = 'MD'
tagged_text = nltk.corpus.brown.tagged_words(categories='news',tagset='universal')


data = nltk.ConditionalFreqDist((word.lower(),tag) for (word, tag) in tagged_text)

for word in sorted(data.conditions()):
     if len(data[word]) > 3:
         tags = [tag for (tag, _) in data[word].most_common()]
         print(word, ' '.join(tags))
         
tagged_text = nltk.corpus.brown.tagged_sents(categories='news')

print(tagged_text[:2])




