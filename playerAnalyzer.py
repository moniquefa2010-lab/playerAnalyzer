import tkinter as tk
from tkinter import ttk, messagebox
from statistics import mean


#This app helps check if a player is overpaid or underpaid
#Based on their stats and salary

players = [] #This list stores all players that get analyzed


def safe_float(value: str, field_name: str) -> float:
#This makes sure the input is a number and not text
#If it fails, it shows an error instead of crashing
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"Please enter a valid number for {field_name}.")


def calculate_performance_score(points: float, assists: float, rebounds: float, steals: float, blocks: float) -> float:
#This creates a performance score using player stats
#Some stats are weighted more because they impact the game more
    return (
        points * 1.0
        + assists * 1.3
        + rebounds * 1.2
        + steals * 1.7
        + blocks * 1.5
    )



def calculate_value_score(performance_score: float, salary_millions: float) -> float:
#This compares performance to salary
#Higher score = better value for the money
    if salary_millions <= 0:
        raise ValueError("Salary must be greater than 0.")
    return performance_score / salary_millions



def classify_player(value_score: float) -> str:
#This decides if the player is overpaid or not
    if value_score >= 18:
        return "Undervalued"
    if value_score >= 12:
        return "Fair Value"
    return "Overpaid"



def build_recommendation(classification: str) -> str:
#This gives a message based on the result
    if classification == "Undervalued":
        return "Strong value for the salary. This player may be worth keeping or targeting."
    if classification == "Fair Value":
        return "Reasonable contract value based on performance."
    return "Performance appears low compared to salary. Review contract value carefully."



def clear_inputs() -> None:
#This clears all input boxes so user can start fresh
    entry_name.delete(0, tk.END)
    entry_team.delete(0, tk.END)
    entry_points.delete(0, tk.END)
    entry_assists.delete(0, tk.END)
    entry_rebounds.delete(0, tk.END)
    entry_steals.delete(0, tk.END)
    entry_blocks.delete(0, tk.END)
    entry_salary.delete(0, tk.END)

#This clears results on the screen
    result_name_var.set("")
    result_team_var.set("")
    result_performance_var.set("")
    result_value_var.set("")
    result_classification_var.set("")
    result_recommendation_var.set("")



def analyze_player() -> None:
#This is the main function when user clicks "Analyze Player"
    try:
        #Get user input from text box
        name = entry_name.get().strip()
        team = entry_team.get().strip()

        #Make sure name and team are entered
        if not name:
            raise ValueError("Please enter the player name.")
        if not team:
            raise ValueError("Please enter the team name.")

        #Convert all stats into numbers
        points = safe_float(entry_points.get(), "PPG")
        assists = safe_float(entry_assists.get(), "APG")
        rebounds = safe_float(entry_rebounds.get(), "RPG")
        steals = safe_float(entry_steals.get(), "SPG")
        blocks = safe_float(entry_blocks.get(), "BPG")
        salary = safe_float(entry_salary.get(), "salary (Millions USD)")

        # Check that stats are real and not negative
        if points < 0 or assists < 0 or rebounds < 0 or steals < 0 or blocks < 0:
            raise ValueError("Stats cannot be negative.")
        if salary <= 0:
            raise ValueError("Salary must be greater than 0.")

        #Calculate performance and value
        performance_score = calculate_performance_score(points, assists, rebounds, steals, blocks)
        value_score = calculate_value_score(performance_score, salary)

        #Decide player category
        classification = classify_player(value_score)

        #create recommendation message
        recommendation = build_recommendation(classification)
        #save player info into list
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


        #shows results on the screen
        result_name_var.set(f"Player: {name}")
        result_team_var.set(f"Team: {team}")
        result_performance_var.set(f"Performance Score: {performance_score:.2f}")
        result_value_var.set(f"Value Score: {value_score:.2f}")
        result_classification_var.set(f"Classification: {classification}")
        result_recommendation_var.set(f"Recommendation: {recommendation}")


    #Update summary and table
        update_summary()
        refresh_table()

    except ValueError as error:
    #Show error instead of crashing
        messagebox.showerror("Input Error", str(error))


def update_summary() -> None:
    #This updates the summary section for the players entered

    if not players:
        summary_total_var.set("Total Players Analyzed: 0")
        summary_average_value_var.set("Average Value Score: 0.00")
        summary_best_var.set("Best Value Player: None")
        summary_worst_var.set("Lowest Value Player: None")
        return

    #This Calculates summary stats
    total_players = len(players)
    average_value = mean(player["value_score"] for player in players)
    best_player = max(players, key=lambda player: player["value_score"])
    worst_player = min(players, key=lambda player: player["value_score"])


    #Show summary on the screen
    summary_total_var.set(f"Total Players Analyzed: {total_players}")
    summary_average_value_var.set(f"Average Value Score: {average_value:.2f}")
    summary_best_var.set(
        f"Best Value Player: {best_player['name']} ({best_player['classification']}, {best_player['value_score']:.2f})"
    )
    summary_worst_var.set(
        f"Lowest Value Player: {worst_player['name']} ({worst_player['classification']}, {worst_player['value_score']:.2f})"
    )



def refresh_table() -> None:
     #Clears table first so it doesnt duplicate any rows
    for item in table.get_children():
        table.delete(item)

    #Add all players back into the table
    for player in players:
        table.insert(
            "",
            tk.END,
            values=(
                player["name"],
                player["team"],
                f"{player['performance_score']:.2f}",
                f"{player['salary']:.2f}",
                f"{player['value_score']:.2f}",
                player["classification"],
            ),
        )



def clear_all_players() -> None:
    #This removes all saved players and resets the app.
    if not players:
        messagebox.showinfo("Nothing to Clear", "There are no saved players to remove.")
        return

    #Ask the user if they are sure before deleting everything
    confirm = messagebox.askyesno("Clear Data", "Do you want to remove all analyzed players?")
    if confirm:
        players.clear()
        refresh_table()
        update_summary()
        clear_inputs()


# ------------------------
# GUI WINDOW SETUP
# ------------------------

#This creates the main app window.
root = tk.Tk()
root.title("Player Performance & Salary Value Analyzer")
root.geometry("1080x760")
root.configure(padx=15, pady=15)

#This creates the main title at the top.
main_title = tk.Label(
    root,
    text="Player Performance & Salary Value Analyzer",
    font=("Arial", 18, "bold"),
)
main_title.grid(row=0, column=0, columnspan=4, pady=(0, 15), sticky="w")

#This is for the explanation under the title
subtitle = tk.Label(
    root,
    text="Analyze if a player is undervalued, fairly paid, or overpaid based on performance and salary.",
    font=("Arial", 10),
)
subtitle.grid(row=1, column=0, columnspan=4, pady=(0, 15), sticky="w")

# ------------------------
# INPUT SECTION
# ------------------------

#This is to cerate the section where the user can type player information.
input_frame = tk.LabelFrame(root, text="Player Inputs", padx=10, pady=10)
input_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=(0, 10), pady=(0, 10))

#These are the labels shown next to each input box.
labels = [
    "Player Name",
    "Team",
    "Points Per Game",
    "Assists Per Game",
    "Rebounds Per Game",
    "Steals Per Game",
    "Blocks Per Game",
    "Salary (Millions)",
]


#This places each label on the screen.
for idx, label_text in enumerate(labels):
    tk.Label(input_frame, text=label_text).grid(row=idx, column=0, sticky="w", pady=4)

#These are the input boxes where the user types data.
entry_name = tk.Entry(input_frame, width=30)
entry_team = tk.Entry(input_frame, width=30)
entry_points = tk.Entry(input_frame, width=30)
entry_assists = tk.Entry(input_frame, width=30)
entry_rebounds = tk.Entry(input_frame, width=30)
entry_steals = tk.Entry(input_frame, width=30)
entry_blocks = tk.Entry(input_frame, width=30)
entry_salary = tk.Entry(input_frame, width=30)

entries = [
    entry_name,
    entry_team,
    entry_points,
    entry_assists,
    entry_rebounds,
    entry_steals,
    entry_blocks,
    entry_salary,
]

#This places each input box in the correct spot.
for idx, entry_widget in enumerate(entries):
    entry_widget.grid(row=idx, column=1, pady=4, padx=(10, 0))

#This is to create a small are to hold the buttons.
button_frame = tk.Frame(input_frame)
button_frame.grid(row=8, column=0, columnspan=2, pady=(12, 0), sticky="w")

#These buttons run the main action of the app.
analyze_button = tk.Button(button_frame, text="Analyze Player", width=16, command=analyze_player)
analyze_button.grid(row=0, column=0, padx=(0, 8))

clear_button = tk.Button(button_frame, text="Clear Inputs", width=16, command=clear_inputs)
clear_button.grid(row=0, column=1, padx=(0, 8))

clear_all_button = tk.Button(button_frame, text="Clear All Players", width=16, command=clear_all_players)
clear_all_button.grid(row=0, column=2)

# ------------------------
# RESULT SECTION
# ------------------------

#This creates the box where the players results will show
result_frame = tk.LabelFrame(root, text="Player Analysis Result", padx=10, pady=10)
result_frame.grid(row=2, column=2, columnspan=2, sticky="nsew", pady=(0, 10))

#These variables hold the result text show on the screen.
result_name_var = tk.StringVar(value="")
result_team_var = tk.StringVar(value="")
result_performance_var = tk.StringVar(value="")
result_value_var = tk.StringVar(value="")
result_classification_var = tk.StringVar(value="")
result_recommendation_var = tk.StringVar(value="")

result_labels = [
    result_name_var,
    result_team_var,
    result_performance_var,
    result_value_var,
    result_classification_var,
    result_recommendation_var,
]


#This places each results label on the screen.
for idx, variable in enumerate(result_labels):
    tk.Label(result_frame, textvariable=variable, wraplength=420, justify="left", anchor="w").grid(
        row=idx, column=0, sticky="w", pady=6
    )

# ------------------------
# SUMMARY SECTION
# ------------------------
#This create the summary box for all players that were entered.
summary_frame = tk.LabelFrame(root, text="Team / Session Summary", padx=10, pady=10)
summary_frame.grid(row=3, column=0, columnspan=4, sticky="nsew", pady=(0, 10))

#These variable hold the summary text.
summary_total_var = tk.StringVar(value="Total Players Analyzed: 0")
summary_average_value_var = tk.StringVar(value="Average Value Score: 0.00")
summary_best_var = tk.StringVar(value="Best Value Player: None")
summary_worst_var = tk.StringVar(value="Lowest Value Player: None")

summary_vars = [summary_total_var, summary_average_value_var, summary_best_var, summary_worst_var]

#This places each summary label on the screen.
for idx, variable in enumerate(summary_vars):
    tk.Label(summary_frame, textvariable=variable, anchor="w", justify="left").grid(row=idx, column=0, sticky="w", pady=4)

# ------------------------
# TABLE SECTION
# ------------------------

#This creates the section that stores all the players results in the table.
table_frame = tk.LabelFrame(root, text="Saved Player Results", padx=10, pady=10)
table_frame.grid(row=4, column=0, columnspan=4, sticky="nsew")

columns = ("Player", "Team", "Performance", "Salary", "Value Score", "Classification")
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

#This creates the column titles in the table.
for column in columns:
    table.heading(column, text=column)
    table.column(column, width=150, anchor="center")

table.grid(row=0, column=0, sticky="nsew")

#This adds a scrollbar so the table can move up and down.
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="ns")

#This lets the window stretch nicely when its resized.
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
table_frame.columnconfigure(0, weight=1)

#This starts the app with the summary updated.
update_summary()
root.mainloop()
