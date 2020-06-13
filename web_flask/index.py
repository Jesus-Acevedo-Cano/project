from models import storage
from models.user import User
from models.recipe import Recipe
from models.review import Review
from os import environ, getenv
from flask import Flask, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route('/index')
def index():
    #recipes = request.get(127.0.0.1:5000/recipes, data=dict)
    recipes_list = []
    return render_template('index.html')

@app.route('/recipes')
def recipes():
    return render_template('recipes.html')


if __name__ == '__main__':
    if getenv('HMCR_API_HOST'):
        app.run(host=getenv('HMCR_API_HOST'),
                port=getenv('HMCR_API_PORT'), threaded=True, debug=True)
    else:
        app.run(host='0.0.0.0', threaded=True, debug=True)
