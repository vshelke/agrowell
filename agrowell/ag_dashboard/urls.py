from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/<plant>/<date>/', views.api, name='api')
]
