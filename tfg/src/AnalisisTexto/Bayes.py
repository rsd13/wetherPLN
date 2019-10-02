import numpy as np  
import pandas as pd  
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import MultinomialNB


def main():
    pd.set_option('display.max_rows', 1000)
    dir_path = os.path.dirname(os.path.abspath(__file__))
    path = dir_path + "/../textos/csv/entrenamiento/SVM/"
    #ficheroCSV = open(path + "entrenamiento.csv", "r")
    
    colnames = ['frase', 'clase']
    total = pd.read_csv(path + "total.csv", names=colnames) 
    
   
    Bayes(total)
    

def evaluacion(y_true, y_pred):
    
    recall = metrics.recall_score(y_true, y_pred, average='macro')
    print("Recall: %f" % recall)
    precision = metrics.precision_score(y_true, y_pred, average='macro')
    print("Precision: %f" % precision)
    f1_score = metrics.f1_score(y_true, y_pred, average='macro')
    print("F1-score: %f" % f1_score)
    accuracy = metrics.accuracy_score(y_true, y_pred)
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