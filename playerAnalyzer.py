import streamlit as st
import pandas as pd
from statistics import mean

# ------------------------
# PAGE TITLE
# ------------------------

st.set_page_config(page_title="Player Analyzer", layout="wide")

st.title("🏀 Player Performance & Salary Value Analyzer")

st.write("""
Analyze if a player is undervalued, fairly paid, or overpaid
based on performance and salary.
""")

# ------------------------
# SESSION STORAGE
# ------------------------

if "players" not in st.session_state:
    st.session_state.players = []

players = st.session_state.players

# ------------------------
# FUNCTIONS
# ------------------------

def calculate_performance_score(points, assists, rebounds, steals, blocks):
    return (
        points * 1.0
        + assists * 1.3
        + rebounds * 1.2
        + steals * 1.7
        + blocks * 1.5
    )

def calculate_value_score(performance_score, salary):
    return performance_score / salary

def classify_player(value_score):
    if value_score >= 18:
        return "Undervalued"
    elif value_score >= 12:
        return "Fair Value"
    else:
        return "Overpaid"

def build_recommendation(classification):
    if classification == "Undervalued":
        return "Strong value for the salary. This player may be worth keeping or targeting."

    elif classification == "Fair Value":
        return "Reasonable contract value based on performance."

    else:
        return "Performance appears low compared to salary. Review contract value carefully."

# ------------------------
# INPUT SECTION
# ------------------------

st.header("Player Inputs")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Player Name")
    team = st.text_input("Team")
    points = st.number_input("Points Per Game", min_value=0.0)
    assists = st.number_input("Assists Per Game", min_value=0.0)

with col2:
    rebounds = st.number_input("Rebounds Per Game", min_value=0.0)
    steals = st.number_input("Steals Per Game", min_value=0.0)
    blocks = st.number_input("Blocks Per Game", min_value=0.0)
    salary = st.number_input("Salary (Millions)", min_value=0.1)

# ------------------------
# ANALYZE BUTTON
# ------------------------

if st.button("Analyze Player"):

    performance_score = calculate_performance_score(
        points,
        assists,
        rebounds,
        steals,
        blocks
    )

    value_score = calculate_value_score(performance_score, salary)

    classification = classify_player(value_score)

    recommendation = build_recommendation(classification)

    player_record = {
        "Player": name,
        "Team": team,
        "Performance Score": round(performance_score, 2),
        "Salary": round(salary, 2),
        "Value Score": round(value_score, 2),
        "Classification": classification
    }

    players.append(player_record)

    # ------------------------
    # RESULTS
    # ------------------------

    st.success("Player analyzed successfully!")

    st.subheader("Player Analysis Result")

    st.write(f"### {name} - {team}")
    st.write(f"Performance Score: {performance_score:.2f}")
    st.write(f"Value Score: {value_score:.2f}")
    st.write(f"Classification: **{classification}**")
    st.write(f"Recommendation: {recommendation}")

# ------------------------
# SUMMARY SECTION
# ------------------------

if players:

    st.header("Team / Session Summary")

    average_value = mean(player["Value Score"] for player in players)

    best_player = max(players, key=lambda x: x["Value Score"])
    worst_player = min(players, key=lambda x: x["Value Score"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Players Analyzed", len(players))
    col2.metric("Average Value Score", f"{average_value:.2f}")
    col3.metric("Best Value Player", best_player["Player"])
    col4.metric("Lowest Value Player", worst_player["Player"])

    # ------------------------
    # TABLE
    # ------------------------

    st.header("Saved Player Results")

    df = pd.DataFrame(players)

    st.dataframe(df, use_container_width=True)

# ------------------------
# CLEAR BUTTON
# ------------------------

if st.button("Clear All Players"):
    st.session_state.players = []
    st.rerun()
