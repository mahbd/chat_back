from django.urls import path

from . import views

urlpatterns = [
    path('connection-test/', views.connection_test, name='connection-test'),
]
