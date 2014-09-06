from math import pow, sqrt
from heapq import heappush, heappop
import matplotlib.pyplot as plt

training_set = [(0, 1, 'A'), (2, 3, 'A'), (4, 4, 'A'), 
                (2, 0, 'B'), (5, 2, 'B'), (6, 3, 'B')]

def euclidDist(pt_1, pt_2):
    return sqrt(pow((pt_1[0] - pt_2[0]), 2) + 
                pow((pt_1[1] - pt_2[1]), 2))

def classifyPtr(pt, tr_set):
    ## Take a point and traning set as input, return 
    ## the current with its label.
    pq = []
    for p in tr_set:
        dist = euclidDist(pt, p)
        heappush(pq, (dist, p))
    return heappop(pq)[1][2]

grid = []
for i in xrange(7):
    grid.append([0,0,0,0,0])

x = []
y = []
colors = [] ## Color array.

for i in xrange(7):
    for j in xrange(5):
        label = classifyPtr((i,j), training_set)
        x.append(i)
        y.append(j)
        if label == 'A': 
            colors.append('r')
        else: 
            colors.append('b')
        grid[i][j] = label
print grid

plt.scatter(x, y, c=colors)

xBoundary = [0.5]
yBoundary = [0]

print 'grid ', grid

for j in range(0, 5):
    for i in range(1, 7):
        if grid[i][j] != grid[i-1][j]:
            xBoundary.append(i - 0.5)
            yBoundary.append(j)
            break

print 'xBoundary ', xBoundary, 'yBoundary ', yBoundary
plt.plot(xBoundary, yBoundary, 'g')             

plt.show()

