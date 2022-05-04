import pandas as pd
import numpy as np
import re
import spacy
nlp = spacy.load('en_core_web_sm')
from collections import Counter

urlRegexp = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
mentionsRegexp = '@\S+'
htmlRegexp = '\<[/]?\S+\>'
unicodeRegexp = '[^a-z^\ ]'
spaceRegexp = '\s+'

def readFile(fileName):
  fileObj = open(fileName, "r") #opens the file in read mode
  words = fileObj.read().splitlines() #puts the file into an array
  fileObj.close()
  return words

def preprocess(text):
  words = np.array([])
  doc = nlp(text)
  for token in doc:
    word = token.text
    url = re.findall(urlRegexp, word)
    mentions = re.findall(mentionsRegexp, word)
    htmlTags = re.findall(htmlRegexp, word)
    unicode = re.findall(unicodeRegexp, word)
    spaces = re.findall(spaceRegexp, word)
    if not token.is_stop and not token.is_punct and not url and not mentions and not htmlTags and not unicode and not spaces and not word.isdigit():
      words = np.append(words, word.lower())
  return words

print('Loadig the Positive and negative models files ...')

positiveInfo = np.array(readFile("modelo_lenguaje_P.txt"))
negativeInfo = np.array(readFile("modelo_lenguaje_N.txt"))

positiveHead = np.array([positiveInfo[0], positiveInfo[1]], dtype=str) #the 2 heading lines
negativeHead = np.array([negativeInfo[0], negativeInfo[1]], dtype=str)

positiveInfo = np.delete(positiveInfo, [0, 1]) #all info without the 2 heading lines
negativeInfo = np.delete(negativeInfo, [0, 1])

positiveFrequecies = {}
for line in positiveInfo:
    word = line.split(" ")
    positiveFrequecies[word[1]] = float(word[5])

negativeFrequencies = {}
for line in negativeInfo:
    word = line.split(" ")
    positiveFrequecies[word[1]] = float(word[5])

print('Loading and processing the testing file ...')
data = pd.read_excel('COV_test.xlsx', header=None, engine='openpyxl')
data.columns = ['Tweets']
data['Processed Tweets'] = data['Tweets'].apply(lambda tweet: preprocess(tweet))

processedList = data['Processed Tweets'].tolist()
file = open('clasificacion_alu0101325583.txt', 'w+')
for tweet in processedList:
  for word in tweet:
    frequency = positiveFrequecies[word]
    
file.close()
