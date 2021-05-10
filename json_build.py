# This code has been inspired by the works of:
# 1: Tech With Tim (2019) Python Chat Bot Tutorial - Chatbot with Deep Learning (Part 2) Available At: https://www.youtube.com/watch?v=ON5pGUJDNow (Accessed: 16/10/2020)
# 2: ugik (2017) Tensorflow chat-bot model.ipynb Available At:  https://github.com/ugik/notebooks/blob/master/Tensorflow%20chat-bot%20model.ipynb (Accessed: 2/02/2021)

import json
import nltk
import sys
import os
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

try:
    with open('intents.json') as json_data:
        intents = json.load(json_data)
except FileNotFoundError:
    print("json file not found")
    sys.exit('Closing Program')

files = ["./templates/index.html", "./static/pop.mp3", "./static/css/style.css"]
for item in files:
    if os.path.isfile(item):
        continue
    else:
        print(item + " does not exist in the correct directory! Please refer back to the guidelines found in the email")
        sys.exit('Closing Program')

words = []
classes = []
documents = []
ignore_words = ['?']

#This section is designed to loop through each pattern in an intent
for intent in intents['intents']:
    for pattern in intent['patterns']:
        #This section is designed for tokenization: This will be proccessed to all words in a sentence
        try:
            w = nltk.word_tokenize(pattern)
        except LookupError as ntlkerror:
            print("Error during tokenization: ", ntlkerror)
            sys.exit('Closing Program')

        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

#This section is designed for stemming each word
#This section will also ensure that any capital letter will be tranformed to lower case
try:
    words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
    words = sorted(list(set(words)))
except IndexError:
    print("Error stemming words")
    sys.exit('Closing Program')


classes = sorted(list(set(classes)))

