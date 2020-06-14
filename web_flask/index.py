from models import storage
from models.user import User
from models.recipe import Recipe
from models.review import Review
from os import environ, getenv
from flask import Flask, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
import requests

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('home'))
    
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("home.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login.html")


@app.route('/index')
def index():
    recipes_list = []
    recipes = "nombre receta"
    description = "Breve descripcion de la receta"
    user = ["Fulanito", "Mario", "Joaquin", "Luz"]
    return render_template('index.html', recipes=recipes,
                            description=description,
                            user=user)

@app.route('/recipes')
def recipes():
    response = requests.get(url="http://127.0.0.1:5000/api/v1/recipes/")
    params = response.json()
    print(params)
    return render_template('recipes.html', params=params)

if __name__ == '__main__':
    if getenv('HMCR_API_HOST'):
        app.run(host=getenv('HMCR_API_HOST'),
                port=getenv('HMCR_API_PORT'), threaded=True, debug=True)
    else:
        app.run(host='0.0.0.0', threaded=True, debug=True)
