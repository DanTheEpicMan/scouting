# app.py
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="web")

# Replace this with your actual data storage (e.g., a list or database)
team_data = []

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
        team_data.append({
            'team_number': team_number,
            'round_number': round_number,
            'auton_notes': auton_notes,
            'speed': speed,
            'extra_notes': extra_notes
        })
        
        print(team_data)

    return render_template('index.html', team_data=team_data)

if __name__ == '__main__':
    app.run(debug=True)
