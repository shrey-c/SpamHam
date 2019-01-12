# -*- coding: utf-8 -*-
from collections import Counter
import re
word_regex = re.compile("[a-zA-Z']+(?:-[a-zA-Z']+)?")
def getWords(text):
    return list(word_regex.findall(text.lower()))

def getWordFreq(wordList):
    return(Counter(wordList))


def getWordsSansStopWords(text,stopWords):
    words=list(word_regex.findall(text.lower()))
    newWord=[]
    for word in words:
        if(word not in stopWords):
            newWord.append(word);
    return(newWord)
    
def readStopWords(path):
    with open(path, encoding='utf-8',errors="ignore") as stopFile:
        stopWords=getWords(stopFile.read())
        return(stopWords)