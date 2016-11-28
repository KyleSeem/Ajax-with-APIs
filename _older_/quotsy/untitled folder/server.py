from flask import Flask, request, render_template, session, flash, redirect, jsonify
app = Flask(__name__)
from mysqlconnection import MySQLConnector
"""
Set variable 'mysql' to be an instance of the MySQLConnector class,
taking our entire application as the first argument and the database
name as the second argument.
"""
mysql = MySQLConnector('myownapi')

@app.route('/quotes')
def index():
    query = "SELECT * FROM quotes"
    quotes = mysql.fetch(query)
    return render_template('index.html', quotes=quotes)

@app.route('/quotes/index_json')
def index_json():
    query = "SELECT * FROM quotes"
    quotes = mysql.fetch(query)
    return jsonify(quotes)

@app.route('/quotes/index_html')
def index_partial():
    query = "SELECT * FROM quotes"
    quotes = mysql.fetch(query)
    return render_template('partials/quotes.html', quotes=quotes)

@app.route('/quotes/create', methods=['POST'])
def create():
    query = "INSERT INTO quotes (author, quote) VALUES ('{}', '{}')".format(request.form['author'], request.form['quote'])
    mysql.change(query)
    return_query = "SELECT * FROM quotes"
    quotes = mysql.fetch(return_query)
    return render_template('partials/quotes.html', quotes=quotes)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
