# -*- coding: utf-8 -*-
"""tezsunum.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m1CbCIjHhGTiJN5R-vb1xKWl-xMLJM2i
"""

import numpy as np
import pandas as pd
import io
import pickle
from tqdm import tqdm
import argparse
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, \
    recall_score, confusion_matrix, classification_report, \
    accuracy_score, f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix,classification_report
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import make_scorer
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_validate
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import AdaBoostClassifier
import lightgbm as lgb
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor
import time
import psutil
from sklearn import preprocessing
import os
from xgboost import XGBClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestRegressor
import logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)



def test_yap(X,y):
    models = []
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('LR', LogisticRegression()))
    models.append(('SVM', SVC()))
    models.append(('DT', DecisionTreeClassifier()))
    models.append(('RF', RandomForestClassifier()))
    models.append(('NB', GaussianNB()))
    models.append(('MLP', MLPClassifier()))
    models.append(('SGD', SGDClassifier()))
    models.append(('ADA', AdaBoostClassifier()))
    models.append(('BAG', BaggingClassifier()))
    df= pd.DataFrame(np.zeros((10,17)),columns=["algoritma","shape0","shape1","data_type","missing_value"
                                          ,"outlier","imbalanced","multicollinearity","SM",
                                             "SS","MS","skew","kurtosis",
                                          "classification_type","time_PRED","acc_PRED","winner"])
    i=1
    num=10
    df["missing_value"][num*(i-1):num*i]= np.mean(X.isnull().sum(axis = 0) / X.shape[0])
    df["data_type"][num*(i-1):num*i]= [len(X.select_dtypes(include=np.number).columns.tolist()) / X.shape[1]] *num
    X= X.fillna(method='ffill')
    X= X.fillna(method='bfill')
    """if y.dtype != np.number:
        le = preprocessing.LabelEncoder()
        y=pd.Series(le.fit_transform(y))"""
    if len(X.select_dtypes(exclude=[np.number]).columns.values) !=0:
        for k in X.select_dtypes(exclude=[np.number]).columns.values:
            X[k]=pd.Series(preprocessing.LabelEncoder().fit_transform(X[k]))

   # X_train, X_test, y_train, y_test= train_test_split(X,y, test_size = 0.25, random_state=0)
    
    names = []
    acc=[]
    pre=[]
    rec=[]
    f1=[]
    speed=[]
    train=[]
    tns=[]
    fps=[]
    fns=[]
    tps=[]
    sm=[]
    ss=[]
    ms=[]
    mem=[]
    
    if y.nunique()==2:
        df["classification_type"][num*(i-1):num*i]=["binary"] *num
    else:
        df["classification_type"][num*(i-1):num*i]=["multiclass"] *num
    
    for name,model in models:
        #modelimiz= model
        #time_start = time.perf_counter()

        #speed.append(time_elapsed)
        names.append(name)
        sm.append(X.std().mean())
        ss.append(X.std().std())
        ms.append(X.mean().std())
        
        """tn, fp, fn, tp = confusion_matrix(y_test,y_pred).ravel()
        tns.append(tn/(tn+fn))
        fps.append(fp/(fp+tp))
        fns.append(fn/(fn+tn))"""
        #mem.append(psutil.virtual_memory()[2])
        

    df['algoritma'][num*(i-1):num*i]=names  
    df["SM"][num*(i-1):num*i]=sm
    df["SS"][num*(i-1):num*i]=ss
    df["MS"][num*(i-1):num*i]=ms
    #df["time"][num*(i-1):num*i]=speed 
    #df["memory"][num*(i-1):num*i]= mem
        
    df["shape0"][num*(i-1):num*i]=[X.shape[0]] * num
    df["shape1"][num*(i-1):num*i]=[X.shape[1]] * num
    
    
    vif = pd.DataFrame()
    vif["variables"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    df["multicollinearity"][num*(i-1):num*i]= vif[vif["VIF"]>10].shape[0] / X.shape[1]
    df["skew"][num*(i-1):num*i]= (X.skew().abs() >2).sum() /X.shape[1]
    df["kurtosis"][num*(i-1):num*i]= (X.kurtosis().abs() >7).sum() /X.shape[1]

    if y.value_counts().values[-1] / y.shape[0] < 0.2: 
        df["imbalanced"][num*(i-1):num*i]=["evet"] *num
    else:
        df["imbalanced"][num*(i-1):num*i]=["hayır"] *num
        
    d=pd.DataFrame((np.abs(stats.zscore(X))))
    df["outlier"][num*(i-1):num*i]= [d[d > 3].count(axis=0).sum() / d.shape[0] / d.shape[1]] * num
    
    #'KNN', 'LR', 'SVM', 'DT', 'RF', 'NB', 'MLP', 'SGD', 'ADA', 'LGB'
    #df["interpretability"][num*(i-1):num*i]= ["A","A","B","A","C","B","E","B","C","D"]

    if len(df.select_dtypes(exclude=[np.number]).columns.values) !=0:
       for k in df.select_dtypes(exclude=[np.number]).columns.values:
           if k!="algoritma":
              df[k]=pd.Series(preprocessing.LabelEncoder().fit_transform(df[k]))
    return df

def pred_acc(X_input):
    pred_accs=[]
    for i in tqdm(range(10)):
        algo= X_input["algoritma"][i]
        filename= "model_{}.sav".format(algo)
        loaded_model = pickle.load(open(filename, 'rb'))
        X_input_new= X_input.drop("algoritma",axis=1).loc[i].values.reshape(1,-1)
        y_pred = loaded_model.predict(X_input_new)
        pred_accs.append(y_pred)
    return pred_accs

def pred_time(X_input):
    filename= "time_model.sav"
    loaded_model = pickle.load(open(filename, 'rb'))
    pred_times = []
    for i in tqdm(range(10)): 
        X_input["algoritma"]=pd.Series(preprocessing.LabelEncoder().fit_transform(X_input["algoritma"]))
        y_pred = loaded_model.predict(X_input.loc[i].values.reshape(1,-1))
        pred_times.append(y_pred)
    return pred_times

def winner(mini):
    num=10
    for j in range(4):
        if mini[mini["acc_PRED"]==j].shape[0]==1:
            return mini[mini["acc_PRED"]==j]["algoritma"].values[0]
            break
        elif mini[mini["acc_PRED"]==j].shape[0] >1 :
            return mini.loc[mini[mini["acc_PRED"]==j]["time_PRED"].sort_values().index[0],:]["algoritma"]
            break
        elif mini[mini["acc_PRED"]==j].shape[0]==0:  #else de denebilir
            continue

def cli():
    """CLI"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-data', required=True,
                        help="Path to input file or dir.", action="store", dest="given_data")
    parser.add_argument('-y', required=True,
                        help="Path to input file or dir.", action="store", dest="y_column")
    
    args = parser.parse_args()
    # Parse arguments
    data_name = args.given_data
    target = args.y_column
    data= pd.read_csv(data_name)
    X= data.drop(target,axis=1)
    y = data[target]
    df= test_yap(X,y)
    X_input=df.iloc[:,:-3]
    df["acc_PRED"]= pred_acc(X_input)
    df["time_PRED"]= pred_time(X_input)
    print(winner(df))


if __name__ == "__main__":
    cli()

