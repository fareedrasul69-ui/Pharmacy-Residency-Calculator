import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Residency Match & Tracker", page_icon="💊", layout="wide"
)

# --- MODERN NEUTRAL & MINIMALISTIC CSS ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    /* Global App Styling */
    .stApp {
        background-color: #fafaf9;
        color: #1c1917;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #f5f5f4;
        border-right: 1px solid #e7e5e4;
    }
    
    /* Input Fields & Selectboxes */
    .stTextInput input, .stSelectbox select, .stSlider {
        background-color: #ffffff !important;
        color: #1c1917 !important;
        border: 1px solid #d6d3d1 !important;
        border-radius: 8px !important;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: #ffffff;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #e7e5e4;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    
    /* Buttons */
    .stButton button {
        background-color: #292524;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        background-color: #44403c;
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f5f5f4;
        border-radius: 8px;
        color: #78716c;
        border: 1px solid #e7e5e4;
        padding: 10px 20px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #1c1917 !important;
        border: 1px solid #d6d3d1 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    
    /* Info / Disclaimer Box */
    .stAlert {
        background-color: #f5f5f4 !important;
        border: 1px solid #e7e5e4 !important;
        color: #44403c !important;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
  excel_path = "saved-programs-2026-08-07.xlsx"
  df = pd.read_excel(excel_path, sheet_name="Report")

  def extract_state(location):
    if pd.isna(location):
      return "Unknown"
    parts = str(location).split(",")
    if len(parts) >= 2:
      return parts[1].strip()
    return "Unknown"

  df["State_Code"] = df["Location"].apply(extract_state)
  df["Deadline_Display"] = (
      df["Application Deadline"]
      .astype(str)
      .str.replace("2025", "2027")
      .str.replace("2026", "2027")
  )
  return df


df_programs = load_data()

# Initialize Session State for Saved Programs List
if "saved_list" not in st.session_state:
  st.session_state.saved_list = []

st.title("Residency Match & Tracker")
st.caption(
    "Clinical Program Match & Strategic Evaluation Engine (ASHP Network)"
)

# --- PROFESSIONAL DISCLAIMER ---
st.info(
    "**System Notice:** This platform functions as an architectural guide for"
    " residency pathways. Competitiveness analytics are modeled using portal"
    " telemetry and metrics, and do not constitute absolute admission"
    " guarantees. Cross-reference with official institutional criteria."
)

# --- COMPLETE LIST OF US COLLEGES OF PHARMACY ---
pharmacy_schools = [
    "Other / International",
    "Albany College of Pharmacy and Health Sciences",
    "American University of Health Sciences",
    "Appalachian College of Pharmacy",
    "Auburn University",
    "Belmont University",
    "Binghamton University (SUNY)",
    "Butler University",
    "California Health Sciences University",
    "California Northstate University",
    "Campbell University",
    "Cedarville University",
    "Chapman University",
    "Chicago State University",
    "Concordia University Wisconsin",
    "Creighton University",
    "D'Youville University",
    "Drake University",
    "Duquesne University",
    "East Tennessee State University",
    "Fairleigh Dickinson University",
    "Ferris State University",
    "Florida Agricultural and Mechanical University",
    "Hampton University",
    "Harding University",
    "High Point University",
    "Howard University",
    "Husson University",
    "Idaho State University",
    "Keck Graduate Institute (KGI)",
    "Lake Erie College of Osteopathic Medicine (LECOM)",
    "Larkin University",
    "Lipscomb University",
    "Loma Linda University",
    "Long Island University (LIU Pharmacy)",
    "Manchester University",
    "Marshall University",
    "Massachusetts College of Pharmacy and Health Sciences (MCPHS)",
    "Mayo Clinic Alix School of Medicine / Pharmacy",
    "Medical University of South Carolina",
    "Mercer University",
    "Midwestern University (Arizona)",
    "Midwestern University (Illinois)",
    "Northeast Ohio Medical University (NEOMED)",
    "Northeastern University",
    "Northwest Nazarene University / Programs",
    "Nova Southeastern University",
    "Ohio Northern University",
    "Oregon State University",
    "Pacific University Oregon",
    "Palm Beach Atlantic University",
    "Philadelphia College of Osteopathic Medicine",
    "Presbyterian College",
    "Purdue University",
    "Regis University",
    "Roosevelt University",
    "Rosalind Franklin University",
    "Rutgers, The State University of New Jersey",
    "Samford University",
    "Shenandoah University",
    "South Dakota State University",
    "South University",
    "Southern Illinois University Edwardsville",
    "St. John Fisher University",
    "St. John's University",
    "St. Louis College of Pharmacy (UHSP)",
    "Temple University",
    "Texas A&M University",
    "Texas Tech University Health Sciences Center",
    "Thomas Jefferson University",
    "Touro College of Pharmacy (New York)",
    "Union University",
    "University of Arizona",
    "University of Arkansas for Medical Sciences",
    "University of Buffalo (SUNY)",
    "University of California, Irvine",
    "University of California, San Diego",
    "University of California, San Francisco",
    "University of Cincinnati",
    "University of Colorado",
    "University of Connecticut",
    "University of Findlay",
    "University of Florida",
    "University of Georgia",
    "University of Hawaii at Hilo",
    "University of Houston",
    "University of Idaho",
    "University of Illinois Chicago",
    "University of Iowa",
    "University of Kansas",
    "University of Kentucky",
    "University of Louisiana Monroe",
    "University of Maryland",
    "University of Massachusetts",
    "University of Michigan",
    "University of Minnesota",
    "University of Mississippi",
    "University of Missouri-Kansas City",
    "University of Montana",
    "University of Nebraska Medical Center",
    "University of New England",
    "University of New Mexico",
    "University of North Carolina at Chapel Hill",
    "University of North Dakota",
    "University of North Texas System",
    "University of Oklahoma",
    "University of the Pacific",
    "University of Pittsburgh",
    "University of Puerto Rico",
    "University of Rhode Island",
    "University of Saint Joseph",
    "University of South Carolina",
    "University of South Florida",
    "University of Southern California (USC)",
    "University of Tennessee Health Science Center",
    "University of Texas at Austin",
    "University of Toledo",
    "University of Utah",
    "University of Vermont",
    "University of Washington",
    "University of Wisconsin-Madison",
    "University of Wyoming",
    "VCU School of Pharmacy (Virginia Commonwealth)",
    "Washington State University",
    "Wayne State University",
    "Western New England University",
    "Western University of Health Sciences",
    "West Virginia University",
    "Wilkes University",
    "Wingate University",
    "Xavier University of Louisiana",
    "Yeshiva University",
]

# --- SIDEBAR: STUDENT PROFILE INPUTS ---
st.sidebar.header("Candidate Profile")

user_pharm_school = st.sidebar.selectbox("College of Pharmacy", pharmacy_schools)
gpa = st.sidebar.slider("PharmD GPA", 2.00, 4.00, 3.50, 0.01)

work_experience = st.sidebar.selectbox(
    "Pharmacy Experience",
    [
        "None / Minimal",
        "Community / Retail Experience (> 1 Year)",
        "Hospital / Health-System Intern (1+ Years)",
        "Multiple Clinical / Specialized Internships",
    ],
)

research = st.sidebar.selectbox(
    "Active Research / Posters", ["No", "Yes"]
)
leadership = st.sidebar.selectbox(
    "Leadership Tier",
    ["None", "Local Committee / Member", "Local Officer", "Executive / Multi-Officer"],
)
lor_strength = st.sidebar.selectbox(
    "Recommendation Quality",
    ["Standard", "Strong", "Exceptional"],
)

# --- SCORING ALGORITHM (100 Max) ---
score = 0.0
score += (gpa / 4.00) * 35

if work_experience == "Multiple Clinical / Specialized Internships":
  score += 20
elif work_experience == "Hospital / Health-System Intern (1+ Years)":
  score += 15
elif work_experience == "Community / Retail Experience (> 1 Year)":
  score += 12
else:
  score += 5

if research == "Yes":
  score += 15

if leadership == "Executive / Multi-Officer":
  score += 15
elif leadership == "Local Officer":
  score += 10
elif leadership == "Local Committee / Member":
  score += 5

if lor_strength == "Exceptional":
  score += 15
elif lor_strength == "Strong":
  score += 10
else:
  score += 5

st.sidebar.markdown("---")
st.sidebar.subheader(f"Calculated Score: {score:.1f} / 100")
st.sidebar.caption(f"Inst: {user_pharm_school}")

if score >= 80:
  st.sidebar.success("Status: Highly Competitive")
elif score >= 65:
  st.sidebar.info("Status: Competitive Standard")
else:
  st.sidebar.warning("Status: Developing Profile")

# Sidebar Saved List Quick View
st.sidebar.markdown("---")
st.sidebar.subheader(f"Saved List ({len(st.session_state.saved_list)})")
if st.session_state.saved_list:
  for saved_item in st.session_state.saved_list:
    st.sidebar.write(f"- {saved_item}")
  if st.sidebar.button("Clear Entire List"):
    st.session_state.saved_list = []
    st.rerun()
else:
  st.sidebar.caption("No programs bookmarked.")


# --- MAIN PANEL: PROGRAM EXPLORATION ---
st.header("Exploration Matrix")

tab1, tab2, tab3 = st.tabs([
    "Program Query",
    "State & Track Filter",
    "Saved Portfolio",
])

with tab1:
  search_query = st.text_input("Search Hospital or Program Name", "", key="t1_search")
  if search_query:
    res = df_programs[
        df_programs["Program Name"]
        .str.contains(search_query, case=False, na=False)
    ]

    if not res.empty:
      st.markdown(f"### Results Found: **{len(res)}**")
      for idx, row in res.iterrows():
        st.markdown("---")
        st.subheader(row["Program Name"])

        beds = row.get("Total Beds", 0)
        is_reach = (
            True
            if (
                pd.notna(beds)
                and beds > 500
                or "University" in str(row["Program Name"])
                or "Academic" in str(row["Program Name"])
            )
            else False
        )

        col_a, col_b, col_c = st.columns(3)
        with col_a:
          if is_reach:
            st.warning("Tier: Reach / High Intensity")
            required_score = 80
          else:
            st.info("Tier: Standard / Competitive")
            required_score = 65

          st.write(
              f"**Fit Status:** {'Optimal Match' if score >= required_score else 'Reach Profile'}"
          )
        with col_b:
          st.write(f"**Location:** {row.get('Location', 'N/A')}")
          st.write(f"**Category:** {row.get('Category', 'N/A')}")
          st.write(f"**Stipend:** {row.get('Estimated Stipend', 'N/A')}")
        with col_c:
          st.write(f"**Deadline:** {row.get('Deadline_Display', 'N/A')}")
          st.write(f"**Slots:** {row.get('Number of Positions', 'N/A')}")

        website = row.get("Website", "")
        if pd.notna(website) and str(website).strip() != "":
          st.markdown(f"**Official Portal:** [Access Link]({website})")

        prog_name_str = row["Program Name"]
        if st.button(f"Save to Portfolio", key=f"save_t1_{idx}"):
          if prog_name_str not in st.session_state.saved_list:
            st.session_state.saved_list.append(prog_name_str)
            st.success("Saved successfully.")
            st.rerun()
          else:
            st.info("Already in portfolio.")

        with st.expander("Inspect Requirements & Specifications"):
          st.write(
              "**Description:**",
              row.get("Residency Description", "No description available."),
          )
          st.write(
              "**Eligibility Requirements:**",
              row.get(
                  "Eligibility Requirements for Program",
                  "No specific requirements listed.",
              ),
          )
    else:
      st.info("No records match query.")

with tab2:
  col_s1, col_s2, col_s3 = st.columns(3)
  with col_s1:
    states = sorted(df_programs["State_Code"].dropna().unique())
    selected_state = st.selectbox("Select State", states, key="t2_state")
  with col_s2:
    categories = ["All"] + sorted(
        df_programs["Category"].dropna().unique().tolist()
    )
    selected_cat = st.selectbox("Category", categories, key="t2_cat")
  with col_s3:
    sub_focus = st.selectbox(
        "Sub-Focus Track",
        ["All Tracks", "Ambulatory Care", "Community-Based", "Health-System / Acute Care", "Managed Care"],
        key="t2_subcat"
    )

  state_df = df_programs[df_programs["State_Code"] == selected_state]
  if selected_cat != "All":
    state_df = state_df[state_df["Category"] == selected_cat]

  if sub_focus != "All Tracks":
    keyword_map = {
        "Ambulatory Care": "ambulatory",
        "Community-Based": "community",
        "Health-System / Acute Care": "acute",
        "Managed Care": "managed care"
    }
    kw = keyword_map.get(sub_focus, "")
    state_df = state_df[
        state_df["Residency Description"].str.contains(kw, case=False, na=False) |
        state_df["Program Name"].str.contains(kw, case=False, na=False)
    ]

  st.markdown(f"### Records Found: **{len(state_df)}** in **{selected_state}**")

  if not state_df.empty:
    display_cols = [
        "Program Name",
        "Program Code",
        "Category",
        "Estimated Stipend",
        "Deadline_Display",
    ]
    st.dataframe(state_df[display_cols], use_container_width=True)

    st.markdown("---")
    st.subheader("Program Competitiveness Inspector")
    
    selected_prog_name = st.selectbox(
        "Select Target Program",
        sorted(state_df["Program Name"].dropna().unique()),
        key="t2_inspector_name",
    )

    if selected_prog_name:
      prog_row = state_df[
          state_df["Program Name"] == selected_prog_name
      ].iloc[0]
      st.markdown(f"### {prog_row.get('Program Name', 'N/A')}")

      beds = prog_row.get("Total Beds", 0)
      is_reach = (
          True
          if (
              pd.notna(beds)
              and beds > 500
              or "University" in str(prog_row["Program Name"])
              or "Academic" in str(prog_row["Program Name"])
          )
          else False
      )

      col_x, col_y = st.columns(2)
      with col_x:
        if is_reach:
          st.warning("Tier: Reach Program")
          req_score = 80
        else:
          st.info("Tier: Standard Program")
          req_score = 65

        st.metric(
            "Match Likelihood",
            (
                "Optimal"
                if score >= req_score
                else "Reach / Focus Required"
            ),
        )
      with col_y:
        st.write(f"**Code:** {prog_row.get('Program Code', 'N/A')}")
        st.write(f"**Location:** {prog_row.get('Location', 'N/A')}")
        st.write(f"**Stipend:** {prog_row.get('Estimated Stipend', 'N/A')}")
        
        website = prog_row.get("Website", "")
        if pd.notna(website) and str(website).strip() != "":
          st.markdown(f"**Official Link:** [Access]({website})")

      if st.button(f"Save to Portfolio", key="save_inspector"):
        if selected_prog_name not in st.session_state.saved_list:
          st.session_state.saved_list.append(selected_prog_name)
          st.success("Saved successfully.")
          st.rerun()
        else:
          st.info("Already in portfolio.")

      with st.expander("View Specifications"):
        st.write(
            "**Description:**",
            prog_row.get("Residency Description", "No description available."),
        )
        st.write(
            "**Eligibility:**",
            prog_row.get(
                "Eligibility Requirements for Program",
                "No requirements listed.",
            ),
        )
  else:
    st.info("No records match the current filter selection.")

with tab3:
  st.header("Saved Portfolio & Target Links")
  if st.session_state.saved_list:
    st.write(f"Total Bookmarked: **{len(st.session_state.saved_list)}**")
    for idx, item in enumerate(st.session_state.saved_list):
      col_item1, col_item2 = st.columns([4, 1])
      with col_item1:
        st.markdown(f"### {idx+1}. {item}")
        match_rows = df_programs[df_programs["Program Name"] == item]
        if not match_rows.empty:
          r_info = match_rows.iloc[0]
          st.write(f"**Location:** {r_info.get('Location', 'N/A')} | **Category:** {r_info.get('Category', 'N/A')}")
          web_link = r_info.get("Website", "")
          if pd.notna(web_link) and str(web_link).strip() != "":
            st.markdown(f"**Official Portal:** [Open Official Page]({web_link})")
          else:
            st.caption("No portal URL available.")
      with col_item2:
        if st.button("Remove", key=f"remove_{idx}"):
          st.session_state.saved_list.remove(item)
          st.rerun()
      st.markdown("---")
  else:
    st.info("Portfolio is currently empty. Bookmark programs from search or state tabs.")
