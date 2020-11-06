from flask import Flask, request, redirect, send_from_directory, render_template, make_response
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
    highscores.sort(reverse=True, key=lambda entry: int(entry[1]))
    return render_template('highscores.html', highscores=highscores)

@app.route('/setcookie', methods=['POST', 'GET'])
def set_cookie():
    resp = make_response(send_from_directory('static', 'set-cookie.html'))
    if request.method == 'POST':
        resp.set_cookie('username', request.form['name'])
    return resp

@app.route('/viewcookie')
def view_cookie():
    name = request.cookies.get('username')
    return f'<h1>{name}</h1>'

if __name__ == '__main__':
    app.run(debug = True)