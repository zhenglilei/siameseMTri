# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 13:40:58 2015

@author: root
"""

import numpy as np
import matplotlib.pyplot as plt

from sklearn import neighbors
knn = neighbors.KNeighborsClassifier()

# Make sure that caffe is on the python path:
caffe_root = '/home/lilei/Downloads/caffe/'  # this file is expected to be in {caffe_root}/examples/siamese
import sys
sys.path.insert(0, caffe_root + 'python')

import caffe


# decrease if you want to preview during training
PRETRAINED_FILE = 'mnist_siamese_iter_30000.caffemodel' 
MODEL_FILE = 'mnist_siamese.prototxt'

caffe.set_mode_cpu()
net = caffe.Net(MODEL_FILE, PRETRAINED_FILE, caffe.TEST)

# ---------read in training data --------#


TRAIN_DATA_FILE = '../../data/mnist/train-images-idx3-ubyte'
TRAIN_LABEL_FILE = '../../data/mnist/train-labels-idx1-ubyte'
n = 60000

with open(TRAIN_DATA_FILE, 'rb') as f:
    f.read(16) # skip the header
    raw_data = np.fromstring(f.read(n * 28*28), dtype=np.uint8)

with open(TRAIN_LABEL_FILE, 'rb') as f:
    f.read(8) # skip the header
    train_labels = np.fromstring(f.read(n), dtype=np.uint8)
    
# reshape and preprocess
caffe_in = raw_data.reshape(n, 1, 28, 28) * 0.00390625 # manually scale data instead of using `caffe.io.Transformer`
out = net.forward_all(data=caffe_in)  
train_feat = out['feat']
#train_feat /= np.sqrt(np.sum(train_feat**2,axis=1))[:,np.newaxis]

print('----------------')

# ---------read in test data --------#
TEST_DATA_FILE = '../../data/mnist/t10k-images-idx3-ubyte'
TEST_LABEL_FILE = '../../data/mnist/t10k-labels-idx1-ubyte'
n = 10000

with open(TEST_DATA_FILE, 'rb') as f:
    f.read(16) # skip the header
    raw_data = np.fromstring(f.read(n * 28*28), dtype=np.uint8)

with open(TEST_LABEL_FILE, 'rb') as f:
    f.read(8) # skip the header
    test_labels = np.fromstring(f.read(n), dtype=np.uint8)
    
# reshape and preprocess
caffe_in = raw_data.reshape(n, 1, 28, 28) * 0.00390625 # manually scale data instead of using `caffe.io.Transformer`
out = net.forward_all(data=caffe_in)  

test_feat = out['feat']
#test_feat /= np.sqrt(np.sum(test_feat**2,axis=1))[:,np.newaxis]

knn.n_neighbors = 5
print ('start KNN')
print ('training size:')
print (np.shape(train_feat))
print (np.shape(train_labels))
knn.fit(train_feat,train_labels)
acc = knn.score(train_feat,train_labels)
print (acc)

c = ['#ff0000', '#ffff00', '#00ff00', '#00ffff', '#0000ff', 
     '#ff00ff', '#990000', '#999900', '#009900', '#009999']

f = plt.figure(figsize=(16,9))
for i in range(10):
    plt.plot(train_feat[train_labels==i,0].flatten(), train_feat[train_labels==i,1].flatten(), '.', c=c[i])
plt.legend(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
plt.grid()
plt.show() 


print ('testing size:')
print (np.shape(test_feat))
print (np.shape(test_labels))
acc = knn.score(test_feat,test_labels)
print (acc)

f = plt.figure(figsize=(16,9))
for i in range(10):
    plt.plot(test_feat[test_labels==i,0].flatten(), test_feat[test_labels==i,1].flatten(), '.', c=c[i])
plt.legend(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
plt.grid()
plt.show()  