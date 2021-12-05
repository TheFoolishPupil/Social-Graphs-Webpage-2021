import streamlit as st
from wordclouds import render_word_clouds
from constants import (
    FILM_DATA,
    FILM_NETWORK,
)
from communities import (
    community_size_distribution_graph,
    community_box_office_histogram,
)
from sentiment import (
    plot_sentiment_scores_by_box_office_group,
    plot_sentiment_scores_by_genre,
    plot_compound_scores,
)
from data import (
    average_number_of,
    box_office_histogram,
)


def data_analysis():
    """Defines what should be shown on the data analysis page."""

    # Sidebar content
    st.sidebar.write("## Parameters")
    bins = st.sidebar.slider(
        "Number of bins", min_value=3, max_value=200, value=60
    )
    # Page content
    "# Data Analysis"
    "## Data Set"
    (
        "Here you can see the dataset that is used for the network analysis "
        "as well as the natural lanuage processing. It consists of the top "
        "box office films for each weekend over the last 20 years. The "
        "included attributes are the actors, producers, writers, and box "
        "office revenue. Additionally, a plot description and associated "
        "tokenization is also present."
    )
    selected_attributes = st.multiselect(
        "Select film attributes",
        FILM_DATA.columns.values,
        [
            FILM_DATA.columns.values[0],
            FILM_DATA.columns.values[2],
            FILM_DATA.columns.values[4],
        ],
    )
    st.write(FILM_DATA[selected_attributes])

    "## Data Insights"
    f"The average number of actors is **{average_number_of('actors')}**"
    f"The average number of writers is **{average_number_of('writers')}**"
    f"The average number of directors is **{average_number_of('directors')}**"
    f"The average number of producers is **{average_number_of('producers')}**"

    "## Data Distribution"
    fig = box_office_histogram(bins=bins)
    st.plotly_chart(fig, use_container_width=True)


def network_visualization():
    """Defines what should be shown on the network visualization page."""

    "# Network Visualization and Degree Distribution"
    FILM_NETWORK


def word_clouds_and_communities():
    """Defines what should be shown on the natural language processing page."""

    "# Word Clouds for Genres"

    "## Word Clouds for Genres"
    render_word_clouds()
    (
        "From the generated wordclouds we can see that almost all genres are"
        " mostly described by the name of their characters. This makes sense"
        " since movie plots describe the storyline of each character. We also"
        " see genres sharing character names, since movies can belong to"
        " multiple genres. A few examples are:"
    )
    "**Action** : Bourne, Katniss, Logan, agent, avenger"
    "**Adventure** : Maleficent, Voldemort, Gandalf"
    "**Animation** : Shrek, McQueen, Simba"
    "**Biography** : Freddie, Zuckerberg, Harvard"
    "**Comedy** : Stiffler, Borat"
    "**Crime** : Clouseau, britt, bank, gangster"
    "**Documentary** : Since Jackass is the only movie in this category we have words like knoxville, butt, skateboard"
    "**Drama** : Bella, Frodo, Simba"
    "**Family** : Simba, Maleficent, Shrek, hiccup"
    "**Fantasy** : Maleficent, Shrek, Aladdin, Dumbledore"
    "**History** : Agamemnon, greek, Achilles, briseis, trojan"
    "**Horror** : Samara, creeper, Leatherface, exorcism, creature"
    "**Music** : Freddie, Farrokh, elgin"
    "**Musical** : Giselle, Elsa, Aladdin"
    "**Mystery** : Moriarty, Holmes, Bourne"
    "**Romance** : Bella, Shrek, Edward"
    "**Sci-Fi** : Optimus, Godzilla, Stark, Thanos"
    "**Sport** : gym, coach, lap, chick"
    "**Thriller** : Lecter, Bourne, Katniss"
    "**War** : Schofield, tugg, savannah, german"
    "**Western** : cogburn, fitzgerald, outlaws"

    "## Community Detection"

    "### Community Analysis"

    (
        "It's interesting seeing that many communities include movies from the"
        " same movie series or similar movie genres. This makes sense, since"
        " it is probable that actors will continue playing in movie sequels or"
        " will be cast to play in the same genre. For example:"
    )
    "*Community 1* includes action movies like **Fast and the Furious, The Expendables, Transformers**"
    "*Community 2* includes animation movies like **Kung Fu Panda, Cars, Despicable Me** "
    "*Community 3* includes fantasy movies like **Harry Potter** and **Pirates of the Carribean**"
    "*Community 4* includes fantasy, adventure movies like **Lord of the Rings** and **Star Wars**"
    "*Community 5* includes superheroe movie series like **Avengers, Captain America, Iron Man, Spider Man**"

    csd_graph = community_size_distribution_graph()
    st.plotly_chart(csd_graph)

    cbo_histogram = community_box_office_histogram()
    st.plotly_chart(cbo_histogram)


def sentiment_analysis():
    """Defines what should be shown on the sentiment analysis page."""

    "# Sentiment Analysis"

    positive_sentiment_plot = plot_sentiment_scores_by_box_office_group(
        type="positivity"
    )
    negative_sentiment_plot = plot_sentiment_scores_by_box_office_group(
        type="negativity"
    )
    neutral_sentiment_plot = plot_sentiment_scores_by_box_office_group(
        type="neutrality"
    )
    positive_sentiment_genre_plot = plot_sentiment_scores_by_genre(
        type="positivity"
    )
    negative_sentiment_genre_plot = plot_sentiment_scores_by_genre(
        type="negativity"
    )
    neutral_sentiment_genre_plot = plot_sentiment_scores_by_genre(
        type="neutrality"
    )
    compound_plot = plot_compound_scores()

    st.write("")
    st.plotly_chart(positive_sentiment_plot)
    st.plotly_chart(negative_sentiment_plot)
    st.plotly_chart(neutral_sentiment_plot)
    st.plotly_chart(compound_plot)
    st.plotly_chart(positive_sentiment_genre_plot)
    st.plotly_chart(negative_sentiment_genre_plot)
    st.plotly_chart(neutral_sentiment_genre_plot)


def main():
    """Entry point for the application."""

    st.sidebar.title("Top Box Office Films")
    page = st.sidebar.radio(
        "Sections",
        [
            "Data Analysis",
            "Network Visualization",
            "Word Clouds & Communities",
            "Sentiment Analysis",
        ],
    )
    st.sidebar.download_button(
        "Download data",
        data=FILM_DATA.to_csv().encode("utf-8"),
        file_name="movie_dataset.csv",
    )
    if page == "Data Analysis":
        data_analysis()

    if page == "Network Visualization":
        network_visualization()

    if page == "Word Clouds & Communities":
        word_clouds_and_communities()

    if page == "Sentiment Analysis":
        sentiment_analysis()


if __name__ == "__main__":
    main()
