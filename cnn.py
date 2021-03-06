
# coding: utf-8

# In[2]:

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
import tensorflow as tf
import os
import cv2
import numpy as np
count = 0
count1 = 0
#import Image
from scipy.misc import imresize
path_train = "./Numerals/"
train = []
train_label = []
test = []
test_label = []
for _,dirs,_ in os.walk(path_train):
    for files in dirs:
        directory = path_train + files + '/'
        for fname in os.listdir(directory):
           # print(os.listdir(directory))
            if(fname.endswith(".png")):
                image = cv2.imread(directory+fname)
                im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                im_resize = cv2.resize(im_gray, (28, 28))
                train.append(np.reshape(im_resize, (1, 784)))
                train_label.append(count)
        count = count + 1
        
#train_label = np.array(train_label)

train_label_new = [] 

for var in train_label :
    if (var == 0) :
         train_label_new.append([0,0,0,0,0,0,0,0,0,0])
    elif (var == 1) :
         train_label_new.append([0,1,0,0,0,0,0,0,0,0])
    elif (var == 2) :
          train_label_new.append([0,0,1,0,0,0,0,0,0,0])
    elif (var == 3) :
          train_label_new.append([0,0,0,1,0,0,0,0,0,0])
    elif (var == 4) :
         train_label_new.append([0,0,0,0,1,0,0,0,0,0])
    elif (var == 5) :
         train_label_new.append([0,0,0,0,0,1,0,0,0,0])
    elif (var == 6) :
         train_label_new.append([0,0,0,0,0,0,1,0,0,0])
    elif (var == 7) :
         train_label_new.append([0,0,0,0,0,0,0,1,0,0])
    elif (var == 8) :
         train_label_new.append([0,0,0,0,0,0,0,0,1,0])
    elif (var == 9) :
         train_label_new.append([0,0,0,0,0,0,0,0,0,1])

train = np.asarray(train)
for x in range (0, 999):
    train[x] = (255 - train[x])/255.
#train = (255 - train)/255.
#train = np.reshape(train,[-1,28,28,1])
train = np.reshape(train, [train.shape[0], train.shape[2]])
train_label = np.asarray(train_label_new)

#• Input
x = tf.placeholder(tf.float32, [None, 784])
#• Parameter Variable
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
#• Softmax regression model:
y = tf.nn.softmax(tf.matmul(x, W) + b)

y_ = tf.placeholder(tf.float32, [None, 10])
cross_entropy = tf.reduce_mean(
-tf.reduce_sum(y_ * tf.log(y),
reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

sess = tf.InteractiveSession()

tf.global_variables_initializer().run()
for _ in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    _,c= sess.run([train_step,cross_entropy], feed_dict={x: batch_xs, y_:batch_ys})
    correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(y_,1))

    accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

    print(sess.run(accuracy, feed_dict={x:
    mnist.test.images, y_: mnist.test.labels}))

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')
def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])
x_image = tf.reshape(x,[-1,28,28,1])
#b_conv1 = bias_variable([32])x_image = tf.reshape(x, [-1, 28, 28, 1])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) +
b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])
y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

cross_entropy = tf.reduce_mean(
tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
accuracy_cnn = []
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(20000):
        batch = mnist.train.next_batch(50)
        if i % 100 == 0:
            train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
            accuracy_cnn.append(train_accuracy)
            print('step %d, training accuracy %g' % (i, train_accuracy))
        train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob:0.5})
    print('test accuracy of MNIST %g' % accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))
    print('test accuracy of USPS %g' % accuracy.eval(feed_dict={x: train[0:999,], y_: train_label[0:999,], keep_prob: 1.0}))
    
  


# In[ ]:



