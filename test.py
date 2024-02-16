# app.py
from flask import Flask, render_template, request
import sqlite3
import csv

app = Flask(__name__, template_folder="web")

# Replace this with your actual data storage (e.g., a list or database)
team_data = []

def sqlstuff(team_number, round_number, auton_notes, speed, extra_notes):
    # Connect to or create the database
    conn = sqlite3.connect('scouting.db')
    c = conn.cursor()

    #Make a table name for each day
    time = ((c.execute("SELECT CURRENT_TIMESTAMP").fetchone()[0])[:10]).replace("-", "_")
    time2 = c.execute("SELECT CURRENT_TIMESTAMP").fetchone()
    tableName = "Robots_" + time
    print(tableName)

    # Create the table (if it doesn't exist)
    # to enforce uniqueness add PRIMARY KEY
    c.execute('''CREATE TABLE IF NOT EXISTS {} (
        team_number TEXT PRIMARY KEY, 
        round_number TEXT,
        auton_notes TEXT,
        speed TEXT,
        extra_notes TEXT
    )'''.format(tableName))

    data = [team_number, round_number, auton_notes, speed, extra_notes]

    try:
            # Insert data into the table
            c.executemany('INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?)'.format(tableName), (team_number, round_number, auton_notes, speed, extra_notes))
    except sqlite3.IntegrityError: # If the team number already exists
            print("Team number already exists, writing to duplicate.csv")

            with open('duplicate.csv', 'a', newline='') as csvfile:  # Open in append mode
                    csvwriter = csv.writer(csvfile)
                    # Include timestamp in the duplicate row
                    csvwriter.writerow([*data[0], c.execute("SELECT CURRENT_TIMESTAMP").fetchone()[0]])

    # Sample data (replace with your actual web server data)
    # need to avoid sql injection when fetching data from the web

    rows = conn.execute("SELECT * FROM {}".format(tableName)).fetchall()
    print(rows)


    # Commit changes and close the connection
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Extract data from the form
        team_number = request.form.get('team_number')
        round_number = request.form.get('round_number')
        auton_notes = request.form.get('auton_notes')
        speed = request.form.get('speed')
        extra_notes = request.form.get('extra_notes')

        # Store the data (you can modify this part)
        sqlstuff(team_number, round_number, auton_notes, speed, extra_notes)


    return render_template('index.html', team_data=team_data)

if __name__ == '__main__':
    app.run(debug=True)
