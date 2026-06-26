from django.urls import path
from . import views

urlpatterns = [
    path('singleobj/<int:pk>/', views.singleObjAPIView.as_view()),
    path('multipleobj', views.multipleObjAPIView.as_view())
]