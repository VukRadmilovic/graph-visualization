from django.urls import path

from . import views

urlpatterns = [
    path('books/<str:arg>', views.books, name='books'),
    path('items/<str:arg>', views.items, name='items'),
    path('books/', views.books, name='books'),
    path('items/', views.items, name='items'),
    path('simple/', views.simple, name='simple'),
    path('complex/', views.complex, name='complex'),
    path('simple/<str:arg>', views.simple, name='simple'),
    path('complex/<str:arg>', views.complex, name='complex'),
    path('', views.books, name="index"),
]