from flask import Flask, request, send_from_directory
import csv

highscores_path = 'highscores.csv'
app = Flask(__name__)

@app.route('/')
def homepage():
    return 'This is from my first server app!'

@app.route('/greeting/<name>')
def greeting(name):
    return f'Hello, {name}! Welcome to my website!'

@app.route('/add-score/', methods=['POST', 'GET'])
def add_score():
    if request.method == 'POST':
        name = request.form['name']
        score = request.form['score']
        with open(highscores_path, 'a') as highscores:
            score_writer = csv.writer(highscores)
            score_writer.writerow([name, score])
    return send_from_directory('static', 'add-score.html')

if __name__ == '__main__':
    app.run(debug = True)