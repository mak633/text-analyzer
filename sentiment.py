# -*- coding: utf-8 -*-

from polyglot.text import Text
from polyglot.downloader import downloader
import polyglot.detect.base
from polyglot.detect import Detector

import numpy as np
import pandas as pd
import re

#downloader.download("sentiment2.en")
#downloader.download("sentiment2.uk")
#downloader.download("embeddings2.uk")
#downloader.download("ner2.uk")

#print("{:<16}{}".format("Word", "Polarity") + "\n" + "-" * 30)
#for w in text.words:
#  print(w.polarity)

# lines_with_polarity = []
# with open('puppeteer-scraper/texts.txt') as f:
#   lines = f.readlines()
#   for line in lines:
#     print(line)
#     error = ''

#     try:
#       detector = Detector(unicode(line, "utf-8"))
#       if (detector.language.code == 'uk'):
#         text = Text(line)
#         polarity = 0
#         for w in text.words:
#           polarity = polarity + w.polarity
        
#         if (polarity != 0):
#           pol = '1' if polarity > 0 else '-1'
#           line = line.rstrip()
#           lines_with_polarity.append(line.__add__('|').__add__(str(pol)).__add__("\n"))
#     except:
#       error = 'Some error'
    
    

# print('WRITING to file')
# with open('data/sentiment_data.txt', 'w') as f:
#   f.writelines(lines_with_polarity)

df = pd.read_csv('data/sentiment_data.txt', delimiter = '|', engine='python', quoting = 3)
# TODO: clear lines

corpus = []
for sent in df['Sentence']:
  sent = sent.replace('.', '').replace(',', '').replace('?', '').replace(';', '').replace('-', '').replace(')', '').replace('(', '')
  corpus.append(sent)

# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

tfidfVectorizer = TfidfVectorizer(max_features =2000)
X = tfidfVectorizer.fit_transform(corpus).toarray()
y = df.iloc[:, 1].values

from sklearn.model_selection import train_test_split
X_train, X_test , y_train, y_test = train_test_split(X, y , test_size = 0.20)

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# save models
from sklearn.externals import joblib
joblib.dump(tfidfVectorizer, 'server/tfidfVectorizer.pkl')
joblib.dump(classifier, 'server/classifier.pkl')

predictions = classifier.predict(X_test)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, predictions)

print(cm)