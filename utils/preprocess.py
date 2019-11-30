# encoding: utf-8

from string import ascii_letters, digits, whitespace
from ua_stopwords import *

def word_count(text):
  text = text.encode('utf-8')
  return len(str(text).split(' '))

def avg_word(text):
  text = text.encode('utf-8')
  words = text.split()
  return (sum(len(word) for word in words)/len(words))

# Clean data:
# - convert to unicode
# - leave only letters and numbers
# - lowercase
# - TODO: Lemmatization
# - remove stopwords
# - replace multiple spaces with one
def clean_text(text):
  ua_alphabet = u"абвгґдеєжзиіїйклмнопрстуфхцчшщьюяАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'"
  allowed_chars = ua_alphabet + whitespace + ascii_letters + digits

  text = unicode(text)
  text = "".join([c for c in text if c in allowed_chars])
  text = text.lower()
  # TODO: lemmatize
  text = text.split()
  text = [word for word in text if not word in ua_stopwords]
  text = " ".join(text)

  return text
