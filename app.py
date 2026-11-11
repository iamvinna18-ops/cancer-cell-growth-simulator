import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Cancer Cell Growth Simulator",
    page_icon="🧬",
    layout="wide"
)

# ---------------------------------------------------------
# PROFESSIONAL THEME
# ---------------------------------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #0B1120;
    color: #F1F5F9;
}
h1, h2, h3 {
    color: #A78BFA !important;
    font-weight: 700;
}
p, label, .stMarkdown {
    color: #CBD5E1;
}
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #334155;
}
div[data-testid="stMetric"] {
    background-color: #1E293B;
    border: 1px solid #475569;
    padding: 18px;
    border-radius: 12px;
}
div[data-testid="stMetricValue"] {
    color: #A78BFA;
}
.stButton > button {
    background-color: #7C3AED;
    color: white;
    border-radius: 8px;
    border: none;
}
hr {
    border-color: #334155;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR: NAVIGATION
# ---------------------------------------------------------
st.sidebar.title("🧬 Cancer Cell Simulator")
st.sidebar.caption("Biology Experiential Learning Project")
st.sidebar.divider()

page = st.sidebar.radio(
    "Website Navigation",
    [
        "Home",
        "Growth Simulation",
        "Cell Population Visualizer",
        "Cell Division Explorer",
        "Tumor Growth",
        "Treatment Analysis",
        "Participant Simulation",
        "About Project"
    ],
    key="main_navigation"
)

st.sidebar.divider()
st.sidebar.title("⚙️ Simulation Controls")

st.sidebar.subheader("Cell Population")
initial_cells = st.sidebar.slider(
    "Initial Cell Population", 10, 1000, 100
)
growth_rate = st.sidebar.slider(
    "Growth Rate", 0.01, 0.50, 0.10, step=0.01
)
days = st.sidebar.slider(
    "Simulation Duration (Days)", 30, 365, 100
)

st.sidebar.subheader("Environment")
nutrients = st.sidebar.selectbox(
    "Nutrient Availability", ["Low", "Medium", "High"]
)
capacities = {"Low": 3000, "Medium": 6000, "High": 10000}
K = capacities[nutrients]

st.sidebar.subheader("Treatment")
treatment_start = st.sidebar.slider(
    "Treatment Start Day", 0, days, min(30, days)
)
treatment_effect = st.sidebar.slider(
    "Treatment Effect (%)", 0, 100, 50
)

# ---------------------------------------------------------
# MATHEMATICAL MODEL CALCULATIONS
# ---------------------------------------------------------
time = np.arange(days + 1)
exponential = initial_cells * np.exp(growth_rate * time)

untreated = [float(initial_cells)]
treated = [float(initial_cells)]

for day in range(1, days + 1):
    previous = untreated[-1]
    growth = growth_rate * previous * (1 - previous / K)
    untreated.append(max(0, previous + growth))

    previous = treated[-1]
    effective_rate = growth_rate
    if day >= treatment_start:
        effective_rate *= (1 - treatment_effect / 100)

    growth = effective_rate * previous * (1 - previous / K)
    treated.append(max(0, previous + growth))

# ---------------------------------------------------------
# REUSABLE PAGE HEADER
# ---------------------------------------------------------
def page_header(title, subtitle):
    st.title(title)
    st.write(subtitle)
    st.divider()

# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------
if page == "Home":
    st.title("🧬 CANCER CELL SIMULATION")
    st.markdown("#### BIOLOGICAL MODELLING & RESEARCH PLATFORM")
    st.write(
        "An interactive educational platform exploring cancer cell "
        "proliferation, population dynamics, environmental limitations "
        "and hypothetical treatment responses using mathematical models."
    )
    st.caption("BIOLOGY EXPERIENTIAL LEARNING PROJECT | 2026")
    st.divider()

    st.header("Welcome to the Simulation")
    st.write(
        "Use the navigation menu on the left to explore cancer cell growth, "
        "cell division, tumor population visualization and hypothetical "
        "treatment scenarios."
    )
    st.info(
        "Educational simulation only. Results are mathematical "
        "illustrations, not clinical predictions."
    )

    st.subheader("📊 Current Simulation Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Initial Cell Population", f"{initial_cells:,}")
    c2.metric("Final Untreated Population", f"{untreated[-1]:,.0f}")
    c3.metric("Final Treated Population", f"{treated[-1]:,.0f}")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(time, untreated, label="Without Treatment", linewidth=2)
    ax.plot(time, treated, label="With Treatment", linewidth=2)
    ax.axvline(treatment_start, linestyle="--", label="Treatment Start")
    ax.set_xlabel("Time (Days)")
    ax.set_ylabel("Cell Population")
    ax.set_title("Cancer Cell Population: Overview")
    ax.legend()
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Explore the website")
    st.markdown("""
    - **Growth Simulation:** Compare exponential and logistic growth.
    - **Cell Population Visualizer:** View an illustrative cell sample.
    - **Cell Division Explorer:** Learn the stages of mitosis.
    - **Tumor Growth:** Explore an expanding illustrative cell cluster.
    - **Treatment Analysis:** Compare hypothetical treatment mechanisms.
    - **About Project:** Read the objectives, equations and methodology.
    """)

# ---------------------------------------------------------
# GROWTH SIMULATION PAGE
# ---------------------------------------------------------
elif page == "Growth Simulation":
    page_header(
        "📈 Cancer Cell Growth Simulation",
        "Explore exponential and logistic population growth under the selected simulation settings."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Initial Population", f"{initial_cells:,}")
    c2.metric("Final Untreated Population", f"{untreated[-1]:,.0f}")
    c3.metric("Final Treated Population", f"{treated[-1]:,.0f}")

    st.subheader("1. Exponential Growth Model")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(time, exponential, color="tomato", linewidth=2,
             label="Exponential Growth")
    ax1.set_xlabel("Time (Days)")
    ax1.set_ylabel("Cell Population")
    ax1.set_title("Exponential Cancer Cell Growth")
    ax1.legend()
    ax1.grid(alpha=0.3)
    st.pyplot(fig1)
    plt.close(fig1)

    st.subheader("2. Logistic Growth Model")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(time, untreated, label="Without Treatment", linewidth=2)
    ax2.plot(time, treated, label="With Treatment", linewidth=2)
    ax2.axvline(treatment_start, linestyle="--", label="Treatment Start")
    ax2.axhline(K, linestyle=":", label=f"Carrying Capacity (K={K})")
    ax2.set_xlabel("Time (Days)")
    ax2.set_ylabel("Cell Population")
    ax2.set_title("Treated vs Untreated Logistic Growth")
    ax2.legend()
    ax2.grid(alpha=0.3)
    st.pyplot(fig2)
    plt.close(fig2)

    st.subheader("Biological Interpretation")
    st.write("**Exponential growth:** Represents growth without resource limitations.")
    st.write("**Logistic growth:** Includes a carrying capacity to represent limited resources.")
    st.write("**Treatment model:** Reduces the assumed effective growth rate after the selected treatment start day.")

# ---------------------------------------------------------
# CELL POPULATION VISUALIZER PAGE
# ---------------------------------------------------------
elif page == "Cell Population Visualizer":
    page_header(
        "🔬 Cancer Cell Population Visualizer",
        "Explore how the simulated population changes at different stages."
    )

    selected_day = st.slider(
        "Select Simulation Day", 0, days, 0, key="visual_day"
    )
    population_type = st.selectbox(
        "Select Population", ["Untreated", "Treated"], key="visual_population"
    )
    current_population = (
        untreated[selected_day]
        if population_type == "Untreated"
        else treated[selected_day]
    )

    st.metric("Cell Population on Selected Day", f"{current_population:,.0f}")

    rng = np.random.default_rng(42)
    number_of_dots = min(max(1, int(current_population)), 150)
    x_points = rng.uniform(0, 10, number_of_dots)
    y_points = rng.uniform(0, 10, number_of_dots)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(x_points, y_points, s=100, color="purple",
               alpha=0.7, edgecolors="black")
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 11)
    ax.set_title(f"Illustrative Cell Population - Day {selected_day}")
    ax.set_xlabel("Cell Distribution X")
    ax.set_ylabel("Cell Distribution Y")
    ax.set_aspect("equal")
    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "Each dot is part of a visual sample, not necessarily one individual cell. "
        "The spatial arrangement is illustrative and is not a real tumor map."
    )

# ---------------------------------------------------------
# CELL DIVISION EXPLORER PAGE
# ---------------------------------------------------------
elif page == "Cell Division Explorer":
    page_header(
        "🧬 Cell Division Explorer",
        "Explore the stages of mitosis and how one parent cell produces two daughter cells."
    )

    stages = {
        "Interphase": "The cell grows and duplicates its DNA.",
        "Prophase": "Chromosomes condense and become visible.",
        "Metaphase": "Chromosomes align at the centre of the cell.",
        "Anaphase": "Sister chromatids move towards opposite poles.",
        "Telophase": "Two new nuclei begin to form.",
        "Cytokinesis": "The parent cell divides into two daughter cells."
    }

    selected_stage = st.selectbox(
        "Choose a Cell Division Stage", list(stages.keys())
    )
    st.info(stages[selected_stage])

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")

    if selected_stage != "Cytokinesis":
        cell = plt.Circle((5, 2.5), 1.5, color="plum", alpha=0.5)
        ax.add_patch(cell)
        nucleus = plt.Circle((5, 2.5), 0.85, color="purple", alpha=0.35)
        ax.add_patch(nucleus)

        positions = {
            "Interphase": [(4.8, 2.5)],
            "Prophase": [(4.5, 2.5), (5.5, 2.5)],
            "Metaphase": [(5, 1.9), (5, 2.5), (5, 3.1)],
            "Anaphase": [(4.3, 2.5), (5.7, 2.5)],
            "Telophase": [(4.4, 2.5), (5.6, 2.5)]
        }
        for x_pos, y_pos in positions[selected_stage]:
            ax.plot(
                [x_pos - 0.15, x_pos + 0.15],
                [y_pos - 0.25, y_pos + 0.25],
                color="darkred", linewidth=3
            )
            ax.plot(
                [x_pos - 0.15, x_pos + 0.15],
                [y_pos + 0.25, y_pos - 0.25],
                color="darkred", linewidth=3
            )
    else:
        for x_pos in [3.2, 6.8]:
            cell = plt.Circle((x_pos, 2.5), 1.2, color="plum", alpha=0.5)
            ax.add_patch(cell)
            nucleus = plt.Circle((x_pos, 2.5), 0.65, color="purple", alpha=0.4)
            ax.add_patch(nucleus)
        ax.text(5, 0.5, "Two Daughter Cells", ha="center", fontsize=13)

    ax.set_title("Illustrative Mitosis Diagram: " + selected_stage)
    st.pyplot(fig)
    plt.close(fig)
    st.caption(
        "Simplified educational illustration. It does not show exact chromosome "
        "counts or every molecular event of mitosis."
    )

# ---------------------------------------------------------
# TUMOR GROWTH PAGE
# ---------------------------------------------------------
elif page == "Tumor Growth":
    page_header(
        "🔬 Tumor Growth Visualization",
        "Observe an illustrative cell cluster as the simulated population changes over time."
    )

    tumor_day = st.slider(
        "Select Tumor Growth Day", 0, days, 0, key="tumor_day"
    )
    tumor_population = int(untreated[tumor_day])
    st.metric("Simulated Tumor Cell Population", f"{tumor_population:,}")

    rng = np.random.default_rng(42)
    number_of_cells = min(max(1, tumor_population), 500)
    angles = rng.uniform(0, 2 * np.pi, number_of_cells)
    radii = np.sqrt(rng.uniform(0, 1, number_of_cells))
    cluster_radius = np.sqrt(tumor_population / initial_cells)
    x_points = cluster_radius * radii * np.cos(angles)
    y_points = cluster_radius * radii * np.sin(angles)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x_points, y_points, s=75, color="purple",
               alpha=0.65, edgecolors="darkred", linewidths=0.5)
    ax.set_title(f"Illustrative Tumor Cell Cluster - Day {tumor_day}")
    ax.set_xlabel("Spatial X")
    ax.set_ylabel("Spatial Y")
    ax.set_aspect("equal")
    ax.grid(alpha=0.2)
    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "Illustrative spatial visualization. The dots are a sample of the "
        "simulated population, not a validated model of tumor shape or invasion."
    )
    st.subheader("Understanding Tumor Development")
    st.write(
        "Cancer cells can divide repeatedly and form expanding populations. "
        "Tumor development is influenced by cell division, cell death, blood "
        "supply, oxygen, nutrients and interactions with surrounding tissue."
    )

# ---------------------------------------------------------
# TREATMENT ANALYSIS PAGE
# ---------------------------------------------------------
elif page == "Treatment Analysis":
    page_header(
        "💊 Advanced Treatment Effectiveness Analysis",
        "Compare hypothetical treatment mechanisms and their effect on the simulated population."
    )

    mechanism = st.selectbox(
        "Select Treatment Mechanism",
        ["Growth Inhibition", "Cell Killing", "Combined Treatment"],
        key="advanced_mechanism"
    )
    intensity = st.slider(
        "Treatment Intensity (%)", 0, 100, 50,
        key="advanced_intensity"
    )

    inhibition_rate = 0.0
    death_rate = 0.0
    if mechanism == "Growth Inhibition":
        inhibition_rate = intensity / 100
    elif mechanism == "Cell Killing":
        death_rate = 0.02 * intensity / 100
    else:
        inhibition_rate = intensity / 100
        death_rate = 0.02 * intensity / 100

    advanced_treated = [float(initial_cells)]
    for day in range(1, days + 1):
        previous = advanced_treated[-1]
        effective_growth = growth_rate
        effective_death = 0.0

        if day >= treatment_start:
            effective_growth = growth_rate * (1 - inhibition_rate)
            effective_death = death_rate

        growth = effective_growth * previous * (1 - previous / K)
        cell_death = effective_death * previous
        next_population = previous + growth - cell_death
        advanced_treated.append(max(0, next_population))

    final_untreated = untreated[-1]
    final_advanced = advanced_treated[-1]
    reduction = (
        ((final_untreated - final_advanced) / final_untreated) * 100
        if final_untreated > 0 else 0
    )

    st.write(f"Treatment begins on Day: **{treatment_start}**")
    c1, c2, c3 = st.columns(3)
    c1.metric("Untreated Population", f"{final_untreated:,.0f}")
    c2.metric("Treated Population", f"{final_advanced:,.0f}")
    c3.metric("Population Difference", f"{reduction:.2f}%")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(time, untreated, label="Without Treatment", linewidth=2)
    ax.plot(time, advanced_treated, label="With Treatment", linewidth=2)
    ax.axvline(treatment_start, linestyle="--", label="Treatment Start")
    ax.set_xlabel("Time (Days)")
    ax.set_ylabel("Cell Population")
    ax.set_title("Treatment Effect on Cancer Cell Population")
    ax.legend()
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("🔬 Treatment Interpretation")
    if mechanism == "Growth Inhibition":
        st.write("Growth inhibition reduces the assumed rate of cell multiplication.")
    elif mechanism == "Cell Killing":
        st.write("The model adds an assumed treatment-related cell death rate.")
    else:
        st.write("Combined treatment includes both assumed growth inhibition and cell death.")

    st.info(
        "This is a hypothetical mathematical model. Its parameters are illustrative "
        "and do not represent actual chemotherapy effectiveness or clinical advice."
    )

# ---------------------------------------------------------
# ABOUT PROJECT PAGE
# ---------------------------------------------------------
elif page == "About Project":
    page_header(
        "📚 About Our Project",
        "Project background, objectives, mathematical models and technologies."
    )

    st.subheader("Project Overview")
    st.write(
        "Cancer is a disease characterized by uncontrolled cell growth and division. "
        "This project uses mathematical models and interactive visualizations to "
        "demonstrate how cancer cell populations change over time under different "
        "environmental conditions and hypothetical treatment scenarios."
    )

    st.subheader("🎯 Project Objectives")
    st.markdown("""
    - Understand cancer cell proliferation.
    - Study exponential and logistic growth models.
    - Explore the biological stages of mitosis.
    - Visualize simulated tumor cell population growth.
    - Understand hypothetical treatment effects.
    - Connect mathematical concepts with biological processes.
    """)

    st.subheader("🧮 Mathematical Models")
    st.markdown("**1. Exponential Growth Model**")
    st.latex(r"N(t) = N_0 e^{rt}")
    st.write("Describes population growth without resource limitations.")

    st.markdown("**2. Logistic Growth Model**")
    st.latex(r"\frac{dN}{dt} = rN\left(1-\frac{N}{K}\right)")
    st.write("Describes population growth when resources are limited.")

    st.markdown("**3. Treatment Model**")
    st.latex(
        r"\frac{dN}{dt} = r_{\mathrm{eff}}N"
        r"\left(1-\frac{N}{K}\right)-dN"
    )
    st.write(
        "Here, the effective growth rate represents assumed treatment-related "
        "growth inhibition and d represents the assumed cell death rate."
    )

    st.subheader("🛠️ Technologies Used")
    st.markdown("""
    - Python
    - Streamlit
    - NumPy
    - Matplotlib
    """)

    st.subheader("🔬 Project Scope")
    st.info(
        "This is an educational mathematical simulation. It does not model every "
        "biological mechanism of cancer and must not be used for medical diagnosis "
        "or treatment decisions."
    )


# --------------------------------------------------
# PARTICIPANT SIMULATION PAGE
# --------------------------------------------------

elif page == "Participant Simulation":

    page_header(
        "👥 Participant Simulation",
        "Compare fictional cancer cell population scenarios"
    )

    st.info(
        "Educational demonstration only. All cell counts and "
        "growth rates are randomly generated and are not real "
        "patient measurements or clinical predictions."
    )

    # Initialize participant storage
    if "participants" not in st.session_state:
        st.session_state.participants = []

    st.subheader("Add Participants")

    with st.form("participant_form"):
        participant_name = st.text_input(
            "Enter participant name"
        )

        add_button = st.form_submit_button(
            "Add Participant and Generate Cells"
        )

        if add_button:
            if not participant_name.strip():
                st.warning("Please enter a name.")

            elif len(st.session_state.participants) >= 5:
                st.warning("Maximum of 5 participants allowed.")

            elif any(
                p["name"].lower() == participant_name.strip().lower()
                for p in st.session_state.participants
            ):
                st.warning("This name has already been added.")

            else:
                new_participant = {
                    "id": f"P{len(st.session_state.participants) + 1:03d}",
                    "name": participant_name.strip(),
                    "cells": random.randint(10, 1000),
                    "rate": random.uniform(0.03, 0.12)
                }

                st.session_state.participants.append(
                    new_participant
                )

                st.success("Participant added successfully!")

    st.divider()

    st.subheader("Participant Cell Population")

    participants = st.session_state.participants

    if participants:

        for p in participants:
            col1, col2, col3 = st.columns(3)

            col1.metric("Participant", p["name"])
            col2.metric("Participant ID", p["id"])
            col3.metric("Initial Cell Count", f'{p["cells"]:,}')

        st.divider()

        st.subheader("Compare Population Growth")

        days = np.arange(0, 31)

        fig, ax = plt.subplots(figsize=(10, 5))

        for p in participants:
            population = (
                p["cells"] * np.exp(p["rate"] * days)
            )

            ax.plot(
                days,
                population,
                label=p["name"]
            )

        ax.set_title("Simulated Cell Population Growth")
        ax.set_xlabel("Time (Days)")
        ax.set_ylabel("Simulated Cell Population")
        ax.legend()
        ax.grid(alpha=0.3)

        st.pyplot(fig)
        plt.close(fig)

        st.caption(
            "Growth curves use hypothetical exponential growth "
            "rates generated randomly for demonstration."
        )

        if st.button("Clear All Participants"):
            st.session_state.participants = []
            st.rerun()

    else:
        st.warning(
            "No participants added yet. Enter a name above "
            "to generate the first simulated population."
        )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.divider()
st.caption(
    "Cancer Cell Growth Simulation | Biology Experiential Learning Project | "
    "Educational use only"
)
