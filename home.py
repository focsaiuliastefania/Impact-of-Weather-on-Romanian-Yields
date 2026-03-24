import streamlit as st
import pandas as pd

st.set_page_config(page_title="Agro-Expansion: Impact of Weather on Romanian Yields", layout="wide")

st.markdown("""
    <style>
    div.stButton > button {
        background-color: #98FF98;
        color: black;
        border-radius: 10px;
        border: none;
        height: 3em;
        width: 100%;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #77DD77;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("Navigation")
    st.info("Select a module:")
    if st.button("📊 Visual Analytics"):
        st.session_state.page = "page_1"
    if st.button("⚙️ Predictive Models"):
        st.session_state.page = "page_2"

st.title("🌱 Home: Agro-Expansion: Impact of Weather on Romanian Yields")

DATA_PATH = 'project.csv' 
if 'df' not in st.session_state:
    try:
        df = pd.read_csv(DATA_PATH)
        st.session_state.df = df[df['Years'] >= 2011]
        st.success("Database connected successfully!")
    except:
        st.error("File 'project.csv' not found.")

if "page" in st.session_state:
    if st.session_state.page == "page_1":
        with open("page_1.py", encoding="utf-8") as f:
            exec(f.read(), {'st': st})
    elif st.session_state.page == "page_2":
        with open("page_2.py", encoding="utf-8") as f:
            exec(f.read(), {'st': st})
else:
    st.write(
    "This project analyzes how climatic factors influence the production of major " \
    "spring crops in Romania, such as corn and sunflower. By combining historical weather" \
    " data with agricultural yield statistics, we aim to identify the main environmental drivers " \
    "of crop success and explore regional patterns for future agricultural expansion.")