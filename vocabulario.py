import spacy
import pandas as pd
nlp = spacy.load('en_core_web_sm')
import openpyxl
from pathlib import Path
import numpy as np
import re

print("Reading the file COV_train.xlsx ...")


def readFile(fileName):
  xlsx_file = Path(fileName)
  wb_obj = openpyxl.load_workbook(filename=xlsx_file, read_only=True)
  sheet = wb_obj.active
  text = []
  for row in sheet.iter_rows(max_col=1):
      for cell in row:
          text.append(cell.value)

# readFile('COV_train.xlsx')
data = pd.read_excel('COV_train.xlsx', header=None, engine='openpyxl')

data.columns = ['tweet', 'Feeling']

text = data.values[:, 0].tolist()

# convert the text to a spacy document
# all spacy documents are tokenized. You can access them using document[i]
#document = nlp(text[0])

print("Tokenizing every tweet and filtering tokens")

words = np.array([])
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
      if(word.islower()):
        words = np.append(words, word)
      else:
        words = np.append(words, word.lower())

print("Sorting and removing uniques from vocabulary ...")

wordList = np.array(words)
uniqueWords = np.unique(wordList)
uniqueWords.sort()

print("Dumping vocabulary into file ...")

file = open("vocabulario.txt", "w+", encoding='utf-8')
file.write("Number of words: " + str(uniqueWords.size) + "\n")
for word in uniqueWords:
  file.write(word + "\n")
file.close()

#the good thing about spacy is a lot of things like lemmatization etc are done when you convert them to a spacy document `using nlp(text)`. You can access sentences using document.sents
#list(document.sents)[0]

# lemmatized words can be accessed using document[i].lemma_ and you can check 
# if a word is a stopword by checking the `.is_stop` attribute of the word.
# here I am extracting the lemmatized form of each word provided they are not a stop word
#lemmas = [token.lemma_ for token in document if not token.is_stop]