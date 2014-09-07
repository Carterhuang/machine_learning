#! /usr/bin/python

import sys
import argparse
import numpy as np
import random
import heapq
import matplotlib.pylab as plt


def getSimilarity(x,y):
    return np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))

def normalize(a):
    averageA = np.mean(a)
    varA = np.var(a)
    return [(x-averageA)/varA for x in a]
    

############### Start of main program ###################

# Parsing args
parser = argparse.ArgumentParser(description='The KNN implementation for Assignment 1')
parser.add_argument('file', nargs='?', default='null', help='The path of the input data file.')
parser.add_argument('-n', '--normalize', action='store_true', help='When specified, the data will be normalized before feeding to knn algorithm.')

args = vars(parser.parse_args())

if args['file'] == 'null':
    print "Invalid input. Please type python knn.py -h for help"

# File IO
f = open(args['file'])

sepalL, sepalW, petalL, petalW, labels = [], [], [], [], []

for line in f:
    parts = line.split(',')
    sepalL.append(float(parts[0]))
    sepalW.append(float(parts[1]))
    petalL.append(float(parts[2]))
    petalW.append(float(parts[3]))
    labels.append(parts[4])
f.close()

similarity_map = [[0.0 for x in xrange(150)] for x in xrange(150)] 

for i in xrange(150):
    x = [sepalL[i], sepalW[i], 
         petalL[i], petalW[i]]
    for j in xrange(150):
        y = [sepalL[j], sepalW[j], 
             petalL[j], petalW[j]]
        similarity_map[i][j] = getSimilarity(x, y)


# Normalize if specified
if args['normalize']:
    print 'Normalizing data set...'
    sepalL = normalize(sepalL)
    sepalW = normalize(sepalW)
    petalL = normalize(petalL)
    petalW = normalize(petalW)
else:
    print 'Skipped normalization.'

ordering = [i for i in range(150)]

accuracyTrend = [] 
for k in range(1,101):
    print 'k='+str(k)
    totalAccuracy = 0.0
    for i in range(25):
        random.shuffle(ordering)
        testing = ordering[0:30]
        training = ordering[30:150]
        correct = 0
        for testi in testing:
            x = [sepalL[testi], sepalW[testi], 
                 petalL[testi], petalW[testi]]
            knns = [] 
            for traini in training:
                y = [sepalL[traini], sepalW[traini],
                     petalL[traini], petalL[traini]]
                distance = similarity_map[testi][traini] 
                if len(knns) < k:
                    heapq.heappush(knns, (distance, labels[traini]))
                else:
                    currentMax = knns[0][0]
                    if distance > currentMax:
                        heapq.heappushpop(knns, (distance, labels[traini]))
            labelCount = {}
            ## Traverse knns heap.
            for knn in knns:
                if knn[1] in labelCount: 
                    labelCount[knn[1]] += 1
                else:
                    labelCount[knn[1]] = 1
            newClassification = ''
            maxNumber = -1 
            for label in labelCount:
                if labelCount[label] > maxNumber:
                    maxNumber = label[1]
                    newClassification = label
            if newClassification == labels[testi]:
                correct += 1
        totalAccuracy += correct/30.0        
        correct = 0
    accuracyTrend.append(totalAccuracy/25)
    totalAccuracy = 0
print accuracyTrend
krange = range(1,101)
plt.plot(krange,accuracyTrend,'r-')
plt.show()


    
