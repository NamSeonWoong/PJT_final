from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
import requests
from decouple import config
from datetime import timedelta, datetime
import requests                  
import datetime					
import json
import os
import sys
import urllib.request

def start(request):
    now = datetime.datetime.now()
    nowdate = now.strftime('%Y')
    movie_key = config('MOVIE_KEY')
    movie_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json"
    # last_week = (now + (datetime.timedelta(weeks=-1))).strftime('%Y%m%d')
    my_url = f'{movie_url}?key={movie_key}&itemPerPage=5&openStartDt={nowdate}&openEndDt={nowdate}'
    res = requests.get(my_url).json()

    result = {}
    boxoffice = []

    client_id= config('NAVER_ID')
    client_secret= config('NAVER_SECRET')

    movieNm = res.get('movieListResult').get('movieList') 
    # print(movieNm)
    for i in movieNm:
        # print('==========================================')
        # print(i)
        encText = urllib.parse.quote(i["movieNm"])
        movie_url = "https://openapi.naver.com/v1/search/movie?query=" + encText
        request = urllib.request.Request(movie_url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        if(rescode==200):
            response_body = response.read()
            temp = response_body.decode('utf-8')
            
            js = json.loads(temp)
            # print('##################################################')
            # print(js)
            if js["items"]:
                img_url = js["items"][0]["image"]
                director = js["items"][0]["director"]
                cast = js["items"][0]["actor"]
            else:
                continue
            # print(img_url)
        else:
            # print("Error Code:" + rescode)
            pass
        
        result[i['movieCd']]= {
                                'movieNm': i['movieNm'],
                                'repGenreNm': i['repGenreNm'],
                                'openDt': i['openDt'],
                                'img_url': img_url,
                                'director': director[:],
                                'cast': cast,
                            }
        print(result)
    # 위에 for문에서 저장한 result값을 빈리스트에 .append 한다.
    idx = 1
    for i in result:
        # boxoffice.append({
    #         'model': 'movies.Movie',
    #         'pk': idx,
    #         'fields': {
    #             'movieCd': i,
    #             'title': result[i]['movieNm'],0000


    #             'genre': result[i]['repGenreNm'],
    #             'pubdate': result[i]['openDt'],
    #             'poster_url': result[i]['img_url'],
    #             'director': result[i]['director'],
    #             'cast': result[i]['cast'],
    #                 }
    #         })
    #     idx += 1
        # Genre.objects.create(
        #     name = result[i]['repGenreNm']
        # )
        Movie.objects.create(
            title = result[i]['movieNm'],
            pubdate = result[i]['openDt'],
            poster_url = result[i]['img_url'],
            director = result[i]['director'],
            cast = result[i]['cast'],
            genre = result[i]['repGenreNm']
        )
    # with open('boxoffice.json', 'w', newline='', encoding='utf-8') as f:
    #     json.dump(boxoffice, f, ensure_ascii=False, indent="\t")
    return redirect('movies:index')
##############################################################################################
# title, audience, poster_url, genre, rating


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
    