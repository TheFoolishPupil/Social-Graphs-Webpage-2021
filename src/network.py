import streamlit as st
import ast
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from constants import ACTOR_NETWORK, FILM_NETWORK, BOX_OFFICE_GROUPS, FILM_DATA
import networkx as nx
import random
import pandas as pd

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

def add_new_nodes(network, amount):
    edge_list = flat_edge_list(network)
    next_node = max(edge_list) + 1
    network.add_edge(random.choice(edge_list), next_node)
    next_node += 1

    for i in range(amount-1):
        edge_list = flat_edge_list(network)
        network.add_edge(random.choice(edge_list), next_node)
        next_node += 1

    return network

def flat_edge_list(network):

    edge_list = []

    for n1,n2 in list(network.edges()):
        edge_list.append(n1)
        edge_list.append(n2)

    return edge_list

@st.cache
def degree_distribution_comparison():
    #Create a list of network names and a list of their respective degree distributions
    types = ['Movie Network','Barabasi-Albert Network','Watts Strogatz Network','Erdős-Rényi Network']
    degree_distributions = []

    #We get the degree distribution of our movie network and add it to the list
    degree_distribution_movies = [FILM_NETWORK.degree(n) for n in FILM_NETWORK.nodes()]
    degree_distributions.append(degree_distribution_movies)

    #We get the degree distribution of a Barabasi-Albert network with the same amount of nodes.
    #The distribution is added to the list
    BA = nx.Graph()
    BA.add_edge(1,2)
    BA = add_new_nodes(BA,712)
    degree_distribution = [BA.degree(n) for n in BA.nodes()]
    degree_distributions.append(degree_distribution)

    #We get the degree distribution for the Watts Strogatz network with the same amount of nodes.
    #The distribution is added to the list
    degree_distribution = [FILM_NETWORK.degree(n) for n in FILM_NETWORK.nodes()]
    avg_k = sum(degree_distribution)/len(degree_distribution)
    p = avg_k/(len(list(FILM_NETWORK.nodes())))
    WSG = nx.watts_strogatz_graph(n=713, k=int(avg_k), p=p)
    WSG_degree_distribution = [WSG.degree(n) for n in WSG.nodes()]
    degree_distributions.append(WSG_degree_distribution)

    #We get the degree distribution of the Erdős-Rényi network with the same amount of nodes.
    #The distribution is added to the list
    ER = nx.gnp_random_graph(713,p)
    degree_distribution = [ER.degree(n) for n in ER.nodes()]
    degree_distributions.append(degree_distribution)

    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, shared_yaxes=True)

    for i, distribution in enumerate(degree_distributions):

        b = (i%2) +1
        a = (i//2) +1
        hist, bins = np.histogram(distribution, bins = np.arange(max(distribution)+1))
        fig.add_trace(go.Bar(x=bins[:-1], y=hist,name=types[i]),i+1,1)

    fig.update_xaxes(title_text="Degree", row = i+1, col = 1)
    fig.update_yaxes(title_text="Frequency", row = 1, col = 1)
    fig.update_layout(title_text="Degree distributions for different networks")

    return fig

def render_degree_distribution_comparison_text():
    st.write(f"The degree distribution of the movie network is compared to the degree distributions"
    " of other networks. These networks were produced with the same amount of nodes and similar statistics"
    " to our movie network. If they were similar we could use some of the properties of the respective "
    " network. However, this is not really the case. The most similar degree distribution is that of the "
    " Erdos-Renyi network, but they are still very different.")

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

def degree_centrality():
    df_centrality = pd.DataFrame()

    # Find the 5 most central movies according to degree centrality.
    movie_degree_centrality = nx.degree_centrality(FILM_NETWORK)
    sortedDict = dict(sorted(movie_degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5])
    sortedDict = {k: round(v, 4) for k, v in sortedDict.items()}
    df_centrality['Degree Centrality'] = sortedDict.keys()
    df_centrality['Degree Centrality Value'] = sortedDict.values()

    # Find the 5 most central movies according to betweenness centrality.
    movie_betweeness_centrality = nx.betweenness_centrality(FILM_NETWORK, endpoints=True)
    sortedDict = dict(sorted(movie_betweeness_centrality.items(), key=lambda x: x[1], reverse=True)[:5])
    sortedDict = {k: round(v, 4) for k, v in sortedDict.items()}
    df_centrality['Betweenness Centrality'] = sortedDict.keys()
    df_centrality['Betweenness Centrality Value'] = sortedDict.values()

    # Find the 5 most central characters according to eigenvector centrality.
    movie_eigenvector_centrality = nx.eigenvector_centrality(FILM_NETWORK)
    sortedDict = dict(sorted(movie_eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:5])
    sortedDict = {k: round(v, 4) for k, v in sortedDict.items()}
    df_centrality['Eigenvector Centrality'] = sortedDict.keys()
    df_centrality['Eigenvector Centrality Value'] = sortedDict.values()

    return df_centrality


def top_movies_degree_centrality():
    df_centrality_genres = pd.DataFrame()
    movie_degree_centrality = nx.degree_centrality(FILM_NETWORK)

    # Find the 5 most central movies for each genre according to degree centrality.
    for i,genre in enumerate(genre_list):
        genre_nodes = [x for x,y in FILM_NETWORK.nodes(data=True) if genre in y['genre']]
        genre_movie_degree_centrality = { key: movie_degree_centrality[key] for key in genre_nodes}

        sortedDict = dict(sorted(genre_movie_degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5])
        sortedDict = {k: round(v, 4) for k, v in sortedDict.items()}
        df_centrality_genres[genre] = sortedDict.keys()
        df_centrality_genres['value'] = sortedDict.values()

        df_centrality_genres[genre] = df_centrality_genres[genre] + ' : ' +  df_centrality_genres["value"].astype(str)

    df_centrality_genres.drop(['value'], axis=1).to_csv("genre_centrality")
    df_centrality_genres.drop(['value'], axis=1)

    return df_centrality_genres


def render_degree_centrality_text():
    st.write(f"Some of the text is from https://cambridge-intelligence.com/keylines-faqs-social-network-analysis/")
    st.text("")

    st.write(f"**Degree centrality**")
    st.text("")

    st.write(f"Definition: Degree centrality assigns an importance score based simply on the number of links held by each node.")
    st.write(f"What it tells us: How many direct, ‘one hop’ connections each node has to other nodes in the network."
    "This matches the previously seen movies that have widely used cast members.")
    st.text("")


    st.write(f"**Betweenness centrality**")
    st.text("")

    st.write(f"Definition: Betweenness centrality measures the number of times a node lies on the shortest path between other nodes.")
    st.write(f"What it tells us: This measure shows which nodes are ‘bridges’ between nodes in a network. It does this by identifying all the"
    " shortest paths and then counting how many times each node falls on one.")
    st.text("")

    st.write(f"Some of the values changed here. Marvel movies still remain in the top 5. However, a movie we haven't seen before appears"
      "here *Valentine's Day*. This movie does have an impressive cast - Julia Robert, Jennifer Garner, Ashton Kutcher and so on. What this"
      "could mean is that the cast appears is quite popular but appears in many different categories/types of movies. So *Valentine's Day* "
      "acts as an intermediate node for those different movies. It could be a similar situation with the movie *New Year's Eve*. It's "
      "starring Zac Effron, Robert De Niro, Hilary Swank, Michelle Pfeiffer and so on.")
    st.text("")

    st.write(f"**Eigenvector centrality**")
    st.text("")

    st.write(f"Definition: Like degree centrality, EigenCentrality measures a node’s influence based on the number of links it has to "
    "other nodes in the network. EigenCentrality then goes a step further by also taking into account how well connected a node is, and"
    " how many links their connections have, and so on through the network.")
    st.write(f" What it tells us: By calculating the extended connections of a node, EigenCentrality can identify nodes with influence over the whole"
    " network, not just those directly connected to it.")
    st.text("")

    st.write(f"Again, we see Marvel movies having lots of influence. A movie we haven't seen before is *Iron Man 2*, which is interesting. "
    " This is one of the earlier Marvel movies starring Robert Downey Jr., Don Cheadle, Mickey Rourke, Samuel L. Jackson, Scarlett Johansson"
    " and so on. ")

def additional_statistics():
    # Returns the average degree of the neighborhood of each node.
    stats = nx.average_neighbor_degree(FILM_NETWORK)

    st.write(f"Movies with the highest average neighbour degree")

    st.write(sorted(stats, key=stats.get, reverse=True)[:5])

def er_comparison():
    #Extracting the biggest component from the movie graph to compute some of the statistics
    degree_distribution = [FILM_NETWORK.degree(n) for n in FILM_NETWORK.nodes()]
    avg_k = sum(degree_distribution)/len(degree_distribution)
    p = avg_k/(len(list(FILM_NETWORK.nodes())))
    ER = nx.gnp_random_graph(713,p)
    Gcc = sorted(nx.connected_components(FILM_NETWORK), key=len, reverse=True)
    H_gcc = FILM_NETWORK.subgraph(Gcc[0])

    Gcc = sorted(nx.connected_components(ER), key=len, reverse=True)
    ER_gcc = ER.subgraph(Gcc[0])

    avg_shortest_path = nx.average_shortest_path_length(H_gcc)
    avg_clustering = nx.average_clustering(FILM_NETWORK)
    movies_avg_clustering = nx.average_clustering(FILM_NETWORK)
    gcc_avg_clustering = nx.average_clustering(H_gcc)

    ER_avg_shortest_path = nx.average_shortest_path_length(ER_gcc)
    ER_avg_clustering = nx.average_clustering(ER)
    ER_movies_avg_clustering = nx.average_clustering(ER)
    ER_gcc_avg_clustering = nx.average_clustering(ER_gcc)


    df_other_statistics = pd.DataFrame()
    statistics = [
        "Network assortativity",
        "Box Office Groups assortativity",
        "Community assortativity",
        "GCC Average Shortest Path",
        "Average Clustering"
    ]

    values = [
        nx.degree_assortativity_coefficient(FILM_NETWORK),
        nx.attribute_assortativity_coefficient(FILM_NETWORK,'bo_group'),
        nx.attribute_assortativity_coefficient(FILM_NETWORK,'community'),
        avg_shortest_path,
        gcc_avg_clustering
    ]
    er_values = [
        nx.degree_assortativity_coefficient(ER),
        np.nan,
        np.nan,
        ER_avg_shortest_path,
        ER_gcc_avg_clustering
    ]

    df_other_statistics['Metric'] = statistics
    df_other_statistics['MN Value'] = values
    df_other_statistics['ER Value'] = er_values

    return df_other_statistics

def render_er_comparsion_text():
    st.write(f"Here we compare some of the statistics to that of the ER network. This is because we wanted to share some"
    " reference point and the Erdős-Rényi network had the most similar degree distribution. Note, it is just for reference"
    " and no additional assumptions are made because of this.")

    st.write(f"The movie network has a degree assortativity of ~0.17. The value is quite close to 0, but it does indicate "
    "a small tendancy for nodes of similar degrees to have connections. This could be in the form of Marvel movies having"
    " connections between each other.")

    st.write(f"Both box office assortativity and community assortativity have quite small values, which indicates that "
    "there's no relation between nodes of similar degree.")

    st.write(f"GCC Average Shortest Path is the value for the giant connected compenent. This value shows how diverse the "
    "casting is/how compact the network is.")

    st.write(f"The average clustering coefficient is ~0.35. This value indicates how densely connected the network is. It "
    "seems that the value is quite high, especially since it's expected for real world networks to be rather sparse.")

def additional_statistics_text():
    st.write(f"The nodes of the 5 movies above have the highest average neighbour degree"
    "values. So they connect to nodes that have very high degree. So these movies"
    "might have casted some actors that are a part of other very influental movies."
    "The actors could be: Scarlett Johansson, Samuel L. Jackson and Chris Evans. "
    "Actually all of these actors were casted by Marvel which might be a big influence"
    "in this statistic.")
