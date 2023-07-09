
from ast import List
import base64
from datetime import datetime
import io
from django.shortcuts import render
from django.http import HttpRequest
import numpy as np
import pandas as pd
import os
from django.shortcuts import HttpResponse
from django.utils.html import strip_tags
from django import forms
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile



# Read the given CSV file, and view some sample records

class DatasetForm(forms.Form):
    def __init__(self, *args, **kwargs):
        dataset_headers = kwargs.pop('dataset_headers')
        super(DatasetForm, self).__init__(*args, **kwargs)
        
        for header in dataset_headers:
            field_name = 'field_{}'.format(header)
            self.fields[field_name] = forms.BooleanField(label=header)

def upload_file(request):
    
    if request.method == 'POST':
        try:
            file = request.FILES['file']

            csv_file = request.FILES['file']

            dataframe = pd.read_csv(csv_file)
        
            # Define the directory to save the CSV file
            save_directory = '/path/to/save/'
        
            # Create the save directory if it doesn't exist
            os.makedirs(save_directory, exist_ok=True)
        
            # Construct the file path to save the CSV file
            file_path = os.path.join(save_directory, csv_file.name)
                        
            file_path = handle_uploaded_file(file,file_path)            
            request.session['file_pa'] = file_path
            dataset_headers = dataframe.columns.tolist() 
            form = DatasetForm(dataset_headers=dataset_headers)

            # Process the dataframe or perform any required operations
            # ...
            return render(
                request, 
                'app/index.html',
                {
                    'datatitle':'Uploaded data',
                    'dataitems': dataframe.to_html(),
                    'form': form
                })
        except Exception as e:
            print(e)
        
    return render(request, 'app/index.html')

def features_sel(request):
    if request.method == 'POST':
        try:
            file = request.session['file_pa']
            dataframe = pd.read_csv(file)
            dataset_headers = dataframe.columns.tolist() 
            form = DatasetForm(dataset_headers=dataset_headers)

            final_fields = request.POST.getlist('field_names')
            #request.session['final_fields'] = final_fields            
            
            final_dataframe = pre_processing_fetures(dataframe,final_fields)            
            corelation_plot = corelation(final_dataframe)
            
            dataset_headers2 = final_dataframe.columns.tolist() 
            form2 = DatasetForm(dataset_headers=dataset_headers2)
            current_path = os. getcwd()
            completePath = os.path.join(current_path, 'data/')
            isExist = os.path.exists(completePath)
            if not isExist:
               # Create a new directory because it does not exist
               os.makedirs(completePath)

            completeName = os.path.join(current_path, 'file1_final.csv')

            final_dataframe.to_csv(completeName,index=False) 

            request.session['file_pa_final'] = completeName
            # Process the dataframe or perform any required operations
            # ...
            return render(
                request, 
                'app/index.html',
                {
                    'datatitle':'Uploaded data',
                    'dataitems': dataframe.to_html(),
                    'dataitems_final': final_dataframe.to_html(),
                    'corel_plot': corelation_plot,
                    'form': form,
                    'form2': form2
                })
        except Exception as e:
            print(e)        
    return render(request, 'app/index.html')

def post2_view(request):
    if request.method == 'POST':
        try:
            selected_fields_x = request.POST.getlist('field_name_x')
            predictor = request.POST.getlist('field_name_y')
            request.session['selected_fields_x'] = selected_fields_x
            request.session['predictor'] = predictor
            file = request.session['file_pa']

            dataframe = pd.read_csv(file)
            dataset_headers = dataframe.columns.tolist() 
            form = DatasetForm(dataset_headers=dataset_headers)

            final_file = request.session['file_pa_final']
            final_dataframe = pd.read_csv(final_file)
            
            corelation_plot = corelation(final_dataframe)

            dataset_headers2 = final_dataframe.columns.tolist() 
            form2 = DatasetForm(dataset_headers=dataset_headers2)

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
                    'corel_plot': corelation_plot,
                    'form': form,
                    'form2': form2
                })
        except Exception as e:
            print(e)
        
    return render(request, 'app/index.html')



def corelation(new_dataframe):
    comumns_count = len(new_dataframe. columns)
    if (comumns_count<11):
        cm=new_dataframe.corr()
        fig,ax = plt.subplots(figsize=(15,15))
        ax=sns.heatmap(cm,annot=True)
        temp_dir = tempfile.mkdtemp()
        temp_image_path = os.path.join(temp_dir, 'my_image.png')    
        plt.savefig(temp_image_path)
        figfile = io.BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)
        figdata_png = base64.b64encode(figfile.getvalue())
        encoded_plot = base64.b64encode(figdata_png).decode('utf-8')
        result = str(figdata_png)[2:-1]    
    else:
        result = ""
    return result

def fields_selection(request):
    
    if request.method == 'POST':
        try:
            
            # Process the dataframe or perform any required operations
            # ...
            return render(
                request, 
                'app/index.html',
                {
                    'xfeatures':'xfeatures',
                    'yfeature': 'yfeature'
                })
        except Exception as e:
            print(e)
        
    return render(request, 'app/index.html')


def handle_uploaded_file(uploaded_file,file_path):
    with open(file_path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_path


def pre_processing_fetures(dataframe,selected_fields):
    new_columns = selected_fields
    new_dataframe = dataframe[new_columns]
    new_dataframe = new_dataframe.dropna() #or fillna
    new_dataframe = pd.get_dummies(new_dataframe, drop_first=True)
    return new_dataframe

def pre_processing(dataframe,selected_fields_x,predictor):
    new_columns = selected_fields_x + predictor
    new_dataframe = dataframe[new_columns]
    new_dataframe = new_dataframe.dropna() #or fillna
    new_dataframe = pd.get_dummies(new_dataframe, drop_first=True)
    return new_dataframe