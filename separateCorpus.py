import pandas as pd
import numpy as np
import re
import spacy

nlp = spacy.load('en_core_web_sm')

def preprocess(text):
  words = []
  for row in text:
    doc = nlp(row)
    for token in doc:
      word = token.text
      url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', word)
      mentions = re.findall('@\S+', word)
      htmlTags = re.findall('\<[/]?\S+\>', word)
      unicode = re.findall('[^a-z^\ ]', word)
      spaces = re.findall('\s+', word)
      #character = re.findall('\w+', word)
      if not token.is_stop and not token.is_punct and not url and not mentions and not htmlTags and not unicode and not spaces and not word.isdigit():
        words.append(word.lower())
  array = np.array(words)
  array.sort()
  return array

data = pd.read_excel('COV_train.xlsx', header=None, engine='openpyxl')

print("Reading the file COV_train.xlsx ...")
data.columns = ['tweet', 'Feeling']

positiveTweets = np.array(data[data['Feeling'] == 'Positive'].iloc[:, 0])
negativeTweets = np.array(data[data['Feeling'] == 'Negative'].iloc[:, 0])

print("Preprocessing each corpus ...")

positiveTokens = preprocess(positiveTweets)
negativeTokens = preprocess(negativeTweets)

print("Dumping vocabulary into file ...")

file = open("corpusP.txt", "w+", encoding='utf-8')
for word in positiveTokens:
  file.write(word + "\n")
file.close()

file = open("corpusN.txt", "w+", encoding='utf-8')
for word in negativeTokens:
  file.write(word + "\n")
file.close()

