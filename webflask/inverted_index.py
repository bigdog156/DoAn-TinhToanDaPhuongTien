import pandas as pd
from pandas import DataFrame
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import base64
import json


# data = pd.read_csv('Gopfile.csv')
data = pd.read_json('csvjson.json')


def xuliText(text):
        conTent = text.lower()
        conTent = re.sub(r'[0-9|”|“|–|-|-|?|$|.|!|"|,|(|)|/|_|\'|`|*|+|@|#|%|^|&|[|]|{|}|;|:|<|>|]',r' ', conTent)
        listConTent = list(conTent.split())
        return listConTent

# Return tất cả các term dạng Dir
def xuliAllText(data):
        DirText = {}
        for i in range(len(data)):
                if type(i) != type(1.):
                        text = xuliText(data[i])
                        DirText = set(text).union(DirText)
        return DirText

def TienXuli(list,Dirtext):
        wordDict = dict.fromkeys(Dirtext, 0)
        for word in list:
                wordDict[word]+=1
        return wordDict

def computeTF(wordDict, words):
    tfDict = {}
    wordsCount = len(words)
    for word, count in wordDict.items():
        tfDict[word] = count/float(wordsCount)
    return tfDict


def computeIDF(docList):
    import math
    idfDict = {}
    N = len(docList)
    
    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / float(val))
        
    return idfDict

def computeTFIDF(tfDocs, idfs):
    arr = []
    for word, val in tfDocs.items():
        arr.append(val*idfs[word])
    return arr

def tfidfQuery(query, DirText, idfs):
        listText = xuliText(query)
        word = TienXuli(listText, DirText)
        tf = computeTF(word,listText)
        tfidf = computeTFIDF(tf, idfs)
        return tfidf

def getString(listText):
        document = ""
        for i in listText:
                document = document +i+" "
        return document


def listItemText(data):
        listItem = []
        for i in range(len(data)):
                text = xuliText(data[i])
                listItem.append(text)
        return listItem

def inverted_index(dataItem, dirText):

        
        wordDict = dict.fromkeys(dirText,'')

        for i in range(len(dataItem)):

                for term in dataItem[i]:

                        temp = wordDict.get(term)
                        a = temp
                        a = a +','+str(i)
                        wordDict[term] = a
                
        return wordDict

def getFileIndex(char, dataJson):
        if char in dataJson:
                index = dataJson[char]
        else:
                index = '-1'
        index = index.split(',')[1:]
        temp = []
        for i in index:
                temp.append(int(i))
        return temp



def getFileSame(queryString, dataJson):

        listQuery = queryString.split(' ')
        
        setIndexQuery = {}

        i = 0
        for term in listQuery:

                indexTerm = getFileIndex(term,dataJson)

                if i==0 :
                        setIndexQuery = set(indexTerm)
                        i = 1
                else:
                        setIndexQuery = setIndexQuery.intersection(indexTerm)    
        
        return setIndexQuery


def readJson(PATH):

    with open(PATH, 'r') as myFile:

        dataJson = myFile.read()

        return json.loads(dataJson)





def test():
        DirText = {}
        for i in data.text:
                if type(i) != type(1.):
                        text = xuliText(i)
                        DirText = set(text).union(DirText)
                # listItem dùng để tính IDF của bộ dữ liệu
        listItem = []
                # Dùng tính TF của từng bộ dữ liệu
        listTF = []
                
        for i in data.text:
                if type(i) != type(1.):
                        listText = xuliText(i)
                        word = TienXuli(listText, DirText)
                        tf = computeTF(word,listText)
                        listTF.append(tf)
                        listItem.append(word)
                # idfs  chỉ tính 1 lần ... Done
        idfs = computeIDF(listItem)
        with open("idfs.json", "w") as write_file:
                json.dump(idfs,write_file,ensure_ascii=False)

        print(len(DirText))
        print(len(listTF))


        listTFIDF = []
        # Có được danh list TF IDF
        for i in range(len(listItem)):
                tfidf = computeTFIDF(listTF[i],idfs)
                listTFIDF.append(tfidf)
        # Lưu file dưới dạng Json

        with open("json_tfidf.json", "w") as write_file:
                json.dump(listTFIDF,write_file)
        

        print(len(listTFIDF[0]))


        TESTTFIDF = readJson('json_tfidf.json')
        print(len(TESTTFIDF[0]))



        listItemJson = listItemText(data.text)

        index = inverted_index(listItemJson, DirText)

        # Ghi ra file dưới dạng json
        with open("data_file.json", "w") as write_file:
                json.dump(index,write_file,ensure_ascii=False)

