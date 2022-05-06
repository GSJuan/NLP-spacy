import pandas as pd
import numpy as np
import re
import spacy
from collections import Counter
from numpy import log as ln

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
vocabulary = np.delete(vocabulary, 0)

print("Printing basic info into model files ...")

#negativo
#Numero de documentos (tweets) del corpus: 15398
#Número de palabras del corpus: 201117

#positivo
#Numero de documentos (tweets) del corpus: 18046
#Número de palabras del corpus: 235230

positiveList = Counter(positiveWords.tolist())
negativeList = Counter(negativeWords.tolist())

vocabSize = vocabulary.size

# numPosWords = len(positiveList.items())
# numNegWords = len(negativeList.items())

numPosWords = positiveWords.size
numNegWords = negativeWords.size

posFile = open("modelo_lenguaje_P.txt", "w+", encoding='utf-8')
posFile.write("Número de documentos (tweets) del corpus: " + str(positiveTweets.size))
posFile.write("\nNúmero de palabras del corpus: " + str(numPosWords))

negFile = open("modelo_lenguaje_N.txt", "w+", encoding='utf-8')
negFile.write("Número de documentos (tweets) del corpus: " + str(negativeTweets.size))
negFile.write("\nNúmero de palabras del corpus: " + str(numNegWords))

print("Computing frequencies ...")

unkFreq = 0

for word in vocabulary:
 
  posFreq = 0
  negFreq = 0

  if word in positiveList:
    posFreq = positiveList[word]

  if word in negativeList:
    negFreq = negativeList[word]

  if ((posFreq + negFreq) > 3):
    probabilityPos = ln(posFreq + 1) - ln(numPosWords + vocabSize)
    probabilityNeg = ln(negFreq + 1) - ln(numNegWords + vocabSize)

    posFile.write("\nPalabra: " + word + " Frec: " + str(posFreq) + " lnProb: " + str(round(probabilityPos, 2)))  
    negFile.write("\nPalabra: " + word + " Frec: " + str(negFreq) + " lnProb: " + str(round(probabilityNeg, 2)))

  else:
    unkFreq += 1

unkPosProb = ln(unkFreq + 1) - ln(numPosWords + vocabSize)
posFile.write("\nPalabra: UNK" + " Frec: " + str(unkFreq) + " lnProb: " + str(round(unkPosProb, 2)))

unkNegProb = ln(unkFreq + 1) - ln(numNegWords + vocabSize)
negFile.write("\nPalabra: UNK" + " Frec: " + str(unkFreq) + " lnProb: " + str(round(unkNegProb, 2)))

posFile.close()
negFile.close()