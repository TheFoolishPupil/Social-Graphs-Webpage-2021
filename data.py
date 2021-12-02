import pandas as pd
import networkx as nx
import math
import plotly.figure_factory as ff


def build_network():
    G = nx.Graph()
    for movie in FILM_DATA.T.iteritems():
        G.add_node(movie[1]["title"])
    return G


def box_office_histogram(bin_size):
    hist_data = [
        [
            int(float(x))
            for x in list(FILM_DATA.box_office)
            if x != "None" and not math.isnan(float(x))
        ]
    ]  # TODO: Data should be processed before this point
    labels = ["Box Office Revenue"]
    return ff.create_distplot(hist_data, labels, [bin_size])


FILM_DATA = pd.read_csv("dataset.csv").iloc[:, 1:]
FILM_NETWORK = build_network()
