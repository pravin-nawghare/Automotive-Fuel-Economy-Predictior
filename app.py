import streamlit as st
from predict import show_predict_page
from explore import show_explore_page


# show_predict_page()
# show_explore_page()

st.sidebar.title("Please choose....")
page = st.sidebar.selectbox("Explore or Predict", ["Explore","Predict"])

if page == "Explore":
    show_explore_page()
else:
    show_predict_page()


    