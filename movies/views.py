from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'movies/index.html', context)

def detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    form = ReviewForm()
    context = {
        'movie': movie,
        'form': form,
    }
    return render(request, 'movies/detail.html', context)

@login_required    
def create_review(request, id):
    movie = get_object_or_404(Movie, id=id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('movies:detail', id)
        return redirect('movies:index')

@login_required
def delete_review(request,movie_id,review_id):
    if request.method == "POST":
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.user:
            review.delete()
    return redirect('movies:detail', movie_id)

@login_required
def movie_like(request, id):
    if request.method == "POST":
        movie = get_object_or_404(Movie, id=id)
        user = request.user
        if user in movie.like_users.all():
            movie.like_users.remove(user)
        else:
            movie.like_users.add(user)
        
        return redirect('movies:detail', id)
    