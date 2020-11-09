from flask import (
    Flask,
    request,
    redirect,
    send_from_directory,
    render_template,
    make_response,
    session
)
import csv
import string
import secrets

def generate_secret():
    usable_characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(usable_characters) for i in range(64))

highscores_path = 'highscores.csv'
app = Flask(__name__)
app.secret_key = generate_secret()

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

@app.route('/setcookie/', methods=['POST', 'GET'])
def set_cookie():
    resp = make_response(send_from_directory('static', 'set-cookie.html'))
    if request.method == 'POST':
        resp.set_cookie('username', request.form['name'])
    return resp

@app.route('/viewcookie/')
def view_cookie():
    name = request.cookies.get('username')
    return f'<h1>{name}</h1>'


@app.route('/session/')
def render_Session_page():
    return render_template('session.html', username=session['username'])

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect('/session/')
    else:
        return send_from_directory('static', 'login.html')

@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug = True)