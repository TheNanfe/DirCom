from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_persons, name='person_list'),
    path('<str:pk>', views.person_details, name='person_details'),
    path('create/', views.create_person, name='create_person')
]