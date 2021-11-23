from django.urls import path

from . import views

urlpatterns = [
    path('connection-test/', views.connection_test, name='connection-test'),
    path('get-ws-token/', views.GetWSToken.as_view(), name='get-ws-token')
]
