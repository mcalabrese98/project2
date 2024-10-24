import requests
from dotenv import load_dotenv
import os
import json
import datetime
import pandas as pd

load_dotenv()

tmdb_api_key = os.getenv("TMDB_API_KEY")

def get_tmdb_movie_list(page_num=None):
  page_num = 1 if page_num == None else page_num
  current_date = datetime.datetime.now().strftime("%Y-%m-%d")
  movie_list = []

  for i in range(page_num, 2):
    movie_list_url = f"https://api.themoviedb.org/3/discover/movie?&api_key={tmdb_api_key}&page={i}&release_date.lte={current_date}"

    movie_list_response = requests.get(movie_list_url).json()

    movie_list.extend(movie_list_response['results'])

    print(f"Page {i} done")

  return movie_list

def get_tmdb_movie_details(movie_list):
  movie_detail_list = []

  for movie in movie_list:
    movie_id = movie['id']
    movie_details = {}

    movie_detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}"

    print(requests.get(movie_detail_url).json())

    result_json = requests.get(movie_detail_url).json()

    movie_detail_list.append(requests.get(movie_detail_url).json())

  print(json.dumps(movie_detail_list[:5], indent=4))
  
  return movie_detail_list

def get_tmdb_movie_credits(movie_list):
  movie_credits_list = []

  for movie in movie_list:
    movie_id = movie['id']

    movie_credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={tmdb_api_key}"

    movie_credits_list.append(requests.get(movie_credits_url).json())

  print(json.dumps(movie_credits_list[:5], indent=4))

  return movie_credits_list


if __name__ == "__main__":
  # movie_list = get_tmdb_movie_list()
  # movie_detail_list = get_tmdb_movie_details(movie_list)

  movie_json = json.load(open('./data.json'))

  movie_df = pd.json_normalize(movie_json, 
          sep='_', # Flatten keys with underscore separator
          meta=['id', 'title', 'imdb_id', 'budget', 'original_language', 'popularity', 'vote_average', 'vote_count', 'revenue', 'runtime', 'adult'], # Extract top-level fields
          record_path=['genres', 'production_companies'], # Flatten nested lists
          record_prefix=['genres_', 'production_companies_'], # Flatten nested field names
          errors='ignore' # Ignore missing values in records
        )
  
  print(movie_df.head())
  movie_df.to_csv("movie_data.csv")