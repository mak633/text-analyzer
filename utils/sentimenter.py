from sklearn.externals import joblib

tfidfVectorizer = joblib.load('models/tfidfVectorizer.pkl')
classifier = joblib.load('models/classifier.pkl')

def get_sentiment(text):
  corpus = [text]
  x_tfid = tfidfVectorizer.transform(corpus).toarray()
  sentiment = classifier.predict(x_tfid)
  return str(sentiment[0])
