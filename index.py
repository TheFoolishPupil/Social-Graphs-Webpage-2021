import streamlit as st
from data import FILM_DATA, FILM_NETWORK


def data_analysis():
    st.write("# Data Analysis")
    st.write("## Data Set")
    st.write(
        "Here you can see the dataset that is used for the network analysis "
        "as well as the natural lanuage processing. It consists of the top "
        "box office films for each weekend over the last 20 years. The "
        "included attributes are the actors, producers, writers, and box "
        "office revenue. Additionally, a plot description and associated "
        "tokenization is also present."
    )
    selected_attributes = st.multiselect(
        "Show/hide film attributes",
        [
            "Tokens",
            "Unique Tokens",
            "Plot",
            "Actors",
            "Directors",
            "Producers",
            "Writers",
            "Box Office",
        ],
        ["Actors"],
    )
    st.write(FILM_DATA)
    st.write("## Summary Statistics")


def network_visualization():
    st.write("## Network Visualization and Degree Distribution")
    st.write(FILM_NETWORK)


def main():
    st.sidebar.title("Top Box Office Films")
    page = st.sidebar.radio(
        "Sections", ["Data Analysis", "Network Visualization"]
    )
    if page == "Data Analysis":
        data_analysis()

    if page == "Network Visualization":
        network_visualization()


if __name__ == "__main__":
    main()
