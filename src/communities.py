import streamlit as st
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from community import community_louvain
from constants import FILM_DATA, FILM_NETWORK_COMMUNITY


partition = community_louvain.best_partition(FILM_NETWORK_COMMUNITY)
print("COMMMS!")
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

community_names = {}
for com in communities:
    temp_degree_dict = {}
    for character in communities[com]:
        film = FILM_DATA[FILM_DATA["link"] == character]
        title = (
            character
            if film.empty
            else FILM_DATA[FILM_DATA["link"] == character].title.values[0]
        )

        temp_degree_dict[title] = FILM_NETWORK_COMMUNITY.degree[character]

    community_names[com] = sorted(
        temp_degree_dict, key=temp_degree_dict.get, reverse=True
    )[:3]


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


@st.cache(allow_output_mutation=True)
def community_box_office_barchart():
    """Returns a bar chart of the total box office distribution for each genre"""

    box_office_sums = {}
    for index, values in communities.items():
        box_office_sum = 0

        for title in values:
            try:
                box_office_sum = (
                    box_office_sum
                    + FILM_DATA[FILM_DATA["link"] == title].box_office.values[
                        0
                    ]
                )
            except IndexError as e:
                print(e)

        box_office_sums[index] = box_office_sum / len(values)

    community_size_bar_chart_data = {
        "Total Box Office": list(box_office_sums.values()),
        "Community Number": list(box_office_sums.keys()),
        "Top Movies": list(community_names.values()),
    }

    color_discrete_sequence = ["#636efa"] * len(communities)
    for index in largest_communities:
        bar_index = list(communities.keys()).index(index)
        color_discrete_sequence[bar_index] = "#ffa15a"

    fig = px.bar(
        community_size_bar_chart_data,
        hover_data=["Community Number", "Total Box Office", "Top Movies"],
        title="Communities Total Box Office",
        x="Community Number",
        y="Total Box Office",
        height=400,
    ).update_traces(marker=dict(color=color_discrete_sequence))

    return fig


@st.cache(allow_output_mutation=True)
def community_size_distribution_graph():
    """Returns a figure object for the community size distribution graph."""

    community_size_bar_chart_data = {
        "Community Size": list(community_sizes.values()),
        "Community Number": list(community_sizes.keys()),
        "Top Movies": list(community_names.values()),
    }
    fig = px.bar(
        community_size_bar_chart_data,
        hover_data=["Community Number", "Community Size", "Top Movies"],
        title="Community Sizes",
        x="Community Number",
        y="Community Size",
        height=400,
    )
    return fig
