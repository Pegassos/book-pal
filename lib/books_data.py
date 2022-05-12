import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

def get_data():
  #Reading the excel sheets into a dataframe
  books = pd.read_csv("data/BX-Books.csv", sep = ";", encoding = "latin-1",  on_bad_lines='skip', low_memory=False)
  users = pd.read_csv("data/BX-Users.csv", sep = ";", encoding = "latin-1",  on_bad_lines='skip')
  ratings = pd.read_csv("data/BX-Book-Ratings.csv", sep = ";", encoding = "latin-1",  on_bad_lines='skip')

  #Extracting only the columns that we'll need 
  books = books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher']]

  #Renaming the columns to make them easy to use
  books.rename(columns = {'Book-Title':'title', 'Book-Author':'author', 'Year-Of-Publication':'year', 'Publisher':'publisher'}, inplace=True)
  users.rename(columns = {'User-ID':'user_id', 'Location':'location', 'Age':'age'}, inplace=True)
  ratings.rename(columns = {'User-ID':'user_id', 'Book-Rating':'rating'}, inplace=True)   

  #Extracting the users with at least 200 ratings
  x = ratings['user_id'].value_counts() > 200
  y = x[x].index  #899 users are included in our model
  
  #Reducing the ratings set to the preselected users
  ratings = ratings[ratings['user_id'].isin(y)]

  rating_with_books = ratings.merge(books, on='ISBN')

  number_rating = rating_with_books.groupby('title')['rating'].count().reset_index()
  number_rating.rename(columns= {'rating':'number_of_ratings'}, inplace=True)
  #Merging everything
  final_rating = rating_with_books.merge(number_rating, on='title')
  final_rating = final_rating[final_rating['number_of_ratings'] >= 50]
  final_rating.drop_duplicates(['user_id','title'], inplace=True)

  # Create pivot table
  book_pivot = final_rating.pivot_table(columns='user_id', index='ISBN', values="rating")
  book_pivot.fillna(0, inplace=True)

  BOOKS_ISBN_LIST = book_pivot.index.tolist()

  return book_pivot, BOOKS_ISBN_LIST, books

