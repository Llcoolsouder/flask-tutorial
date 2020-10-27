from flask import Flask, request, redirect, send_from_directory, render_template
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
    if request.method == 'GET':
        return send_from_directory('static', 'add-score.html')
    elif request.method == 'POST':
        name = request.form['name']
        score = request.form['score']
        with open(highscores_path, 'a') as highscores:
            score_writer = csv.writer(highscores)
            score_writer.writerow([name, score])
        return redirect('/highscores/')

@app.route('/highscores/')
def highscores():
    highscores = []
    with open(highscores_path, 'r') as highscores_file:
        highscores_csv = csv.reader(highscores_file)
        for row in highscores_csv:
            highscores.append(row)
    highscores.sort(reverse=True, key=lambda entry: entry[1])
    return render_template('highscores.html', highscores=highscores)

if __name__ == '__main__':
    app.run(debug = True)