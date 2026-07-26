import streamlit as st
import pandas as pd
import numpy as np

# Set up the page
st.set_page_config(page_title="UBC Mining Method Selector", layout="wide")
st.title("⛏️ UBC Mining Method Selection Tool")
st.markdown("Based on the UBC methodology for underground mining method selection.")

# Sidebar for User Inputs
st.sidebar.header("Orebody Characteristics")

general_shape = st.sidebar.selectbox(
    "General Shape", 
    ["Massive", "Platty-Tabular", "Irregular"]
)

ore_thickness = st.sidebar.selectbox(
    "Ore Thickness", 
    ["Very narrow (<3m)", "Narrow (3-10m)", "Intermediate (10-30m)", "Thick (30-100m)", "Very thick (>100m)"]
)

ore_plunge = st.sidebar.selectbox(
    "Ore Plunge", 
    ["Flat (<20°)", "Intermediate (20-55°)", "Steep (>55°)"]
)

# You would add the rest of your inputs here (Grade Distribution, Depth, RMR, RSS, etc.)
st.sidebar.header("Rock Mechanics")
rmr_ore = st.sidebar.slider("Rock Mass Rating (Ore Zone)", 0, 100, 50)

# Main Page - Logic & Results
st.write("### Recommended Mining Methods")

# TODO: Load the scoring matrix from 'UBC Mining Method Selection 251016.xlsx'
# and calculate the total scores for each mining method based on the sidebar inputs.
# For example, if General Shape == 'Massive', Open Pit gets 4 points, Block Caving gets 4 points, etc.

# Placeholder for results
results = {
    "Mining Method": ["Cut & Fill Stoping", "Shrinkage Stoping", "Open Pit Mining"],
    "Score": [24, 18, -49] # Example scores
}

df_results = pd.DataFrame(results)

# Filter out excluded methods (-49 points means exclusion)
df_valid = df_results[df_results["Score"] > 0].sort_values(by="Score", ascending=False)

st.table(df_valid)