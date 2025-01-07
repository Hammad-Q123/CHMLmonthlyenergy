import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Microgrid Analysis Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    # Read the CSV data and parse dates
    df = pd.read_csv('Full Dataset with months.csv')
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    # Add hour and month columns for filtering
    df['Hour'] = df['DateTime'].dt.hour
    df['Month'] = df['DateTime'].dt.strftime('%B')
    return df

# Load the data
df = load_data()

# Sidebar for filters
st.sidebar.header('Filters')

# Month selection
selected_month = st.sidebar.selectbox(
    'Select Month',
    options=df['Month'].unique()
)

# Time range selection within day
hour_range = st.sidebar.slider(
    'Select Hour Range',
    min_value=0,
    max_value=23,
    value=(0, 23)
)

# Filter data based on selections
filtered_df = df[
    (df['Month'] == selected_month) &
    (df['Hour'].between(hour_range[0], hour_range[1]))
]

# Main dashboard
st.title('Microgrid System Analysis Dashboard')

# Top row with key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_pv = filtered_df['PV Production (kWh)'].mean()
    st.metric("Avg PV Production", f"{avg_pv:.2f} kWh")

with col2:
    avg_load = filtered_df['Load Demand (kWh)'].mean()
    st.metric("Avg Load Demand", f"{avg_load:.2f} kWh")

with col3:
    avg_h2_prod = filtered_df['Hydrogen Production (kg)'].mean()
    st.metric("Avg H₂ Production", f"{avg_h2_prod:.2f} kg")

with col4:
    avg_fc_output = filtered_df['Fuel Cell Output (kWh)'].mean()
    st.metric("Avg Fuel Cell Output", f"{avg_fc_output:.2f} kWh")

# Energy Balance Chart
st.subheader('Energy Balance Overview')
energy_fig = go.Figure()

energy_fig.add_trace(go.Scatter(
    x=filtered_df['DateTime'],
    y=filtered_df['PV Production (kWh)'],
    name='PV Production',
    line=dict(color='#FFA500')
))

energy_fig.add_trace(go.Scatter(
    x=filtered_df['DateTime'],
    y=filtered_df['Load Demand (kWh)'],
    name='Load Demand',
    line=dict(color='#FF0000')
))

energy_fig.add_trace(go.Scatter(
    x=filtered_df['DateTime'],
    y=filtered_df['Energy Imported from Grid (kWh)'],
    name='Grid Import',
    line=dict(color='#00FF00')
))

energy_fig.update_layout(
    title='Energy Production vs Demand',
    xaxis_title='Date',
    yaxis_title='Energy (kWh)',
    hovermode='x unified'
)

st.plotly_chart(energy_fig, use_container_width=True)

# Hydrogen System Performance
st.subheader('Hydrogen System Performance')

# Create two columns for hydrogen charts
col1, col2 = st.columns(2)

with col1:
    # Hydrogen Production and Usage
    h2_fig = go.Figure()
    
    h2_fig.add_trace(go.Scatter(
        x=filtered_df['DateTime'],
        y=filtered_df['Hydrogen Production (kg)'],
        name='H₂ Production',
        line=dict(color='#0000FF')
    ))
    
    h2_fig.add_trace(go.Scatter(
        x=filtered_df['DateTime'],
        y=filtered_df['Hydrogen Supply to Fuel Cell (kg)'],
        name='H₂ to Fuel Cell',
        line=dict(color='#800080')
    ))
    
    h2_fig.update_layout(
        title='Hydrogen Production and Usage',
        xaxis_title='Date',
        yaxis_title='Hydrogen (kg)',
        hovermode='x unified'
    )
    
    st.plotly_chart(h2_fig, use_container_width=True)

with col2:
    # System Efficiencies
    eff_fig = go.Figure()
    
    eff_fig.add_trace(go.Scatter(
        x=filtered_df['DateTime'],
        y=filtered_df['Electrolyser Efficiency (%)'],
        name='Electrolyzer Eff.',
        line=dict(color='#4B0082')
    ))
    
    eff_fig.add_trace(go.Scatter(
        x=filtered_df['DateTime'],
        y=filtered_df['Fuel Cell Electrical Efficiency (%)'],
        name='Fuel Cell Eff.',
        line=dict(color='#008080')
    ))
    
    eff_fig.update_layout(
        title='System Efficiencies',
        xaxis_title='Date',
        yaxis_title='Efficiency (%)',
        hovermode='x unified'
    )
    
    st.plotly_chart(eff_fig, use_container_width=True)

# Additional Analysis Section
st.subheader('Daily Patterns')

# Create daily averages
daily_avg = filtered_df.groupby(filtered_df['DateTime'].dt.hour).agg({
    'PV Production (kWh)': 'mean',
    'Load Demand (kWh)': 'mean',
    'Hydrogen Production (kg)': 'mean',
    'Fuel Cell Output (kWh)': 'mean'
}).reset_index()

# Daily patterns chart
daily_fig = go.Figure()

daily_fig.add_trace(go.Scatter(
    x=daily_avg['DateTime'],
    y=daily_avg['PV Production (kWh)'],
    name='Avg PV Production',
    line=dict(color='#FFA500')
))

daily_fig.add_trace(go.Scatter(
    x=daily_avg['DateTime'],
    y=daily_avg['Load Demand (kWh)'],
    name='Avg Load Demand',
    line=dict(color='#FF0000')
))

daily_fig.update_layout(
    title='Daily Energy Patterns',
    xaxis_title='Hour of Day',
    yaxis_title='Energy (kWh)',
    hovermode='x unified'
)

st.plotly_chart(daily_fig, use_container_width=True)
