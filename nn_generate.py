# This code has been inspired by the works of:
# 1: Tech With Tim (2019) Python Chat Bot Tutorial - Chatbot with Deep Learning (Part 3) Available At: https://www.youtube.com/watch?v=PzzHOvpqDYs&ab_channel=TechWithTim (Accessed: 16/10/2020)
# 2: ugik (2017) Tensorflow chat-bot model.ipynb Available At:  https://github.com/ugik/notebooks/blob/master/Tensorflow%20chat-bot%20model.ipynb (Accessed: 2/02/2021)

import tflearn
import tensorflow as tf
import numpy as np
import random

import pickle

import json_build

import math

import sys
import os

from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

# create our training data
training = []
output = []
# create an empty array for our output
output_empty = [0] * len(json_build.classes)

# training set, bag of words for each sentence
for doc in json_build.documents:
    bag_of_words = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # stem each word
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # bag_of_words array
    for w in json_build.words:
        if w in pattern_words:
            bag_of_words.append(1)
        else:
            bag_of_words.append(0)
    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[json_build.classes.index(doc[1])] = 1

    training.append([bag_of_words, output_row])

# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)

# create train and test lists
train_x = list(training[:, 0])
train_y = list(training[:, 1])

try:
    tf.reset_default_graph()
except AttributeError as tfgrapherror:
    print("Error resetting tensorflow graph: ", tfgrapherror)
    sys.exit('Closing Program')

try:
    hiddenLayerNode = math.ceil(((len(train_x[0]) + len(train_y[0])) / 2))
    net = tflearn.input_data(shape=[None, len(train_x[0])])
    net = tflearn.fully_connected(net, hiddenLayerNode)
    net = tflearn.fully_connected(net, math.ceil((hiddenLayerNode / 2)))
    net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
    net = tflearn.regression(net)
except ValueError as nnbuilderror:
    print("Error creating the neural network model: ", nnbuilderror)
    sys.exit('Closing Program')

if not os.path.isdir('./tflearnModel'):
    try:
        os.mkdir("./tflearnModel")
    except OSError:
        print("Creation of the directory failed")
        sys.exit('Closing Program')
    else:
        print("Successfully created the directory")

# Define model and setup tensorboard
try:
    model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
    # Start training (apply gradient descent algorithm)
    model.fit(train_x, train_y, n_epoch=100, batch_size=32, show_metric=True)
    model.save('./tflearnModel/model.tflearn')
except IndexError as nnfiterror:
    print("Error fitting the neural network model: ", nnfiterror)
    sys.exit('Closing Program')

try:
    pickle.dump({'words': json_build.words, 'classes': json_build.classes, 'train_x': train_x, 'train_y': train_y},
                open("./tflearnModel/model.tflearn", "wb"))
except (IOError, OSError, pickle.PickleError, pickle.UnpicklingError):
    print("Error writing/saving pickled data as tflearn model")
    sys.exit("Closing Program")
except FileNotFoundError:
    print("tflearn model does not exist")
    sys.exit("Closing Program")

try:
    data = pickle.load(open("./tflearnModel/model.tflearn", "rb"))
except (IOError, OSError, pickle.PickleError, pickle.UnpicklingError):
    print("Error loading pickled data from tflearn model")
    sys.exit("Closing Program")
except FileNotFoundError:
    print("tflearn model does not exist")
    sys.exit("Closing Program")

words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']
