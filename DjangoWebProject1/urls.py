"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import Readdata, forms, views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    #path('', Readdata.upload_file, name='upload_file'),
    path('contact/', views.contact, name='contact'),
    #path('upload/', Readdata.upload, name='about'),
    path('post1/', views.post1_view, name='post1'),
    path('method2', Readdata.post2_view, name='post2_view'),
    path('method1', Readdata.upload_file, name='upload_file'),
    path('fields_selection/', Readdata.fields_selection, name='fields_selection'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
