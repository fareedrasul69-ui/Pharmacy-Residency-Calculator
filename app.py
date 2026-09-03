import streamlit as st
import pandas as pd

st.set_page_config(page_title="Residency Match Analyzer", layout="wide")

# Custom CSS injected to enforce text-wrapping and clean container formatting
st.markdown("""
    <style>
    .wrapped-box {
        background-color: #f0f2f6;
        border: 2px solid #ff4b4b;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
        color: #111111;
        margin-bottom: 15px;
    }
    .highlight-fit {
        background-color: #e6f4ea;
        border: 2px solid #34a853;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        color: #137333;
        text-align: center;
    }
    /* Enforce text wrapping across dataframes */
    .stDataFrame {
        word-wrap: break-word;
    }
    </style>
""", unsafe_allow_html=True)

# Dummy dataset initialization for demonstration
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Candidate_Name": ["Jane Doe", "John Smith"],
        "Candidate_Scores": ["Step 1: Pass | Step 2: 255", "Step 1: Pass | Step 2: 240"],
        "Program_Name": ["General Surgery - Mass General", "Internal Medicine - Mayo Clinic"],
        "Program_Intensity": ["High Volume / Academic", "Moderate / Community-Academic"],
        "Tier": ["Top Tier", "Mid Tier"],
        "Fit_Status": ["Target", "Safety"],
        "Likelihood_Definition": ["High interview conversion based on historical quartile alignment.", "Very high match probability given step filters and geographic preference."],
        "Recommendation": ["Strongly apply; emphasize research portfolio in personal statement.", "Safety choice; highlight longitudinal primary care experience."]
    })

df = st.session_state.data

# Sidebar Navigation
tab = st.sidebar.radio("Navigation", ["Program Query", "Exploration Matrix", "Candidate Profile"])

def render_split_layout(candidate_content_func, school_content_func):
    """Utility to enforce candidate info on the left, school info + tier on the right."""
    left_col, right_col = st.columns([1, 1])
    with left_col:
        st.subheader("Candidate Information")
        candidate_content_func()
    with right_col:
        st.subheader("School Information & Tier")
        school_content_func()

if tab == "Program Query":
    st.title("Program Query")
    
    # Filter selection
    selected_program = st.selectbox("Select Program to Query", df["Program_Name"].unique())
    prog_row = df[df["Program_Name"] == selected_program].iloc[0]
    
    def render_candidate_side():
        st.write(f"**Name:** {prog_row['Candidate_Name']}")
        st.write(f"**Metrics:** {prog_row['Candidate_Scores']}")

    def render_school_side():
        st.write(f"**Program:** {prog_row['Program_Name']}")
        st.write(f"**Intensity:** {prog_row['Program_Intensity']}")
        # Tier moved to the right-hand side alongside school information
        st.info(f"**Tier Category:** {prog_row['Tier']}")

    render_split_layout(render_candidate_side, render_school_side)
    
    st.markdown("---")
    
    # Highlighted Fit Result (Replacing the old highlighted tier)
    st.markdown(f"""
        <div class="highlight-fit">
            FIT RESULT: {prog_row['Fit_Status'].upper()}
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Fit Status, Likelihood Definition, and Recommendation in bold inside an obvious box with text wrapping
    st.markdown(f"""
        <div class="wrapped-box">
            <p><strong>Fit Status:</strong> {prog_row['Fit_Status']} (Options: Reach, Target, Safety)</p>
            <p><strong>Likelihood Definition:</strong> {prog_row['Likelihood_Definition']}</p>
            <p><strong>Recommendation:</strong> {prog_row['Recommendation']}</p>
        </div>
    """, unsafe_allow_html=True)

elif tab == "Exploration Matrix":
    st.title("Exploration Matrix")
    st.write("Comprehensive overview utilizing the standardized Fit Status (**Reach, Target, Safety**) feature across all choices.")
    
    # Display dataframe with text wrapping configuration applied via column config
    st.dataframe(
        df,
        column_config={
            "Fit_Status": st.column_config.TextColumn("Fit Status (Reach/Target/Safety)", width="medium"),
            "Likelihood_Definition": st.column_config.TextColumn("Likelihood Definition", width="large"),
            "Recommendation": st.column_config.TextColumn("Recommendation", width="large")
        },
        use_container_width=True
    )

elif tab == "Candidate Profile":
    st.title("Candidate Profile Management")
    
    def render_cand_side():
        st.text_input("Edit Candidate Name", value=df.loc[0, "Candidate_Name"])
        st.text_area("Edit Qualifications", value=df.loc[0, "Candidate_Scores"])

    def render_inst_side():
        st.text_input("Program Target", value=df.loc[0, "Program_Name"])
        st.selectbox("Tier Assignment", ["Top Tier", "Mid Tier", "Community Tier"], index=0)

    render_split_layout(render_cand_side, render_inst_side)
