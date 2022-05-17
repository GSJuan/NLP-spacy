# Author: Juan García Santos
## Python programs to build the vocabulary, generate learning models, classify testing set and calculate classification error
### Programs implemented: 
  - python vocabulario.py  // Generates file vocabulario.txt containing all words from the COV_train.xlsx ass well as corpusP and corpusN files that contain the words inside positive and negative tweets, with repetitions, correspondingly.
  - python aprendizaje.py // Generates language model files (modelo_lenguaje_P o N) which contain the appearence probability of each word of the vocabulary in positive and negative class separately. They are generated using unknown words treatment as well ass laplacian smoothing
  - python clasificacion.py // Takes a set of tweets as testing input and for each tweet calculates the probability of it belonging to the positive and the negative class using the previously calculated probability of each word inside of the language models. Then, according to those probabilities, classifies each tweet in its corresponding class and dumps all that information in two files: resumen_aluXXX.txt and clasificacion_aluXXX.txt
  - python calculateError.py // simply opens the resumen file wich contains the simplified version of the clasification results and then compares those results with the actual tweet classification inside the original .xlsx file
 
### Transformations used:
  - Tokenization
  - Lower case everything
  - Delete punctuators and emojis
  - Delete hashtags, mentions, URLs and HTML tags
  - Lematization (Optional, it is calculated but not used)

### Libraries Used:
  - Spacy: used for tokenizing each tweet in the preprocessing phase as well as identifying stop words, punctuators and calculating the lemmatization of each token
  - NumPy: used for fast array indexation and included array operations (sort, unique ...)
  - Pandas: used for fast .xlsx loading into program and reliable data indexation
  - Collections: used for its useful Counter object, which when given an array, generates an object of "key value" pairs where "key" is the word inside the array and "value" is the number of repetitions of that word inside of the array.

### Calculated error over training Corpus
My model was able to achieve a 82.28% of accuracy when tested with the training corpus.


### Using Monkey Learn to classify the test corpus with a previous training using the given training corpus 
MonkeyLearn is a cloud-based text analytics solution that extracts data from emails, surveys, tweets, or any text and turns it into custom visualizations. Text analysis tools can label topics, analyze sentiment, and detect intent, as well as extract features, keywords, and named entities from text.
It has a free plan that allows you to train up to 1 model for free. I used that opportunity to train a sentiment analysis model using the given training tweet corpus. Once it was trained (just by simply uploading the xlsx file to the web and marking the columns as text and tags), it allowed me to test the model, for which i used the given testing model file. Here, i encountered a problem since the free plan only allows training files of up to 10,000 rows. In order to solve this, i contacted other colleagues and we split the file in four pieces in order to classify the test file. Once each one had their part, we fused the four filles together into the complete classified file (MonkeyLear_full.xlsx).

In order to test and debug the resulting resumen file (alu0101325583_monkeyLearn_resumen.txt), i compared the results in certain positions using the testing debug file given in the previous lab. After executing the python program debug.py which calculates the accuracy and confusion matrix, i got the following results: 
```bash
The accuracy is: 64.51612903225806
Confusion matrix:
  P   N
P 6 , 8
N 3 , 14
```