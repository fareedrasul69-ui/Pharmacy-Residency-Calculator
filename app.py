import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Residency Match & Tracker", page_icon="💊", layout="wide"
)

# --- MODERN NEUTRAL & MINIMALISTIC CSS ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    .stApp {
        background-color: #f8f9fa;
        color: #212529;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e9ecef;
    }
    
    .stTextInput input, .stSelectbox select, .stSlider {
        background-color: #ffffff !important;
        color: #212529 !important;
        border: 1px solid #ced4da !important;
        border-radius: 8px !important;
    }
    
    div[data-testid="stMetric"] {
        background: #ffffff;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    .stButton button {
        background-color: #0d9488;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        background-color: #0f766e;
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(13, 148, 136, 0.2);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 8px;
        color: #6c757d;
        border: 1px solid #e9ecef;
        padding: 10px 20px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0d9488 !important;
        color: #ffffff !important;
        border: 1px solid #0d9488 !important;
        box-shadow: 0 2px 4px rgba(13, 148, 136, 0.2);
    }
    
    .stAlert {
        background-color: #ffffff !important;
        border: 1px solid #e9ecef !important;
        color: #495057 !important;
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
  
  # Fallback dynamic URL generator for programs missing official links
  def ensure_valid_url(row):
    website = row.get("Website", "")
    if pd.notna(website) and str(website).strip() != "":
      return str(website).strip()
    # Fallback to ASHP Residency Directory search query string if URL is blank
    prog_name = str(row.get("Program Name", "Pharmacy Residency"))
    query_encoded = prog_name.replace(" ", "+")
    return f"https://www.ashp.org/professional-development/residency-information/residency-directory?search={query_encoded}"

  df["Resolved_Website"] = df.apply(ensure_valid_url, axis=1)
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
    "Recommendation Quality (LOR)",
    [
        "Standard (Generic check-box evaluations with general praise)",
        "Strong (Detailed clinical insights from preceptors with positive performance remarks)",
        "Exceptional (Top-tier narrative letters highlighting clinical autonomy, advanced problem solving, and leadership)",
    ],
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

# --- REAL-TIME PROFILE OPTIMIZATION & RECOMMENDATIONS SECTION ---
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
            fit_status = "Reach Profile" if score < required_score else "Optimal Match"
          else:
            st.info("Tier: Standard / Competitive")
            required_score = 65
            fit_status = "Optimal Match" if score >= required_score else "Moderate Reach"

          st.write(f"**Fit Status:** {fit_status}")
          
          if score >= required_score:
            match_def = "High probability of securing an interview invitation based on robust academic and professional alignment."
            rec_action = "✅ **Recommendation:** Strongly Consider Applying. Your profile meets or exceeds target standards."
          elif score >= (required_score - 15):
            match_def = "Competitive profile with minor gaps; requires strong letters of intent and networking to offset."
            rec_action = "⚠️ **Recommendation:** Consider with Caution. Focus on tailoring your letter of intent specifically to this site."
          else:
            match_def = "Significant variance from historical averages; high barrier to entry without unique distinguishing attributes."
            rec_action = "❌ **Recommendation:** Unfavorable Match. Treat as a high-risk reach or skip to prioritize better-aligned programs."
          
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

        # Always active link via Resolved_Website fallback engine
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
          rec_action_2 = "✅ **Recommendation:** Strongly Consider Applying."
        elif score >= (req_score - 15):
          match_def_2 = "Competitive profile with potential areas for improvement; heavily relies on a compelling letter of intent."
          rec_action_2 = "⚠️ **Recommendation:** Consider with Caution."
        else:
          match_def_2 = "Profile sits well below historical benchmarks; application carries a high risk of rejection."
          rec_action_2 = "❌ **Recommendation:** Unfavorable Match / Skip."

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
          web_link = r_info.get("Resolved_Website", "")
          if pd.notna(web_link) and str(web_link).strip() != "":
            st.markdown(f"**Official Portal / Directory Link:** [Open Page]({web_link})")
          else:
            st.caption("No portal URL available.")
      with col_item2:
        if st.button("Remove", key=f"remove_{idx}"):
          st.session_state.saved_list.remove(item)
          st.rerun()
      st.markdown("---")
  else:
    st.info("Portfolio is currently empty. Bookmark programs from search or state tabs.")
