import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from math import log, sqrt
import pandas as pd
import numpy as np
import re
import pickle
from sklearn.externals import joblib
#print (1000)
#classifier = joblib.load('model.pkl')
#print(1)
#predict = classifier.predict(msg_test)
#print (2)
#print (predict)
from trained_model2 import classified, SpamClassifier
a = classified("Free free free new sale buy 1 get 1 free")
print(a)
