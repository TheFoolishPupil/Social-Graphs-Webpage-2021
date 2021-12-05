import streamlit as st
import ast
import plotly.express as px
from constants import FILM_DATA


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
