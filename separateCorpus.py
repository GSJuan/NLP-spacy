from pathlib import Path
import pandas as pd
import re

data = pd.read_excel('COV_train.xlsx', header=None, engine='openpyxl')

print("Reading the file COV_train.xlsx ...")
data.columns = ['tweet', 'Feeling']

positiveTweets = data[data['Feeling'] == 'Positive'].values[:, 0].tolist()
negativeTweets = data[data['Feeling'] == 'Negative'].values[:, 0].tolist()

print("Dumping vocabulary into file ...")

file = open("Positivo.txt", "w+", encoding='utf-8')
for tweet in positiveTweets:
    file.write(tweet + "\n")
file.close()

file = open("Negativo.txt", "w+", encoding='utf-8')
for tweet in negativeTweets:
  file.write(tweet + "\n")
file.close()