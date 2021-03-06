# This is a function for k-fold cross-validation on (X; y)
# Yi Ding

import numpy as np


# This function return the accuracy score of the prediction for classification
def my_accuracy_score_classification(ytrue, ypred, metric):
    ytrue = np.array(ytrue)
    ypred = np.array(ypred)
    if ytrue.shape[0] != ypred.shape[0]:
        raise Exception('ERROR: ytrue and ypred not same length!')
    accuracy_score = 0
    for i in range(0,ytrue.shape[0]):
        if ytrue[i] == ypred[i]:
            accuracy_score = accuracy_score + 1
    if metric == 'accuracy':
        return float(accuracy_score)/float(ytrue.shape[0])
    else:
        raise Exception('No that metric')


# This function return the accuracy score of the prediction for regression
def my_accuracy_score_regression(ytrue, ypred, metric='mae'):
    ytrue = np.array(ytrue)
    ypred = np.array(ypred)
    if ytrue.shape[0] != ypred.shape[0]:
        raise Exception('ERROR: ytrue and ypred not same length!')
    # Here we use R^2(R Square) to evaluate the performance of the model
    y_bar = np.mean(ytrue)
    sum_hat_sqr = 0
    sum_bar_sqr = 0
    sum_abs_err = 0
    for i in range(0,ytrue.shape[0]):
        sum_hat_sqr = sum_hat_sqr + (ytrue[i]-ypred[i])*(ytrue[i]-ypred[i])
        sum_bar_sqr = sum_bar_sqr + (ytrue[i]-y_bar)*(ytrue[i]-y_bar)
        sum_abs_err = sum_abs_err + np.abs(ytrue[i]-ypred[i])
    r_sqr = 1 - sum_hat_sqr/sum_bar_sqr
    mse = sum_hat_sqr/ytrue.shape[0]
    mae = sum_abs_err/ytrue.shape[0]
    if metric == 'mae':
        return mae
    elif metric == 'mse':
        return mse
    elif metric == 'r_square':
        return r_sqr
    else:
        raise Exception('No that metric')


# Main function
# ml_type = 0 means classification
# ml_type = 1 means regression
def my_cross_val(method, X, y, k, ml_type='classification', metric = 'accuracy'):
    X = np.array(X)
    y = np.array(y)
    y = np.reshape(y,(X.shape[0],1))    
    # Initialize array for the test set error    
    errRat = np.empty([k, 1])
    # Permute the indices randomly
    rndInd = np.random.permutation(y.size)
    # Start and end index of test set
    sttInd = 0
    endInd = (np.array(y.size/k).astype(int))
    indLen = (np.array(y.size/k).astype(int))
    for i in range(0, k):
        # Prepare training data and test data
        Xtrain = np.concatenate((X[rndInd[0:sttInd],:],X[rndInd[endInd:y.size],:]), axis=0)
        ytrain = np.concatenate((y[rndInd[0:sttInd]],y[rndInd[endInd:y.size]]), axis=0)
        Xtest = X[rndInd[sttInd:endInd],:]
        ytest = y[rndInd[sttInd:endInd]]
        sttInd = endInd
        endInd = endInd + indLen
        # Create the model
        # myMethod = method()
        myMethod = method   # Directly passing the model
        # Fit the data
        myMethod.fit(Xtrain,ytrain.ravel())
        # Test the model on (new) data
        ypred = myMethod.predict(Xtest)
        #print("ytest:",ytest)
        #print("ypred:",ypred)
        # Save error rate
        if ml_type == 'classification':
            errRat[i] = 1 - my_accuracy_score_classification(ytest, ypred, metric)
        elif ml_type == 'regression':
            errRat[i] = my_accuracy_score_regression(ytest, ypred, metric)
        else:
            raise Exception('Invalid ml_type!')
    return errRat