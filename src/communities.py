import streamlit as st
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from community import community_louvain
from constants import FILM_DATA, FILM_NETWORK_COMMUNITY


partition = community_louvain.best_partition(FILM_NETWORK_COMMUNITY)

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
