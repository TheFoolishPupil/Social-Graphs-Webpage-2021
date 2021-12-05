import pandas as pd
import pickle


with open("data/movie_network", "rb") as f:
    FILM_NETWORK = pickle.load(f)

with open("data/movie_network_community", "rb") as f:
    FILM_NETWORK_COMMUNITY = pickle.load(f)

FILM_DATA = pd.read_csv("data/dataset.csv").iloc[:, 1:]
