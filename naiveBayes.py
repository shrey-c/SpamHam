# -*- coding: utf-8 -*-
from collections import Counter
from NBHelper import *
import math as m
import sys
class NBClassifier:
    numOfClasses=0
    classMapping={}
    dictOfVocabs={}
    dictPriorProb={}
    arrayDictCondProb={}
    totVocabList=[]
    vocabSet=set()

    ###################################
    #========Constructor===============
    ####################################

    def __init__(self,numOfClasses,classNames):
        self.numOfClasses=numOfClasses
        for i in range(0,self.numOfClasses):
            self.classMapping[i]=classNames[i];
            self.arrayDictCondProb[classNames[i]]={}

    #################################
    #updates the Vocabulary Dictionary of the instance.
    #Also updates the Prior Probability dictionary of the instance
    #input:=Path where mails are stored
    #################################

    def buildVocab(self,pathArray):
        numOfMails={}
        totMails=0
        for key,value in self.classMapping.items():
            setOfMails=getMailDictionary(pathArray[key]);
            numOfMails[value]=len(setOfMails)
            totMails+=len(setOfMails)
            self.dictOfVocabs[value]=getVocabulary(setOfMails);
        for key,value in numOfMails.items():
            self.dictPriorProb[key]=numOfMails[key]/totMails

    ###############################
    #Removes the stopwords from the vocabulary and updates
    # the instance vocab dictionary with that. Also updates the
    # prior prob dictionary of the instance
    #input:=Path where the mail files are stored
    ###############################

    def buildVocabWOStopWords(self,pathArray,stopWordPath):
        numOfMails={}
        totMails=0
        stopWords=readStopWords(stopWordPath);
        for key,value in self.classMapping.items():
            setOfMails=getMailDictionaryWOStopWords(pathArray[key],stopWords);
            numOfMails[value]=len(setOfMails)
            totMails+=len(setOfMails)
            self.dictOfVocabs[value]=getVocabulary(setOfMails);
        for key,value in numOfMails.items():
            self.dictPriorProb[key]=numOfMails[key]/totMails


    ##############################
    # Removes the duplicates from the vocabulary
    #############################
    def buildVocabSet(self):
        totVocabList=[]
        for value in self.dictOfVocabs.values():
            totVocabList.extend(value)
        self.vocabSet=set(totVocabList);

    ############################
    #Gets the Post conditional probabilities with LaPlace Smoothening
    ############################
    def train(self):
        for value in self.classMapping.values():
            wordFreqDict=Counter(self.dictOfVocabs[value]);
           # print("for",value,len(wordFreqDict))
            for term in self.vocabSet:
                if term in wordFreqDict.keys():
                    termCount=wordFreqDict[term];
                    self.arrayDictCondProb[value][term]=(1+termCount)/(len(self.vocabSet)+len(self.dictOfVocabs[value]))
                else:
                    self.arrayDictCondProb[value][term]=(1)/(len(self.vocabSet)+len(self.dictOfVocabs[value]));

    ##########################
    # Depending on which post probability is more, returns the
    # class for the input mail(list of words in that mail)
    #input:=words contained in the test mail
    #output:=Class of the mail Spam or Ham
    ##########################
    def getClassification(self,listOfWords):
        posteriorProb={}
        for val in self.classMapping.values():
            posteriorProb[val]=m.log(self.dictPriorProb[val]);
        for term in listOfWords:
            for val in self.classMapping.values():
                if term in self.arrayDictCondProb[val]:
                    posteriorProb[val]+=m.log(self.arrayDictCondProb[val][term])
        v=list(posteriorProb.values())
        k=list(posteriorProb.keys())
        return k[v.index(max(v))]


    ##############################
    #Gets the accuracy for test mails
    #Input:=Path for test mails
    #############################
    def validate(self,testPaths):
        spamTestMails=getMailDictionary(testPaths[0]);
        hamTestMails=getMailDictionary(testPaths[1]);
        spamcorrect=0;
        hamcorrect=0;
        for key,value in spamTestMails.items():
            if(self.getClassification(value)==("spam")):
                spamcorrect=spamcorrect+1
        for key,value in hamTestMails.items():
            if(self.getClassification(value)==("ham")):
                hamcorrect=hamcorrect+1;
        spamaccuracy=(spamcorrect/(len(spamTestMails)))*100;
        hamaccuracy=(hamcorrect/(len(hamTestMails)))*100;
        accuracy=((spamcorrect+hamcorrect)/(len(spamTestMails)+len(hamTestMails)))*100
        #print(spamaccuracy)
        #print(hamaccuracy)
        print("Accuracy without removing stopwords",accuracy)

    ####################################
    #Same function as above but also removes
    #stopwords from the test mails.
    ###################################3
    def validateWOStopWords(self,testPaths,stopPath):
        stopWords=readStopWords(stopPath);
        spamTestMails=getMailDictionaryWOStopWords(testPaths[0],stopWords);
        hamTestMails=getMailDictionaryWOStopWords(testPaths[1],stopWords);
        spamcorrect=0;
        hamcorrect=0;
        for key,value in spamTestMails.items():
            if(self.getClassification(value)==("spam")):
                spamcorrect=spamcorrect+1
        for key,value in hamTestMails.items():
            if(self.getClassification(value)==("ham")):
                hamcorrect=hamcorrect+1;
        spamaccuracy=(spamcorrect/(len(spamTestMails)))*100;
        hamaccuracy=(hamcorrect/(len(hamTestMails)))*100;
        accuracy=((spamcorrect+hamcorrect)/(len(spamTestMails)+len(hamTestMails)))*100
        #print(spamaccuracy)
        #print(hamaccuracy)
        print("Accuracy after removing stopwords",accuracy)

def main():
    NB=NBClassifier(2,["spam","ham"]);
    argvList=sys.argv
    trainPaths=[]
    testPaths=[]
    trainPaths.append(argvList[1]);
    trainPaths.append(argvList[2]);
    testPaths.append(argvList[3]);
    testPaths.append(argvList[4]);
    NB.buildVocab(trainPaths);
    NB.buildVocabSet();
    NB.train();
    NB.validate(testPaths)

    NB1=NBClassifier(2,["spam","ham"]);
    NB1.buildVocabWOStopWords(trainPaths,argvList[5]);
    NB1.buildVocabSet();
    NB1.train();
    NB1.validateWOStopWords(testPaths,argvList[5])


main()
