import streamlit as st
import pandas as pd

# 1. Set up the page configuration (wide mode)
st.set_page_config(page_title="UBC Mining Method Selector", layout="wide", page_icon="⛏️")

# 2. Inject Custom HTML/CSS for advanced styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #E67E22;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        padding-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        color: #7F8C8D;
        margin-bottom: 30px;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⛏️ UBC Mining Method Selection Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Advanced evaluation dashboard based on the UBC methodology</div>', unsafe_allow_html=True)

# 3. Create interactive Tabs for a cleaner layout
tab1, tab2 = st.tabs(["📋 Input Parameters", "📊 Results & Analysis"])

with tab1:
    # 4. Use columns to organize the inputs side-by-side
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🌍 Orebody Characteristics")
        general_shape = st.selectbox("General Shape", ["Massive", "Platty-Tabular", "Irregular"])
        ore_thickness = st.selectbox("Ore Thickness", ["Very narrow (< 3 m)", "Narrow (3 - 10 m)", "Intermediate (10 - 30 m)", "Thick (30 - 100 m)", "Very thick (> 100 m)"])
        ore_plunge = st.selectbox("Ore Plunge", ["Flat (< 20°)", "Intermediate (20 - 55°)", "Steep (> 55°)"])
        grade_dist = st.selectbox("Grade Distribution", ["Uniform", "Gradational", "Erratic"])
        depth = st.selectbox("Depth", ["Shallow (0 - 100 m)", "Intermediate (100 - 600 m)", "Deep (> 600 m)"])

    with col2:
        st.markdown("### 🪨 Rock Mass Rating (RMR)")
        rmr_ore = st.selectbox("RMR (Ore Zone)", ["Very weak (0-20)", "Weak (20-40)", "Moderate (40-60)", "Strong (60-80)", "Very strong (80-100)"])
        rmr_hw = st.selectbox("RMR (Hanging Wall)", ["Very weak (0-20)", "Weak (20-40)", "Moderate (40-60)", "Strong (60-80)", "Very strong (80-100)"])
        rmr_fw = st.selectbox("RMR (Footwall)", ["Very weak (0-20)", "Weak (20-40)", "Moderate (40-60)", "Strong (60-80)", "Very strong (80-100)"])

    with col3:
        st.markdown("### 🔨 Rock Substance Strength")
        rss_ore = st.selectbox("RSS (Ore Zone)", ["Very weak (<5)", "Weak (5-10)", "Medium (10-15)", "Strong (>15)"])
        rss_hw = st.selectbox("RSS (Hanging Wall)", ["Very weak (<5)", "Weak (5-10)", "Medium (10-15)", "Strong (>15)"])
        rss_fw = st.selectbox("RSS (Footwall)", ["Very weak (<5)", "Weak (5-10)", "Medium (10-15)", "Strong (>15)"])

# --- THE UBC SCORING MATRIX ---
# (Paste the exact same 'scoring_matrix' dictionary from the previous code here!)
scoring_matrix = {
    'Block Caving': {
        'Depth': {'Deep (> 600 m)': 3, 'Intermediate (100 - 600 m)': 3, 'Shallow (0 - 100 m)': 2},
        'General Shape': {'Irregular': 0, 'Massive': 4, 'Platty-Tabular': 2},
        'Grade Distribution': {'Erratic': 2, 'Gradational': 2, 'Uniform': 3},
        'Ore Plunge': {'Flat (< 20°)': 3, 'Intermediate (20 - 55°)': 2, 'Steep (> 55°)': 4},
        'Ore Thickness': {'Intermediate (10 - 30 m)': 0, 'Narrow (3 - 10 m)': -49, 'Thick (30 - 100 m)': 3, 'Very narrow (< 3 m)': -49, 'Very thick (> 100 m)': 4},
        'RMR (Footwall)': {'Moderate (40-60)': 3, 'Strong (60-80)': 2, 'Very strong (80-100)': 2, 'Very weak (0-20)': 3, 'Weak (20-40)': 3},
        'RMR (Hanging Wall)': {'Moderate (40-60)': 3, 'Strong (60-80)': 2, 'Very strong (80-100)': 2, 'Very weak (0-20)': 3, 'Weak (20-40)': 3},
        'RMR (Ore Zone)': {'Moderate (40-60)': 2, 'Strong (60-80)': 0, 'Very strong (80-100)': -49, 'Very weak (0-20)': 4, 'Weak (20-40)': 3},
        'RSS (Footwall)': {'Medium (10-15)': 2, 'Strong (>15)': 1, 'Very weak (<5)': 4, 'Weak (5-10)': 3},
        'RSS (Hanging Wall)': {'Medium (10-15)': 2, 'Strong (>15)': 0, 'Very weak (<5)': 4, 'Weak (5-10)': 3},
        'RSS (Ore Zone)': {'Medium (10-15)': 1, 'Strong (>15)': 0, 'Very weak (<5)': 4, 'Weak (5-10)': 2}
    },
    'Cut & Fill Stoping': {
        'Depth': {'Deep (> 600 m)': 4, 'Intermediate (100 - 600 m)': 3, 'Shallow (0 - 100 m)': 2},
        'General Shape': {'Irregular': 4, 'Massive': 1, 'Platty-Tabular': 4},
        'Grade Distribution': {'Erratic': 4, 'Gradational': 3, 'Uniform': 2},
        'Ore Plunge': {'Flat (< 20°)': 1, 'Intermediate (20 - 55°)': 3, 'Steep (> 55°)': 4},
        'Ore Thickness': {'Intermediate (10 - 30 m)': 4, 'Narrow (3 - 10 m)': 4, 'Thick (30 - 100 m)': 1, 'Very narrow (< 3 m)': 3, 'Very thick (> 100 m)': 0},
        'RMR (Footwall)': {'Moderate (40-60)': 2, 'Strong (60-80)': 2, 'Very strong (80-100)': 2, 'Very weak (0-20)': 3, 'Weak (20-40)': 3},
        'RMR (Hanging Wall)': {'Moderate (40-60)': 4, 'Strong (60-80)': 3, 'Very strong (80-100)': 3, 'Very weak (0-20)': 3, 'Weak (20-40)': 5},
        'RMR (Ore Zone)': {'Moderate (40-60)': 2, 'Strong (60-80)': 3, 'Very strong (80-100)': 3, 'Very weak (0-20)': 0, 'Weak (20-40)': 1},
        'RSS (Footwall)': {'Medium (10-15)': 2, 'Strong (>15)': 2, 'Very weak (<5)': 1, 'Weak (5-10)': 3},
        'RSS (Hanging Wall)': {'Medium (10-15)': 4, 'Strong (>15)': 2, 'Very weak (<5)': 3, 'Weak (5-10)': 5},
        'RSS (Ore Zone)': {'Medium (10-15)': 3, 'Strong (>15)': 3, 'Very weak (<5)': 0, 'Weak (5-10)': 1}
    },
    'Longwall Mining': {
        'Depth': {'Deep (> 600 m)': 3, 'Intermediate (100 - 600 m)': 2, 'Shallow (0 - 100 m)': 2},
        'General Shape': {'Irregular': -49, 'Massive': -49, 'Platty-Tabular': 4},
        'Grade Distribution': {'Erratic': 0, 'Gradational': 1, 'Uniform': 4},
        'Ore Plunge': {'Flat (< 20°)': 4, 'Intermediate (20 - 55°)': 0, 'Steep (> 55°)': -49},
        'Ore Thickness': {'Intermediate (10 - 30 m)': 0, 'Narrow (3 - 10 m)': 3, 'Thick (30 - 100 m)': -49, 'Very narrow (< 3 m)': 4, 'Very thick (> 100 m)': -49},
        'RMR (Footwall)': {'Moderate (40-60)': 0, 'Strong (60-80)': 0, 'Very strong (80-100)': 0, 'Very weak (0-20)': 0, 'Weak (20-40)': 0},
        'RMR (Hanging Wall)': {'Moderate (40-60)': 4, 'Strong (60-80)': 3, 'Very strong (80-100)': 3, 'Very weak (0-20)': 6, 'Weak (20-40)': 5},
        'RMR (Ore Zone)': {'Moderate (40-60)': 4, 'Strong (60-80)': 2, 'Very strong (80-100)': 2, 'Very weak (0-20)': 6, 'Weak (20-40)': 6},
        'RSS (Footwall)': {'Medium (10-15)': 0, 'Strong (>15)': 0, 'Very weak (<5)': 0, 'Weak (5-10)': 0},
        'RSS (Hanging Wall)': {'Medium (10-15)': 2, 'Strong (>15)': 2, 'Very weak (<5)': 6, 'Weak (5-10)': 5},
        'RSS (Ore Zone)': {'Medium (10-15)': 2, 'Strong (>15)': 1, 'Very weak (<5)': 6, 'Weak (5-10)': 5}
    },
    'Open Pit Mining': {
        'Depth': {'Deep (> 600 m)': -49, 'Intermediate (100 - 600 m)': 0, 'Shallow (0 - 100 m)': 4},
        'General Shape': {'Irregular': 3, 'Massive': 4, 'Platty-Tabular': 2},
        'Grade Distribution': {'Erratic': 2, 'Gradational': 3, 'Uniform': 3},
        'Ore Plunge': {'Flat (< 20°)': 3, 'Intermediate (20 - 55°)': 3, 'Steep (> 55°)': 1},
        'Ore Thickness': {'Intermediate (10 - 30 m)': 3, 'Narrow (3 - 10 m)': 2, 'Thick (30 - 100 m)': 4, 'Very narrow (< 3 m)': 1, 'Very thick (> 100 m)': 4},
        'RMR (Footwall)': {'Moderate (40-60)': 4, 'Strong (60-80)': 4, 'Very strong (80-100)': 4, 'Very weak (0-20)': 2, 'Weak (20-40)': 3},
        'RMR (Hanging Wall)': {'Moderate (40-60)': 4, 'Strong (60-80)': 4, 'Very strong (80-100)': 4, 'Very weak (0-20)': 2, 'Weak (20-40)': 3},
        'RMR (Ore Zone)': {'Moderate (40-60)': 3, 'Strong (60-80)': 3, 'Very strong (80-100)': 3, 'Very weak (0-20)': 3, 'Weak (20-40)': 3},
        'RSS (Footwall)': {'Medium (10-15)': 4, 'Strong (>15)': 4, 'Very weak (<5)': 3, 'Weak (5-10)': 3},
        'RSS (Hanging Wall)': {'Medium (10-15)': 4, 'Strong (>15)': 4, 'Very weak (<5)': 3, 'Weak (5-10)': 3},
        'RSS (Ore Zone)': {'Medium (10-15)': 3, 'Strong (>15)': 3, 'Very weak (<5)': 4, 'Weak (5-10)': 3}
    },
    'Room and Pillar Mining': {
        'Depth': {'Deep (> 600 m)': 2, 'Intermediate (100 - 600 m)': 3, 'Shallow (0 - 100 m)': 3},
        'General Shape': {'Irregular': 2, 'Massive': 0, 'Platty-Tabular': 4},
        'Grade Distribution': {'Erratic': 0, 'Gradational': 2, 'Uniform': 4},
        'Ore Plunge': {'Flat (< 20°)': 4, 'Intermediate (20 - 55°)': 0, 'Steep (> 55°)': -49},
        'Ore Thickness': {'Intermediate (10 - 30 m)': 1, 'Narrow (3 - 10 m)': 3, 'Thick (30 - 100 m)': -49, 'Very narrow (< 3 m)': 4, 'Very thick (> 100 m)': -49},
        'RMR (Footwall)': {'Moderate (40-60)': 0, 'Strong (60-80)': 0, 'Very strong (80-100)': 0, 'Very weak (0-20)': 0, 'Weak (20-40)': 0},
        'RMR (Hanging Wall)': {'Moderate (40-60)': 3, 'Strong (60-80)': 5, 'Very strong (80-100)': 6, 'Very weak (0-20)': -49, 'Weak (20-40)': 0},
        'RMR (Ore Zone)': {'Moderate (40-60)': 3, 'Strong (60-80)': 5, 'Very strong (80-100)': 6, 'Very weak (0-20)': -49, 'Weak (20-40)': 0},
        'RSS (Footwall)': {'Medium (10-15)': 0, 'Strong (>15)': 0, 'Very weak (<5)': 0, 'Weak (5-10)': 0},
        'RSS (Hanging Wall)': {'Medium (10-15)': 2, 'Strong (>15)': 6, 'Very weak (<5)': 0, 'Weak (5-10)': 0},
        'RSS (Ore Zone)': {'Medium (10-15)': 3, 'Strong (>15)': 6, 'Very weak (<5)': 0, 'Weak (5-10)': 0}
    },
    'Shrinkage Stoping': {
        'Depth': {'Deep (> 600 m)': 2, 'Intermediate (100 - 600 m)': 3, 'Shallow (0 - 100 m)': 3},
        'General Shape': {'Irregular': 2, 'Massive': 0, 'Platty-Tabular': 4},
        'Grade Distribution': {'Erratic': 2, 'Gradational': 2, 'Uniform': 3},
        'Ore Plunge': {'Flat (< 20°)': -49, 'Intermediate (20 - 55°)': 0, 'Steep (> 55°)': 4},
        'Ore Thickness': {'Intermediate (10 - 30 m)': 0, 'Narrow (3 - 10 m)': 4, 'Thick (30 - 100 m)': -49, 'Very narrow (< 3 m)': 4, 'Very thick (> 100 m)': -49},
        'RMR (Footwall)': {'Moderate (40-60)': 2, 'Strong (60-80)': 3, 'Very strong (80-100)': 3, 'Very weak (0-20)': 0, 'Weak (20-40)': 0},
        'RMR (Hanging Wall)': {'Moderate (40-60)': 2, 'Strong (60-80)': 4, 'Very strong (80-100)': 4, 'Very weak (0-20)': 0, 'Weak (20-40)': 0},
        'RMR (Ore Zone)': {'Moderate (40-60)': 3, 'Strong (60-80)': 3, 'Very strong (80-100)': 3, 'Very weak (0-20)': 0, 'Weak (20-40)': 1},
        'RSS (Footwall)': {'Medium (10-15)': 3, 'Strong (>15)': 3, 'Very weak (<5)': 0, 'Weak (5-10)': 2},
        'RSS (Hanging Wall)': {'Medium (10-15)': 3, 'Strong (>15)': 4, 'Very weak (<5)': 0, 'Weak (5-10)': 1},
        'RSS (Ore Zone)': {'Medium (10-15)': 3, 'Strong (>15)': 4, 'Very weak (<5)': 0, 'Weak (5-10)': 1}
    },
    'Sublevel Caving': {
        'Depth': {'Deep (> 600 m)': 2, 'Intermediate (100 - 600 m)': 2, 'Shallow (0 - 100 m)': 3},
        'General Shape': {'Irregular': 1, 'Massive': 3, 'Platty-Tabular': 4},
        'Grade Distribution': {'Erratic': 2, 'Gradational': 2, 'Uniform': 3},
        'Ore Plunge': {'Flat (< 20°)': 1, 'Intermediate (20 - 55°)': 1, 'Steep (> 55°)': 4},
        'Ore Thickness': {'Intermediate (10 - 30 m)': 0, 'Narrow (3 - 10 m)': -49, 'Thick (30 - 100 m)': 4, 'Very narrow (< 3 m)': -49, 'Very thick (> 100 m)': 4},
        'RMR (Footwall)': {'Moderate (40-60)': 3, 'Strong (60-80)': 3, 'Very strong (80-100)': 3, 'Very weak (0-20)': 1, 'Weak (20-40)': 2},
        'RMR (Hanging Wall)': {'Moderate (40-60)': 3, 'Strong (60-80)': 2, 'Very strong (80-100)': 2, 'Very weak (0-20)': 4, 'Weak (20-40)': 4},
        'RMR (Ore Zone)': {'Moderate (40-60)': 3, 'Strong (60-80)': 1, 'Very strong (80-100)': 0, 'Very weak (0-20)': 3, 'Weak (20-40)': 4},
        'RSS (Footwall)': {'Medium (10-15)': 2, 'Strong (>15)': 2, 'Very weak (<5)': 1, 'Weak (5-10)': 2},
        'RSS (Hanging Wall)': {'Medium (10-15)': 2, 'Strong (>15)': 1, 'Very weak (<5)': 4, 'Weak (5-10)': 3},
        'RSS (Ore Zone)': {'Medium (10-15)': 3, 'Strong (>15)': 2, 'Very weak (<5)': 2, 'Weak (5-10)': 3}
    },
    'Sublevel Stoping': {
        'Depth': {'Deep (> 600 m)': 2, 'Intermediate (100 - 600 m)': 4, 'Shallow (0 - 100 m)': 3},
        'General Shape': {'Irregular': 1, 'Massive': 3, 'Platty-Tabular': 4},
        'Grade Distribution': {'Erratic': 3, 'Gradational': 4, 'Uniform': 4},
        'Ore Plunge': {'Flat (< 20°)': 2, 'Intermediate (20 - 55°)': 1, 'Steep (> 55°)': 4},
        'Ore Thickness': {'Intermediate (10 - 30 m)': 3, 'Narrow (3 - 10 m)': 1, 'Thick (30 - 100 m)': 4, 'Very narrow (< 3 m)': -10, 'Very thick (> 100 m)': 3},
        'RMR (Footwall)': {'Moderate (40-60)': 2, 'Strong (60-80)': 3, 'Very strong (80-100)': 3, 'Very weak (0-20)': 0, 'Weak (20-40)': 0},
        'RMR (Hanging Wall)': {'Moderate (40-60)': 3, 'Strong (60-80)': 4, 'Very strong (80-100)': 4, 'Very weak (0-20)': -49, 'Weak (20-40)': 0},
        'RMR (Ore Zone)': {'Moderate (40-60)': 4, 'Strong (60-80)': 4, 'Very strong (80-100)': 4, 'Very weak (0-20)': 1, 'Weak (20-40)': 3},
        'RSS (Footwall)': {'Medium (10-15)': 3, 'Strong (>15)': 3, 'Very weak (<5)': 0, 'Weak (5-10)': 1},
        'RSS (Hanging Wall)': {'Medium (10-15)': 4, 'Strong (>15)': 5, 'Very weak (<5)': 0, 'Weak (5-10)': 1},
        'RSS (Ore Zone)': {'Medium (10-15)': 4, 'Strong (>15)': 4, 'Very weak (<5)': 0, 'Weak (5-10)': 2}
    }
}

# --- CALCULATION LOGIC ---
selections = {
    'General Shape': general_shape, 'Ore Thickness': ore_thickness, 'Ore Plunge': ore_plunge,
    'Grade Distribution': grade_dist, 'Depth': depth,
    'RMR (Ore Zone)': rmr_ore, 'RMR (Hanging Wall)': rmr_hw, 'RMR (Footwall)': rmr_fw,
    'RSS (Ore Zone)': rss_ore, 'RSS (Hanging Wall)': rss_hw, 'RSS (Footwall)': rss_fw
}

results = []
for method, categories in scoring_matrix.items():
    total_score = 0
    excluded = False
    
    for category, selected_option in selections.items():
        points = categories[category][selected_option]
        if points == -49:
            excluded = True
            break
        total_score += points
        
    if not excluded:
        results.append({"Mining Method": method, "Score": total_score})

# --- TAB 2: VISUAL RESULTS ---
with tab2:
    st.markdown("### Recommendation Ranking")
    
    if results:
        # Sort results
        df_results = pd.DataFrame(results).sort_values(by="Score", ascending=False).reset_index(drop=True)
        top_method = df_results.iloc[0]["Mining Method"]
        top_score = df_results.iloc[0]["Score"]
        
        # 5. Highlight the top recommendation distinctly
        st.success(f"🏆 **Top Recommendation:** {top_method} (Score: {top_score})")
        
        col_chart, col_table = st.columns([2, 1])
        
        with col_chart:
            # 6. Add a visual bar chart comparison
            st.bar_chart(df_results.set_index("Mining Method"), color="#E67E22")
            
        with col_table:
            # 7. Make the dataframe look nicer
            st.dataframe(
                df_results.style.highlight_max(subset=['Score'], color='#2ECC71'), 
                use_container_width=True,
                hide_index=True
            )
    else:
        st.error("⚠️ All methods are excluded (-49 penalty hit) based on the current selections.")
