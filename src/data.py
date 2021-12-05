import streamlit as st
import pickle
import ast
import pandas as pd
import numpy as np
import networkx as nx
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from community import community_louvain

with open("data/movie_graph", "rb") as f:
    GRAPH = pickle.load(f)


# Communities
# We could pickle our largest communities and just load that.
partition = community_louvain.best_partition(GRAPH)

communities = {}
for key, value in sorted(partition.items()):
    communities.setdefault(value, []).append(key)

community_sizes = {}
for k in sorted(communities, key=lambda k: len(communities[k]), reverse=True):
    community_sizes[k] = len(communities[k])

largest_communities = {}
for (key, value) in communities.items():
    if key in list(community_sizes)[:5]:
        largest_communities[key] = value


# Sentiment Analysis
with open("data/movie_plots", "rb") as f:
    movie_plots = pickle.load(f)

box_office_groups = [
    "very low box office",
    "low box office",
    "medium box office",
    "high box office",
    "very high box office",
]
temp = list(set(movie_plots["genres"].values))
movie_genres = [
    value for sublist in temp for value in ast.literal_eval(sublist)
]
movie_genres_set = list(set(movie_genres))
genre_list = []
for genre in movie_genres_set:
    genre_list.append(genre.replace(" ", ""))
genre_list = np.sort(list(set(genre_list)))


# Plots
def plot_compound_scores():
    fig = go.Figure()

    data = np.array(list(movie_plots["compound"].values))
    hist, bins = np.histogram(data, bins=30)
    fig.add_trace(go.Bar(x=bins[:-1], y=hist))
    fig.update_layout(
        title_text="Movie plot compound scores",
        xaxis_title="Compound scores",
        yaxis_title="Frequency",
    )
    return fig


def plot_sentiment_scores_by_genre(type="positivity", height=800):
    if type not in ["positivity", "negativity", "neutrality"]:
        raise ValueError(
            "Expecting one of ['positivity', 'negativity', 'neutrality'],"
            f" but received {type}",
        )
    fig = make_subplots(rows=10, cols=2, shared_xaxes=True, shared_yaxes=True)

    for i, genre in enumerate(genre_list[:-1]):
        genre_values = []
        for index, row in movie_plots.iterrows():
            if str(genre) in row.genres:
                if type == "positivity":
                    genre_values.append(row.positive)
                elif type == "negativity":
                    genre_values.append(row.negative)
                else:
                    genre_values.append(row.neutral)

        b = (i % 2) + 1
        a = (i // 2) + 1
        hist, bins = np.histogram(genre_values, bins=30)
        fig.add_trace(go.Bar(x=bins[:-1], y=hist, name=genre), a, b)

    if type == "positivity":
        fig.update_layout(
            title_text="Movie plot positivity scores for different genres"
        )
        fig.update_xaxes(title_text="Positivity score", row=10, col=1)
    elif type == "negativity":
        fig.update_layout(
            title_text="Movie plot negativity scores for different genres"
        )
        fig.update_xaxes(title_text="Negativity score", row=10, col=1)
    else:
        fig.update_layout(
            title_text="Movie plot neutrality scores for different genres"
        )
        fig.update_xaxes(title_text="Neutrality score", row=10, col=1)

    fig.update_yaxes(title_text="Frequency", row=4, col=1)
    fig.update_layout(height=height)
    return fig


@st.cache
def plot_sentiment_scores_by_box_office_group(
    type="positivity", showlegend=True, height=700
):
    if type not in ["positivity", "negativity", "neutrality"]:
        raise ValueError(
            "Expecting one of ['positivity', 'negativity', 'neutrality'],"
            f" but received {type}",
        )
    fig = make_subplots(
        rows=5,
        cols=1,
        shared_xaxes=True,
    )
    for i, group in enumerate(box_office_groups):
        j = 1
        temp_df = movie_plots[movie_plots.bo_groups == group]

        if type == "negativity":
            data = np.array(list(temp_df["negative"].values))
            fig.update_xaxes(title_text="Negativity score", row=5, col=1)
            fig.update_layout(
                title_text="Movie plot negativity scores for different box offices",
            )

        elif type == "positivity":
            data = np.array(list(temp_df["positive"].values))
            fig.update_xaxes(title_text="Positivity score", row=5, col=1)
            fig.update_layout(
                title_text="Movie plot positivity scores for different box offices",
            )
        else:
            data = np.array(list(temp_df["neutral"].values))
            fig.update_xaxes(title_text="Neautrality score", row=5, col=1)
            fig.update_layout(
                title_text="Movie plot neautrality scores for different box offices",
            )

        hist, bins = np.histogram(data, bins=30)
        fig.add_trace(go.Bar(x=bins[:-1], y=hist, name=group), i + 1, j)

    fig.update_yaxes(title_text="Frequency", row=3, col=1)
    fig.update_layout(height=height, showlegend=showlegend)
    return fig


@st.cache
def community_box_office_histogram():
    """Returns a figure object of box office histograms for each community."""
    fig = make_subplots(rows=5, cols=1, shared_xaxes=True, shared_yaxes=True)
    fig.update_layout(
        title_text="Box office distribution for 5 largest communities",
        height=700,
    )
    fig.update_xaxes(title_text="USD", row=5, col=1)

    counter = 1
    for k, dk in largest_communities.items():
        temp_df = FILM_DATA[FILM_DATA["link"].isin(dk)]
        hist, bins = np.histogram(temp_df.box_office, bins=30)
        fig.add_trace(go.Bar(x=bins[:-1], y=hist, name=k), counter, 1)
        counter += 1
    return fig


@st.cache
def community_size_distribution_graph():
    """Returns a figure object for the community size distribution graph."""

    community_sizes = {}
    for k in sorted(
        communities, key=lambda k: len(communities[k]), reverse=True
    ):
        community_sizes[k] = len(communities[k])

    community_size_bar_chart_data = {
        "Community Size": list(community_sizes.values()),
        "Community Number": list(community_sizes.keys()),
    }
    fig = px.bar(
        community_size_bar_chart_data,
        title="Comunity Sizes",
        x="Community Number",
        y="Community Size",
        height=400,
    )
    return fig


@st.cache
def movie_network():
    """Returns our pickeld network object."""
    with open("data/movie_graph", "rb") as f:
        return pickle.load(f)


@st.cache
def build_network():
    """Builds our network from scratch."""
    G = nx.Graph()
    for movie in FILM_DATA.T.iteritems():
        G.add_node(movie[1]["title"])
    return G


@st.cache
def box_office_histogram(bins):
    """Return Figure object for box office historgram.

    Args:
        bins (int): The number of bins for the histogram.
    """
    return px.histogram(
        FILM_DATA,
        x="box_office",
        marginal="rug",
        title="Box Office Distrubtion",
        nbins=bins,
    )


@st.cache
def average_number_of(attribute):
    """Return average number of provdide attributes"""
    if attribute in ["actors", "directors", "producers", "writers"]:
        xs = FILM_DATA[attribute]
        sum = 0
        for x in xs:
            sum += len(ast.literal_eval(x))
        return round(sum / len(FILM_DATA), 2)
    else:
        raise TypeError(
            "Expecting one of 'actors', 'directors', 'producers', 'writers'\n"
            f"Got '{attribute}'"
        )


FILM_DATA = pd.read_csv("data/dataset.csv").iloc[:, 1:]
FILM_NETWORK = movie_network()
