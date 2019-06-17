import json
import pandas as pd
from pandas import DataFrame
import numpy as np
import inverted_index
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import OrderedDict
from operator import itemgetter

# Có các file JSON 
# 1/ data của các tour du lịch
# 2/ Inverted index 
# 3/ TF IDF của các tour du lịch

class Dulich:
        def __init__(self, query, dataJson, dataIndex, dataTFIDF, idfs):
                self.query = query
                self.dataJson = dataJson
                self.dataIndex = dataIndex
                self.dataTFIDF = dataTFIDF
                self.idfs = idfs

def readJson(PATH):

    with open(PATH, 'r') as myFile:

        dataJson = myFile.read()

        return json.loads(dataJson)

def getTfidfIndex(index, dataJson):

    return dataJson[index]


Query = "nha trang"

dataJson = pd.read_json('csvjson.json')

dataIndex = readJson('data_file.json')

dataTFIDF = readJson('json_tfidf.json')

idfs = readJson('idfs.json')


DirText =  []
for i in idfs:
        DirText.append(i)
# DirText = {}
# for i in dataJson.text:
#         if type(i) != type(1.):
#                 text = inverted_index.xuliText(i)
#                 DirText = set(text).union(DirText)


# , dataJson, dataIndex, dataTFIDF, idfs
def searchQuery(query):

        tfidfQue = inverted_index.tfidfQuery(query,DirText,idfs)
        
        #set các giá trị trong item
        indexFile = inverted_index.getFileSame(query, dataIndex)
        
        indexDir = dict.fromkeys(indexFile,0)

        ar1 = np.asarray(tfidfQue).reshape(1,-1)
        
        
        for index in indexFile:
                # print(str(index)+ "    "+ dataJson.text[index])
                ar2 = np.asarray(dataTFIDF[index]).reshape(1,-1)
                a = 1 - cosine_similarity(ar1,ar2)
                indexDir[index] = a
        d = OrderedDict(sorted(indexDir.items(), key=itemgetter(1)))
        obj = []
        for key, value in d.items():
                i = int(key)
                obj.append({
                        'text':dataJson.text[i],
                        'address': dataJson.address[i],
                        'time': dataJson.time[i],
                        'link': dataJson.link[i],
                        'price': dataJson.price[i],
                })
        return obj



