import streamlit as st
from constants import (
    FILM_DATA
)
from data import average_number_of, box_office_histogram
from network import (
    network_degree_distribution,
    network_degree_distribution_by_box_office,
    network_degree_distribution_by_genre,
    network_degree_distribution_by_community,
)
from wordclouds import (
    render_word_clouds,
    render_genre_tf_idf,
    render_wordcloud_text
)
from communities import (
    community_size_distribution_graph,
    community_box_office_histogram,
    community_box_office_barchart,
)
from sentiment import (
    plot_sentiment_scores_by_box_office_group,
    plot_sentiment_scores_by_genre,
    plot_compound_scores,
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
    st.plotly_chart(network_degree_distribution(type="film"))
    st.plotly_chart(network_degree_distribution(type="actor"))
    st.plotly_chart(network_degree_distribution_by_box_office())
    st.plotly_chart(network_degree_distribution_by_genre())
    st.plotly_chart(network_degree_distribution_by_community())


def word_clouds():
    """Defines what should be shown on the natural language processing page."""

    '# Text analysis of movie plots'

    '## Genre Most Popular Words'
    "By analyzing movie plots per genre, we are interested in seeing whether genres"
    " share any words, as well as what words make a genre unique. To do that we "
    " calculate the top frequent words in each genre (TF value) but also the top "
    " relevant words in each genre (TF-IDF value)."

    render_genre_tf_idf()
    (
        "As we can see there is a significant difference between TF and TF-IDF values."
        " TF (term frequency) gives us words that are often used in a document. In our "
        " dataset, for example, we can see that words like **kill, find, leave, attack,**"
        " **help, return** are appearing very often. This makes sense, since these are "
        " verbs that can generally describe a plot. However, these words are not very "
        " descriptive of the genres."

        "The IDF (inverse document frequency) of a word gives us the measure of how"
        " significant that term is between all genres because it takes into account "
        " the number of genres containing a term. Therefore, it mainly returns "
        " protagonist nameslike **katniss, voldemort, shrek, zuckerberg, gandalf** "
        " which help us get a better sense of a genre's movies."

        "Ideally, when using TF-IDF, we would want to get words that describe a genre"
        " more accurately, without seeing character names. Since we were unable to"
        " remove these names for more than 700 movies, they now dominate the dataset's"
        " top words."
    )

    "## Genre Word Clouds"
    render_word_clouds()

    render_wordcloud_text()


def communities():
    "# Movie Community Detection"

    "Each time the Louvain Algorithm runs, it returns a different community partition."
    " However, throughout executions it was interesting seeing that the communities "
    " formed included movies from the same series or similar genres. This makes sense, "
    " since our network is build based on movies that share actors and it is probable "
    " that actors will continue playing in movie sequels or will be cast to play in "
    " the same genre."

    "*Community 1* includes action movies like **Fast and the Furious, The Expendables, Transformers**"
    "*Community 2* includes animation movies like **Kung Fu Panda, Cars, Despicable Me** "
    "*Community 3* includes fantasy movies like **Harry Potter** and **Pirates of the Carribean**"
    "*Community 4* includes fantasy, adventure movies like **Lord of the Rings** and **Star Wars**"
    "*Community 5* includes superheroe movie series like **Avengers, Captain America, Iron Man, Spider Man**"

    csd_graph = community_size_distribution_graph()
    st.plotly_chart(csd_graph)

    "**Do larger communities make a bigger box office hit?**"
    " From the following plot we can see that the top 5 largest communities (orange bars) "
    " are also getting a quite high box office revenue. This indicates that larger communities"
    " tend to have more popular and thus more profitable movies. Considering the largest"
    " communities include a lot of famous movie series this is reasonable."

    cbo_barchart = community_box_office_barchart()
    st.plotly_chart(cbo_barchart)

    # cbo_histogram = community_box_office_histogram()
    # st.plotly_chart(cbo_histogram)

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
            "Text Analysis",
            "Communities Analysis",
            "Sentiment Analysis"
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

    if page == "Text Analysis":
        word_clouds()

    if page == "Communities Analysis":
        communities()

    if page == "Sentiment Analysis":
        sentiment_analysis()


if __name__ == "__main__":
    main()
