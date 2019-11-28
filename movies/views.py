from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from decouple import config
from datetime import timedelta, datetime
import requests, datetime, json, os, sys
import urllib.request
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
from django.core.paginator import Paginator

# 영진위api 관련
movie_key = config('MOVIE_KEY')
movie_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
movie_detail = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'

# 네이버api 관련
naver_url = 'https://openapi.naver.com/v1/search/movie.json'
naver_id= config('NAVER_ID')
naver_secret = config('NAVER_SECRET')
headers = {
    'X-Naver-Client-Id' : naver_id,
    'X-Naver-Client-Secret' : naver_secret
}

# movies=[]
# Cd = []
# def start(request):
#     startweek = datetime(2019, 11, 16)
#     for k in range(20):
#         # 영진위 주간 api요청
#         startweek_str = startweek.strftime("%Y%m%d")
#         url = f'{movie_url}?key={movie_key}&targetDt={startweek_str}&movieCd&movieNm&audiCnt&weekGb=0'
#         res = requests.get(url).json()
#         for i in range(10):
#             # 주간 정보들 1~10위까지
#             movie_Cd = res.get('boxOfficeResult').get('weeklyBoxOfficeList')[i].get('movieCd')
#             if not movie_Cd in Cd:
#                 Cd.append(movie_Cd)
#                 movie_audiAcc = res.get('boxOfficeResult').get('weeklyBoxOfficeList')[i].get('audiAcc')
#                 movie_Nm = res.get('boxOfficeResult').get('weeklyBoxOfficeList')[i].get('movieNm')
#                 movie_Dt = res.get('boxOfficeResult').get('weeklyBoxOfficeList')[i].get('openDt')

#                 # 영진위 상세정보 api요청
#                 detailurl = f'{movie_detail}?key={movie_key}&movieCd={movie_Cd}'
#                 res_detail = requests.get(detailurl).json()
#                 movie_genre = res_detail.get('movieInfoResult').get('movieInfo').get('genres')[0].get('genreNm')

#                 # 네이버 api요청
#                 naver_data = f'{naver_url}?query={movie_Nm}'
#                 res_naver = requests.get(naver_data, headers = headers).json()

#                 if res_naver.get('items'):
#                     movie_cast = res_naver.get('items')[0].get('actor').split('|')
#                     movie_directors = res_naver.get('items')[0].get('director').split('|')
#                     img_url_code = res_naver.get("items")[0].get("link")[51:]
#                     img_url = f'https://movie.naver.com/movie/bi/mi/basic.nhn?code={img_url_code}'
#                     resp = requests.get(img_url)
#                     soup = BeautifulSoup(resp.content, 'html.parser')
#                     img = soup.select('#content > div.article > div.mv_info_area > div.poster > a > img')
#                     movie_img = img[0].get('src')
 
#                     # 영화정보 추가
#                     movies.append([movie_Cd,movie_Nm,movie_genre,movie_Dt,movie_directors,movie_cast,movie_img,movie_audiAcc])
#         # 날짜 변경
#         startweek = startweek - timedelta(7)
#     # 누적 관객수에 따른 내림차순 정렬
#     movies.sort(key=lambda x:int(x[-1]), reverse=True)

#     for i in range(len(movies)):
#         Movie.objects.create(
#             title = movies[i][1],
#             pubdate = movies[i][3],
#             poster_url = movies[i][6],
#             director = movies[i][4],
#             cast = movies[i][5],
#             genre = movies[i][2],
#             audience = movies[i][-1]
#         )
#     return redirect('movies:index')


def index(request):
    res = []
    movies = Movie.objects.all()
    paginator = Paginator(movies, 9) 
    page = request.GET.get('page')
    movies = paginator.get_page(page)
    for movie in Movie.objects.all():
        res.append([movie.title,movie.like_users.count(),movie.id])

    res.sort(key=lambda x:x[1], reverse=True)
    first = {'title': res[0][0], 'id': res[0][2]}
    second = {'title': res[1][0], 'id': res[1][2]}
    third = {'title': res[2][0], 'id': res[2][2]}
    context = {
        'movies': movies,
        'first': first,
        'second': second,
        'third': third
    }
    return render(request, 'movies/index.html', context)

def detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    form = ReviewForm()
    context = {
        'movie': movie,
        'form': form,
        'update':0,
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
def update_review(request,movie_id,review_id):
    movie = get_object_or_404(Movie, id=movie_id)
    review = get_object_or_404(Review, id=review_id)
    if request.user ==review.user:
        if request.method == "POST":
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save()
            return redirect('movies:detail',movie_id)
        else:
            form = ReviewForm(instance=review)
        context={
            'movie':movie,
            'form':form,
            'review':review,
            'update':1,
        }
        return render(request,'movies/detail.html',context)
    else:
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

def search(request):
    res = []
    if request.method == 'POST':
        keyword = request.POST.get("keyword")
        option = request.POST.get("target")
        if option == "title":
            movies = Movie.objects.filter(title__icontains=keyword)
        else:
            movies = Movie.objects.filter(genre__icontains=keyword)
        paginator = Paginator(movies, 9) 
        page = request.GET.get('page')
        movies = paginator.get_page(page)

        for movie in Movie.objects.all():
            res.append([movie.title,movie.like_users.count(),movie.id])

        res.sort(key=lambda x:x[1], reverse=True)
        first = {'title': res[0][0], 'id': res[0][2]}
        second = {'title': res[1][0], 'id': res[1][2]}
        third = {'title': res[2][0], 'id': res[2][2]}

        context = {
            'movies': movies,
            'first': first,
            'second': second,
            'third': third
        }
        return render(request, 'movies/search.html', context)
    else:
        movies = Movie.objects.all()
        paginator = Paginator(movies, 9) 
        page = request.GET.get('page')
        movies = paginator.get_page(page)
        for movie in Movie.objects.all():
            res.append([movie.title,movie.like_users.count(),movie.id])

        res.sort(key=lambda x:x[1], reverse=True)
        first = {'title': res[0][0], 'id': res[0][2]}
        second = {'title': res[1][0], 'id': res[1][2]}
        third = {'title': res[2][0], 'id': res[2][2]}
        
        context = {
            'movies': movies,
            'first': first,
            'second': second,
            'third': third
        }
        return render(request, 'movies/search.html',context)
    