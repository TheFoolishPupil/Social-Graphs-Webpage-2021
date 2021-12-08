import pandas as pd
import pickle


with open("data/movie_network", "rb") as f:
    FILM_NETWORK = pickle.load(f)

with open("data/movie_network_community", "rb") as f:
    FILM_NETWORK_COMMUNITY = pickle.load(f)

with open("data/actor_network", "rb") as f:
    ACTOR_NETWORK = pickle.load(f)

FILM_DATA = pd.read_csv("data/dataset.csv").iloc[:, 1:]

GENRE_TF_IDF_DATA = pd.read_csv("data/genres_tf_idf.csv").iloc[:, 1:]

BOX_OFFICE_GROUPS = [
    "very low box office",
    "low box office",
    "medium box office",
    "high box office",
    "very high box office",
]
