import streamlit as st
from statistics import mean

# This app helps check if a player is overpaid or underpaid
# Based on their stats and salary

if "players" not in st.session_state:
    st.session_state.players = []

players = st.session_state.players


def calculate_performance_score(points, assists, rebounds, steals, blocks):
    return (
        points * 1.0
        + assists * 1.3
        + rebounds * 1.2
        + steals * 1.7
        + blocks * 1.5
    )


def calculate_value_score(performance_score, salary_millions):
    if salary_millions <= 0:
        st.error("Salary must be greater than 0.")
        return 0
    return performance_score / salary_millions


def classify_player(value_score):
    if value_score >= 18:
        return "Undervalued"
    if value_score >= 12:
        return "Fair Value"
    return "Overpaid"


def build_recommendation(classification):
    if classification == "Undervalued":
        return "Strong value for the salary. This player may be worth keeping or targeting."
    if classification == "Fair Value":
        return "Reasonable contract value based on performance."
    return "Performance appears low compared to salary. Review contract value carefully."


def update_summary():
    if not players:
        st.write("Total Players Analyzed: 0")
        st.write("Average Value Score: 0.00")
        st.write("Best Value Player: None")
        st.write("Lowest Value Player: None")
        return

    total_players = len(players)
    average_value = mean(player["value_score"] for player in players)
    best_player = max(players, key=lambda player: player["value_score"])
    worst_player = min(players, key=lambda player: player["value_score"])

    st.write(f"Total Players Analyzed: {total_players}")
    st.write(f"Average Value Score: {average_value:.2f}")
    st.write(
        f"Best Value Player: {best_player['name']} "
        f"({best_player['classification']}, {best_player['value_score']:.2f})"
    )
    st.write(
        f"Lowest Value Player: {worst_player['name']} "
        f"({worst_player['classification']}, {worst_player['value_score']:.2f})"
    )


# ------------------------
# STREAMLIT APP SETUP
# ------------------------

st.set_page_config(page_title="Player Analyzer", layout="wide")

st.title("Player Performance & Salary Value Analyzer")

st.write(
    "Analyze if a player is undervalued, fairly paid, or overpaid based on performance and salary."
)

# ------------------------
# INPUT SECTION
# ------------------------

st.subheader("Player Inputs")

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
# BUTTON SECTION
# ------------------------

analyze_button = st.button("Analyze Player")
clear_all_button = st.button("Clear All Players")

# ------------------------
# RESULT SECTION
# ------------------------

if analyze_button:
    if not name:
        st.error("Please enter the player name.")
    elif not team:
        st.error("Please enter the team name.")
    else:
        performance_score = calculate_performance_score(
            points, assists, rebounds, steals, blocks
        )

        value_score = calculate_value_score(performance_score, salary)

        classification = classify_player(value_score)

        recommendation = build_recommendation(classification)

        player_record = {
            "name": name,
            "team": team,
            "points": points,
            "assists": assists,
            "rebounds": rebounds,
            "steals": steals,
            "blocks": blocks,
            "salary": salary,
            "performance_score": performance_score,
            "value_score": value_score,
            "classification": classification,
        }

        players.append(player_record)

        st.subheader("Player Analysis Result")
        st.write(f"Player: {name}")
        st.write(f"Team: {team}")
        st.write(f"Performance Score: {performance_score:.2f}")
        st.write(f"Value Score: {value_score:.2f}")
        st.write(f"Classification: {classification}")
        st.write(f"Recommendation: {recommendation}")

# ------------------------
# SUMMARY SECTION
# ------------------------

st.subheader("Team / Session Summary")
update_summary()

# ------------------------
# TABLE SECTION
# ------------------------

st.subheader("Saved Player Results")

if players:
    st.table(
        [
            {
                "Player": player["name"],
                "Team": player["team"],
                "Performance": f"{player['performance_score']:.2f}",
                "Salary": f"{player['salary']:.2f}",
                "Value Score": f"{player['value_score']:.2f}",
                "Classification": player["classification"],
            }
            for player in players
        ]
    )
else:
    st.write("No saved players yet.")

# ------------------------
# CLEAR ALL PLAYERS
# ------------------------

if clear_all_button:
    st.session_state.players = []
    st.rerun()
