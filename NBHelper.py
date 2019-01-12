# -*- coding: utf-8 -*-

import os
import re
import string

# Regex defining what to consider as a word
word_regex = re.compile("[a-zA-Z']+(?:-[a-zA-Z']+)?")
def getWords(text):
    return list(word_regex.findall(text.lower()))     
            

def getWordsSansStopWords(text,stopWords):
    words=list(word_regex.findall(text.lower()))
    newWordList=[]
    for word in words:
        if(word not in stopWords) :
            newWordList.append(word)
    return(newWordList)
    
    
def getMailDictionary(path):
    messages={}
    files = list(os.walk(path))[0][2]
    
    for file in files:
        filePath=path+"/"+file       
        with open(filePath, encoding='utf-8',errors="ignore") as mailFile:
            messages[file]=getWords(mailFile.read())
    return(messages)
    
def getMailDictionaryWOStopWords(path,stopWords):
    messages={}
    files = list(os.walk(path))[0][2]
    
    for file in files:
        filePath=path+"/"+file       
        with open(filePath, encoding='utf-8',errors="ignore") as mailFile:
            messages[file]=getWordsSansStopWords(mailFile.read(),stopWords)
    return(messages)
    
def readStopWords(path):
    with open(path, encoding='utf-8',errors="ignore") as stopFile:
        stopWords=getWords(stopFile.read())
       # print(len(stopWords))
        return(stopWords)

def getVocabulary(mailDict):
    vocab=[]
    for key,value in mailDict.items():
        for i in value:
            vocab.append(i)
    return(vocab)
