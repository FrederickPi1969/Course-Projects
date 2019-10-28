# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018

"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import sys
import numpy as np
import nltk 
from nltk import bigrams

path = sys.path[0]
stop_words = ['no', 'how', 'just', 'y', 'are', 'and', 'whom', 'isn', 'i', 'ma', 'hers', 'up', 'doing', 'your', 'don', 'again', 'through', 'above', 'should', 'doesn', 'does', 'any', 'very', 'ourselves', 'can', 'o', 'both', 'out', 'now', 'there', 'down', "that'll", 'yourselves', 'for', 'be', 'about', 're', 'too', 'd', "shan't", 'these', 'myself', "couldn't", 'which', 'shouldn', 'wasn', 'further', 'against', 'into', "you've", "you'd", 'by', 'while', 'so', 'had', 'couldn', 'more', 'my', 'll', 'itself', 'have', 'who', 'each', 'needn', 'ours', 'not', "hadn't", 'few', 'at', 'once', 'was', 'a', 'some', 've', 'haven', 'has', "wouldn't", 'when', 'where', 'hadn', 'being', 'mustn', 'it', 't', 'what', 'before', 'him', 'they', 'with', "don't", 'then', 'all', "weren't", 'aren', "mightn't", "won't", 'only', 'we', 'nor', 'that', 'am', 'between', 'to', 'did', 'off', 'if', 'the', 'after', 'our', "you're", "mustn't", 'most', 'an', 'himself', 'mightn', 'weren', 'of', 'theirs', "wasn't", 'on', 'over', 'herself', 'ain', "haven't", 'shan', 'their', "shouldn't", "it's", 'or', 'themselves', 'why', 'but', 'own', 'having', 'during', "aren't", "hasn't", 'will', 'as', 'this', "didn't", 'its', "needn't", 's', "doesn't", 'below', 'didn', 'them', 'his', 'because', 'yours', 'same', 'won', 'you', 'm', 'yourself', 'were', 'do', 'hasn', 'he', 'her', 'is', 'those', 'other', "isn't", 'here', 'wouldn', 'she', 'until', 'such', "should've", "you'll", 'than', 'from', 'under', 'me', "she's", 'in', 'been']

def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter you provided with --laplace (1.0 by default)
    """
    # TODO: Write your code here
    # return predicted labels of development set
    #
    ### len(train_set)  8000, len(dev) = 5000 P(pos) = 0.8 
    #### 0.55, 4.0, 0.30 ----------- 0.766
    #### 0.25 3.5 0.3 -------------- 0.766
    print(pos_prior)
    smoothing_parameter = 3.5
    pos_total_word = 0
    neg_total_word = 0
    pos_word_dict = {}
    neg_word_dict = {}
    dicts = [neg_word_dict, pos_word_dict]
    for i, sentence in enumerate(train_set):

        if train_labels[i] == 1: # positive reviews
            for word in sentence:
                pos_total_word += 1 
                if word in stop_words:
                    continue
                if word in pos_word_dict:
                    pos_word_dict[word] += 1
                else :
                    pos_word_dict[word] = 1

        else: # negative reviews
            for word in sentence:
                neg_total_word += 1 
                if word in stop_words:
                    continue
                if word in neg_word_dict:
                    neg_word_dict[word] += 1
                else :
                    neg_word_dict[word] = 1


    prob = {}
    denominator_pos = pos_total_word + smoothing_parameter * (len(pos_word_dict) + 1)
    denominator_neg = neg_total_word + smoothing_parameter * (len(neg_word_dict) + 1)
    de = [denominator_neg, denominator_pos]

    for t, dictionary in enumerate(dicts):
        for key, value in dictionary.items():
            if key not in prob:
                prob[key] = {0 : 0, 1 : 0}
                if smoothing_parameter != 0:
                    prob[key][1 - t] = -1 * np.log(smoothing_parameter / de[t]) 
                    # print(prob[key][1 - t])

            prob[key][t] = -1 * np.log((value + smoothing_parameter) / de[t])  
            

    revised_prob = {}
    for key, value in prob.items():
        if np.abs(value[0] - value[1]) >= 0.25:
            revised_prob[key] = value 

    print(len(revised_prob))

    dev_labels = []
    num_0 = 0
    for i, sentence in enumerate(dev_set):
        pos_odd = -1 * np.log(pos_prior)
        neg_odd = -1 * np.log(1.0 - pos_prior)
        for word in sentence:
            if word in revised_prob:
                pos_odd += revised_prob[word][1]
                neg_odd += revised_prob[word][0]
    
        if pos_odd > neg_odd:
            num_0 += 1
        dev_labels.append(1 if pos_odd <= neg_odd else 0)
    print(num_0)

    
    #### bigram model 
    















    return dev_labels









