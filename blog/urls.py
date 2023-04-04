# urlconf for blog
from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),  #Class Base View(CBV)
    path('category/<str:slug>/', views.categories_page), #Function Base View(FBV)
    path('tag/<str:slug>/', views.tag_page),  # Function Base View(FBV)
]