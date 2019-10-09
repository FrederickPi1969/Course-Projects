import numpy as np
import time
from io import BytesIO
import time
ten_sec = int(round(time.time()/20))
#314, 10,11
if ten_sec %3 == 0:
    prng = np.random.RandomState(314)
elif ten_sec%3 == 1:
    prng = np.random.RandomState(11)
else:
    prng = np.random.RandomState(10)

data = np.loadtxt(BytesIO(data_files["data/wine/wine.data"]), dtype=float, delimiter=',')
overall_data =  data[:,1:]
overall_labels = data[:,0].astype(int)

max_array = np.amax(overall_data, axis = 0)
min_array = np.amin(overall_data, axis = 0)
denominator = max_array - min_array
num_data = len(overall_labels)
for i in range(num_data):
    overall_data[i] = (overall_data[i]-min_array)/denominator

indices = np.ones(len(overall_labels),dtype= bool)
indices[10:21] = False
indices[60:71] = False
indices[131:141] = False

training_data = overall_data[indices]
training_label = overall_labels[indices]
reversed_indices = np.logical_not(indices)
testing_data = overall_data[reversed_indices]
testing_label = overall_labels[reversed_indices]

#shuffle
perm = prng.permutation(len(training_label))
training_data = training_data[perm]
training_label = training_label[perm]

def softmax(x):
    """
    A numerically stable version of the softmax function
    """
    exps = np.exp(x - np.max(x))
    return exps / np.sum(exps)

    import numpy as np
import matplotlib.pyplot as plt

def weight_init(fan_in, fan_out):
    """
    @param      fan_in   The number of input units
    @param      fan_out  The number of output units
    @return     The 2d weight matrix initialized using xavier uniform initializer
    """
    # IMPLEMENT ME
    s = np.sqrt(2. / (fan_in + fan_out))
    weight = np.random.uniform(low=-1 * s, high=s, size=(fan_out, fan_in))
    return weight

def to_one_hot(y, k):
    """
    @brief      Convert numeric class values to one hot vectors
    @param      y     An array of labels of length N
    @param      k     Number of classes
    @return     A 2d array of shape (N x K), where K is the number of classes
    """
    # IMPLEMENT ME
    labels = np.zeros([y.shape[0], k])
    for i in range(labels.shape[0]):
        labels[i, y[i] - 1] = 1
    return labels

def accuracy(y, y_hat):
    """
    @param      y      ground truth labels of shape (N x K)
    @param      y_hat  Estimated probability distributions of shape (N x K)
    @return     the accuracy of the prediction as a scalar
    """
    # IMPLEMENT ME
    truth = []
    pred = []
    for i in range(y.shape[0]):
        truth.append(np.argmax(y[i]))
        pred.append(np.argmax(y_hat[i]))
    return np.mean(np.array(truth) == np.array(pred))

class NeuralNetwork:
    """The Python class that represents our neural network"""

    def __init__(self, d, h, k):
        """
        @brief      Initialize weight and bias
        @param      d     size of the input layer
        @param      h     size of the hidden layer
        @param      k     size of the output layer
        """
        wb = weight_init(d + 1, h)
        self.w1 = wb[:, :d]
        self.b1 = wb[:, d]
        self.z1 = None
        self.a1 = None
        wb = weight_init(h + 1, k)
        self.w2 = wb[:, :h]
        self.b2 = wb[:, h]

    def forward(self, x):
        """
        @brief      Takes a batch of samples and compute the feedforward output
        @param      x     A numpy array of shape (N x D)
        @return     The output at the last layer (N x K)
        """
        # IMPLEMENT ME
        x = x.copy().T
        self.z1 = self.w1 @ x + self.b1.reshape(-1,1)
        self.a1 = np.maximum(0,self.z1)
        z2 = (self.w2 @ self.a1 + self.b2.reshape(-1,1)).T
        return z2

    def backprop(self, x, y, y_hat, lr):
        """
        @brief      Compute the gradients and update Ws and bs, you don't
                    need to return anything - instead, please modify
                    self.w1, self.w2, self.b1, self.b2 as needed
        @param      x      the features (N x D)
        @param      y      ground truth label of shape (N x K)
        @param      y_hat  predictions of shape (N x K)
        @param      lr     Learning rate
        """
        # IMPLEMENT ME
        x = x.T
        y = y.T
        y_hat = y_hat.T
        one_minus_y = y_hat - y
        d_w2 = one_minus_y @ self.a1.T
        d_b2 = one_minus_y
        d_w1 = self.w2.T @ one_minus_y @ x.T
        d_b1 = self.w2.T @ one_minus_y
        self.w2 = self.w2 - lr / x.shape[1] * (d_w2)
        self.b2 = self.b2 - lr * np.mean(d_b2, axis = 1)
        self.w1 = self.w1 - lr / x.shape[1] * (d_w1)
        self.b1 = self.b1 - lr * np.mean(d_b1, axis = 1)

def train_one_epoch(model, x, y, test_x, test_y, lr):
    """
    @brief      Takes in a model and train it for one epoch.
    @param      model   The neural network
    @param      x       The features of training data (N x D)
    @param      y       The labels of training data (N x K)
    @param      test_x  The features of testing data (M x D)
    @param      test_y  The labels of testing data (M x K)
    @param      lr      Learning rate
    @return     (train_accuracy, test_accuracy), the training accuracy and
                testing accuracy of the current epoch
    """
    # IMPLEMENT ME
    z2 = model.forward(x)
    y_hat = np.zeros(z2.shape)
    for i in range(z2.shape[0]):
        y_hat[i,:] = softmax(z2[i, :])
    model.backprop(x, y, y_hat, lr)
    train_accuracy = accuracy(y, y_hat)

    z2_test = model.forward(test_x)
    y_hat_test = np.zeros(z2_test.shape)
    for i in range(z2_test.shape[0]):
        y_hat_test[i,:] = softmax(z2_test[i, :])
    test_accuracy = accuracy(test_y, y_hat_test)
    return (train_accuracy, test_accuracy)

# Implement step 6 here
fig, ax = plt.subplots(2,1,figsize=(10,10))
y = to_one_hot(training_label, 3)
test_y = to_one_hot(testing_label, 3)
nn_model = NeuralNetwork(13, 50 ,3)
tr_ac_003, te_ac_003, tr_ac_03, te_ac_03, tr_ac_3, te_ac_3 = [],[],[],[],[],[]
for e in range(100):
    a, b= train_one_epoch(nn_model, training_data, y, testing_data, test_y, lr=3)
    tr_ac_3.append(a); te_ac_3.append(b)

nn_model = NeuralNetwork(13, 50, 3)
for e in range(100):
    a, b= train_one_epoch(nn_model, training_data, y, testing_data, test_y, lr=0.03)
    tr_ac_003.append(a); te_ac_003.append(b)

nn_model = NeuralNetwork(13, 50, 3)
for e in range(100):
    a, b= train_one_epoch(nn_model, training_data, y, testing_data, test_y, lr=0.3)
    tr_ac_03.append(a); te_ac_03.append(b)

x = np.linspace(1, 100, 100)
ax[0].plot(x, tr_ac_3, label="train lr=3")
ax[0].plot(x, te_ac_3, label="test lr=3")
ax[0].plot(x, tr_ac_03, label="train lr=0.3")
ax[0].plot(x, te_ac_03, label="test lr=0.3")
ax[0].plot(x, tr_ac_003, label="train lr=0.03")
ax[0].plot(x, te_ac_003, label="test lr=0.03")
ax[0].set_title("train/test accuracy with learning rate = [3, 0.3, 0.03], round 1")
ax[0].legend()

nn_model = NeuralNetwork(13, 50 ,3)
tr_ac_003, te_ac_003, tr_ac_03, te_ac_03, tr_ac_3, te_ac_3 = [],[],[],[],[],[]
for e in range(100):
    a, b= train_one_epoch(nn_model, training_data, y, testing_data, test_y, lr=3)
    tr_ac_3.append(a); te_ac_3.append(b)

nn_model = NeuralNetwork(13, 50, 3)
for e in range(100):
    a, b= train_one_epoch(nn_model, training_data, y, testing_data, test_y, lr=0.03)
    tr_ac_003.append(a); te_ac_003.append(b)

nn_model = NeuralNetwork(13, 50, 3)
for e in range(100):
    a, b= train_one_epoch(nn_model, training_data, y, testing_data, test_y, lr=0.3)
    tr_ac_03.append(a); te_ac_03.append(b)

x = np.linspace(1, 100, 100)
ax[1].plot(x, tr_ac_3, label="train lr=3")
ax[1].plot(x, te_ac_3, label="test lr=3")
ax[1].plot(x, tr_ac_03, label="train lr=0.3")
ax[1].plot(x, te_ac_03, label="test lr=0.3")
ax[1].plot(x, tr_ac_003, label="train lr=0.03")
ax[1].plot(x, te_ac_003, label="test lr=0.03")
ax[1].set_title("train/test accuracy with learning rate = [3, 0.3, 0.03], round 2")
ax[1].legend()
plt.show()

print("learning rate = 0.3 is the best.", "For a=0.03, the step size is too small to make achieve a good acuracy in 100 rounds. We might need \
100,000 epoches to reach the final optimum, as gradient is also getting smaller and smaller. But then the run time is unacceptable.",\
"For a = 3, The step size is so large that it make the gradient desent very unstable. I ran the code a few times and discovered that it's not guranteed to \
reach a good accuracy in the end with a=3. Usually the code is wandering around the optimum and simply walk past it everytime due to large step size.",\
"a = 0.3 gives us very steady increment of accuracy each epoch, and a stable good final accuracy. In this example it ends with a final accuracy over 90% everytime.", sep = "\n")