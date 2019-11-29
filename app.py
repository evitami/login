from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3
from flask import g

app = Flask(__name__)

DATABASE = './users.db'
app.secret_key = b"{'\x16\xccj6\xcay\xc5k\xb6\xe0\xfe\xd8\xd2\xe0I\xeb~\xe35\xa0&\xee"


@app.route("/")
def index():
    if 'username' in session:
        return render_template('profil.html', username=session['username'])
    else:
        return render_template('index.html')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def valid_login(username, password):
    user = query_db('select * from User where username = ? and password = ?', [username, password], one=True)
    if user is None:
        return False
    else:
        return True

def log_the_user_in(username):
    return render_template('secret.html', username=username)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username or password'

    return render_template('login.html', error=error)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    msg = "msg"
    if request.method == 'POST':
        try:
            username = request.form["username"]
            password = request.form["password"]
            with sqlite3.connect("users.db") as sqliteConnection:
                cur = sqliteConnection.cursor()
                cur.execute("INSERT into User (username, password) values (?,?)", (username, password))
                sqliteConnection.commit()
                msg = "You have been successfully registered"
        except sqlite3.Error as a:
            sqliteConnection.rollback()
            msg = "Your username is already used"
        finally:
            if msg == "You have been successfully registered":
                return render_template('login.html', msg=msg)
            else:
                return render_template('signup.html', msg=msg)
            sqliteConnection.close()

    return render_template('signup.html')

@app.route('/logout', methods=["POST"])
def logout():
    session.pop('username')
    return render_template('index.html')

if __name__ == "__main__":
    app.run()