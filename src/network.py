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
                go.Bar(x=bins[:-1], y=hist, name=str(community)), a, b
            )
            counter += 1

    fig.update_xaxes(title_text="Degree", row=a, col=1)
    fig.update_yaxes(title_text="Frequency", row=1, col=1)
    fig.update_layout(
        title_text="Degree distributions of the movie network for different communities",
        height=600,
    )
    return fig

def render_actor_distribution_text():
    st.write(f"The most frequently occuring degree value for the actor network is **7**.This value makes"
    " a lot of sense. On average there are **7-8** seven actors listed on a movie's wikipedia "
    " page, so every actor is connected to their cast member producing the specific number of"
    " edges. It can be noted, that  many of the degree values are between **5** and **10**. "
    " So usually an actor has that many colleagues/fellow actors he/she acts in movies with."
    " Of course, this is highly biased because of several reasons. Our dataset is quite small,"
    " we only look at very profitable movies and not all of the actors that acted"
    " in the movie are extracted.")

    st.text("")

    st.write(f"5 actors with the most connections:")
    st.write(f"*  Samuel L. Jackson")
    st.write(f"*  Idris Elba")
    st.write(f"* Dwayne Johnson")
    st.write(f"* Tyler Perry")
    st.write(f"* Kevin Hart")

    st.text("")
    st.write(f"5 actors with the least connections:")
    st.write(f"* Clint Eastwood")
    st.write(f"* Chaney Kley")
    st.write(f"* Emma Caulfield")
    st.write(f"* Israel Broussard")
    st.write(f"* Jessica Rothe")

    st.write(f"Regarding, the lists. It could be expected that Samuel L. Jackson would be one of the most"
    " connected actors. He is known for his good acting and his uniqueness. He appeared in many Marvel movies"
    " and films directed by Quentin Tarantino. This fact alone makes the actor very well known. Dwayne Johnson"
    " could also be expected to appear in such a list. He's been very active the past years appearing in many"
    " 'Casual' movies. What is suprising is Clint Eastwood appearing as an actor with the top5 least connections."
    " He is a legend is widely known for his famous roles. However, even though he is still quite involved in "
    " workng with cinema his prime years are long gone. Now Clint Eastwood carefully chooses his projects appearing"
    " in movies every few years or so.")

def render_movie_distribution_text():
    st.write(f"The degree distribution illustrates how movies are sharing actors among them. No single value stands"
    " out. We could say that **3-30** are the most frequently occuring degree values. More specifically, **21,17** "
    " and **23** are the top 3 degree values. In a way this could mean that some actors are not favored when choosing"
    " the cast for a movie or that movies are quite diverse with how they choose the movie cast.")

    st.text("")
    st.write(f"The 5 movies with the most connections / actors that are heavily casted for other movies as well:")
    st.write(f"* Avengers: Age of Ultron")
    st.write(f"* The Other Guys")
    st.write(f"* Avengers: Endgame")
    st.write(f"* Avengers: Infinity War")
    st.write(f"* The Avengers")

    st.text("")
    st.write(f"The 5 movies with the least connections / actors that are rarely selected for oher movies:")
    st.write(f"* Boogeyman")
    st.write(f"* Come Play")
    st.write(f"* Darkness Falls")
    st.write(f"* Friday the 13th")
    st.write(f"* Gran Torino")

    st.text("")
    st.write(f"So it can be seen that Marvel studios chose widely casted actors or made their cast members a very"
    " popular option for others. Marvel are making big budget movies, producing huge amounts of revenue, so it makes"
    " sense they are also choosing the popular/good actors. The Other Guys is also coming in strong. This movie has "
    " actors like Will Ferell, Mark Wahlberg, Dwayne Johnson and Samuel L. Jackson. These are huge names in the industry."
    " For the movies with the least connections we see some interesting things. 4 out of 5 of the listed movies are horror"
    " movies, which is quite interesting. This means that horror movies might cast less known actors. We can also see Gran"
    " Torino appearing in the list. This is the movie from Clint Eastwood, where he was the director and the main actor. "
    " We saw before that Clint Eastwood had 0 connections in the actor's network. We saw Samuel L. Jackson and Dwanye Johnson"
    " in the top 5 of the actor's network degree distribution.")

def render_box_office_distribution_text():
    st.write(f"Above we have the degree distributions for the movie network. They are "
    " categorized with respect to their box office values. A trend is seen where"
    " the movies with higher box office values have more widely used cast and movies"
    " with lower box office values have actors that are less used. This relationship "
    " makes sense. A popular/widely casted actor can be casted for his/her skills but "
    " also for their marketing value. An actor like Dwanye Johnson is probably quite"
    " aware of his value as a marketing asset and he definetely utilizes that.")

def render_genre_distribution_text():
    st.write(f"Above we have the degree distributions for the movie network categorized by"
        " different genres. Many of the distributions are quite wide, so no obvious patterns"
        " emerge. However, we previously saw that horror movies have casts that are not that"
        " widely used. This can be seen here again where **16** of the movies have **0** "
        " connections. Otherwise, adventure, sci-fi and crime movies seem to have more popular"
        " cast members.")
