import streamlit as st
import pandas as pd

# 1. Set up the page configuration (wide mode)
st.set_page_config(page_title="UESA - Underground Extraction & Stability Analyzer", layout="wide", page_icon="⛏️")

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

st.markdown('<div class="main-title">⛏️ Underground Extraction & Stability Analyzer (UESA)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Comprehensive Geomechanics, Blasting, and Extraction Evaluation Suite</div>', unsafe_allow_html=True)

# 3. Create SIX interactive Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 UBC Method Selection", 
    "🧨 Blasting Models", 
    "📳 Vibration Control",
    "🎯 Drill Pattern Design",
    "🏛️ Pillar Design",
    "⛰️ Stope Stability"
])

# --- TAB 1: UBC INPUTS AND RESULTS ---
with tab1:
    st.markdown("### 1. Input Parameters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🌍 Orebody Characteristics")
        general_shape = st.selectbox("General Shape", ["Massive", "Platty-Tabular", "Irregular"])
        ore_thickness = st.selectbox("Ore Thickness", ["Very narrow (< 3 m)", "Narrow (3 - 10 m)", "Intermediate (10 - 30 m)", "Thick (30 - 100 m)", "Very thick (> 100 m)"])
        ore_plunge = st.selectbox("Ore Plunge", ["Flat (< 20°)", "Intermediate (20 - 55°)", "Steep (> 55°)"])
        grade_dist = st.selectbox("Grade Distribution", ["Uniform", "Gradational", "Erratic"])
        depth = st.selectbox("Depth", ["Shallow (0 - 100 m)", "Intermediate (100 - 600 m)", "Deep (> 600 m)"])

    with col2:
        st.markdown("#### 🪨 Rock Mass Rating (RMR)")
        rmr_ore = st.selectbox("RMR (Ore Zone)", ["Very weak (0-20)", "Weak (20-40)", "Moderate (40-60)", "Strong (60-80)", "Very strong (80-100)"])
        rmr_hw = st.selectbox("RMR (Hanging Wall)", ["Very weak (0-20)", "Weak (20-40)", "Moderate (40-60)", "Strong (60-80)", "Very strong (80-100)"])
        rmr_fw = st.selectbox("RMR (Footwall)", ["Very weak (0-20)", "Weak (20-40)", "Moderate (40-60)", "Strong (60-80)", "Very strong (80-100)"])

    with col3:
        st.markdown("#### 🔨 Rock Substance Strength")
        rss_ore = st.selectbox("RSS (Ore Zone)", ["Very weak (<5)", "Weak (5-10)", "Medium (10-15)", "Strong (>15)"])
        rss_hw = st.selectbox("RSS (Hanging Wall)", ["Very weak (<5)", "Weak (5-10)", "Medium (10-15)", "Strong (>15)"])
        rss_fw = st.selectbox("RSS (Footwall)", ["Very weak (<5)", "Weak (5-10)", "Medium (10-15)", "Strong (>15)"])

    # --- THE UBC SCORING MATRIX ---
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

    st.divider()
    st.markdown("### 2. Recommendation Ranking")
    
    if results:
        df_results = pd.DataFrame(results).sort_values(by="Score", ascending=False).reset_index(drop=True)
        top_method = df_results.iloc[0]["Mining Method"]
        top_score = df_results.iloc[0]["Score"]
        
        st.success(f"🏆 **Top Recommendation:** {top_method} (Score: {top_score})")
        
        col_chart, col_table = st.columns([2, 1])
        
        with col_chart:
            st.bar_chart(df_results.set_index("Mining Method"), color="#E67E22")
            
        with col_table:
            st.dataframe(
                df_results.style.highlight_max(subset=['Score'], color='#2ECC71'), 
                use_container_width=True,
                hide_index=True
            )
    else:
        st.error("⚠️ All methods are excluded (-49 penalty hit) based on the current selections.")


# --- TAB 2: BLASTING MODELS ---
with tab2:
    st.markdown("### 🧨 Advanced Blasting Models")
    
    blast_method = st.selectbox(
        "Select Blasting Model",
        [
            "1. Lilly's Blastability Index (BI)",
            "2. Kuz-Ram Fragmentation Model"
        ]
    )
    
    st.divider()

    if "Lilly" in blast_method:
        st.markdown("#### Lilly's Blastability Index (BI)")
        st.markdown("Calculate the theoretical powder factor required for optimal fragmentation.")
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            rmd = st.selectbox("Rock Mass Description (RMD)", [("Powdery/Friable", 10), ("Blocky", 20), ("Massive", 50)], format_func=lambda x: x[0])
            jps = st.selectbox("Joint Plane Spacing (JPS)", [("Close (< 0.1m)", 10), ("Intermediate (0.1 - 1m)", 20), ("Wide (> 1m)", 50)], format_func=lambda x: x[0])
            jpo = st.selectbox("Joint Plane Orientation (JPO)", [("Horizontal", 10), ("Dip out of face", 20), ("Strike normal to face", 30), ("Dip into face", 40)], format_func=lambda x: x[0])
            sg = st.number_input("Specific Gravity of Rock (t/m³)", 1.0, 5.0, 2.7, 0.1)

        with col_b2:
            sgi = 25 * sg - 50
            bi = 0.5 * (rmd[1] + jps[1] + jpo[1] + sgi)
            powder_factor = 0.004 * bi
            
            st.info("#### Results")
            st.metric(label="Calculated Blastability Index (BI)", value=f"{bi:.2f}")
            st.metric(label="Estimated Powder Factor (kg/t)", value=f"{powder_factor:.3f}")
            st.caption("A higher BI indicates rock that is harder to blast, requiring a tighter drill spacing.")

    elif "Kuz-Ram" in blast_method:
        st.markdown("#### Kuz-Ram Fragmentation Model")
        st.markdown("Predict the mean fragment size (X50) to ensure rock passes safely through drawpoints.")
        
        col_k1, col_k2, col_k3 = st.columns(3)
        with col_k1:
            rock_factor = st.slider("Rock Factor (A)", 7.0, 13.0, 8.0, 0.5, help="7 = Medium rock, 13 = Hard rock")
            hole_diam = st.number_input("Hole Diameter (mm)", 50, 200, 89)
            bench_height = st.number_input("Stope/Bench Height (m)", 5.0, 50.0, 20.0)
        with col_k2:
            burden = st.number_input("Burden (m)", 1.0, 10.0, 2.5)
            spacing = st.number_input("Spacing (m)", 1.0, 10.0, 3.0)
            rock_sg = st.number_input("Rock SG (t/m³)", 1.0, 5.0, 2.7)
        with col_k3:
            exp_density = st.number_input("Explosive Density (g/cm³)", 0.5, 1.5, 1.2)
            rws = st.number_input("Relative Weight Strength (ANFO=100)", 50, 150, 115)

        volume = burden * spacing * bench_height
        charge_mass = (3.14159 * (hole_diam/2000)**2) * bench_height * (exp_density * 1000)
        
        if charge_mass > 0 and volume > 0:
            mean_frag = rock_factor * ((volume / charge_mass)**0.8) * (charge_mass**0.16) * ((115 / rws)**0.63)
            pf_volume = charge_mass / volume
            
            st.success("#### Fragmentation Prediction")
            res_col1, res_col2 = st.columns(2)
            res_col1.metric("Mean Fragment Size (X50)", f"{mean_frag * 100:.1f} cm")
            res_col2.metric("Powder Factor", f"{pf_volume:.2f} kg/m³")

# --- TAB 3: VIBRATION CONTROL ---
with tab3:
    st.markdown("### 📳 Ground Vibration Prediction & Control")
    st.markdown("Predict Peak Particle Velocity (PPV) and calculate the allowable Maximum Instantaneous Charge (MIC) using the Scaled Distance Model.")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("**1. Predict Peak Particle Velocity (PPV)**")
        k_factor = st.number_input("Site Constant (K)", 500, 2500, 1140, help="Typical values: Hard rock = 1140, Sedimentary = 500")
        alpha = st.number_input("Attenuation Factor (α)", 1.0, 2.5, 1.6, 0.1)
        dist_to_structure = st.number_input("Distance to Infrastructure (m)", 10.0, 1000.0, 100.0)
        mic_actual = st.number_input("Charge Mass per Delay (W in kg)", 1.0, 500.0, 100.0)
        
        scaled_distance = dist_to_structure / (mic_actual ** 0.5)
        ppv_predicted = k_factor * (scaled_distance ** -alpha)
        
        st.info(f"**Predicted PPV:** {ppv_predicted:.2f} mm/s")
        
    with col_v2:
        st.markdown("**2. Calculate Maximum Allowable Charge (MIC)**")
        st.markdown("Determine the maximum explosives you can detonate per delay to stay below a vibration limit.")
        target_ppv = st.number_input("Maximum Allowable PPV (mm/s)", 5.0, 100.0, 25.0)
        
        max_mic = (dist_to_structure / ((target_ppv / k_factor) ** (-1 / alpha))) ** 2
        
        st.success(f"**Max Charge per Delay (MIC):** {max_mic:.1f} kg")
        
    st.divider()
    st.markdown("""
    **Vibration Control Strategies (Delay Timing):**
    * If the **Predicted PPV** exceeds your regulatory limit (e.g., 25 mm/s), you must reduce the charge weight detonating at any single moment.
    * Use **Electronic Delay Detonators** to separate the blast holes by at least 8 milliseconds.
    * By splitting a 200 kg blast into two 100 kg blasts separated by a delay, the vibration waves will not overlap, keeping ground vibrations safe and protecting the hanging wall from overbreak.
    """)

# --- TAB 4: DRILL PATTERN DESIGN ---
with tab4:
    st.markdown("### 🎯 Underground Drill Pattern Design")
    st.markdown("Calculate geometric layouts for both production stoping and development tunneling based on empirical industry standards.")
    
    drill_mode = st.radio("Select Drilling Type", ["Production (Ring/Bench Drilling)", "Development (Burn Cut Tunneling)"], horizontal=True)
    st.divider()

    if "Production" in drill_mode:
        st.markdown("#### Production Drilling (Stope Ring & Bench Design)")
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            prod_hole_diam = st.number_input("Production Hole Diameter (mm)", 50, 150, 89, step=1, key="prod_hole")
            burden_ratio = st.slider("Burden-to-Diameter Ratio", 25, 40, 30, help="Hard rock usually requires a tighter ratio (closer to 25), while softer rock allows a wider ratio (closer to 40).")
            spacing_ratio = st.slider("Spacing-to-Burden Ratio (S/B)", 1.15, 1.50, 1.25, step=0.05)
            
        with col_d2:
            calc_burden = (prod_hole_diam * burden_ratio) / 1000
            calc_spacing = calc_burden * spacing_ratio
            max_toe_spacing = calc_burden * 1.5
            
            st.success("#### 📐 Recommended Drill Geometry")
            st.metric("Design Burden", f"{calc_burden:.2f} m")
            st.metric("Design Spacing", f"{calc_spacing:.2f} m")
            st.metric("Max Allowable Toe Spacing", f"{max_toe_spacing:.2f} m")
            
        st.caption("⚠️ **Toe Spacing Rule:** In ring/fan drilling, the distance between the ends (toes) of the drill holes must never exceed 1.5x the burden, otherwise massive boulders will form.")

    else:
        st.markdown("#### Development Drilling (Burn Cut Geometry)")
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            dev_hole_diam = st.number_input("Blast Hole Diameter (mm)", 30.0, 60.0, 45.0, step=1.0)
            empty_hole_diam = st.number_input("Empty Relief Hole Diameter (mm)", 76.0, 152.0, 102.0, step=1.0)
            
        with col_t2:
            b1 = (1.5 * empty_hole_diam) / 1000
            max_burden = (0.015 * dev_hole_diam)
            spacing = max_burden * 1.2
            
            st.success("#### 📐 Burn Cut Specifications")
            st.metric("1st Square Burden (Distance from empty hole)", f"{b1:.2f} m")
            st.metric("Max Production Hole Burden", f"{max_burden:.2f} m")
            st.metric("Recommended Spacing", f"{spacing:.2f} m")

# --- TAB 5: PILLAR DESIGN ---
with tab5:
    st.markdown("### 🏛️ Pillar Design & Stability")
    st.markdown("Calculate induced stresses (Tributary Area Theory) and pillar strength (Obert-Duvall) to determine the Factor of Safety (FOS).")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        depth_m = st.number_input("Depth of Cover (m)", 10.0, 3000.0, 500.0)
        rock_density = st.number_input("Rock Density (t/m³)", 1.0, 5.0, 2.7, key="pillar_density")
        extraction_ratio = st.slider("Extraction Ratio (%)", 10, 90, 75) / 100.0
        pillar_width = st.number_input("Pillar Width (W in m)", 2.0, 50.0, 10.0)
        pillar_height = st.number_input("Pillar Height (H in m)", 2.0, 50.0, 15.0)
        ucs = st.number_input("Uniaxial Compressive Strength (UCS in MPa)", 10.0, 300.0, 150.0)

    with col_p2:
        vertical_stress = depth_m * rock_density * 0.00981
        pillar_stress = vertical_stress / (1 - extraction_ratio)
        pillar_strength = ucs * (0.778 + 0.222 * (pillar_width / pillar_height))
        fos = pillar_strength / pillar_stress

        st.info("#### Stress & Strength Results")
        st.metric("Induced Pillar Stress", f"{pillar_stress:.1f} MPa")
        st.metric("Estimated Pillar Strength", f"{pillar_strength:.1f} MPa")
        st.metric("Factor of Safety (FOS)", f"{fos:.2f}")

        if fos >= 1.4:
            st.success("✅ **Stable:** FOS is above the standard industry threshold (1.4).")
        elif fos >= 1.0:
            st.warning("⚠️ **Marginal:** FOS is between 1.0 and 1.4. Pillar may experience localized yielding or scaling.")
        else:
            st.error("❌ **Unstable:** FOS is below 1.0. High risk of pillar failure.")

# --- TAB 6: STOPE STABILITY ---
with tab6:
    st.markdown("### ⛰️ Stope Stability (Mathews Graph)")
    st.markdown("Evaluate open stope surface stability using the Modified Stability Number (N') and Hydraulic Radius (HR).")

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown("**1. Modified Tunnelling Quality Index (Q')**")
        rqd = st.number_input("RQD (%)", 10, 100, 75)
        jn = st.number_input("Joint Set Number (Jn)", 0.5, 20.0, 9.0)
        jr = st.number_input("Joint Roughness (Jr)", 0.5, 4.0, 1.5)
        ja = st.number_input("Joint Alteration (Ja)", 0.75, 20.0, 1.0)
        
        q_prime = (rqd / jn) * (jr / ja)
        st.info(f"**Calculated Q':** {q_prime:.2f}")

    with col_s2:
        st.markdown("**2. Stability Factors**")
        factor_a = st.slider("Rock Stress Factor (A)", 0.1, 1.0, 1.0)
        factor_b = st.slider("Joint Orientation Factor (B)", 0.2, 1.0, 0.2, step=0.01)
        factor_c = st.slider("Gravity/Orientation Factor (C)", 2.0, 8.0, 5.0)

        n_prime = q_prime * factor_a * factor_b * factor_c
        st.success(f"**Modified Stability Number (N'):** {n_prime:.2f}")

    with col_s3:
        st.markdown("**3. Stope Geometry (Hydraulic Radius)**")
        stope_length = st.number_input("Stope Strike Length (m)", 5.0, 100.0, 30.0)
        stope_height = st.number_input("Stope Height (m)", 5.0, 100.0, 40.0)

        hr = (stope_length * stope_height) / (2 * (stope_length + stope_height))
        st.warning(f"**Hydraulic Radius (HR):** {hr:.2f} m")

    st.divider()
    st.markdown("#### 📉 Stability Assessment")
    
    if n_prime > (hr * 2.5):
        st.success("🟩 Based on empirical boundaries, this stope surface is likely **STABLE** without support.")
    elif n_prime > (hr * 0.5):
        st.warning("🟨 This surface is in the **TRANSITION ZONE**. Cable bolting or ground support is highly recommended.")
    else:
        st.error("🟥 This surface falls in the **CAVING ZONE**. Significant dilution or failure is expected. A redesign of the stope dimensions is required.")
