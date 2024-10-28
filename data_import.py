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

    movie_cast_response = requests.get(movie_credits_url).json()

    movie_cast = movie_cast_response["cast"]

    for member in movie_cast:
      member["movie_id"] = movie_cast_response["id"]

    movie_credits_list.extend(movie_cast)

    index += 1

  return movie_credits_list

def get_tmdb_movie_reviews(movie_list):
  movie_reviews_list = []

  index = 0
  for movie in movie_list:
    if (index % 50 == 0):
        time.sleep(1)

    movie_id = movie['id']

    movie_reviews_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={tmdb_api_key}"

    movie_review_response = requests.get(movie_reviews_url).json()

    movie_review_results = movie_review_response["results"]

    for review in movie_review_results:
      print(review)
      review["movie_id"] = movie_review_response["id"]

    movie_reviews_list.extend(movie_review_results)

    index += 1

  return movie_reviews_list


if __name__ == "__main__":
  start = 1
  end = 500

  movie_list = get_tmdb_movie_list(page_num=start, max_page_num=end)
  movie_detail_list = get_tmdb_movie_details(movie_list)

  time.sleep(60)

  movie_detail_list_flattened = [flatten(movie) for movie in movie_detail_list]

  movie_df = pd.DataFrame(movie_detail_list_flattened)

  movie_df.to_csv(f"movie_data.csv")

  time.sleep(60)

  movie_credits_list = get_tmdb_movie_credits(movie_list)

  movie_credits_list_flattened = [flatten(movie) for movie in movie_credits_list]

  movie_credits_df = pd.DataFrame(movie_credits_list_flattened)

  movie_credits_df.to_csv(f"movie_credits_data.csv")

  time.sleep(60)

  movie_reviews_list = get_tmdb_movie_reviews(movie_list)

  movie_reviews_list_flattened = [flatten(movie) for movie in movie_reviews_list]

  movie_reviews_df = pd.DataFrame(movie_reviews_list_flattened)

  movie_reviews_df.to_csv(f"movie_reviews_data.csv")

  time.sleep(60)



