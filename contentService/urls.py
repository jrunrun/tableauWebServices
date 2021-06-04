from django.urls import path
from django.conf.urls import url
from . import views
# from authService.views import GetTicket

urlpatterns = [
    path('', views.index, name='index'),
    # url(r'^ticket/api/', GetTicket.as_view()),
]