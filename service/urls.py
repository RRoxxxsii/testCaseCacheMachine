from django.urls import path

from . import views

urlpatterns = [
    path('cach_machine/', views.CreateCheckPDF.as_view(), name='cach_machine')
]
