import streamlit as st
from constants import FILM_DATA
from data import average_number_of, box_office_histogram
from network import (
    network_degree_distribution,
    network_degree_distribution_by_box_office,
    network_degree_distribution_by_genre,
    network_degree_distribution_by_community,
    render_actor_distribution_text,
    render_movie_distribution_text,
    render_box_office_distribution_text,
    render_genre_distribution_text,
    degree_distribution_comparison,
    render_degree_distribution_comparison_text,
    degree_centrality,
    render_degree_centrality_text,
    top_movies_degree_centrality,
    additional_statistics,
    er_comparison,
    render_er_comparsion_text,
    additional_statistics_text
)
from wordclouds import (
    render_word_clouds,
    render_genre_tf_idf,
    render_wordcloud_text,
)
from communities import (
    community_size_distribution_graph,
    community_box_office_histogram,
    community_box_office_barchart,
    render_community_text,
)
from sentiment import (
    plot_sentiment_scores_by_box_office_group,
    plot_sentiment_scores_by_genre,
    plot_compound_scores,
)


def introduction():
    """Defines what will be shown on our introduction page."""

    "# Top Box Office Films"
    "## Introduction"
    (
        "This website is set on presenting the insights gained from carrying"
        " out network and text analysis on top box office films. There are a"
        " few things we would ask you to keep in mind when using this site."
        " Firstly, it is important to point out that this is not a static site."
        " It is in fact quite the opposite, almost all of the graphs are dynamic;"
        " Hovering over a diagram reveals an entire toolset that you can  use to"
        " play around with the data. Similarly you can scroll around and explore"
        " the dataset in the Data Analysis section."
    )
    (
        "Since the page is so dynamic it will be a little slower to load the pages"
        " than if it was static, please have some patience. It will use your browsers"
        " cache so as you navigate pages it should become faster. In the siderbar"
        " you can find the page navigation as well as options to download the dataset"
        " and view the explainer notebook. All that being said, we hope you enjoy"
        " your time here and look forward to hearing your feedback 😁"
    )
    "## Motivation"
    (
        "The dataset we used to conduct our analysis is the set of films that"
        " grossed the highest revenue in the US box office for a given weekend"
        " from 2001 to 2021. We ultimately chose this dataset because we found"
        " it very compelling to see if we can draw any conclusions about what"
        " might bring success to a film. Are there certain specific actors, or"
        " groups of actors that seem to contribute to a films success to a large"
        " degree? Some genres of films are certainly more likely to be successfull"
        " than others."
    )
    (
        "These are the sorts of questions we hope to answer for ourselves, and"
        " convey in an effective way to any readers. We hope that this"
        " website in addition to the explainer notebook serve to provide insight"
        "  into our analysis and ilicit a desire to examine the anlysis closer."
    )


def data_analysis():
    """Defines what should be shown on the data analysis page."""

    # Page content
    "# Data Analysis"
    "## Data Set"
    (
        "Here you can see the dataset that is used for the network analysis "
        "as well as the natural lanuage processing. It consists of the top "
        "box office films for each weekend over the last 20 years. The "
        "included attributes are the actors, producers, writers, box "
        "office revenue, plot description with associated "
        "tokenization, and community. Try scrolling around and exploring the"
        " data for yourself!"
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
    bins = st.slider("Number of bins", min_value=3, max_value=200, value=60)
    fig = box_office_histogram(bins=bins)
    st.plotly_chart(fig, use_container_width=True)


def network_visualization():
    """Defines what should be shown on the network visualization page."""

    "# Network Analysis"

    "## Visualizations"

    (
        "Below you can see visualations of each of ther networks. For the movie"
        " network colors have been assigned to any communities that are larger"
        " than 50 films. The actor network is particularly interesting to look"
        " at when considering the connected componenets that can be found along"
        " the edge of the visualization. These connected componenets correspond"
        " to films as all actors within a film will have a and edge between eachother."
        " Futhermore, it is very interesting to note that there are some connected"
        " components that are not connected to any one but themselves. These represent"
        " films where actors have not starred in any box office hit other than that one."
    )

    col1, col2 = st.columns(2)

    col1.image("img/movie_network.png")

    col2.image("img/actor_network.png")

    "## Degree Distributions"
    st.plotly_chart(network_degree_distribution(type="film"))
    render_movie_distribution_text()

    st.plotly_chart(network_degree_distribution(type="actor"))
    render_actor_distribution_text()

    st.plotly_chart(network_degree_distribution_by_box_office())
    render_box_office_distribution_text()

    st.plotly_chart(network_degree_distribution_by_genre())
    render_genre_distribution_text()

    st.plotly_chart(network_degree_distribution_by_community())

    "# Comparison to network models"
    st.plotly_chart(degree_distribution_comparison())
    render_degree_distribution_comparison_text()

    "## Degree Centrality"
    st.write(degree_centrality())
    render_degree_centrality_text()

    "### 5 most central movies for each genre according to degree centrality"
    st.write(top_movies_degree_centrality())

    "## Additional Statistics"
    additional_statistics()
<<<<<<< HEAD
    additional_statistics_text()

    "### Comparison with the ER Network"
    st.write(er_comparison())
    render_er_comparsion_text()
=======

>>>>>>> 039bbb793008464eb2551f01d0d745a9f2bd6fe1

def word_clouds():
    """Defines what should be shown on the natural language processing page."""

    "# Text analysis of movie plots"

    "## Genre Most Popular Words"
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

    render_community_text()

    csd_graph = community_size_distribution_graph()
    st.plotly_chart(csd_graph)

    (
        "**Do larger communities make a bigger box office hit?**"
        " From the following plot we can see that the top 5 largest communities (orange bars) "
        " are also getting a quite high box office revenue. This indicates that larger communities"
        " tend to have more popular and thus more profitable movies. Considering the largest"
        " communities include a lot of famous movie series this is reasonable."
    )

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
    "In the above graphs there's also no obvious pattern. It seems that the higher the box office the more the higher positive score it has. But this is barely noticable."
    st.plotly_chart(negative_sentiment_plot)
    "It's seems that there's no pattern appearing here. Perhaps the very high box office movies have a slighly higher negative rating."
    st.plotly_chart(neutral_sentiment_plot)
    "Here we have the neutrality scores for different box office groups. All of the groups have high neutrality scores and there's not much difference. It seems like the neutrality value is reducing the higher the box office value is."
    st.plotly_chart(compound_plot)
    "Above we have the compound scores for all of the movies. It can be seen that the values are very extreme with the majority being around -1 and 1. A huge amount of the movies are at -1. "
    st.plotly_chart(positive_sentiment_genre_plot)
    "The postivity values for the different genres has some more differences. It seems like mystery, sci-fi and thriller have lower positivity scores. It makes sense since they also had higher negativity scores. The logic is similar for romatinc films, which have higher positivity scores compared to the other genres. What also pops out here, is that horror movies have small positivity values (where as the negativity scores didn't stand out)."
    st.plotly_chart(negative_sentiment_genre_plot)
    "In the plot above the negativity scores for different genres are shown. The values are quite similar. Perhaps mystery, sci-fi and thriller have slighly higher negativity scores than the rest. It also seems, that romance has lower negativity scores than the other genres and it's quite noticable."
    st.plotly_chart(neutral_sentiment_genre_plot)
    "Again, all of the movies have high values of neutrality, no matter the genre. It seems like there are no patterns or exceptions."


def main():
    """Entry point for the application."""

    st.sidebar.title("Top Box Office Films")
    page = st.sidebar.radio(
        "Sections",
        [
            "Introduction",
            "Basic Stats",
            "Network Analysis",
            "Text Analysis",
            "Communities Analysis",
            "Sentiment Analysis",
        ],
    )
    st.sidebar.download_button(
        "Download data",
        data=FILM_DATA.to_csv().encode("utf-8"),
        file_name="movie_dataset.csv",
    )
    link = "[Notebook](https://colab.research.google.com/drive/1kB3vDGY3Js_ex5OzXbJN9jb7qjJTkaoM?usp=sharing)"
    st.sidebar.markdown(link, unsafe_allow_html=True)
    if page == "Introduction":
        introduction()

    if page == "Basic Stats":
        data_analysis()

    if page == "Network Analysis":
        network_visualization()

    if page == "Text Analysis":
        word_clouds()

    if page == "Communities Analysis":
        communities()

    if page == "Sentiment Analysis":
        sentiment_analysis()


if __name__ == "__main__":
    main()
