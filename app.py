import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Pharmacy Residency Match & Tracker", page_icon="💊", layout="wide"
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

st.title("💊 Pharmacy Residency Match & Competitiveness Calculator")

# --- PROFESSIONAL DISCLAIMER ---
st.info(
    "**Notice & Disclaimer:** This application is designed as an interactive"
    " guide to assist pharmacy students with the residency application"
    " process. The competitiveness calculations and program insights are"
    " derived from the ASHP residency portal database and algorithmic scoring,"
    " and do not serve as a definitive guarantee of admission or match"
    " outcomes. Use this tool alongside professional mentorship and official"
    " program guidelines."
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
st.sidebar.header("Step 1: Your Profile Metrics")

user_pharm_school = st.sidebar.selectbox("College of Pharmacy", pharmacy_schools)
gpa = st.sidebar.slider("PharmD GPA", 2.00, 4.00, 3.50, 0.01)

work_experience = st.sidebar.selectbox(
    "Pharmacy Work Experience",
    [
        "None / Minimal",
        "Community / Retail Experience (> 1 Year)",
        "Hospital / Health-System Intern (1+ Years)",
        "Multiple Clinical / Specialized Internships",
    ],
)

research = st.sidebar.selectbox(
    "Active Research / Poster Presentation", ["No", "Yes"]
)
leadership = st.sidebar.selectbox(
    "Leadership Level",
    ["None", "Local Committee / Member", "Local Officer", "Executive / Multi-Officer"],
)
lor_strength = st.sidebar.selectbox(
    "Letters of Recommendation (LOR) Quality",
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
st.sidebar.subheader(f"Calculated Profile Score: {score:.1f} / 100")
st.sidebar.caption(f"Institution: {user_pharm_school}")

if score >= 80:
  st.sidebar.success("Competitiveness: Highly Competitive (Strong PGY1/PGY2 Profile)")
elif score >= 65:
  st.sidebar.info("Competitiveness: Competitive (Solid Standard Profile)")
else:
  st.sidebar.warning(
      "Competitiveness: Developing (Focus on targeted program selection & boosting"
      " CV)"
  )


# --- MAIN PANEL: PROGRAM EXPLORATION ---
st.header("Step 2: Explore & Analyze Programs")

tab1, tab2 = st.tabs(["🔍 Search by Program Name (e.g. NYU)", "🗺️ Filter by State & PGY-1 Track"])

with tab1:
  search_query = st.text_input("Enter Hospital or Program Name", "", key="t1_search")
  if search_query:
    res = df_programs[
        df_programs["Program Name"]
        .str.contains(search_query, case=False, na=False)
    ]

    if not res.empty:
      st.markdown(
          f"### Found **{len(res)}** matching programs for '{search_query}'"
      )
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
            st.warning("Tier: Highly Competitive (Reach)")
            required_score = 80
          else:
            st.info("Tier: Competitive / Standard")
            required_score = 65

          st.write(
              f"**Match Likelihood:** {'🟢 Strong Fit' if score >= required_score else '🟡 Reach / Moderate Fit'}"
          )
        with col_b:
          st.write(f"**Location:** {row.get('Location', 'N/A')}")
          st.write(f"**Category:** {row.get('Category', 'N/A')}")
          st.write(f"**Stipend:** {row.get('Estimated Stipend', 'N/A')}")
        with col_c:
          st.write(f"**Deadline:** {row.get('Deadline_Display', 'N/A')}")
          st.write(f"**Positions:** {row.get('Number of Positions', 'N/A')}")

        with st.expander("View Residency Description & Requirements"):
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
      st.info("No matching programs found.")

with tab2:
  col_s1, col_s2, col_s3 = st.columns(3)
  with col_s1:
    states = sorted(df_programs["State_Code"].dropna().unique())
    selected_state = st.selectbox("Select State", states, key="t2_state")
  with col_s2:
    categories = ["All"] + sorted(
        df_programs["Category"].dropna().unique().tolist()
    )
    selected_cat = st.selectbox("Program Category", categories, key="t2_cat")
  with col_s3:
    # Subcategory filter based on text inside Residency Description or Program Name
    sub_focus = st.selectbox(
        "PGY-1 Sub-Focus Track",
        ["All Tracks", "Ambulatory Care", "Community-Based", "Health-System / Acute Care", "Managed Care"],
        key="t2_subcat"
    )

  state_df = df_programs[df_programs["State_Code"] == selected_state]
  if selected_cat != "All":
    state_df = state_df[state_df["Category"] == selected_cat]

  # Filter by PGY-1 sub-focus text in description if selected
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

  st.markdown(
      f"### Found **{len(state_df)}** programs matching your filters in **{selected_state}**"
  )

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
    st.subheader("🎯 Program Competitiveness Inspector")
    selected_prog_code = st.selectbox(
        "Select a Program Code from this list to evaluate your competitiveness:",
        state_df["Program Code"].dropna().unique(),
        key="t2_inspector",
    )

    if selected_prog_code:
      prog_row = state_df[
          state_df["Program Code"] == selected_prog_code
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
          st.warning("Tier: Highly Competitive (Reach Program)")
          req_score = 80
        else:
          st.info("Tier: Competitive / Standard Program")
          req_score = 65

        st.metric(
            "Your Match Likelihood",
            (
                "🟢 Strong Fit"
                if score >= req_score
                else "🟡 Reach / Needs Focus"
            ),
        )
      with col_y:
        st.write(f"**Program Code:** {prog_row.get('Program Code', 'N/A')}")
        st.write(f"**Location:** {prog_row.get('Location', 'N/A')}")
        st.write(f"**Stipend:** {prog_row.get('Estimated Stipend', 'N/A')}")

      with st.expander("View Full Program Details"):
        st.write(
            "**Description:**",
            prog_row.get("Residency Description", "No description available."),
        )
        st.write(
            "**Eligibility Requirements:**",
            prog_row.get(
                "Eligibility Requirements for Program",
                "No specific requirements listed.",
            ),
        )
  else:
    st.info("No programs match your current filter and sub-focus combination.")
