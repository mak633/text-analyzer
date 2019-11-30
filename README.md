## Prerequisites
1. Python3
2. gcc
3. Jupyter Notebook for convenient development in Python
4. Python libraries:
    4.1 numpy
    4.2 Word2vec (win support is experimental. Further read: https://github.com/danielfrg/word2vec)
    4.3 pandas

#### In Terminal:
```
pip install -U gensim
```
##### OR:
```
pip install word2vec
```

#### in Python:
```
from gensim.models import word2vec
```
##### OR:
```
import word2vec
```
Done!

# **Run Flask server with Angular app**

### install npm deps, build angular app
```
cd client/
npm i
ng build -c prouction
```

### go back and run flask server
```
cd ..
cd server/
export FLASK_APP=server.py
flask run
```
