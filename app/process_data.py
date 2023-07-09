# This is for processing the data and call appropriate model for analysis


from ast import List
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
import numpy as np
import pandas as pd
import os
from django.shortcuts import HttpResponse
from django.utils.html import strip_tags
from django import forms
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score,mean_absolute_error
from sklearn.preprocessing import StandardScaler


from app.Readdata import DatasetForm, corelation, pre_processing

def processdata(request):
    if request.method == 'POST':
        try:
            selected_fields_x = request.session['selected_fields_x']
            predictor = request.session['predictor']
            file = request.session['file_pa']        
            final_file = request.session['file_pa_final']  

            dataframe = pd.read_csv(file)
            final_dataframe = pd.read_csv(final_file)
            corelation_plot = corelation(final_dataframe)
            dataset_headers = dataframe.columns.tolist() 
            form = DatasetForm(dataset_headers=dataset_headers)

            dataset_headers2 = final_dataframe.columns.tolist() 
            form2 = DatasetForm(dataset_headers=dataset_headers2)

            X=final_dataframe.drop(predictor,axis=1)
            y=final_dataframe[predictor]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
            sc = StandardScaler()
            X_train = sc.fit_transform(X_train)
            X_test = sc.transform(X_test)

            selected_models = request.POST.getlist('models_selection')
            for model in selected_models:
                if model == "Linear_Regression":
                    mae,r2=Linear_Regression(X_train, X_test, y_train, y_test)
                    Models_Result =  "<b><u>Linear regression resuls:</u></b> <br/>Mean Absolute Error:" + str(mae) + " & " + "<br/>R-squared Score:" + str(r2)
                if model == "Logistic_Regression":
                    Accuracy_score =Logistic_Regression(X_train, X_test, y_train, y_test)
                    Models_Result = Models_Result + "<br/><br/> <b><u>Logistic regression results:</u></b> <br/>Accuracy score:" + str(Accuracy_score)
                if model == "Decision_Trees":
                    Accuracy_score =Decision_Trees(X_train, X_test, y_train, y_test)
                    Models_Result = Models_Result + "<br/><br/> <b><u>Decision Tree results:</u></b> <br/>Accuracy score:" + str(Accuracy_score)
                if model == "SVM":
                    Accuracy_score =SVM(X_train, X_test, y_train, y_test)
                    Models_Result = Models_Result + "<br/><br/> <b><u>Support Vector Machine Algorithm results:</u></b> <br/>Accuracy score:" + str(Accuracy_score)

            # Process the dataframe or perform any required operations
            # ...
            return render(
                request, 
                'app/index.html',
                {
                    'datatitle':'Uploaded data',
                    'dataitems': dataframe.to_html(),
                    'xfeatures': selected_fields_x,
                    'yfeatures': predictor,
                    'dataitems_final': final_dataframe.to_html(),
                    'form': form,
                    'form2': form2,
                    'corel_plot': corelation_plot,
                    'selected_models': selected_models,
                    'Results': Models_Result,
                })
        except Exception as e:
            print(e)
        
    return render(request, 'app/index.html')

def Linear_Regression(X_train, X_test, y_train, y_test):
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mae,r2
 
def Logistic_Regression(X_train, X_test, y_train, y_test):
    from sklearn.linear_model import LogisticRegression  
    from sklearn.metrics import accuracy_score  
    classifier= LogisticRegression(random_state=42)  
    classifier.fit(X_train, y_train)  

    y_pred= classifier.predict(X_test) 

    accuracy= accuracy_score(y_test,y_pred) 

    return accuracy 

def Decision_Trees(X_train, X_test, y_train, y_test): 
    #Fitting Decision Tree classifier to the training set  
    from sklearn.tree import DecisionTreeClassifier 
    from sklearn.metrics import accuracy_score  
    classifier= DecisionTreeClassifier(criterion='entropy', random_state=42)  
    classifier.fit(X_train, y_train)  

    #Predicting the test set result  
    y_pred= classifier.predict(X_test)  

    accuracy= accuracy_score(y_test,y_pred) 

    return accuracy

def SVM(X_train, X_test, y_train, y_test): 
    #Fitting Decision Tree classifier to the training set  
    from sklearn.tree import DecisionTreeClassifier 
    from sklearn.metrics import accuracy_score  
    from sklearn.svm import SVC # "Support vector classifier"  
    classifier = SVC(kernel='linear', random_state=0)  
    classifier.fit(X_train, y_train) 
    
    #Predicting the test set result  
    y_pred= classifier.predict(X_test)  

    accuracy= accuracy_score(y_test,y_pred) 

    return accuracy