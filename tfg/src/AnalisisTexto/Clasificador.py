'''
Created on Jan 5, 2019

@author: rafaelsoriadiez
'''


from sklearn.svm import LinearSVC
from sklearn import preprocessing

import numpy as np  
import matplotlib.pyplot as plt  
import pandas as pd 
from sklearn.model_selection import train_test_split  
from sklearn.svm import SVC  
from sklearn.metrics import confusion_matrix
import os
from sklearn.feature_extraction.text import CountVectorizer
from math import sin #para usar la función seno
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn import datasets
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
import itertools
import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_selection import SelectPercentile
from sklearn.feature_selection import chi2
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer


def main():
    pd.set_option('display.max_rows', 1000)
    dir_path = os.path.dirname(os.path.abspath(__file__))
    path = dir_path + "/../textos/csv/entrenamiento/"
    #ficheroCSV = open(path + "entrenamiento.csv", "r")
    
    colnames = ['frase', 'clase1','clase2']
    #colnames = ['frase', 'clase']
    weather = pd.read_csv(path + "entrenamiento.csv", names=colnames) 
    weatherTest =  pd.read_csv(path + "test.csv", names=colnames) 
    normal =  pd.read_csv(path + "normal.csv", names=colnames) 
    
    #SVM(weather,weatherTest)
    print("------")
    #Bayes(weather,weatherTest)
    print("-----")
    weatherTest2 =  pd.read_csv(path + "testMultilabel.csv", names=colnames) 
    weather2 = pd.read_csv(path + "entrenamientoMultilabel.csv", names=colnames)
    #multilabel(weather2, weatherTest2)
    multilabel2(weather2, weatherTest2)



def evaluacion(y_true, y_pred):
    
    recall = metrics.recall_score(y_true, y_pred, average='macro')
    print("Recall: %f" % recall)
    precision = metrics.precision_score(y_true, y_pred, average='macro')
    print("Precision: %f" % precision)
    f1_score = metrics.f1_score(y_true, y_pred, average='macro')
    print("F1-score: %f" % f1_score)
    accuracy = metrics.accuracy_score(y_true, y_pred)
    return recall, precision, f1_score, accuracy

def SVM(weather,weatherTest):
    categorias =["clase","humedad","nieve","nubes","nubes-precipitacion","otros","precipitacion","temperatura","viento"]
    text_clf = Pipeline([
     ('vect', CountVectorizer()),
     ('tfidf', TfidfTransformer()),
     ('clf', SGDClassifier(loss='hinge', penalty='l2',
                           alpha=1e-3, random_state=42,
                           max_iter=5, tol=None)),
    ])
    
    #Para construir el modelo a partir de nuestros datos, esto es, aprender a clasificar nuevos puntos,
    # llamamos a la función fit pasándole los datos de entrenamiento, y las etiquetas correspondientes (la salida deseada para los datos de entrenamiento):
   

    print(text_clf.fit(weather.frase, weather.clase))
    predicted = text_clf.predict(weatherTest.frase)
    #predicted = text_clf.predict(normal.frase)
    print(predicted)

    
    print(np.mean(predicted == weatherTest.clase))
    #print(metrics.classification_report(weather.clase, predicted))
    print(metrics.classification_report(weatherTest.clase, predicted))
    print(metrics.confusion_matrix(weatherTest.clase, predicted))
    df_confusion = pd.crosstab(weatherTest.clase, predicted)
    print(df_confusion)
    fichero = open("matriz.txt","a")
    fichero.write(str(df_confusion.to_string()))
    fichero.write("------")
    fichero.close()
    '''
    cnf_matrix = confusion_matrix(weatherTest.clase, predicted)
    np.set_printoptions(precision=2)

    # Plot non-normalized confusion matrix
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=categorias,
                          title='Confusion matrix, without normalization')
    
    
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=categorias, normalize=True,
                      title='Normalized confusion matrix')
    plt.show()
    '''
    
def Bayes(weather,weatherTest):
    
    text_clf = Pipeline([
         ('vect', CountVectorizer()),
         ('tfidf', TfidfTransformer()),
         ('clf', MultinomialNB()),
     ])
     
    print(text_clf.fit(weather.frase, weather.clase))
    predicted = text_clf.predict(weatherTest.frase)
    #predicted = text_clf.predict(normal.frase)
    print(predicted)
    
    
    print(np.mean(predicted == weatherTest.clase))
    #print(metrics.classification_report(weather.clase, predicted))
    print(metrics.classification_report(weatherTest.clase, predicted))
    print(metrics.confusion_matrix(weatherTest.clase, predicted))
    df_confusion = pd.crosstab(weatherTest.clase, predicted)
    print(df_confusion)
    fichero = open("matriz.txt","a")
    fichero.write(str(df_confusion.to_string()))
    fichero.close()
    
    
def multilabel(weather,weatherTest):
    
    categorias =["clase","humedad","nieve","nubes","nubes-precipitacion","otros","precipitacion","temperatura","viento"]
    pipeline = Pipeline([
        ('vectorize', CountVectorizer()),
        ('tf_idf', TfidfTransformer(norm='l2')),
        # play with the parameters and check the model size
        ('select', SelectPercentile(chi2, percentile=50)),
        ('clf', OneVsRestClassifier(SGDClassifier(loss='modified_huber')))
    ])
    multi_labels = [
        ["humedad"], ["nieve"], ["nubes"], ["nubes","precipitación"], ["otros"],
        ["precipitacion"], ["temperatura"], ["viento"],
       
    ]

    mlb = MultiLabelBinarizer().fit(weather.clase)
    mlb_labels = mlb.transform(weather.clase)
   
    print(mlb_labels)
    clf = pipeline.fit(weather.frase, mlb_labels)
    print("classifier has %s bytes" % len(pickle.dumps(pipeline.named_steps['clf'])))
    
  
    predicted = pipeline.predict(weatherTest.frase)
    print(predicted)
    #print(np.mean(predicted == weatherTest.clase))
    #print(metrics.classification_report(weatherTest.clase, predicted))
    all_labels = mlb.inverse_transform(predicted)
    print(all_labels)
    for item, labels in zip(weatherTest.frase, all_labels):
        print('%s => %s' % (item, ', '.join(labels)))




def multilabel2(weather,weatherTest):
    X = weather.frase
    y = weather[["clase1", "clase2"]]
    y = y.replace(np.nan, '', regex=True)
   
    X_train = weather.iloc [:, [0]] 
    y_train = weather.iloc [:, [1,2]] 
    y_train =y_train.replace(np.nan, '', regex=True)
    
    X_Test = weatherTest.iloc [:, [0]] 
    y_test = weatherTest.iloc [:, [1,2]] 
    y_test =y_test.replace(np.nan, '', regex=True)
   
    
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_test = np.array(X_Test)
    y_test = np.array(y_test)

   
    pipeline = Pipeline([
        ('vectorize', CountVectorizer()),
        ('tf_idf', TfidfTransformer(norm='l2')),
        # play with the parameters and check the model size
        ('select', SelectPercentile(chi2, percentile=50)),
        ('clf', OneVsRestClassifier(SGDClassifier(loss='modified_huber')))
    ])
    
    '''
    scores = []
    kf = KFold(n_splits=10, random_state=0, shuffle=True)
    for train, test in kf.split(total):

        X_train = X[train]
        X_test = X[test]
        y_train = y[train]
        y_test = y[test]
        
        print(X_test)
        pipeline.fit(X_train, y_train)
        predicted = pipeline.predict(X_test)
        scores.append(evaluacion(y_test, predicted))
    '''
    mlb = MultiLabelBinarizer()
    y_train = mlb.fit_transform(y_train)
    y_test = mlb.transform(y_test)
    

    
    aux = []
    for test in X_test:
     
       aux.append(test[0])
    
    X_test = aux
    
    aux = []
    for train in X_train:
     
       aux.append(train[0])
    
    X_train = aux
    
    #Name: frase, dtype: object
    print(len(X))
    print(y_train.shape)
    #print(X)
   
    print(X_train)
    pipeline.fit(X_train,  y_train)
   
    #print(X_test)
    predicted = pipeline.predict(X_test)
    print("predicte")
   # print(predicted)
   
    
    recall = metrics.recall_score(y_test, predicted, average='macro')
    print("Recall: %f" % recall)
    precision = metrics.precision_score(y_test, predicted, average='macro')
    print("Precision: %f" % precision)
    f1_score = metrics.f1_score(y_test, predicted, average='macro')
    print("F1-score: %f" % f1_score)
    accuracy = metrics.accuracy_score(y_test, predicted)
    print("accuracy: %f" % accuracy)
    return recall, precision, f1_score, accuracy


   
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    
main()


'''
def multilabel2(weather,weatherTest):
    X = weather.frase
    y = weather[["clase1", "clase2"]]
    yvalues = y.values
    #print(yvalues)
    final = []
    for i in range(0, len(yvalues)):
        r = yvalues[:][i:i + 1]

        
        r = np.array(r[[~pd.isnull(r)]])
        final.append(r)

    final = np.array(final)
    print("\n")
    
    "---- parte del test"
    Xtest = weatherTest.frase
    ytest = weatherTest[["clase1", "clase2"]]
    yvaluestest = ytest.values
    
    finaltest = []
    for i in range(0, len(yvaluestest)):
        ra = yvaluestest[:][i:i + 1]

        
        ra = np.array(ra[[~pd.isnull(ra)]])
        finaltest.append(ra)
        
   
    finaltest = np.array(finaltest)
    pipeline = Pipeline([
        ('vectorize', CountVectorizer()),
        ('tf_idf', TfidfTransformer(norm='l2')),
        # play with the parameters and check the model size
        ('select', SelectPercentile(chi2, percentile=50)),
        ('clf', OneVsRestClassifier(SGDClassifier(loss='modified_huber')))
    ])
     
    mlb = MultiLabelBinarizer()
    Y = mlb.fit_transform(final)
    mlb1 = MultiLabelBinarizer()
    Ytest = mlb1.fit_transform(finaltest)
    
    
    
    clf = pipeline.fit(X,  Y)
    print("classifier has %s bytes" % len(pickle.dumps(pipeline.named_steps['clf'])))
    
  
    predicted = clf.predict(Xtest)
    print("predicte")
    print(predicted)
    print("Y")
    print(Ytest)
    all_labels = mlb.inverse_transform(predicted)
    print(all_labels)
    for item, labels in zip(weatherTest.frase, all_labels):
        print('%s => %s' % (item, ', '.join(labels)))
    
    
    cnf_matrix = confusion_matrix(Ytest.argmax(axis=1), predicted.argmax(axis=1))
    
    print(cnf_matrix)
    print(np.mean(Ytest == predicted))
    score = metrics.accuracy_score(Ytest, predicted)
    print(score)
    print( "Accuracy Score: ",accuracy_score(Ytest, predicted))

    
    np.set_printoptions(precision=2)
    categorias =["clase","humedad","nieve","nubes","viento","otros","precipitacion","temperatura"]
    # Plot non-normalized confusion matrix
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=categorias,
                          title='Confusion matrix, without normalization')
    
    
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=categorias, normalize=True,
                      title='Normalized confusion matrix')
    plt.show()
    print(np.mean(Ytest == predicted))
    '''
    