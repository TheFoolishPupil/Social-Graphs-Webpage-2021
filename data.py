import pandas as pd
import networkx as nx


def build_network():
    G = nx.Graph()
    for movie in FILM_DATA.T.iteritems():
        G.add_node(movie[1]["title"])
    return G


FILM_DATA = pd.read_csv("dataset.csv").iloc[:, 1:]
FILM_NETWORK = build_network()
