import requests
from dotenv import load_dotenv
import os
import json
import time
import datetime
import pandas as pd
from flatten_json import flatten

load_dotenv()

tmdb_api_key = os.getenv("TMDB_API_KEY")

def get_tmdb_movie_list(page_num=None, max_page_num=1):
  page_num = 1 if page_num == None else page_num
  current_date = datetime.datetime.now().strftime("%Y-%m-%d")
  movie_list = []

  for i in range(page_num, max_page_num):
    if (i % 50 == 0):
        time.sleep(1)

    movie_list_url = f"https://api.themoviedb.org/3/discover/movie?&api_key={tmdb_api_key}&page={i}&release_date.lte={current_date}"

    movie_list_response = requests.get(movie_list_url).json()

    movie_list.extend(movie_list_response['results'])

    print(f"Page {i} done")

  return movie_list

def get_tmdb_movie_details(movie_list):
  movie_detail_list = []

  index = 0
  for movie in movie_list:
    if (index % 50 == 0):
        time.sleep(1)

    movie_id = movie['id']
    movie_details = {}

    movie_detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}"

    print(requests.get(movie_detail_url).json())

    result_json = requests.get(movie_detail_url).json()

    movie_detail_list.append(requests.get(movie_detail_url).json())

    index += 1
  
  return movie_detail_list

def get_tmdb_movie_credits(movie_list):
  movie_credits_list = []

  index = 0
  for movie in movie_list:
    if (index % 50 == 0):
        time.sleep(1)

    movie_id = movie['id']

    movie_credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={tmdb_api_key}"

    movie_credits_list.append(requests.get(movie_credits_url).json())

    index += 1

  return movie_credits_list


if __name__ == "__main__":
  movie_list = get_tmdb_movie_list(max_page_num=50)
  # movie_detail_list = get_tmdb_movie_details(movie_list)

  # movie_detail_list_flattened = [flatten(movie) for movie in movie_detail_list]

  # movie_df = pd.DataFrame(movie_detail_list_flattened)

  # columns_to_remove = ['belongs_to_collection_id', 'belongs_to_collection_name', 'belongs_to_collection_poster_path', 'belongs_to_collection_backdrop_path', 'genres_0_id', 'genres_1_id', 'genres_2_id', 'genres_3_id', 'genres_4_id', 'spoken_languages_0_name']

  # movie_df.drop(columns=columns_to_remove, inplace=True)

  # movie_df = movie_df[sorted(movie_df.columns)]

  # movie_df.to_csv("movie_data.csv")

  movie_credits_list = get_tmdb_movie_credits(movie_list)

  movie_credits_list_flattened = [flatten(movie) for movie in movie_credits_list]

  movie_credits_df = pd.DataFrame(movie_credits_list_flattened)

  movie_credits_df.to_csv("movie_credits_data.csv")