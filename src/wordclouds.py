import streamlit as st
from constants import GENRE_TF_IDF_DATA
import ast

def render_genre_tf_idf():
    st.text("")
    st.write(f"### Top 10 words according to TF:")
    for index, row in GENRE_TF_IDF_DATA.head(13).iterrows():
        li = ast.literal_eval(row.Top_10_TF)
        words = ', '.join(li)
        st.write(f"**{row.Genre}** : {words}")

    st.text("")
    st.write(f"### Top 10 words according to TF-IDF:")
    for index, row in GENRE_TF_IDF_DATA.head(13).iterrows():
        li = ast.literal_eval(row.Top_10_TF_IDF)
        words = ', '.join(li)
        st.write(f"**{row.Genre}** : {words}")

def render_word_clouds():
    """Renders wordclouds on the page."""

    col1, col2, col3 = st.columns(3)
    col1.image("img/Action.png")
    col1.markdown(
        "<h3 style='text-align: center; '>Action</h3>",
        unsafe_allow_html=True,
    )
    col2.image("img/Adventure.png")
    col2.markdown(
        "<h3 style='text-align: center; '>Adventure</h3>",
        unsafe_allow_html=True,
    )
    col3.image("img/Animation.png")
    col3.markdown(
        "<h3 style='text-align: center; '>Animation</h3>",
        unsafe_allow_html=True,
    )
    with st.expander("See all word clouds"):
        col1, col2, col3 = st.columns(3)

        col1.image("img/Biography.png")
        col1.markdown(
            "<h3 style='text-align: center; '>Biography</h3>",
            unsafe_allow_html=True,
        )
        col2.image("img/Comedy.png")
        col2.markdown(
            "<h3 style='text-align: center; '>Comedy</h3>",
            unsafe_allow_html=True,
        )
        col3.image("img/Crime.png")
        col3.markdown(
            "<h3 style='text-align: center; '>Crime</h3>",
            unsafe_allow_html=True,
        )
        col1.write("***")
        col2.write("***")
        col3.write("***")

        col1.image("img/Documentary.png")
        col1.markdown(
            "<h3 style='text-align: center; '>Documentary</h3>",
            unsafe_allow_html=True,
        )
        col2.image("img/Drama.png")
        col2.markdown(
            "<h3 style='text-align: center; '>Drama</h3>",
            unsafe_allow_html=True,
        )
        col3.image("img/Family.png")
        col3.markdown(
            "<h3 style='text-align: center; '>Fantasy</h3>",
            unsafe_allow_html=True,
        )
        col1.write("***")
        col2.write("***")
        col3.write("***")

        col1.image("img/History.png")
        col1.markdown(
            "<h3 style='text-align: center; '>History</h3>",
            unsafe_allow_html=True,
        )
        col2.image("img/Horror.png")
        col2.markdown(
            "<h3 style='text-align: center; '>Horror</h3>",
            unsafe_allow_html=True,
        )
        col3.image("img/Music.png")
        col3.markdown(
            "<h3 style='text-align: center; '>Music</h3>",
            unsafe_allow_html=True,
        )
        col1.write("***")
        col2.write("***")
        col3.write("***")

        col1.image("img/Musical.png")
        col1.markdown(
            "<h3 style='text-align: center; '>Musical</h3>",
            unsafe_allow_html=True,
        )
        col2.image("img/Mystery.png")
        col2.markdown(
            "<h3 style='text-align: center; '>Mystery</h3>",
            unsafe_allow_html=True,
        )
        col3.image("img/Romance.png")
        col3.markdown(
            "<h3 style='text-align: center; '>Romance</h3>",
            unsafe_allow_html=True,
        )
        col1.write("***")
        col2.write("***")
        col3.write("***")

        col1.image("img/Sci-Fi.png")
        col1.markdown(
            "<h3 style='text-align: center; '>Sci-Fi</h3>",
            unsafe_allow_html=True,
        )
        col2.image("img/Thriller.png")
        col2.markdown(
            "<h3 style='text-align: center; '>Thriller</h3>",
            unsafe_allow_html=True,
        )
        col3.image("img/War.png")
        col3.markdown(
            "<h3 style='text-align: center; '>War</h3>",
            unsafe_allow_html=True,
        )
        col1.write("***")
        col2.write("***")
        col3.write("***")

        col1.image("img/Western.png")
        col1.markdown(
            "<h3 style='text-align: center; '>Western</h3>",
            unsafe_allow_html=True,
        )

def render_wordcloud_text():
    st.write(f"From the generated wordclouds we can see that almost all genres are mostly "
    "described by the name of their characters, same way as before. Again, we "
    "would ideally want names to be filtered out so that we could comment on the"
    " language used in different genres. This wasn't practically feasible so we "
    "need to interperet the wordclouds differently. Instead of telling us about "
    "the general language used in a particular genre, the wordclouds tell us, "
    "through the character names, which film titles are the most popular in a "
    "genre and have become cult favorites.")

    st.text("")
    st.write(f"**Shrek** has become a very popular movie and has attained a cultural "
    "  status. This can be seen from our worldclouds, since Shrek is one of "
    "  the top words in genres *Romance, Family, Animation, Fantasy*")

    st.text("")
    st.write(f"**Katniss** is also a very prevelant character name throughout our wordclouds."
    "  This also makes sense, since Katniss is the protagonist of the *Hunger Games*"
    "  series which consists of four movies and had a large fanbase.")

    st.text("")
    st.write(f"Same goes for **Bella** and **Edward**, the main characters of the *Twilight* "
    " *series* but also **Stark, Thor, Logan** from the *Avenges* and **Frodo, Gandalf**"
    "  from *The Lord of the Rings*. It seems movie series have a great influence over"
    "  our wordclouds.")

    st.text("")
    st.write(f"Since **Jackass** is the only movie in the *Documentary* category we get"
    " a wordcloud only from its own plot. This is why we have more non-character"
    " words in this wordcloud.")
