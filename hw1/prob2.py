from math import pow, sqrt
from heapq import heappush, heappop
from copy import copy
import matplotlib.pyplot as plt
import argparse


################### Start of main program ###################

# Parsing args
parser = argparse.ArgumentParser(description='Implementation for PROBLEM 2')
parser.add_argument('-g', '--grid', action='store_true', help='Print the grid and then draw the boundary')
parser.add_argument('-k', '--kneighbors', nargs='?', default='1', help='Specify number of neighnors selected for knn method. k is initialized to be 1 by default')
parser.add_argument('-y', '--ymultiple', nargs='?', default='1', help='For problem 2(b), it requires the y coordinates to be multiplied by 5. To see how that affects the result, add -y 5 in command line')

args = vars(parser.parse_args())

K = int(args['kneighbors'])
Y = int(args['ymultiple'])

training_set = [(0, 1 * Y, 'A'), (2, 3 * Y, 'A'), (4, 4 * Y, 'A'), 
                (2, 0 * Y, 'B'), (5, 2 * Y, 'B'), (6, 3 * Y, 'B')]


def euclidDist(pt_1, pt_2):
    return sqrt(pow((pt_1[0] - pt_2[0]), 2) + 
                pow((pt_1[1] - pt_2[1]), 2))

def classifyPtr(pt, tr_set):
    ## Take a point and traning set as input, return 
    ## the current with its label.
    pq = []
    weight_map = {'A': 0, 'B': 0}
    for p in tr_set:
        dist = euclidDist(pt, p)
        heappush(pq, (dist, p))
    for i in xrange(K):
        pair = heappop(pq)
        weight_map[pair[1][2]] += 1 / (pair[0] + 0.0001)
    if (weight_map['A'] >= weight_map['B']): return 'A'
    return 'B'



grid = []
for i in xrange(7):
    row = [0] * (5 * Y)
    grid.append(copy(row))

x, y, gridx, gridy = [], [], [], []


colors, gridcolors = [], []

for p in training_set:
    x.append(p[0])
    y.append(p[1])
    color = 'r' if p[2] == 'A' else 'b'
    colors.append(color)

plt.scatter(x, y, c=colors)

for i in xrange(7):
    for j in xrange(5 * Y):
        label = classifyPtr((i,j), training_set)
        gridx.append(i)
        gridy.append(j)
        if label == 'A': 
            gridcolors.append('r')
        else: 
            gridcolors.append('b')
        grid[i][j] = label

if args['grid']:
    plt.scatter(gridx, gridy, c=gridcolors)

xBoundary = []
yBoundary = []


for j in range(0, 5 * Y):
    for i in range(1, 7):
        if grid[i][j] != grid[i-1][j]:
            xBoundary.append(i - 0.5)
            yBoundary.append(j)
            break

plt.plot(xBoundary, yBoundary, 'g')             

plt.show()

