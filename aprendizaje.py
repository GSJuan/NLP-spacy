import pandas as pd
import numpy as np
import re
import spacy
from collections import Counter
from math import log

def readFile(fileName):
  fileObj = open(fileName, "r") #opens the file in read mode
  words = fileObj.read().splitlines() #puts the file into an array
  fileObj.close()
  return words

data = pd.read_excel('COV_train.xlsx', header=None, engine='openpyxl')

print("Reading the file COV_train.xlsx ...")
data.columns = ['tweet', 'Feeling']

positiveTweets = np.array(data[data['Feeling'] == 'Positive'].iloc[:, 0])
negativeTweets = np.array(data[data['Feeling'] == 'Negative'].iloc[:, 0])

print("Reading the Positive and negative vocabulary ...")

positiveWords = np.array(readFile("corpusP.txt"))
negativeWords = np.array(readFile("corpusN.txt"))
vocabulary = np.array(readFile("vocabulario.txt"))

print("Printing basic info into model files ...")

file = open("modelo_lenguaje_P.txt", "w+", encoding='utf-8')
file.write("Numero de documentos (tweets) del corpus: " + str(positiveTweets.size))
file.write("\nNúmero de palabras del corpus: " + str(positiveWords.size))
file.close()

file = open("modelo_lenguaje_N.txt", "w+", encoding='utf-8')
file.write("Numero de documentos (tweets) del corpus: " + str(negativeTweets.size))
file.write("\nNúmero de palabras del corpus: " + str(negativeWords.size))
file.close()

#negativo
#Numero de documentos (tweets) del corpus: 15398
#Número de palabras del corpus: 201117

#positivo
#Numero de documentos (tweets) del corpus: 18046
#Número de palabras del corpus: 235230

print("Computing frequencies ...")

positiveList = Counter(positiveWords.tolist())
negativeList = Counter(negativeWords.tolist())

posFile = open("modelo_lenguaje_P.txt", "a+", encoding='utf-8')
negFile = open("modelo_lenguaje_N.txt", "a+", encoding='utf-8')

unkPos = 0
unkNeg = 0
for word in vocabulary:

  positiveFrequency = positiveList[word] 
  if positiveFrequency > 3:
    probabilityPos = log(positiveFrequency + 1) - log(positiveWords.size + vocabulary.size)
    posFile.write("\nPalabra: " + word + " Frec: " + str(positiveFrequency) + " LogProb: " + str(probabilityPos))
  else:
    unkPos += 1

  negativeFrequency = negativeList[word]
  if negativeFrequency > 3:
    probabilityNeg = log(negativeFrequency + 1) - log(negativeWords.size + vocabulary.size)
    negFile.write("\nPalabra: " + word + " Frec: " + str(negativeFrequency) + " LogProb: " + str(probabilityNeg))
  else:
    unkNeg += 1

unkPosProb = log(unkPos + 1) - log(positiveWords.size + vocabulary.size)
posFile.write("\nPalabra: <UNK>" + " Frec: " + str(unkPos) + " LogProb: " + str(unkPosProb))

unkNegProb = log(unkNeg + 1) - log(negativeWords.size + vocabulary.size)
negFile.write("\nPalabra: <UNK>" + " Frec: " + str(unkNeg) + " LogProb: " + str(unkNegProb))

posFile.close()
negFile.close()