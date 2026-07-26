# --- TAB 3: BLAST DESIGN ---
with tab3:
    st.markdown("### 🧨 Advanced Drill & Blast Design")
    
    # Dropdown to select which blasting standard to use
    blast_method = st.selectbox(
        "Select Blasting Design Standard",
        [
            "1. Lilly's Blastability Index (BI)",
            "2. Kuz-Ram Fragmentation Model",
            "3. Langefors & Kihlström (Tunnel/Drift Development)",
            "4. Holmberg-Persson (Contour/Perimeter Blasting)"
        ]
    )
    
    st.divider()

    # --- 1. LILLY'S BI ---
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

    # --- 2. KUZ-RAM MODEL ---
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

        # Calculations
        volume = burden * spacing * bench_height
        tonnage = volume * rock_sg
        charge_mass = (3.14159 * (hole_diam/2000)**2) * bench_height * (exp_density * 1000)
        
        if charge_mass > 0:
            mean_frag = rock_factor * ((volume / charge_mass)**0.8) * (charge_mass**0.16) * ((115 / rws)**0.63)
            pf_volume = charge_mass / volume
            
            st.success("#### Fragmentation Prediction")
            res_col1, res_col2 = st.columns(2)
            res_col1.metric("Mean Fragment Size (X50)", f"{mean_frag * 100:.1f} cm")
            res_col2.metric("Powder Factor", f"{pf_volume:.2f} kg/m³")

    # --- 3. LANGEFORS & KIHLSTRÖM ---
    elif "Langefors" in blast_method:
        st.markdown("#### Langefors & Kihlström (Development Blasting)")
        st.markdown("Empirical design for burn cuts in tunnel development (creating access drives).")
        
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            hole_diam_mm = st.number_input("Production Hole Diameter (mm)", 30.0, 100.0, 45.0)
            empty_hole_diam = st.number_input("Empty Relief Hole Diameter (mm)", 50.0, 200.0, 102.0)
        
        with col_l2:
            # Empirical rules of thumb based on L&K
            b1 = 1.5 * empty_hole_diam # First square burden
            max_burden = 0.015 * hole_diam_mm * 1000 # general empirical rule translated to mm
            spacing = max_burden * 1.2 
            
            st.info("#### Initial Cut Geometry")
            st.metric("1st Square Burden (B1)", f"{b1:.1f} mm")
            st.metric("Recommended Max Stope Burden", f"{max_burden:.0f} mm")
            st.metric("Recommended Stope Spacing", f"{spacing:.0f} mm")

    # --- 4. HOLMBERG-PERSSON ---
    elif "Holmberg" in blast_method:
        st.markdown("#### Holmberg-Persson (Contour Blasting)")
        st.markdown("Design smooth-wall perimeter blasting to protect the hanging wall and footwall from damage.")
        
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            perimeter_diam = st.number_input("Perimeter Hole Diameter (mm)", 30, 100, 45)
            rock_cond = st.selectbox("Rock Condition", ["Good", "Average", "Poor"])
            
        with col_h2:
            # Empirical spacing calculation (15 to 16 times hole diameter)
            multiplier = 16 if rock_cond == "Good" else (15 if rock_cond == "Average" else 14)
            p_spacing = (multiplier * perimeter_diam) / 1000  # Convert to meters
            p_burden = p_spacing * 1.25
            charge_concentration = 90 * ((perimeter_diam/1000)**2) # kg/m
            
            st.info("#### Contour Design Variables")
            st.metric("Perimeter Spacing", f"{p_spacing:.2f} m")
            st.metric("Perimeter Burden", f"{p_burden:.2f} m")
            st.metric("Linear Charge Concentration", f"{charge_concentration:.3f} kg/m")
