import streamlit as st
import pandas as pd
import networkx as nx
import plotly.figure_factory as ff


@st.cache
def build_network():
    G = nx.Graph()
    for movie in FILM_DATA.T.iteritems():
        G.add_node(movie[1]["title"])
    return G


@st.cache
def box_office_histogram():
    hist_data = [list(FILM_DATA.box_office)]
    labels = ["Box Office Revenue"]
    return ff.create_distplot(hist_data, labels, [9000000])


FILM_DATA = pd.read_csv("dataset.csv").iloc[:, 1:]
FILM_NETWORK = build_network()
