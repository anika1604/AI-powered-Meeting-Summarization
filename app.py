from flask import Flask, render_template
import json

app = Flask(__name__)

def read_json_file():
    with open("json_responses/meeting_summary.json", "r") as file:
        data = json.load(file)
    return data


@app.route('/')
def index():
    json_data = read_json_file()
    return render_template("index.html", data=json_data)

@app.route('/home')
def home():
    json_data = read_json_file()
    return render_template('home.html', data=json_data)


if __name__ == '__main__':
    app.run(debug=True)