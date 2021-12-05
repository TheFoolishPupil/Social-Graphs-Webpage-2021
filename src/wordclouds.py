import streamlit as st


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
