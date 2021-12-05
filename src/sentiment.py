import streamlit as st
import pickle
import ast
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go


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
@st.cache
def plot_compound_scores():
    """Returns a figure object of our compound score."""

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


@st.cache
def plot_sentiment_scores_by_genre(type="positivity", height=800):
    """Returns a figure object of sentiment scores by genre."""

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
    """Returns a figure object of sentiment scores by box office."""

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
