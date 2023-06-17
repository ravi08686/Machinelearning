"""
Definition of views.
"""

from datetime import datetime
from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpRequest

from app.Readdata import DatasetForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action=='method1':
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
        if action=='method2':
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
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


def form1_submit(request):
    
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

def form2_submit(request):
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

def post1_view(request):
    if request.method == 'POST':
        my_file = request.FILES['my_file']  # Get the uploaded file
        file_path = handle_uploaded_file(my_file)  # Process the file
        
        # Additional code to perform further operations with the file_path
        
        return HTTPResponse('File uploaded successfully.')
    else:
        # Render the upload form
        return render(request, 'upload.html')


def handle_uploaded_file(uploaded_file):
    file_path = 'path/to/save/file.txt'  # Specify the desired file path
    with open(file_path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_path

def upload2(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/upload.html',
        {
            'title':'Upload page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
