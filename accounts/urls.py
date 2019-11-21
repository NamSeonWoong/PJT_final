from django.urls import path
from . import views

app_name="accounts"

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('', views.index, name="index"),
    path('<int:id>/', views.detail, name="detail"),
    path('<int:id>/follow/', views.follow, name="follow"),
]