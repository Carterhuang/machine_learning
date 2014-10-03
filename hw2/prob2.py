import sys
import argparse
import math
import matplotlib.pylab as plt
from copy import copy, deepcopy


class Node:
    def __init__(self):
        self.value = ''
        self.d = 1
        self.n = 1
        self.left = None
        self.right = None

def getCounts(root_set):
    positives = 0.0
    negatives = 0.0
    for instance in root_set:
        if instance[0]=='B':
            positives += 1
        elif instance[0]=='M':
            negatives += 1 
        else:
            raise Exception("getCounts: not a valid set of instances!")
    #print '['+str(positives)+'+,'+str(negatives)+'-]'
    return [positives, negatives]

def getEntrophy(positives, negatives):
    if positives==0 or negatives==0:
        return 0.0
    pos_ratio = abs(positives/(positives+negatives))
    neg_ratio = abs(negatives/(positives+negatives))
    return  -pos_ratio*math.log(pos_ratio,2)-neg_ratio*math.log(neg_ratio,2)

# use the decision tree to classify an instance
def useID3(instance, dt):
    cursor = dt
    while cursor is not None:
        value = cursor.value
        if value=='B':
            return 'B'
        if value=='M':
            return 'M'
        condition_parts = value.split('<=')
        print 'condition_parts', condition_parts;
        if instance[int(condition_parts[0])]<=int(condition_parts[1]):
            cursor = cursor.left
        else:
            cursor = cursor.right

# the ID3 algorithm to learn a decision tree
def learnID3(root_set, att_table, d):
    set_counts = getCounts(root_set) 
    # set_counts[0] is the number of positive examples in the set
    # set_counts[1] is the number of negative examples in the set
    total_set = set_counts[0] + set_counts[1]
    # if all positives or negatives, return a leaf node
    # or if depth limit is reached
    if set_counts[0]==0 or set_counts[1]==0 or d==1:
        root = Node()
        if set_counts[0] > set_counts[1]:
            root.value = 'B'
        else:
            root.value = 'M'
        return root
    else:
        set_entrophy = getEntrophy(set_counts[0], set_counts[1]) 
        left = []
        right = []
        left_counts = []
        right_counts = []
        max_gain = [0.0, 0.0, 0.0]  #[info_gain_value, i, j]
        # iterate through all possible unused conditions
        for i in range(1, 10):
            for j in range(1, 10):
                if att_table[i-1][j-1]==1:
                    continue;
                tmp_left = []
                tmp_right = []
                # divide all examples into left and right according to current condition
                for example in root_set:
                    if example[i] <= j:
                        tmp_left.append(example)
                    else:
                        tmp_right.append(example)
                tmp_left_counts = getCounts(tmp_left)
                total_left = tmp_left_counts[0]+tmp_left_counts[1]
                tmp_right_counts = getCounts(tmp_right)
                total_right = tmp_right_counts[0]+tmp_right_counts[1]
                gain = set_entrophy - total_left/total_set*getEntrophy(tmp_left_counts[0], tmp_left_counts[1]) - total_right/total_set*getEntrophy(tmp_right_counts[0], tmp_right_counts[1])
                if gain > max_gain[0]:
                    max_gain = [gain, i, j]
                    left = tmp_left
                    right = tmp_right
                    left_counts = tmp_left_counts
                    right_counts = tmp_right_counts
        if max_gain[0] <= 0:
            root = Node()
            if set_counts[0] > set_counts[1]:
                root.value = 'B'
            else:
                root.value = 'M'
            return root
        att_table[max_gain[1]-1][max_gain[2]-1] = 1;
        root = Node()
        root.value = str(max_gain[1])+'<='+str(max_gain[2])
        root.left = learnID3(left, deepcopy(att_table), d-1)
        root.right = learnID3(right, deepcopy(att_table), d-1)
        root.d = max(root.left.d,root.right.d)+1
        root.n = root.left.n+root.right.n+1
        return root


####################Start Of Main Program#########################
parser = argparse.ArgumentParser(description='The ID3 implementation for problem 2.')
parser.add_argument('file', nargs='?', default='null', help='The path of the training data file.')
parser.add_argument('-t', '--test_data', nargs='?', default='null', help='The path of the test data file.')
parser.add_argument('-d', '--depth', action='store_true', help='If specified, analyze tree depth influnces on accuracy.') 

args = vars(parser.parse_args())

if args['file'] == 'null':
    print "Invalid input. Please type python prob3.py -h for help"

# File IO
f = open(args['file'])

training_set = []

for line in f:
    parts = line.split()
    instance = [parts[0]]
    for i in range(1, 10):
       value = parts[i].split(':')[1]
       instance.append(int(value))
    training_set.append(instance)

f.close()

# Read in test set
test_set = []
if args['test_data'] != 'null':
    f = open(args['test_data'])
    for line in f:
        parts = line.split()
        instance = [parts[0]]
        for i in range(1, 10):
            value = parts[i].split(':')[1]
            instance.append(int(value))
        test_set.append(instance)
    f.close()


if args['depth']:
    depth = []
    accuracy = []
    for d in range(2,21):
        # Attribute table for looking up if an attribute has been used
        att_table = [[0 for x in xrange(9)] for x in xrange(9)] 
        dt = learnID3(training_set, att_table,d) 
        print d, dt.d, dt.n
        correct = 0.0
        count = 0
        for instance in test_set:
            count += 1
            label = useID3(instance, dt)
            if label==instance[0]:
                correct+=1
        depth.append(d)
        accuracy.append(correct/count)
    plt.plot(depth, accuracy, 'r-')
    plt.show()
else:
    att_table = [[0 for x in xrange(9)] for x in xrange(9)] 
    dt = learnID3(training_set, deepcopy(att_table), 82)
    print dt.d, dt.n

# print out the learned tree
'''
stack = [dt]
while len(stack) != 0:
    next = stack.pop()
    print next.value
    if next.left is not None:
        stack.append(next.left)
    if next.right is not None:
        stack.append(next.right)

errors = 0
count = 0
for instance in test_set:
    count += 1
    label = useID3(instance, dt) 
    if label!=instance[0]:
        errors+=1
print str(errors)+'/'+str(count)
'''
