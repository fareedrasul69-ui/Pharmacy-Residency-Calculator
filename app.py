import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Pharmacy Residency Match Analyzer", page_icon="💊", layout="wide"
)

# --- MODERN POLISHED NEUTRAL & WARM NEUTRAL PALETTE CSS WITH FULL TEXT WRAPPING ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    :root {
        --background-color: #FAF6F0;
        --secondary-background: #FFFFFF;
        --text-color: #5C4E43;
        --border-color: #E3D5C9;
        --primary-color: #C8AD93;
    }

    .stApp {
        background-color: #FAF6F0 !important;
        color: #5C4E43 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #F4EDE4 !important;
        border-right: 1px solid #E3D5C9 !important;
        color: #5C4E43 !important;
        box-shadow: 2px 0 10px rgba(0,0,0,0.01);
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div {
        color: #5C4E43 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    .stTextInput input, .stSelectbox select, .stSlider {
        background-color: #FFFFFF !important;
        color: #5C4E43 !important;
        border: 1px solid #D9C8B9 !important;
        border-radius: 10px !important;
        padding: 8px !important;
    }
    
    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #E3D5C9 !important;
        box-shadow: 0 4px 6px -1px rgba(92, 78, 67, 0.03), 0 2px 4px -1px rgba(92, 78, 67, 0.02);
    }
    
    div[data-testid="stMetric"] label, div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #5C4E43 !important;
    }
    
    .stButton button {
        background-color: #C8AD93 !important;
        color: #FFFFFF !important;
        border: none;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease-in-out;
        white-space: normal !important;
        word-break: break-word !important;
    }
    .stButton button:hover {
        background-color: #B59A80 !important;
        color: #FFFFFF !important;
        box-shadow: 0 6px 15px rgba(200, 173, 147, 0.25);
        transform: translateY(-1px);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
        padding-bottom: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #F4EDE4 !important;
        border-radius: 10px !important;
        color: #8C7A6B !important;
        border: 1px solid #E3D5C9 !important;
        padding: 12px 18px !important;
        font-weight: 600;
        box-shadow: 0 1px 3px rgba(92, 78, 67, 0.02);
    }
    .stTabs [aria-selected="true"] {
        background-color: #C8AD93 !important;
        color: #FFFFFF !important;
        border: 1px solid #C8AD93 !important;
        box-shadow: 0 4px 12px rgba(200, 173, 147, 0.25) !important;
    }
    
    .stAlert {
        background-color: #F4EDE4 !important;
        border: 1px solid #E3D5C9 !important;
        color: #5C4E43 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 4px rgba(92, 78, 67, 0.01);
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    p, span, label, h1, h2, h3, h4, h5, h6, li, div {
        color: #5C4E43;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }

    /* Custom highlight boxes and universal text wrapping utility */
    .wrapped-box {
        background-color: #FFFFFF;
        border: 2px solid #C8AD93;
        padding: 15px;
        border-radius: 12px;
        font-weight: bold;
        color: #5C4E43;
        margin-bottom: 15px;
        box-shadow: 0 2px 6px rgba(92, 78, 67, 0.04);
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }
    .highlight-fit {
        background-color: #F4EDE4;
        border: 2px solid #C8AD93;
        padding: 12px;
        border-radius: 10px;
        font-weight: bold;
        color: #5C4E43;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 15px;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    /* Force table cells and dataframe wrappers to wrap long texts cleanly */
    .stDataFrame, .stDataFrame div, .stDataFrame table, .stDataFrame th, .stDataFrame td {
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
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

st.title("Pharmacy Residency Match Analyzer")
st.caption(
    "Clinical Program Match & Strategic Evaluation Engine (ASHP Network)"
)

# --- DESKTOP EXPERIENCE NOTICE ---
st.warning(
    "Optimal Experience Notice: For the best viewing experience and"
    " easiest navigation through program metrics and data tables, please view"
    " this platform on a laptop or desktop computer."
)

# --- PROFESSIONAL DISCLAIMER ---
st.info(
    "System Notice & Credits: This platform was created by **Fareed"
    " Rasul** as an architectural guide for residency pathways. "
    "\n\n"
    "⚠️ **Important Reference Disclaimer:** This tool is strictly provided for general reference and self-evaluation purposes only. It does not constitute an absolute admission or match guarantee. **All information, program requirements, deadlines, and criteria must be double-checked and verified via official accounts, official ASHP directories, and primary program websites.**"
    "\n\n"
    "Connect with Fareed:\n"
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

high_pass_rate_schools = [
    "University of Michigan College of Pharmacy (Ann Arbor)",
    "University of Puerto Rico Medical Sciences Campus School of Pharmacy (San Juan)",
    "Husson University College of Health and Pharmacy School of Pharmacy (Bangor, Maine)",
    "Idaho State University L.S. Skaggs College of Pharmacy (Meridian)",
    "East Tennessee State University Bill Gatton College of Pharmacy (Johnson City)",
    "University of Oklahoma Health Sciences Center College of Pharmacy (Oklahoma City)",
    "University of the Incarnate Word Feik School of Pharmacy (San Antonio)",
    "University of California San Diego Skaggs School of Pharmacy & Pharmaceutical Sciences",
    "University of South Carolina College of Pharmacy (Columbia)",
    "University at Buffalo (N.Y.) School of Pharmacy & Pharmaceutical Sciences",
    "Ohio Northern University Raabe College of Pharmacy (Ada)",
    "Union University College of Pharmacy (Jackson, Tenn.)",
    "University of Cincinnati James L. Winkle College of Pharmacy",
    "University of Findlay (Ohio) College of Pharmacy",
    "Purdue University",
    "University of Utah",
    "University of Minnesota",
    "University of Washington",
    "Auburn University",
    "Duquesne University",
    "Ferris State University",
    "University of Kentucky",
    "Samford University",
    "Creighton University",
    "Drake University",
    "Rutgers, The State University of New Jersey",
]

# --- SIDEBAR NAVIGATION & USER PROFILE INPUTS ---
st.sidebar.title("Navigation & Profile")
sidebar_mode = st.sidebar.radio("Go To", ["Platform Tools", "📖 User Guide & Instructions"])

if sidebar_mode == "📖 User Guide & Instructions":
    st.header("User Guide & Instructions")
    st.markdown("""
    ### Welcome, Future Pharmacy Resident
    This platform is designed to serve as your comprehensive command center for navigating the ASHP residency match process. Here is how to use this tool effectively:

    #### 1. Build Your Candidate Profile (Sidebar)
    * Input your College of Pharmacy, PharmD GPA, Honor Society Memberships, Leadership Experience, Community Service, Research Background, Poster Presentation Level, Recommendation Letter Quality, and Work Experience.
    * The system instantly calculates your Match Competitiveness Score (out of 100) and generates live, tailored recommendations to strengthen your application.

    #### 2. Explore Programs (Exploration Matrix Tabs)
    * Program Query: Search specific hospitals or health systems across the national database.
    * State & Track Filter: Filter programs by state, category, and sub-focus tracks.
    * Interactive Map: Visualize residency hub distributions across the US.
    * Peer Cohort Analytics: Compare your profile metrics against historical benchmarks.
    * CV Match Evaluator: Upload your CV document to receive a structured gap analysis.
    * Program Interview Hub: Review tailored ASHP common prompt alignments.
    * Advanced LOI Generator: Dynamically generate a customized Letter of Intent draft.
    * LOR Strategy & Guide: Review strategies on how to secure strong recommendations.

    #### 3. Track & Save
    * Bookmark programs using the Save to Portfolio button in program inspect views to build your personal application target list in the sidebar.

    ---
    *Created by Fareed Rasul.*
    """)
else:
    st.sidebar.markdown("---")
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

    leadership = st.sidebar.selectbox(
        "Leadership Experience",
        ["None", "Local Committee / Member", "Local Officer", "Executive / Multi-Officer"],
    )

    community_service = st.sidebar.selectbox(
        "Community Service During Pharmacy School",
        [
            "Minimal / None",
            "Moderate Involvement (Local Events / Health Fairs)",
            "Extensive Involvement (Regular Volunteering / Board Lead)",
        ],
    )

    research = st.sidebar.selectbox(
        "Active Research Background", ["No", "Yes"]
    )

    poster_level = st.sidebar.selectbox(
        "Highest Poster Presentation Level",
        ["None", "Local", "State", "Regional", "National"],
    )

    lor_strength = st.sidebar.selectbox(
        "Recommendation Quality (LOR)",
        [
            "Highly recommend",
            "Recommend",
            "Recommend with reservations",
            "Do not recommend",
        ],
    )

    work_experience = st.sidebar.selectbox(
        "Work Experience (Hospital or Community)",
        [
            "None / Minimal",
            "0 - 6 Months",
            "6 - 12 Months",
            "1 Year Plus Experience",
        ],
    )

    # --- SCORING ALGORITHM ---
    score = 0.0
    
    score += (gpa / 4.00) * 30

    if user_pharm_school in high_pass_rate_schools:
        score += 8
    else:
        score += 4

    if honor_society == "Officer / Leadership Role in Rho Chi or PLS":
        score += 10
    elif honor_society == "Member of Both (Rho Chi AND PLS)":
        score += 8
    elif honor_society == "Member of One (Rho Chi OR PLS)":
        score += 5

    if leadership == "Executive / Multi-Officer":
        score += 10
    elif leadership == "Local Officer":
        score += 7
    elif leadership == "Local Committee / Member":
        score += 4

    if community_service == "Extensive Involvement (Regular Volunteering / Board Lead)":
        score += 8
    elif community_service == "Moderate Involvement (Local Events / Health Fairs)":
        score += 5
    else:
        score += 2

    if research == "Yes":
        score += 7

    if poster_level == "National":
        score += 6
    elif poster_level == "Regional":
        score += 5
    elif poster_level == "State":
        score += 4
    elif poster_level == "Local":
        score += 2

    if lor_strength == "Highly recommend":
        score += 12
    elif lor_strength == "Recommend":
        score += 7
    elif lor_strength == "Recommend with reservations":
        score += 2
    else:
        score += 0

    if work_experience == "1 Year Plus Experience":
        score += 18
    elif work_experience == "6 - 12 Months":
        score += 12
    elif work_experience == "0 - 6 Months":
        score += 8
    else:
        score += 2

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
            "• Institutional Context: Coming from an external or international program means leaning heavily on strong regional APPE rotations and establishing direct connections with program preceptors."
        )
    elif user_pharm_school != "":
        recommendations.append(
            "• Network Leverage: Leverage your institution's alumni network and established regional preceptor ties to gain familiarity and comfort during application reviews."
        )

    if gpa < 3.5:
        recommendations.append(
            "• GPA Elevation: Consider highlighting high grades in advanced therapeutics or securing strong APPE rotation evaluations to compensate for a sub-3.5 GPA."
        )
    if honor_society == "None" and gpa >= 3.5:
        recommendations.append(
            "• Honor Society Eligibility: With a strong GPA, check your academic standing for Rho Chi or PLS eligibility to add formal academic prestige to your application."
        )
    if leadership in ["None", "Local Committee / Member"]:
        recommendations.append(
            "• Leadership Growth: Stepping into an officer role within professional organizations strengthens your executive profile."
        )
    if community_service == "Minimal / None":
        recommendations.append(
            "• Community Service: Engaging in pharmacy-led health fairs or community outreach events demonstrates civic leadership and patient advocacy."
        )
    if research == "No":
        recommendations.append(
            "• Research Background: Participating in clinical research or case reports adds significant value to your profile."
        )
    if poster_level == "None":
        recommendations.append(
            "• Poster Presentations: Submitting a poster to a state or national convention highlights scientific communication skills."
        )
    if lor_strength in ["Recommend", "Recommend with reservations", "Do not recommend"]:
        recommendations.append(
            "• Recommendation Quality: Cultivate relationships with clinical preceptors early during APPE rotations to secure a 'Highly recommend' evaluation."
        )
    if work_experience in ["None / Minimal", "0 - 6 Months"]:
        recommendations.append(
            "• Work Experience: Accumulating longitudinal pharmacy practice experience (hospital or community) strengthens clinical readiness metrics."
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
if sidebar_mode == "Platform Tools":
    st.header("Exploration Matrix")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "Program Query",
        "State & Track Filter",
        "Interactive Map",
        "Peer Cohort Analytics",
        "CV Match Evaluator",
        "Program Interview Hub",
        "Advanced LOI Generator",
        "LOR Strategy & Guide",
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
                    is_reach_prog = (
                        True
                        if (
                            pd.notna(beds)
                            and beds > 500
                            or "University" in str(row["Program Name"])
                            or "Academic" in str(row["Program Name"])
                        )
                        else False
                    )
                    
                    intensity_label = "High Intensity (Academic / Large Health System)" if is_reach_prog else "Standard Intensity (Community / General)"
                    required_score = 80 if is_reach_prog else 65

                    if score >= required_score:
                        fit_status = "Safety" if score >= (required_score + 10) else "Target"
                    else:
                        fit_status = "Reach"

                    st.markdown(f"""
                        <div class="highlight-fit">
                            FIT STATUS: {fit_status.upper()}
                        </div>
                    """, unsafe_allow_html=True)

                    col_candidate, col_school = st.columns(2)

                    with col_candidate:
                        st.markdown("#### Candidate Assessment")
                        st.write(f"**Your Match Score:** {score:.1f} / 100")

                    with col_school:
                        st.markdown("#### School Information & Tier")
                        st.write(f"**Location:** {row.get('Location', 'N/A')}")
                        st.write(f"**Category:** {row.get('Category', 'N/A')}")
                        st.write(f"**Stipend:** {row.get('Estimated Stipend', 'N/A')}")
                        st.info(f"**Intensity Tier:** {intensity_label}")

                    st.markdown("---")

                    if fit_status == "Safety":
                        match_def = "High probability of interview extension and successful match alignment given strong profile metrics relative to program demands."
                        rec_action = "**Recommendation:** Strongly consider applying; exceptional strategic fit for your background."
                    elif fit_status == "Target":
                        match_def = "Balanced alignment with historical cohort averages; highly competitive with solid application packaging."
                        rec_action = "**Recommendation:** Solid target choice. Ensure targeted tailoring of your letter of intent."
                    else:
                        match_def = "Significant variance from program score benchmarks; high barrier to entry without unique distinguishing attributes."
                        rec_action = "**Recommendation:** Reach choice. Treat with caution or prioritize higher-aligned safety/target options."

                    state_code = row.get("State_Code", "Unknown")
                    umpje_states = ["IL", "CO", "ID", "ND", "UT", "WA"]
                    if state_code in umpje_states:
                        exam_policy = f"State MPJE Required (Participates/Aligns with multi-state standard options or UMPJE frameworks where applicable for {state_code})."
                    else:
                        exam_policy = f"Dedicated State MPJE Required for {state_code} licensure."

                    st.markdown(f"""
                        <div class="wrapped-box">
                            <p>Fit Status: {fit_status}</p>
                            <p>Likelihood Definition: {match_def}</p>
                            <p>Recommendation: {rec_action}</p>
                            <p>Licensure Policy: {exam_policy}</p>
                        </div>
                    """, unsafe_allow_html=True)

                    st.write(f"**Deadline:** {row.get('Deadline_Display', 'N/A')} | **Slots:** {row.get('Number of Positions', 'N/A')}")

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
            display_df = state_df.copy()
            def calc_fit(r):
                b = r.get("Total Beds", 0)
                is_r = True if (pd.notna(b) and b > 500 or "University" in str(r["Program Name"]) or "Academic" in str(r["Program Name"])) else False
                req = 80 if is_r else 65
                if score >= req:
                    return "Safety" if score >= (req + 10) else "Target"
                return "Reach"

            display_df["Fit_Status"] = display_df.apply(calc_fit, axis=1)
            display_cols = [
                "Program Name",
                "Program Code",
                "Category",
                "Fit_Status",
                "Estimated Stipend",
                "Deadline_Display",
            ]
            st.dataframe(display_df[display_cols], use_container_width=True)

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
                is_reach_prog = (
                    True
                    if (
                        pd.notna(beds)
                        and beds > 500
                        or "University" in str(prog_row["Program Name"])
                        or "Academic" in str(prog_row["Program Name"])
                    )
                    else False
                )
                
                intensity_label = "High Intensity (Academic / Large Health System)" if is_reach_prog else "Standard Intensity (Community / General)"
                req_score = 80 if is_reach_prog else 65

                if score >= req_score:
                    fit_status_2 = "Safety" if score >= (req_score + 10) else "Target"
                else:
                    fit_status_2 = "Reach"

                st.markdown(f"""
                    <div class="highlight-fit">
                        FIT STATUS: {fit_status_2.upper()}
                    </div>
                """, unsafe_allow_html=True)

                col_x, col_y = st.columns(2)
                with col_x:
                    st.markdown("#### Candidate Assessment")
                    st.write(f"**Your Score:** {score:.1f} / 100")

                with col_y:
                    st.markdown("#### School Information & Tier")
                    st.write(f"**Code:** {prog_row.get('Program Code', 'N/A')}")
                    st.write(f"**Location:** {prog_row.get('Location', 'N/A')}")
                    st.write(f"**Stipend:** {prog_row.get('Estimated Stipend', 'N/A')}")
                    st.info(f"**Intensity Tier:** {intensity_label}")

                if fit_status_2 == "Safety":
                    match_def_2 = "High probability of interview extension; metrics satisfy or exceed historical cohort cutoffs."
                    rec_action_2 = "**Recommendation:** Strongly Consider Applying."
                elif fit_status_2 == "Target":
                    match_def_2 = "Competitive profile with potential areas for improvement; heavily relies on a compelling letter of intent."
                    rec_action_2 = "**Recommendation:** Consider with Caution."
                else:
                    match_def_2 = "Profile sits well below historical benchmarks; application carries a high risk of rejection."
                    rec_action_2 = "**Recommendation:** Unfavorable Match / Skip."

                state_code_2 = prog_row.get("State_Code", selected_state)
                umpje_states = ["IL", "CO", "ID", "ND", "UT", "WA"]
                if state_code_2 in umpje_states:
                    exam_policy_2 = f"State MPJE Required (Compatible with flexible/multi-state frameworks or UMPJE alternatives in {state_code_2})."
                else:
                    exam_policy_2 = f"Dedicated State MPJE Required for {state_code_2} licensure."

                st.markdown(f"""
                    <div class="wrapped-box">
                        <p>Fit Status: {fit_status_2}</p>
                        <p>Likelihood Definition: {match_def_2}</p>
                        <p>Recommendation: {rec_action_2}</p>
                        <p>Licensure Policy: {exam_policy_2}</p>
                    </div>
                """, unsafe_allow_html=True)

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
        else:
            st.info("No programs found matching the selected state/track filter combination.")
