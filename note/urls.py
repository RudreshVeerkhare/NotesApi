from django.urls import path, include
from . import views

urlpatterns = [
    # Showing all Notes in ListView
    path('sites/list/', views.notes_list),
    # Creating New Note
    path('sites/', views.create_note),
    # User login
    path('user/auth/', views.user_login),
    # User Creation
    path('user/', views.user_register)
]