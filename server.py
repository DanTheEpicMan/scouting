import sqlite3
import csv

# Connect to or create the database
conn = sqlite3.connect('scouting.db')
c = conn.cursor()

#Make a table name for each day
time = ((c.execute("SELECT CURRENT_TIMESTAMP").fetchone()[0])[:10]).replace("-", "_")
tableName = "Robots_" + time

# Create the table (if it doesn't exist)
# to enforce uniqueness add PRIMARY KEY
c.execute('''CREATE TABLE IF NOT EXISTS {} (
    team_number INTEGER PRIMARY KEY, 
    round_number INTEGER,
    auton_notes TEXT,
    speed REAL,
    extra_notes TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)'''.format(tableName))


def addDate(data):
    try:
        # Insert data into the table
        c.executemany('INSERT INTO {} (team_number, round_number, auton_notes, speed, extra_notes) VALUES (?, ?, ?, ?, ?)'.format(tableName), data)
    except sqlite3.IntegrityError: # If the team number already exists
        print("Team number already exists, writing to duplicate.csv")

        with open('duplicate.csv', 'a', newline='') as csvfile:  # Open in append mode
                csvwriter = csv.writer(csvfile)
                # Include timestamp in the duplicate row
                csvwriter.writerow([*data[0], c.execute("SELECT CURRENT_TIMESTAMP").fetchone()[0]])

# Sample data (replace with your actual web server data)
# need to avoid sql injection when fetching data from the web
data = [
    (2, 1, "Completed all objectives", 2.5, "Robot bumped a wall slightly"),
]
addDate(data)

rows = conn.execute("SELECT * FROM {}".format(tableName)).fetchall()
print(rows)


# Commit changes and close the connection
conn.commit()
conn.close()


"""
#flask code here 
import sqlite3

#simulated flask peramiters, should be filtered to remove sql injection
flaskPeramTeam = "3637"
flaskPeramPoints = "36"
flaskPeramAutonRings = "3"
flaskPeramNotes = "Insignfull and helpfull notes"

connection = sqlite3.connect("scouting.db")

cursor = connection.cursor()
cursor.execute("INSERT INTO Robots VALUES(?, ?, ?, ?)", (flaskPeramTeam, flaskPeramPoints, flaskPeramAutonRings, flaskPeramNotes))
cursor.execute("INSERT INTO Robots VALUES(?, ?, ?, ?)", ("69420", "37", "2", "bad notes"))


## Would be dont in a diffrent file but just as example
#get all rows
rows = cursor.execute("SELECT * FROM Robots").fetchall()
print(rows)

#get by team number
rows = cursor.execute("SELECT * FROM Robots WHERE Team = ?", (flaskPeramTeam,)).fetchall()
print(rows)
"""