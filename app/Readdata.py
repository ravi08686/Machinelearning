
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

file = ''
dataframe = pd.DataFrame
dataset_headers = []






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
            dataframe = pd.read_csv(file)
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

def post2_view(request):
    if request.method == 'POST':
        try:
            selected_fields_x = request.POST.getlist('field_name_x')
            predictor = request.POST.getlist('field_name_y')
            # Process the dataframe or perform any required operations
            # ...
            return render(
                request, 
                'app/index.html',
                {
                    'xfeatures':selected_fields_x,
                    'yfeatures': predictor
                })
        except Exception as e:
            print(e)
        
    return render(request, 'app/index.html')

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


def handle_uploaded_file(uploaded_file):
    file_path = 'path/to/save/file.txt'  # Specify the desired file path
    with open(file_path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_path