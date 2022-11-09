#!/usr/bin/env python3

from src.dataMovies import search_movie_reviews_df
from src.dataMovies import search_movies_reviews_df
from src.dataMovies import search_movie_users_ratings_df
from src.dataMovies import search_movies_users_ratings_df

# print(search_movie_reviews_df('k_12345678','spiderman far from home').tail())
# print(search_movie_reviews_df('k_0dyi34y8','spiderman far from home').tail())

# print(search_movie_users_ratings_df('k_12345678', 'inception', stat='demographicFemales'))
# print(search_movie_users_ratings_df('k_0dyi34y8', 'inception', stat='demographicFemales'))

moviesExpressions = ['Inception', 'spiderman far from home']
print(search_movies_reviews_df('k_0dyi34y8', moviesExpressions))
print(search_movies_users_ratings_df('k_0dyi34y8', moviesExpressions))
