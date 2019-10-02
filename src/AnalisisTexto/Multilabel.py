
import numpy as np  
import matplotlib.pyplot as plt  
import pandas as pd 
from sklearn.metrics import confusion_matrix
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import KFold
from sklearn.naive_bayes import MultinomialNB
import pickle
from sklearn.feature_selection import SelectPercentile
from sklearn.feature_selection import chi2

from sklearn.preprocessing import MultiLabelBinarizer


def main():
    pd.set_option('display.max_rows', 1000)
    dir_path = os.path.dirname(os.path.abspath(__file__))
    path = dir_path + "/../textos/csv/entrenamiento/SVM/"
    #ficheroCSV = open(path + "entrenamiento.csv", "r")
    
    colnames = ['frase', 'clase1','clase2']
    total = pd.read_csv(path + "totalMulti.csv", names=colnames) 
    
    total = total.replace(np.nan, '', regex=True)
    
   
    multilabel2(total)
    

def evaluacion(y_true, y_pred):
    
    recall = metrics.recall_score(y_true, y_pred, average='macro')
    print("Recall: %f" % recall)
    precision = metrics.precision_score(y_true, y_pred, average='macro')
    print("Precision: %f" % precision)
    f1_score = metrics.f1_score(y_true, y_pred, average='macro')
    print("F1-score: %f" % f1_score)
    accuracy = metrics.accuracy_score(y_true, y_pred)
    return recall, precision, f1_score, accuracy

def multilabel2(total):
    X = total.frase
    y = total[["clase1", "clase2"]]
    y = y.replace(np.nan, '', regex=True)
   
    X = total.iloc [:, [0]] 
    y = total.iloc [:, [1,2]] 
    y =y.replace(np.nan, '', regex=True)
    
    X = np.array(X)
    y = np.array(y)
   
    pipeline = Pipeline([
        ('vectorize', CountVectorizer()),
        ('tf_idf', TfidfTransformer()),
        ('clf', OneVsRestClassifier(SGDClassifier(loss='modified_huber')))
    ])
    
    mlb = MultiLabelBinarizer()
    scores = []
    kf = KFold(n_splits=10, random_state=0, shuffle=True)
    for train, test in kf.split(total):
        
        X_train = total.iloc [train, [0]] 
        X_train = np.array(X_train)
        
        y_train = total.iloc [train, [1,2]] 
        y_train = np.array(y_train)
        
        X_test = total.iloc [test, [0]] 
        X_test = np.array(X_test)
        
        y_test = total.iloc [test, [1,2]] 
        y_test = np.array(y_test)
        aux = []
        for test in X_test:
           aux.append(test[0])
           
        X_test = aux
        
        aux = []
        for train in X_train:
     
            aux.append(train[0])
        X_train = aux
        
        y_train = mlb.fit_transform(y_train)
        y_test = mlb.transform(y_test)
        
        
        pipeline.fit(X_train, y_train)
        predicted = pipeline.predict(X_test)
        scores.append(evaluacion(y_test, predicted))
    
    
    

    


   
    
    recall = metrics.recall_score(y_test, predicted, average='macro')
    print("Recall: %f" % recall)
    precision = metrics.precision_score(y_test, predicted, average='macro')
    print("Precision: %f" % precision)
    f1_score = metrics.f1_score(y_test, predicted, average='macro')
    print("F1-score: %f" % f1_score)
    accuracy = metrics.accuracy_score(y_test, predicted)
    print("accuracy: %f" % accuracy)
    return recall, precision, f1_score, accuracy



def Bayes(total):
    
    
    text_clf = Pipeline([
         ('vect', CountVectorizer()),
         ('tfidf', TfidfTransformer()),
         ('clf', MultinomialNB()),
     ])
    
   
    X = np.array(total.frase)
    y = np.array(total.clase)
    
    scores = []
    kf = KFold(n_splits=10, random_state=0, shuffle=True)
    for train, test in kf.split(total):

        X_train = X[train]
        X_test = X[test]
        y_train = y[train]
        y_test = y[test]
        
        text_clf.fit(X_train, y_train)
        predicted = text_clf.predict(X_test)
        scores.append(evaluacion(predicted, y_test))
        print(confusion_matrix(y_test, predicted))
     
    recall = sum([x[0] for x in scores]) / len(scores)
    print("Averaged total recall", recall)
    precision = sum([x[1] for x in scores]) / len(scores)
    print("Averaged total precision", precision)
    f_score = sum([x[2] for x in scores]) / len(scores)
    print("Averaged total f-score", f_score)
    accuracy = sum([x[3] for x in scores]) / len(scores)
    print("Accuracy total ", accuracy)

    
        
   

    '''
    X_train, X_test, y_train, y_test = train_test_split(X, y)
   
    kfold =KFold(n_splits=10, random_state=0, shuffle=False)

    results = cross_val_score(text_clf, X_train, y_train, cv=kfold) #Cross validation on training set
    print(results)
    text_clf.fit(X_train, y_train)
    predicted = text_clf.predict(X_test)
   
    result = (accuracy_score(predicted, y_test))
    print(result)
    evaluacion1 = evaluacion(y_test, predicted)
    aux = metrics.precision_score(y_test, predicted, average='micro')  
    print(evaluacion1)
    
    '''
main()