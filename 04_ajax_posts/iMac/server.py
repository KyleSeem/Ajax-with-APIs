from flask import Flask, render_template, redirect, request, jsonify, session
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "Wv4wUTG3SBeeY0Aan2QMkn2ksZKCXpcJChBRP9KzL3UMC"
mysql = MySQLConnector(app, 'posts_db')

@app.route('/')
def index():
    query = "SELECT post, DATE_FORMAT(updated_at, '%b %e, %Y') AS post_date FROM posts ORDER BY updated_at DESC"
    posts = mysql.query_db(query)
    return render_template('index.html', posts=posts)

@app.route('/index_json')
def index_json():
    form.clear()
    
    query = "SELECT * FROM posts"
    posts = mysql.query_db(query)
    return jsonify(posts)

@app.route('/index_html')
def index_partial():
    query = "SELECT post, DATE_FORMAT(updated_at, '%b %e, %Y') AS post_date FROM posts ORDER BY updated_at DESC"
    posts = mysql.query_db(query)
    return render_template('partials/post_partial.html', posts=posts)

@app.route('/new_post', methods=['POST'])
def create():
    # insert text from form into database
    query = "INSERT INTO posts (post, created_at, updated_at) VALUES ('{}', NOW(), NOW())".format(request.form['new_post'])
    mysql.query_db(query)

    # requery all to avoid redirect/refresh
    requery = "SELECT post, DATE_FORMAT(updated_at, '%b %e, %Y') AS post_date FROM posts ORDER BY updated_at DESC"
    posts = mysql.query_db(requery)

    return render_template('partials/post_partial.html', posts=posts)

app.run(debug=True)
