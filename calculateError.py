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

right = 0
for index in range(len(classes)):
  if classes[index] == 'Positive' and classified[index] == 'P':
    right += 1
  elif classes[index] == 'Negative' and classified[index] == 'N':
    right += 1

print("The accuracy is: " + str(100 * (right/len(classes))))
      

