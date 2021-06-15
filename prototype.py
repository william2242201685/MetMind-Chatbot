#This code has been inspired by the works of:
#FreeBirdsCrew (2020) CHATBOTS - Using Natural Language Processing and Tensorflow Available At: https://github.com/FreeBirdsCrew/AI_ChatBot_Python/blob/master/Contextual%20Chatbot%20-%20NLP%20and%20Tensorflow.ipynb (Accessed: 6/02/2020)
#For Dialogue Contexulisation


import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

import numpy as np
import random

import webbrowser
import urllib.error
import urllib.request

import smtplib

from flask import Flask, render_template, request

import nn_generate

import time

import binascii

import json

import sys

class ContextHistory:
    contextOld = ""
    myIntent = ""
    myOldTag = ""
    myTag = ""
    myFirstContext = ""

    myFirstInput = 0

    myEmailIntent = 0
    studentEmail = ""
    studentPassword = ""
    staffEmail = ""
    symptomType = ""
    symptomProblem = ""

    time = 0.0
    startTime = 0.0

    chatRestart = "<br/><br/>Please specify if you want " \
                  "guidance for your ""fears"" or anxiety ""symptoms"" whilst at Cardiff Met during the coronavirus " \
                  "epidemic"


myOldContext = ContextHistory()

qaCode = binascii.unhexlify(
    "5468616e6b20796f7520666f722070617274696369706174696e6720666f72203130206d696e75746573212054686520436f646520666f7220746865207175657374696f6e6e61697265206973204135337274593133322120596f752063616e206b6565702074657374696e6720696620796f752077616e743a203c62722f3e3c62722f3e")

with open('intents.json') as json_data:
    intents = json.load(json_data)

# This will load the model that was generated in nn_generate
try:
    nn_generate.model.load('./tflearnModel/model.tflearn')
except ValueError:
    print("There seems to be an error trying to load the neural network from ./tflearnModel/model.tflearn")
    sys.exit("Closing Program")


def clean_up_sentence(sentence):
    #This is designed to tokenize the  user input
    sentence_words = nltk.word_tokenize(sentence)
    #This is designed to stem the words from the users inputs
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag_of_words = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag_of_words[i] = 1
                if show_details:
                    print("found in bag: %s" % w)

    return np.array(bag_of_words)


def myTime():
    if ContextHistory.myFirstInput < 1:
        ContextHistory.startTime = time.perf_counter()

    ContextHistory.time = (time.perf_counter() - ContextHistory.startTime)
    print(ContextHistory.time)



context = {}

ERROR_THRESHOLD = 0.70


def classify(sentence):
    #This section is designed to calculate the probability values from the users input to the model
    results = nn_generate.model.predict([bow(sentence, nn_generate.words)])[0]
    #If a prediction is below the error thresehold of 0.70 then it is filtered out
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    #Calculates and sorts the probability rates comparing to its strength/probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((nn_generate.classes[r[0]], r[1]))
    return return_list


def filtering(i, show_details):
    if 'context_set' in i:
        if show_details:
            return 'context:', i['context_set']
        myOldContext.contextOld = i['context_set']
        myOldContext.myTag = i['tag']
        return i['context_set']


def advancedResponse(i):
    if 'web' in i:
        myWeb = i['web']
        try:
            urllib.request.urlopen(myWeb)
        except urllib.error.HTTPError:
            return "I am sorry but I am having trouble connecting to the site: " + random.choice(i['responses'])
        except urllib.error.URLError:
            return "I am sorry but I am having trouble connecting to the site" + random.choice(i['responses'])
        else:
            webbrowser.open_new(myWeb)
            return "Redirecting: " + random.choice(i['responses'])

    else:
        return random.choice(i['responses'])


def email(userInput):
    if myOldContext.myEmailIntent == 1:
        myOldContext.studentEmail = str(userInput) + "@outlook.cardiffmet.ac.uk"
        print(str(userInput) + "from email")
        myOldContext.myEmailIntent += 1
        return "Please Enter Your Student Password"
    else:
        recEmail = myOldContext.staffEmail
        subject = myOldContext.studentEmail + " " + myOldContext.symptomType + " anxiety symptom issues"
        body = "Dear Sir/Madam,\n\n This student has been recorded at a high priority as the participant has shown " \
               "signs of suffering from severe " + myOldContext.symptomType + " anxiety symptoms. The symptoms " \
                                                                              "specified indicate that the " \
                                                                              "student could be suffering from " \
                                                                              "anxities that can lead to " + \
               myOldContext.symptomProblem + "\n\nPlease Email them as soon as possible as to arrange a formal meetup "\
                                             "and/or conversation. \n\n Kindest Regards\nMetMind Chatbot"
        msg = f'Subject: {subject}\n\n{body}'

        myOldContext.studentPassword = str(userInput)

        try:
            server = smtplib.SMTP('smtp.outlook.com', 587)
            server.starttls()
            server.login(myOldContext.studentEmail, myOldContext.studentPassword)
            server.sendmail(myOldContext.studentEmail, recEmail, msg)
            myOldContext.myEmailIntent = 0
            myOldContext.contextOld = ""
            myOldContext.myFirstContext = ""
            myOldContext.myIntent = ""
            myOldContext.myOldTag = myOldContext.chatRestart
            return "email sent! you will hear from the wellbeing team shortly" + myOldContext.chatRestart
        except smtplib.SMTPAuthenticationError:
            myOldContext.myEmailIntent = 1
            return "Incorrect email or password: please enter your username"


def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    #If the user input is correctly classified find matching intent/tag
    if results:
        #Loop through possible matches
        print(results)
        while results:
            for i in intents['intents']:
                #Get tag from first result(if matching)
                if i['tag'] == results[0][0]:

                    if 'email' in i:
                        myOldContext.myEmailIntent = 1
                        myOldContext.staffEmail = i['email']
                        myOldContext.symptomType = i['symptom_type']
                        myOldContext.symptomProblem = i['symptom_problem']

                    if 'context_set' in i and 'context_filter' not in i and myOldContext.myFirstContext == "":
                        myOldContext.myOldTag = random.choice(i['responses'])
                        myOldContext.myFirstContext = i['context_set']
                        myOldContext.myIntent = i['intent']

                    try:
                        if ('intent' in i and i['context_filter'] == myOldContext.contextOld) or (
                                i['tag'] == myOldContext.myTag):
                            myOldContext.myOldTag = random.choice(i['responses'])
                            myOldContext.myIntent = i['intent']
                            print(myOldContext.myIntent)

                    except KeyError:
                        print("Filter Not In Requested Object")

                    print(myOldContext.contextOld)

                    if 'context_filter' in i and i['context_filter'] == myOldContext.contextOld:
                        context[userID] = filtering(i, show_details)
                        if 'context_set' not in i and myOldContext.myEmailIntent < 1:
                            myOldContext.contextOld = ""
                            myOldContext.myIntent = ""
                            myOldContext.myFirstContext = ""
                            myOldContext.myOldTag = myOldContext.chatRestart
                            myResp = advancedResponse(i) + myOldContext.chatRestart
                        else:
                            myResp = advancedResponse(i)
                        print("reached")
                        return myResp
                    elif 'context_filter' not in i and myOldContext.contextOld != "" or (
                            'context_filter' in i and i['context_filter'] != myOldContext.contextOld):
                        return "I'm sorry? Can you repeat that?: " + myOldContext.myOldTag
                    else:
                        context[userID] = filtering(i, show_details)

                        if 'context_filter' not in i or \
                                (userID in context and 'context_filter' in i and i['context_filter'] == context[
                                    userID]):
                            if show_details:
                                return 'tag:', i['tag']
                            # a random response from the intent
                            return random.choice(i['responses'])

            results.pop(0)
    else:
        if myOldContext.myIntent != "":
            return "I'm sorry? Can you repeat that?: " + myOldContext.myOldTag
        else:
            return "I'm sorry? Can you repeat that?: " + myOldContext.myOldTag


app = Flask(__name__)


@app.route('/get')
def userChat():
    myStr = ""
    if ContextHistory.time > 600.00 and ContextHistory.myFirstInput != 2:
        ContextHistory.myFirstInput = 2
        myStr += qaCode.decode()

    userInput = request.args.get('msg')

    myTime()

    if myOldContext.myEmailIntent != 0:
        myStr = email(userInput)
    else:
        if myOldContext.myIntent != "":
            userInput = myOldContext.myIntent + userInput
        print(userInput)
        myStr += response(userInput)

        if ContextHistory.myFirstInput < 1:
            ContextHistory.myFirstInput = 1
    return str(myStr)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(threaded=True)

