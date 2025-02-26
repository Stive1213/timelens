from django.urls import path
from . import views

urlpatterns = [
    path('', views.timeline, name='timeline'),
    path('create/', views.create_entry, name='create_entry'),
    path('share/<int:entry_id>/', views.share_entry, name='share_entry'),
    path('shared/<uuid:token>/', views.view_shared_entry, name='view_shared_entry'),
    path('insights/', views.insights, name='insights'),
]