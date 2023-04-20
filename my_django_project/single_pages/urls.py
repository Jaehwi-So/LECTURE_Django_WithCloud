from django.urls import path
from . import views


urlpatterns = [
    path('', views.lender),
    path('about_me/', views.about_me)
]