from django.shortcuts import render,redirect
from html.parser import HTMLParser
import requests
import random

from django.conf import settings

def get_movie_response(movie, year):
    
     url = "https://api.themoviedb.org/3/search/movie?api_key={}&language=en-US&query={}&page=1&include_adult=false&year={}".format(settings.TMDB_API_KEY,movie,year)
     response = requests.get(url)
     return response

def get_movie_overview(similar_movie_ids):
    movie_overviews = []
    for movie_id in similar_movie_ids:
           url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id,settings.TMDB_API_KEY)
           response = requests.get(url)
           overview = response.json()['overview']
           movie_overviews.append(overview)
    return movie_overviews


 #by entering the name and the year the movieID can be retrieved
 #only the movieId CAN BE USED TO RETRIEVE all the nessasary data 
def get_movie_id(movie,year):
   movie_id =  get_movie_response(movie,year).json()['results'][0]['id']
   return movie_id


def similar_movies_data(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}/recommendations?api_key={}&language=en-US&page=1".format(
    movie_id,settings.TMDB_API_KEY)
    response = requests.get(url)
    data = response.json()
    return data

def youtube_keys(similar_movie_ids):
    youtube_keys = []
    for movie_id in similar_movie_ids:
      url = "https://api.themoviedb.org/3/movie/{}/videos?api_key={}&language=en-US".format(movie_id,settings.TMDB_API_KEY)
      response = requests.get(url)
      data = response.json()["results"]
      for result in data:
         if result['type']=="Trailer":
            youtube_keys.append(result['key'])
            break
    return youtube_keys

def get_posters(similar_movie_ids):
    poster_paths = []
    for movie_id in similar_movie_ids:
        url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id,settings.TMDB_API_KEY)
        response = requests.get(url)
        data = response.json()['poster_path']
        poster_paths.append("https://image.tmdb.org/t/p/original"+data)
    return poster_paths
        

#not all the movies have trailers so this method only returns the movieID with trailers
def updated_movie_ids(similar_movie_ids):
    upadated_movie_ids = []
    for movie_id in similar_movie_ids:
      url = "https://api.themoviedb.org/3/movie/{}/videos?api_key={}&language=en-US".format(movie_id,settings.TMDB_API_KEY)
      response = requests.get(url)
      data = response.json()["results"]
      for result in data:
         if result['type']=="Trailer":
            upadated_movie_ids.append(movie_id)
            break
    return upadated_movie_ids






def get_youtube_video_data(video_keys):
    video_ids = ','.join(video_keys)
    get_videos_url =  "https://www.googleapis.com/youtube/v3/videos"
    params = {
    'part' :'snippet',
    'id':video_ids,
    'key': settings.YOUTUBE_DATA_API_KEY
    }
    r =requests.get(get_videos_url, params=params)
    data = r.json()['items']
    return data

#main method 
def index(request):
    similar_movie_ids = []
    movie_json_data = []
    context = ""

    try:
      if request.method == 'POST':
        #user inputs movie and data  of similar movies is returned 
          
        user_input = request.POST['searchbar'].split()
        movie = ' '.join(user_input[:-1])
        year = int(user_input[-1])
        movie_id = get_movie_id(movie,year)
        data = similar_movies_data(movie_id)


         #retrieving the id of the simialr movies and the oveview
        for result in data['results']:
           similar_movie_ids.append(result['id'])
        
        #updating the ids
        similar_movie_ids = updated_movie_ids(similar_movie_ids)
        #the movie id's can me used to retrieve the youtube video keys
        movie_youtube_keys = youtube_keys(similar_movie_ids)
        #gettting overviews and posters of the siilar movies
        movie_overviews = get_movie_overview(similar_movie_ids)
        poster_path = get_posters(similar_movie_ids)
        #retrieving the youtube data
        youtube_trailer_data = get_youtube_video_data(movie_youtube_keys)
        
        if request.POST['submit']=='lucky':
            return redirect("https://www.youtube.com/watch?v="+youtube_trailer_data[random.choice(range(len(youtube_trailer_data)))]['id'])

       

         
          #looping through the youtube data and getting the relevant information which will be used on the index.html
        for i in range(len(youtube_trailer_data)):
            video_data = {
            'title':youtube_trailer_data[i]['snippet']['title'],
            'id':youtube_trailer_data[i]['id'],
            'thumbnail': youtube_trailer_data[i]['snippet']['thumbnails']['high']['url'],
            'overview': movie_overviews[i],
            'poster_path': poster_path[i],
            'url':"https://www.youtube.com/watch?v="+youtube_trailer_data[i]['id']
            
            }  
            movie_json_data.append(video_data)

            context = {
             'movies': movie_json_data
           }
      return render(request, 'search_app/index.html',context)
    except Exception as err:
      return render(request, 'search_app/index.html')

