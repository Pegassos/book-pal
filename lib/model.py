import pickle
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

import books_data

book_pivot, books_isbn_list, books = books_data.get_data()

book_sparse = csr_matrix(book_pivot)

model = NearestNeighbors(n_neighbors= 10, algorithm = "brute")
model.fit(book_sparse)


# Save the trained model ---------------------
pickle_model = open('lib/pickle_model', 'wb')
pickle.dump(model, pickle_model)
pickle_model.close()

# Save the data ---------------------
pickle_data = open('lib/pickle_data', 'wb')
pickle.dump([book_pivot, books_isbn_list, books], pickle_data)
pickle_data.close()
