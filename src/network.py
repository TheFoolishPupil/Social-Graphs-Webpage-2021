import streamlit as st
import ast
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from constants import ACTOR_NETWORK, FILM_NETWORK, BOX_OFFICE_GROUPS, FILM_DATA


temp = list(set(FILM_DATA["genres"].values))
movie_genres = [
    value for sublist in temp for value in ast.literal_eval(sublist)
]
movie_genres_set = list(set(movie_genres))
genre_list = []

for genre in movie_genres_set:
    genre_list.append(genre.replace(" ", ""))

genre_list = np.sort(list(set(genre_list)))
genre_list = list(genre_list)
small_genres = [
    "War",
    "Sport",
    "History",
    "Biography",
    "Music",
    "Musical",
    "Western",
    "Documentary",
]

for genre in small_genres:
    genre_list.remove(genre)


@st.cache
def network_degree_distribution(type="film"):

    if type not in ["film", "actor"]:
        raise ValueError(
            "Expecting one of ['film', 'actor']," f" but received {type}",
        )
    fig = go.Figure()

    if type == "film":
        degree_distribution = [
            FILM_NETWORK.degree(n) for n in FILM_NETWORK.nodes()
        ]
        fig.update_layout(title_text="Degree distribution of the film network")
    else:
        degree_distribution = [
            ACTOR_NETWORK.degree(n) for n in ACTOR_NETWORK.nodes()
        ]
        fig.update_layout(
            title_text="Degree distribution of the actors network"
        )
    hist, bins = np.histogram(
        degree_distribution, bins=np.arange(max(degree_distribution) + 1)
    )
    fig.add_trace(go.Bar(x=bins[:-1], y=hist))
    fig.update_layout(
        xaxis_title="Node degree",
        yaxis_title="Frequency",
    )
    return fig


@st.cache
def network_degree_distribution_by_box_office():
    fig = make_subplots(rows=5, cols=1, shared_xaxes=True, shared_yaxes=True)

    for i, group in enumerate(BOX_OFFICE_GROUPS):
        degree_distribution = []
        for n in FILM_NETWORK.nodes():
            if FILM_NETWORK.nodes[n]["bo_group"] == group:
                degree_distribution.append(FILM_NETWORK.degree(n))

        hist, bins = np.histogram(
            degree_distribution, bins=np.arange(max(degree_distribution) + 1)
        )
        fig.add_trace(go.Bar(x=bins[:-1], y=hist, name=group), i + 1, 1)

    fig.update_xaxes(title_text="Degree", row=5, col=1)
    fig.update_yaxes(title_text="Frequency", row=4, col=1)
    fig.update_layout(
        title_text="Degree distributions of the movie network for different box office ranges",
        height=600,
    )
    return fig


@st.cache
def network_degree_distribution_by_genre():
    fig = make_subplots(rows=7, cols=2, shared_xaxes=True)

    for i, genre in enumerate(genre_list):
        degree_distribution = []
        for n in FILM_NETWORK.nodes():
            if genre in FILM_NETWORK.nodes[n]["genre"]:
                degree_distribution.append(FILM_NETWORK.degree(n))

        b = (i % 2) + 1
        a = (i // 2) + 1
        hist, bins = np.histogram(degree_distribution, bins=30)
        fig.add_trace(go.Bar(x=bins[:-1], y=hist, name=genre), a, b)

    fig.update_xaxes(title_text="Degree", row=7, col=1)
    fig.update_yaxes(title_text="Frequency", row=5, col=1)
    fig.update_layout(
        title_text="Degree distributions of the movie network for different genres",
        height=800,
    )
    return fig


@st.cache
def network_degree_distribution_by_community():
    community_list = list(set(FILM_DATA["community"].values))

    fig = make_subplots(rows=3, cols=2, shared_xaxes=True, shared_yaxes=True)
    counter = 0
    for i, community in enumerate(community_list):
        degree_distribution = []
        for n in FILM_NETWORK.nodes():
            if community == FILM_NETWORK.nodes[n]["community"]:
                degree_distribution.append(FILM_NETWORK.degree(n))

        if len(degree_distribution) > 50:
            b = (counter % 2) + 1
            a = (counter // 2) + 1
            hist, bins = np.histogram(degree_distribution, bins=30)
            fig.add_trace(
                go.Bar(x=bins[:-1], y=hist, name=str(community), dx=a, dy=b)
            )
            counter += 1

    fig.update_xaxes(title_text="Degree", row=a, col=1)
    fig.update_yaxes(title_text="Frequency", row=1, col=1)
    fig.update_layout(
        title_text="Degree distributions of the movie network for different communities",
        height=600,
    )
    return fig
