import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page setup
st.set_page_config(page_title="Microgrid Analysis", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('Full Dataset (2).csv')
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['Month'] = df['DateTime'].dt.strftime('%B')
    return df

# Test if the app is working
st.title('Microgrid Analysis Dashboard')
st.write('Setting up the dashboard...')
