import pandas as pd
import numpy as np
import re
import spacy
nlp = spacy.load('en_core_web_sm')


def readFile(fileName):
  fileObj = open(fileName, "r") #opens the file in read mode
  words = fileObj.read().splitlines() #puts the file into an array
  fileObj.close()
  return words

classified = readFile("resumen_alu0101325583.txt")

data = pd.read_excel('COV_test_g1_debug.xlsx', header=None, engine='openpyxl')

print("Reading the file COV_test_g1_debug.xlsx")
data.columns = ['Number','Tweet', 'Feeling']

classes = data['Feeling'].to_list()
Number = data['Number'].to_list()

PP = 0
PN = 0
NP = 0
NN = 0
right = 0
for index in range(0, len(classes)):
  tweet = Number[index]
  tweet -= 1
  if classes[index] == 'Positive' and classified[tweet] == 'P':
    right += 1
    PP += 1
  elif classes[index] == 'Positive' and classified[tweet] == 'N':
    PN += 1
  elif classes[index] == 'Negative' and classified[tweet] == 'N':
    right += 1
    NN += 1
  elif classes[index] == 'Negative' and classified[tweet] == 'P':
    NP += 1

print("The accuracy is: " + str(100 * (right/len(classes))))
print("Confusion matrix: ")
print(str(PP) + " , " + str(PN))
print(str(NP) + " , " + str(NN))
      
