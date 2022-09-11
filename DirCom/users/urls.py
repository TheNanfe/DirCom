from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_users, name='user_list'),
    path('<int:pk>', views.get_user, name='user_details'),
    path('create/', views.create_user, name='create_user'),
    path('delete/<int:pk>', views.delete_user, name='delete_user'),
]