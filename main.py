import streamlit as st
import pandas as pd
import json

st.title("Top Box Office Films")

st.write("## Data Analysis")

st.write(
    "Here you can see the dataset that is used for the network analysis"
    "as well as the natural lanuage processing. It consists of the top"
    "box office films for each weekend over the last 20 years. The included"
    "attributes are the box office revenue and starring actors. Plot"
    "description and its tokenization is also present."
)

df = pd.read_csv("dataset.csv").iloc[:, 1:]
st.write(df)

with open("movie_data.json", "r") as f:
    data = json.load(f)
