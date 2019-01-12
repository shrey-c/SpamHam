# -*- coding: utf-8 -*-
import LRHelper as helper
import Mail as m
import os
import math
import sys
class LR:
    totTrainingSetInfo={}
    totTestSetInfo={}
    vocabSet=set()
    learningConstant=0
    weightVector={}
    def __init__(self,learningConst,penalty):
        self.totTrainingSetInfo={}
        self.totTestSetInfo={}
        self.weightVector={}
        self.vocabSet=set()
        self.learningConstant=float(learningConst)
        self.penalty=float(penalty)
        
        
    def retrieveVocabSet(self):
        for mailFileKey,mailFileValue in self.totTrainingSetInfo.items():
            for word in mailFileValue.thisMailWords:
                self.vocabSet.add(word)
                
                
    def setInitialWeights(self):
        for word in self.vocabSet:
            self.weightVector[word]=0.0
            
    def runGradientAscent(self,iterationThreshold):
        i=0;
        weight=0
        iter=0
        for iter in range(0,int(iterationThreshold)):
            print("iter",iter)
            for weightWord in self.weightVector:
                sum=0.0
                weight=weight+1
                #print("weight",weight)
                yl=0
                for mail in self.totTrainingSetInfo.values():
                    i=i+1
                    #print(i)
                    if(mail.thisMailTrueClass==1):
                        yl=1
                    if weightWord in mail.thisMailWords:
                        sum+=mail.thisMailWordFreqDict[weightWord]*(yl-self.condProb(1,mail))
                self.weightVector[weightWord]+= ((self.learningConstant*sum)) - ((self.learningConstant)*(self.penalty)*self.weightVector[weightWord])
                        
            
            
    def condProb(self,classNum,mail):
        sum=0.0;
        retValue=0.0
       
        for key,value in mail.thisMailWordFreqDict.items():
            if key not in self.weightVector:
                self.weightVector[key]=0.0
            sum+=self.weightVector[key]*value
            
        if(classNum==1): 
            retValue=(math.exp(sum)/(1+math.exp(sum)))
        elif(classNum==0):
            retValue=(1/(1+math.exp(sum)))        
        return(retValue)
        
        
    def getClass(self,mail):
        score={}
        score[0]=self.condProb(0,mail)
        score[1]=self.condProb(1,mail)
        if(score[0]>score[1]):
            return(0)
        else:
            return(1)
            
    def buildTestInfo(self,directoryPath,givenClass):
        listOfWords=[]
        wordFreqDict={}
        files = list(os.walk(directoryPath))[0][2]
        for file in files:
            filePath=directoryPath+"/"+file
            with open(filePath, encoding='utf-8',errors="ignore") as mailFile:
                listOfWords=helper.getWords(mailFile.read())
                wordFreqDict=helper.getWordFreq(listOfWords)
                self.totTestSetInfo[file]=m.Mail(listOfWords,wordFreqDict,givenClass)
                
                
    def buildTestInfoWOStopWords(self,directoryPath,givenClass,stopPath):
        listOfWords=[]
        wordFreqDict={}
        listOfWords=[]
        wordFreqDict={}
        #print(stopPath)
        stopWords=helper.readStopWords(stopPath)
        files = list(os.walk(directoryPath))[0][2]
        for file in files:
            filePath=directoryPath+"/"+file
            with open(filePath, encoding='utf-8',errors="ignore") as mailFile:
                listOfWords=helper.getWordsSansStopWords(mailFile.read(),stopWords)
                wordFreqDict=helper.getWordFreq(listOfWords)
                self.totTestSetInfo[file]=m.Mail(listOfWords,wordFreqDict,givenClass)
    
    
    def applyLR(self):
        correct=0
        spam=0
        ham=0
        for mailValue in self.totTestSetInfo.values():
            classVal=self.getClass(mailValue)
            if(classVal==mailValue.thisMailTrueClass):
                correct+=1
                if(classVal==1):
                    ham+=1
                else:
                    spam+=1
        accuracy=((correct)/len(self.totTestSetInfo))*100
        #print(spam)
        #print(ham)
        print(accuracy) 

               
    def buildTrainingInfo(self,directoryPath,givenClass):
        listOfWords=[]
        wordFreqDict={}
        files = list(os.walk(directoryPath))[0][2]
        for file in files:
            filePath=directoryPath+"/"+file
            with open(filePath, encoding='utf-8',errors="ignore") as mailFile:
                listOfWords=helper.getWords(mailFile.read())
                wordFreqDict=helper.getWordFreq(listOfWords)
                self.totTrainingSetInfo[file]=m.Mail(listOfWords,wordFreqDict,givenClass)
    
    
    def buildTrainingInfoWOStopWords(self,directoryPath,givenClass,stopPath):
        listOfWords=[]
        wordFreqDict={}
        #print(stopPath)
        stopWords=helper.readStopWords(stopPath)
        files = list(os.walk(directoryPath))[0][2]
        for file in files:
            filePath=directoryPath+"/"+file
            with open(filePath, encoding='utf-8',errors="ignore") as mailFile:
                listOfWords=helper.getWordsSansStopWords(mailFile.read(),stopWords)
                wordFreqDict=helper.getWordFreq(listOfWords)
                self.totTrainingSetInfo[file]=m.Mail(listOfWords,wordFreqDict,givenClass)


def main():
        print(sys.argv)
        LRHandle=LR(sys.argv[5],sys.argv[6])
        spamTrainingPath=sys.argv[1];
        hamTrainingPath=sys.argv[2]        
        spamTestPath=sys.argv[3]
        hamTestPath=sys.argv[4]
        LRHandle.buildTrainingInfo(spamTrainingPath,0)
        LRHandle.buildTrainingInfo(hamTrainingPath,1);
        LRHandle.buildTestInfo(spamTestPath,0)
        LRHandle.buildTestInfo(hamTestPath,1);
        LRHandle.retrieveVocabSet()
        LRHandle.setInitialWeights()
        LRHandle.runGradientAscent(sys.argv[7])
        print("Accuracy without removing stopwords")
        LRHandle.applyLR()
       
        
        #Running same code but without considering stopwords
        LRHandle2=LR(sys.argv[5],sys.argv[6])
        LRHandle2.buildTrainingInfoWOStopWords(spamTrainingPath,0,sys.argv[8])
        LRHandle2.buildTrainingInfoWOStopWords(hamTrainingPath,1,sys.argv[8]);
        LRHandle2.buildTestInfoWOStopWords(spamTestPath,0,sys.argv[8])
        LRHandle2.buildTestInfoWOStopWords(hamTestPath,1,sys.argv[8]);
        LRHandle2.retrieveVocabSet()
        LRHandle2.setInitialWeights()
        LRHandle2.runGradientAscent(sys.argv[7])
        print("Accuracy after removing stopwords")
        LRHandle2.applyLR()    
        
        
main()
    