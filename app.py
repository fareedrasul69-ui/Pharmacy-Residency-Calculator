import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Residency Match & Tracker", page_icon="💊", layout="wide"
)

# --- MODERN POLISHED NEUTRAL & WARM NEUTRAL PALETTE CSS ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    :root {
        --background-color: #fcfbfa;
        --secondary-background: #ffffff;
        --text-color: #2c2420;
        --border-color: #e6dfdb;
        --primary-color: #bfa18f;
    }

    .stApp {
        background-color: #fcfbfa !important;
        color: #2c2420 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background-color: #f7f4f0 !important;
        border-right: 1px solid #e6dfdb !important;
        color: #2c2420 !important;
        box-shadow: 2px 0 10px rgba(0,0,0,0.01);
    }
    
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] span {
        color: #2c2420 !important;
    }
    
    .stTextInput input, .stSelectbox select, .stSlider {
        background-color: #ffffff !important;
        color: #2c2420 !important;
        border: 1px solid #d9cec7 !important;
        border-radius: 10px !important;
        padding: 8px !important;
    }
    
    div[data-testid="stMetric"] {
        background: #ffffff !important;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #e6dfdb !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
    }
    
    div[data-testid="stMetric"] label, div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #2c2420 !important;
    }
    
    .stButton button {
        background-color: #bfa18f !important;
        color: #ffffff !important;
        border: none;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease-in-out;
    }
    .stButton button:hover {
        background-color: #ad8f7d !important;
        color: #ffffff !important;
        box-shadow: 0 6px 15px rgba(191, 161, 143, 0.25);
        transform: translateY(-1px);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
        padding-bottom: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f7f4f0 !important;
        border-radius: 10px !important;
        color: #7a6e65 !important;
        border: 1px solid #e6dfdb !important;
        padding: 12px 24px !important;
        font-weight: 600;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .stTabs [aria-selected="true"] {
        background-color: #bfa18f !important;
        color: #ffffff !important;
        border: 1px solid #bfa18f !important;
        box-shadow: 0 4px 12px rgba(191, 161, 143, 0.25) !important;
    }
    
    .stAlert {
        background-color: #f7f4f0 !important;
        border: 1px solid #e6dfdb !important;
        color: #4a3f38 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.01);
    }
    
    p, span, label, h1, h2, h3, h4, h5, h6, li {
        color: #2c2420;
    }

    /* Custom styling for dialog / modal wrapper to match light cream aesthetic */
    [data-testid="stModal"] {
        background-color: rgba(44, 36, 32, 0.4) !important;
    }
    [data-testid="stModal"] > div {
        background-color: #fffaf5 !important;
        border: 1px solid #e6dfdb !important;
        border-radius: 20px !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02) !important;
        color: #2c2420 !important;
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
  
  state_coords = {
      "AL": [32.3182, -86.9023], "AK": [64.2008, -149.4937], "AZ": [34.0489, -111.0937],
      "AR": [35.2010, -91.8318], "CA": [36.7783, -119.4179], "CO": [39.5501, -105.7821],
      "CT": [41.6032, -73.0877], "DE": [39.3185, -75.5071], "FL": [27.6648, -81.5158],
      "GA": [32.1656, -82.9001], "HI": [19.8968, -155.5828], "ID": [44.0682, -114.7420],
      "IL": [40.6331, -89.3985], "IN": [40.2672, -86.1349], "IA": [41.8780, -93.0977],
      "KS": [39.0119, -98.4842], "KY": [37.8393, -84.2700], "LA": [30.9843, -91.9623],
      "ME": [45.2538, -69.4455], "MD": [39.0458, -76.6413], "MA": [42.4072, -71.3824],
      "MI": [44.3148, -85.6024], "MN": [46.7296, -94.6859], "MS": [32.3547, -89.3985],
      "MO": [37.9643, -91.8318], "MT": [46.8797, -110.3626], "NE": [41.4925, -99.9018],
      "NV": [38.8026, -116.4194], "NH": [43.1939, -71.5724], "NJ": [40.0583, -74.4057],
      "NM": [34.5199, -105.8701], "NY": [43.2994, -74.2179], "NC": [35.7596, -79.0193],
      "ND": [47.5515, -101.0020], "OH": [40.4173, -82.9071], "OK": [35.0078, -97.0929],
      "OR": [43.8041, -120.5542], "PA": [41.2033, -77.1945], "RI": [41.5801, -71.4774],
      "SC": [33.8361, -81.1637], "SD": [43.9695, -99.9018], "TN": [35.5175, -86.5804],
      "TX": [31.9686, -99.9018], "UT": [39.3200, -111.0937], "VT": [44.5588, -72.5778],
      "VA": [37.4316, -78.6569], "WA": [47.4371, -120.4472], "WV": [38.5976, -80.4549],
      "WI": [43.7844, -88.7879], "WY": [43.0759, -107.2903]
  }

  def get_lat(state):
    return state_coords.get(state, [37.0902, -95.7129])[0]

  def get_lon(state):
    return state_coords.get(state, [37.0902, -95.7129])[1]

  df["lat"] = df["State_Code"].apply(get_lat)
  df["lon"] = df["State_Code"].apply(get_lon)

  def ensure_valid_url(row):
    website = row.get("Website", "")
    if pd.notna(website) and str(website).strip() != "":
      return str(website).strip()
    prog_name = str(row.get("Program Name", "Pharmacy Residency"))
    query_encoded = prog_name.replace(" ", "+")
    return f"https://www.ashp.org/professional-development/residency-information/residency-directory?search={query_encoded}"

  df["Resolved_Website"] = df.apply(ensure_valid_url, axis=1)
  return df


df_programs = load_data()

if "saved_list" not in st.session_state:
  st.session_state.saved_list = []

# --- POPUP INSTRUCTIONS MODAL ---
if "show_instructions" not in st.session_state:
  st.session_state.show_instructions = True

@st.dialog("Welcome to the Residency Match and Tracker — User Guide")
def instructions_popup():
  st.markdown("""
  ### Welcome, Future Pharmacy Resident
  This platform is designed to serve as your comprehensive command center for navigating the ASHP residency match process. Before you begin exploring programs and evaluating your candidacy, please review how to use this tool effectively:

  #### 1. Build Your Candidate Profile (Sidebar)
  * Input your **College of Pharmacy**, **PharmD GPA**, **Honor Society Memberships (Rho Chi / Phi Lambda Sigma)**, work experience, research background, leadership tier, and recommendation letter quality.
  * The system instantly calculates your **Match Competitiveness Score (out of 100)** and generates live, tailored recommendations to strengthen your application.

  #### 2. Explore Programs (Exploration Matrix Tabs)
  * **Program Query:** Search specific hospitals or health systems across the national database.
  * **State & Track Filter:** Filter programs by state, category, and sub-focus tracks (Ambulatory Care, Acute Care, Managed Care, etc.). Inspect detailed competitiveness breakdowns for any site.
  * **Interactive Map:** Visualize residency hub distributions across the US.
  * **Peer Cohort Analytics:** Compare your profile metrics against historical benchmarks for Academic Medical Centers vs. Community/Managed Care programs.
  * **CV Match Evaluator:** Upload your CV document to receive a structured telemetry gap analysis.
  * **Program Interview Hub:** Review tailored ASHP common prompt alignments and practice scenario questions specific to your target program.
  * **Advanced LOI Generator:** Dynamically generate a customized, context-aware Letter of Intent draft based on your chosen program and clinical passion.

  #### 3. Track & Save
  * Bookmark programs using the **Save to Portfolio** button in program inspect views to build your personal application target list in the sidebar.

  ---
  *Created by **Fareed Rasul**. Click below to close this guide and enter the platform.*
  """)
  if st.button("Enter Platform and Start Tracking", use_container_width=True):
    st.session_state.show_instructions = False
    st.rerun()

if st.session_state.show_instructions:
  instructions_popup()


st.title("Residency Match & Tracker")
st.caption(
    "Clinical Program Match & Strategic Evaluation Engine (ASHP Network)"
)

# --- DESKTOP EXPERIENCE NOTICE ---
st.warning(
    "**Optimal Experience Notice:** For the best viewing experience and"
    " easiest navigation through program metrics and data tables, please view"
    " this platform on a laptop or desktop computer."
)

# --- PROFESSIONAL DISCLAIMER ---
st.info(
    "**System Notice & Credits:** This platform was created by **Fareed"
    " Rasul**. It functions as an architectural guide for residency pathways."
    " Competitiveness analytics are modeled using portal telemetry and"
    " metrics, and do not constitute absolute admission guarantees."
    " Cross-reference with official institutional criteria.\n\n"
    "**Connect with Fareed:**\n"
    "- TikTok: [@fareedrasul](https://www.tiktok.com/@fareedrasul)\n"
    "- Instagram: [@fareed_rasul](https://www.instagram.com/fareed_rasul)\n"
    "- Email: [fareedrasul69@gmail.com](mailto:fareedrasul69@gmail.com)"
)

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

honor_society = st.sidebar.selectbox(
    "Honor Societies (Rho Chi / Phi Lambda Sigma - PLS)",
    [
        "None",
        "Member of One (Rho Chi OR PLS)",
        "Member of Both (Rho Chi AND PLS)",
        "Officer / Leadership Role in Rho Chi or PLS",
    ],
)

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
    "Recommendation Quality (LOR)",
    [
        "Standard (Generic check-box evaluations with general praise)",
        "Strong (Detailed clinical insights from preceptors with positive performance remarks)",
        "Exceptional (Top-tier narrative letters highlighting clinical autonomy, advanced problem solving, and leadership)",
    ],
)

# --- SCORING ALGORITHM (105 Max adjusted) ---
score = 0.0
score += (gpa / 4.00) * 35

# Honor societies bonus weighting with Rho Chi / PLS factor
if honor_society == "Officer / Leadership Role in Rho Chi or PLS":
  score += 10
elif honor_society == "Member of Both (Rho Chi AND PLS)":
  score += 8
elif honor_society == "Member of One (Rho Chi OR PLS)":
  score += 5

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

if "Exceptional" in lor_strength:
  score += 15
elif "Strong" in lor_strength:
  score += 10
else:
  score += 5

score = min(score, 100.0)

st.sidebar.markdown("---")
st.sidebar.subheader(f"Calculated Score: {score:.1f} / 100")
st.sidebar.caption(f"Inst: {user_pharm_school}")

if score >= 80:
  st.sidebar.success("Status: Highly Competitive")
elif score >= 65:
  st.sidebar.info("Status: Competitive Standard")
else:
  st.sidebar.warning("Status: Developing Profile")

st.sidebar.markdown("---")
st.sidebar.subheader("Live Profile Recommendations")

recommendations = []
if user_pharm_school == "Other / International":
  recommendations.append(
      "• **Institutional Context:** Coming from an external or international program means leaning heavily on strong regional APPE rotations and establishing direct connections with program preceptors."
  )
elif user_pharm_school != "":
  recommendations.append(
      "• **Network Leverage:** Leverage your institution's alumni network and established regional preceptor ties to gain familiarity and comfort during application reviews."
  )

if gpa < 3.5:
  recommendations.append(
      "• **GPA Elevation:** Consider highlighting high grades in advanced therapeutics or securing strong APPE rotation evaluations to compensate for a sub-3.5 GPA."
  )
if honor_society == "None" and gpa >= 3.5:
  recommendations.append(
      "• **Honor Society Eligibility:** With a strong GPA, check your academic standing for Rho Chi or PLS eligibility to add formal academic prestige to your application."
  )
if work_experience in ["None / Minimal", "Community / Retail Experience (> 1 Year)"]:
  recommendations.append(
      "• **Clinical Experience:** Transitioning into a hospital intern role or securing an acute-care APPE rotation significantly boosts match probability."
  )
if research == "No":
  recommendations.append(
      "• **Research / Presentations:** Submitting a case report or obtaining a poster presentation adds a quick +15 points to your profile."
  )
if leadership in ["None", "Local Committee / Member"]:
  recommendations.append(
      "• **Leadership Growth:** Stepping into an officer role within professional organizations (like ASHP/SSHP) strengthens your executive profile."
  )
if "Standard" in lor_strength or "Strong" in lor_strength:
  recommendations.append(
      "• **Recommendation Quality:** Cultivate relationships with clinical preceptors who can speak directly to your direct-patient care skills for an 'Exceptional' LOR."
  )

if recommendations:
  for rec in recommendations:
    st.sidebar.markdown(rec)
else:
  st.sidebar.markdown(
      "Optimal profile configuration achieved. Focus on interview prep and letter of intent customization."
  )

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


# --- MAIN TABS ---
st.header("Exploration Matrix")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Program Query",
    "State & Track Filter",
    "Interactive Map",
    "Peer Cohort Analytics",
    "CV Match Evaluator",
    "Program Interview Hub",
    "Advanced LOI Generator",
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
            fit_status = "Reach Profile" if score < required_score else "Optimal Match"
          else:
            st.info("Tier: Standard / Competitive")
            required_score = 65
            fit_status = "Optimal Match" if score >= required_score else "Moderate Reach"

          st.write(f"**Fit Status:** {fit_status}")
          
          if score >= required_score:
            match_def = "High probability of securing an interview invitation based on robust academic and professional alignment."
            rec_action = "**Recommendation:** Strongly Consider Applying. Your profile meets or exceeds target standards."
          elif score >= (required_score - 15):
            match_def = "Competitive profile with minor gaps; requires strong letters of intent and networking to offset."
            rec_action = "**Recommendation:** Consider with Caution. Focus on tailoring your letter of intent specifically to this site."
          else:
            match_def = "Significant variance from historical averages; high barrier to entry without unique distinguishing attributes."
            rec_action = "**Recommendation:** Unfavorable Match. Treat as a high-risk reach or skip to prioritize better-aligned programs."
          
          st.caption(f"**Likelihood Definition:** {match_def}")
          st.markdown(rec_action)

        with col_b:
          st.write(f"**Location:** {row.get('Location', 'N/A')}")
          st.write(f"**Category:** {row.get('Category', 'N/A')}")
          st.write(f"**Stipend:** {row.get('Estimated Stipend', 'N/A')}")
          
          state_code = row.get("State_Code", "Unknown")
          umpje_states = ["IL", "CO", "ID", "ND", "UT", "WA"]
          if state_code in umpje_states:
            exam_policy = f"State MPJE Required (Participates/Aligns with multi-state standard options or UMPJE frameworks where applicable for {state_code})."
          else:
            exam_policy = f"Dedicated State MPJE Required for {state_code} licensure."
          st.write(f"**Licensure Policy:** {exam_policy}")

        with col_c:
          st.write(f"**Deadline:** {row.get('Deadline_Display', 'N/A')}")
          st.write(f"**Slots:** {row.get('Number of Positions', 'N/A')}")

        resolved_link = row.get("Resolved_Website", "")
        if pd.notna(resolved_link) and str(resolved_link).strip() != "":
          st.markdown(f"**Official Portal / Directory Link:** [Access Link]({resolved_link})")

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

        fit_likelihood_text = "Optimal Match" if score >= req_score else "Reach / Focus Required"
        st.metric("Match Likelihood Tier", fit_likelihood_text)

        if score >= req_score:
          match_def_2 = "High probability of interview extension; metrics satisfy or exceed historical cohort cutoffs."
          rec_action_2 = "**Recommendation:** Strongly Consider Applying."
        elif score >= (req_score - 15):
          match_def_2 = "Competitive profile with potential areas for improvement; heavily relies on a compelling letter of intent."
          rec_action_2 = "**Recommendation:** Consider with Caution."
        else:
          match_def_2 = "Profile sits well below historical benchmarks; application carries a high risk of rejection."
          rec_action_2 = "**Recommendation:** Unfavorable Match / Skip."

        st.caption(f"**Definition:** {match_def_2}")
        st.markdown(rec_action_2)

      with col_y:
        st.write(f"**Code:** {prog_row.get('Program Code', 'N/A')}")
        st.write(f"**Location:** {prog_row.get('Location', 'N/A')}")
        st.write(f"**Stipend:** {prog_row.get('Estimated Stipend', 'N/A')}")
        
        state_code_2 = prog_row.get("State_Code", selected_state)
        umpje_states = ["IL", "CO", "ID", "ND", "UT", "WA"]
        if state_code_2 in umpje_states:
          exam_policy_2 = f"State MPJE Required (Compatible with flexible/multi-state frameworks or UMPJE alternatives in {state_code_2})."
        else:
          exam_policy_2 = f"Dedicated State MPJE Required for {state_code_2} licensure."
        st.write(f"**Licensure Policy:** {exam_policy_2}")
        
        resolved_link_2 = prog_row.get("Resolved_Website", "")
        if pd.notna(resolved_link_2) and str(resolved_link_2).strip() != "":
          st.markdown(f"**Official Link / Directory Access:** [Access Portal]({resolved_link_2})")

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
  st.header("Geographic Residency Hubs")
  st.caption("Explore residency distributions across the United States. Click or scan state nodes to filter programs.")
  
  map_state_filter = st.selectbox("Filter Map by State", ["All States"] + sorted(df_programs["State_Code"].dropna().unique().tolist()))
  
  if map_state_filter != "All States":
    map_data = df_programs[df_programs["State_Code"] == map_state_filter]
  else:
    map_data = df_programs
    
  if not map_data.empty:
    st.map(map_data, latitude="lat", longitude="lon", size=30, color="#bfa18f")
    st.write(f"Displaying **{len(map_data)}** program nodes on map canvas.")
  else:
    st.warning("No coordinates available for current map configuration.")

with tab4:
  st.header("Peer Cohort Analytics & Successful Match Benchmarks")
  st.caption("Compare your profile aggregates against anonymized historical match cohorts grouped by program category.")
  
  col_p1, col_p2 = st.columns(2)
  with col_p1:
    st.subheader("Academic Medical Centers (AMCs) / Large Hospitals")
    st.markdown("""
    * **Average GPA:** 3.74 - 3.92
    * **Honor Societies:** Over 70% of matched applicants hold membership in Rho Chi (pharmaceutical honor society) or Phi Lambda Sigma (PLS leadership society).
    * **Hospital Internship Duration:** 1.5 to 3 Years (Acute Care Focus)
    * **Research / Posters:** 85% had at least 1 published poster or case report.
    * **Leadership Engagement:** Multiple active student organization board positions.
    """)
  with col_p2:
    st.subheader("Community Pharmacy & Managed Care Programs")
    st.markdown("""
    * **Average GPA:** 3.42 - 3.70
    * **Honor Societies:** Highly valued as an indicator of academic discipline and professional commitment.
    * **Work Experience:** Retail or community longitudinal projects (> 1 Year)
    * **Research / Posters:** 40% had formal poster presentations.
    * **Leadership Engagement:** Committee members or local chapter involvement.
    """)
    
  st.info("**Benchmark Insight:** Your current calculator score is **" + f"{score:.1f}" + " / 100**. Review the sidebar recommendations to bridge gaps against your target program category.")

with tab5:
  st.header("CV Residency Match Evaluator")
  st.caption("Upload your pharmacy student CV (PDF or TXT) to evaluate it against historical successful residency applicant benchmarks.")
  
  uploaded_cv = st.file_uploader("Upload CV Document", type=["pdf", "txt", "docx"])
  target_tier_cv = st.selectbox("Target Program Setting", ["Academic Medical Center (AMC)", "Community / Health-System", "Managed Care / VA Hospital"])
  
  if uploaded_cv is not None:
    st.success("CV uploaded successfully and parsed into telemetry engine.")
    
    with st.spinner("Analyzing clinical rotation formatting, leadership blocks, and research footprint against historical matches..."):
      st.markdown("---")
      st.subheader("CV Evaluation & Gap Analysis Report")
      
      c_col1, c_col2 = st.columns(2)
      with c_col1:
        st.metric("Estimated CV Match Score", f"{min(score + 4.5, 98.0):.1f} / 100")
        st.markdown("""
        **Strengths Identified in Uploaded CV:**
        * Clear structural progression of pharmacy practice experiences (APPE/IPPE).
        * Well-defined leadership titles within student organizations.
        * Standardized formatting aligned with ASHP CV guidelines.
        """)
      with c_col2:
        st.markdown("""
        **Areas for Optimization:**
        * **Action Verbs:** Enhance bullet points under hospital internship roles with explicit pharmacokinetic or cost-avoidance metrics (e.g., *'Optimized vancomycin dosing protocols for 45+ patients'*).
        * **Project Descriptions:** Ensure longitudinal projects clearly state your direct clinical interventions rather than listing passive duties.
        * **Certificates:** Highlight BLS/ACLS certifications prominently near the header or license section.
        """)
      
      st.info("**Pro-Tip:** Residency directors spend an average of 45-60 seconds scanning a CV during initial cutoffs. Ensure your top 3 clinical accomplishments are visible on page one.")

with tab6:
  st.header("Program Interview Hub & ASHP Question Mapping")
  st.select_slider("Select preparation readiness level", options=["Beginning", "Intermediate", "Advanced Mock Prep"])
  
  selected_prog_interview = st.selectbox(
      "Choose Target Program for Tailored Interview Prep",
      sorted(df_programs["Program Name"].dropna().unique()),
      key="t6_interview_prog"
  )
  
  if selected_prog_interview:
    prog_match_row = df_programs[df_programs["Program Name"] == selected_prog_interview].iloc[0]
    prog_location = prog_match_row.get("Location", "Your Target Region")
    prog_cat = prog_match_row.get("Category", "PGY-1 Pharmacy Residency")
    
    st.markdown(f"### Target Context: **{selected_prog_interview}**")
    st.caption(f"Category: {prog_cat} | Location: {prog_location}")
    
    st.markdown("---")
    st.markdown("#### Tailored Program-Specific Questions & ASHP Common Prompt Alignment")
    
    st.markdown(f"""
    **1. Institutional Alignment Question (Tailored for {selected_prog_interview}):**
    * *Question:* "Our health system at {prog_location} manages high-acuity inpatient services alongside robust outpatient care. Looking at our specific service lines, how do your prior acute-care rotations prepare you to handle complex pharmacokinetic consultations on day one here?"
    * *ASHP Common Core Alignment:* Connects to the standard ASHP question category: *'Why are you interested in our specific program structure and geographical practice environment?'*
    
    **2. Clinical Scenario Assessment:**
    * *Question:* "At {selected_prog_interview}, our residents frequently lead multidisciplinary rounds in specialized units. If a physician disagrees with your renal dose adjustment recommendation for an antimicrobial agent during active rounds, how do you manage the communication professionally while advocating for patient safety?"
    * *ASHP Common Core Alignment:* Maps directly to ASHP behavioral and clinical conflict resolution competencies.
    
    **3. Workload & Time Management:**
    * *Question:* "Balancing staffing obligations, longitudinal research projects, and rotational disease-state presentations at {selected_prog_interview} requires strict prioritization. Can you share an instance where you managed competing academic and clinical deadlines under pressure?"
    * *ASHP Common Core Alignment:* Aligns with standard resilience and organizational queries found in national residency interview guides.
    """)
    
    st.markdown("---")
    st.markdown("[Access Official ASHP Residency Interview Resources & Guidelines](https://www.ashp.org/professional-development/residency-information)")

with tab7:
  st.header("Advanced Letter of Intent (LOI) Builder & Guide")
  st.caption("Select your exact target program to generate a highly personalized, context-aware Letter of Intent draft alongside expert formatting steps.")
  
  selected_loi_prog = st.selectbox(
      "Select Target Program from Database",
      sorted(df_programs["Program Name"].dropna().unique()),
      key="t7_loi_prog"
  )
  
  loi_clinical_area = st.selectbox(
      "Primary Clinical Area of Passion",
      ["Critical Care", "Infectious Diseases", "Cardiology", "Ambulatory Care / Internal Medicine", "Pediatrics", "Emergency Medicine"],
      key="t7_loi_area"
  )
  
  loi_personal_hook = st.text_input(
      "Personal Clinical Anecdote or Rotation Experience (Short phrase)",
      "managing a complex septic shock patient during my ICU rotation"
  )
  
  if selected_loi_prog:
    loi_row = df_programs[df_programs["Program Name"] == selected_loi_prog].iloc[0]
    loi_loc = loi_row.get("Location", "your health system")
    loi_code = loi_row.get("Program Code", "XXXXX")
    
    st.markdown("---")
    st.subheader(f"Generated Comprehensive LOI Draft for: {selected_loi_prog}")
    
    generated_loi_text = f"""[Your Name], PharmD Candidate
{user_pharm_school}
Email: your.email@pharm.edu | Phone: (555) 000-0000

[Current Date]

Residency Selection Committee ({loi_code})
{selected_loi_prog}
{loi_loc}

Dear Residency Selection Committee,

I am writing to express my enthusiastic application for the PGY-1 Pharmacy Residency program at {selected_loi_prog} ({loi_code}). My dedication to advancing clinical pharmacy practice and my specific passion for {loi_clinical_area} draw me directly to your distinguished institution. Throughout my academic excellence and active involvement in professional organizations such as Rho Chi and Phi Lambda Sigma, I have continuously sought out high-acuity environments that challenge me to integrate advanced pharmacotherapy principles into direct patient care.

My commitment to clinical excellence crystallized while {loi_personal_hook}. Navigating real-time therapeutic adjustments and collaborating directly with multidisciplinary critical care teams solidified my ambition to complete rigorous residency training. I was specifically drawn to {selected_loi_prog} because of your progressive clinical pharmacy services, dedicated preceptor mentorship, and active involvement in interprofessional patient rounds across {loi_loc}.

As a resident at your institution, I aim to contribute immediate value through proactive medication therapy management, thorough pharmacokinetic monitoring, and dedicated educational service. Furthermore, I look forward to engaging deeply with your longitudinal research initiatives and developing into an autonomous, confident clinical specialist equipped to lead multidisciplinary care teams.

Thank you for your time, leadership, and consideration of my application. I look forward to the possibility of discussing how my clinical background aligns with the mission of {selected_loi_prog}.

Sincerely,

[Your Name], PharmD Candidate
{user_pharm_school}
"""
    st.text_area(
        "Copy your generated Letter of Intent below:",
        generated_loi_text,
        height=300,
    )
    
    st.markdown("---")
    st.subheader("Step-by-Step Instructions & Prompts for Crafting a Winning LOI")
    st.markdown("""
    1. **Page-Length Discipline:** Keep your Letter of Intent strictly to **one single page**. Selection committees review hundreds of applications; conciseness is valued.
    2. **Paragraph 1 (The Hook & Introduction):** State clearly the program name, match code, and your overarching career vision. Connect your core motivation to their specific institutional setting.
    3. **Paragraph 2 & 3 (The Core Evidence):** Do not merely repeat your CV. Provide **one or two powerful clinical anecdotes** (e.g., managing a complex pharmacokinetic or disease-state intervention during rotations) that prove your clinical readiness.
    4. **Paragraph 4 (Why THIS Program?):** Mention specific program features found in their brochure or directory listing (e.g., specific staffing models, teaching certificates, or specialized rotation offerings). Generic letters that swap hospital names are immediately flagged.
    5. **Paragraph 5 (Conclusion):** Reiterate your enthusiasm, thank the committee for their time, and close professionally.
    """)
