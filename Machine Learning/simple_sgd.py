import matplotlib.pyplot as plt
import numpy as np
# Already defined variables/functions
# plot_classifier
# plot_classifier(data, label, w, transform_first=lambda x:x, transform_second=lambda x:x, margin=1)
# transform_first and transform_second are used to transform the data into the desired feature space
# margin is a postive value used to color in the region in {x | yw^T Phi(x) <= margin}

def calc_gradient(y, w, x, lmbda):
    gradient =  lmbda * w
    if 1 - y * w.reshape(-1,1).T @ x.reshape(-1,1) <= 0:
        return gradient
    else:
        return gradient - y * x


def linear_sgd(data, labels, nepochs=10, gamma=0.025, w0=np.array([0.3, -0.3, 0.3]), lmbda=0.1):
    w = w0
    for epoch in range(nepochs):
        # YOUR CODE GOES HERE!
        for i in range(len(labels)):
            x = np.concatenate([data[i], [1]])
            gradient = calc_gradient(labels[i], w, x, lmbda)
            w = w - gradient * gamma
    return w




def quadratic_sgd(data, labels, nepochs=10, gamma=0.025, w0=np.array([0.3, 0.3, 0.3, 0.3, -0.3, -0.3]), lmbda=0.1):
    w = w0
    for epoch in range(nepochs):
        # YOUR CODE GOES HERE!
        for i in range(len(labels)):
            x = np.array([data[i][0]**2, data[i][0] * data[i][1], data[i][1] ** 2, data[i][0], data[i][1], 1])
            gradient = calc_gradient(labels[i], w, x, lmbda)
            w = w - gradient * gamma
    return w



###################
#### The following are variables for the extra part of
###################
# points
print("X.shape =", X.shape)
print("Y.shape =", Y.shape)
# gamma
print("gamma={}".format(gamma))
# n_epochs
print("n_epochs={}".format(n_epochs))
# lmbda
print("lmbda={}".format(lmbda))


### [Optional] YOUR PLOTTING CODE GOES HERE