
# coding: utf-8

# In[ ]:


# Remove warnings on Windows
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

# imports
# import word2vec
# imports needed and logging
import gzip
import gensim
import numpy
import pandas
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.INFO)


# In[ ]:


# Read input texts to train model

# English texts
#input_file = 'data/article_results.txt'

# Ukranian texts
input_file = 'puppeteer-scraper/texts.txt'


# In[ ]:


def read_input(input_file):
    """This method reads the input file which is in txt format"""

    logging.info("Start reading file {0}... this may take a while".format(input_file))
    with open(input_file, encoding="utf8") as f:
        for i, line in enumerate(f):
            yield format_line(line)
        logging.info("Done reading input file, bro. TOTAL LINES: {0}".format(i))

def format_line(line):
    # Convert a document into a list of lowercase tokens,
    # ignoring tokens that are too short or too long.
    return gensim.utils.simple_preprocess(line)

# read the tokenized reviews into a list
# each review item becomes a serries of words
# so this becomes a list of lists
documents = list(read_input(input_file))
logging.info("Read file complete and formatted list saved, bro!")


# model.train PARAMS:
# 
# size
# The size of the dense vector to represent each token or word. If you have very limited data, then size should be a much smaller value. If you have lots of data, its good to experiment with various sizes. A value of 100-150 has worked well for me.
# 
# window
# The maximum distance between the target word and its neighboring word. If your neighbor's position is greater than the maximum window width to the left and the right, then, some neighbors are not considered as being related to the target word. In theory, a smaller window should give you terms that are more related. If you have lots of data, then the window size should not matter too much, as long as its a decent sized window.
# 
# min_count
# Minimium frequency count of words. The model would ignore words that do not statisfy the min_count. Extremely infrequent words are usually unimportant, so its best to get rid of those. Unless your dataset is really tiny, this does not really affect the model.
# 
# workers
# How many threads to use behind the scenes?

# In[ ]:


# create a vocabulary
model = gensim.models.Word2Vec(documents, size=150, window=10, min_count=2, workers=10)
# start training a simple neural network with a single hidden layer
model.train(documents,total_examples=len(documents),epochs=10)


# In[ ]:


model.wv['trump']


# In[ ]:


######## Save the model
# model.save('articles.model')

######## Load with:
# model = gensim.models.word2vec.Word2Vec.load('articles.model')

# now we can look for similar words:
w1 = "осел"

try:
    model.wv.most_similar(positive=w1)
except Exception as e:
    logging.error("OOOOOPS brother, {0}".format(e))


# In[ ]:


# similarity between two words
# works by computing cosine similarity between two words
print(model.wv.similarity(w1="осел",w2="телевізор"))

