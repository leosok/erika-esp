from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('page/<str:hashid>/content/', views.page_content, name='page_content'),
]
