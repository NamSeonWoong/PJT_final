from django.urls import path
from . import views

app_name="movies"

urlpatterns = [
    path('',views.index, name="index"),
    path('<int:id>/',views.detail, name="detail"),
    path('<int:id>/reviews/new/', views.create_review, name="create_review"),
    path('<int:movie_id>/reviews/<int:review_id>/delete/', views.delete_review, name="delete_review"),
    path('<int:id>/like/', views.movie_like, name="movie_like"),
    
]
