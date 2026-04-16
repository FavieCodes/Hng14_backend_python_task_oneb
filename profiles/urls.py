from django.urls import path
from . import views

urlpatterns = [
    path('profiles', views.profile_list_create, name='profile-list-create'),
    path('profiles/<str:profile_id>', views.profile_detail_delete, name='profile-detail-delete'),
]