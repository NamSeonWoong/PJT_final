import requests
from decouple import config
from datetime import timedelta, datetime

movie_key = config('MOVIE_KEY')
movie_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'

students=[]
startweek = datetime(2019, 11, 14) #토요일

for k in range(5):
    startweek_str = startweek.strftime("%Y%m%d")
    url = f'{movie_url}?key={movie_key}&targetDt={startweek_str}&movieCd&movieNm&audiCnt&weekGb=0'
    # url = f'{movie_url}?key={movie_key}&movieCd={startweek_str}'
    res = requests.get(url).json()
    # print(res)
    for i in range(10):
        movie_name = res.get('boxOfficeResult').get('weeklyBoxOfficeList')[i].get('movieNm')
    #     movie_people = res.get('boxOfficeResult').get('weeklyBoxOfficeList')[i].get('audiAcc')
    #     students.append({'movieCd' : movie_code, 'movieNm' : movie_name, 'audiAcc' : movie_people})
        students.append({'movieNm': movie_name, })
    print(students)
    startweek = startweek - timedelta(30)

# c = list({asd['movieNm']: asd for asd in students}.values())

# print(students)