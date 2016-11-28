from flask import Flask, request, render_template, redirect, session, jsonify
app = Flask(__name__)
app.secret_key = "HpjE9goMyH9KlQrPy1L0VhSNQj456JKhGhtMj6cm"
from mysqlconnection import MySQLConnector
mysql = MySQLConnector(app,'ajax_posts')

@app.route('/posts')
def index():
    session.clear()
    query = "SELECT * FROM posts ORDER BY created_at DESC"
    posts = mysql.fetch(query)
    return render_template('index.html', posts=posts)


@app.route('/posts/index_json')
def index_json():
    query = "SELECT * FROM posts ORDER BY created_at DESC"
    posts = mysql.fetch(query)
    return jsonify(posts)


@app.route('/index')
def index_html():
    query = "SELECT * FROM posts ORDER BY created_at DESC"
    posts = mysql.fetch(query)
    return render_template('partials/post_partial.html', posts=posts)


@app.route('/posts/create', methods=['POST'])
def create():
    session.clear()
    session['new_note'] = request.form['new_note']

    query = "INSERT INTO posts (note, created_at, updated_at) VALUES ('{}', NOW(), NOW())".format(session['new_note'])
    mysql.change(query)

    return_query = "SELECT * FROM posts ORDER BY created_at DESC"
    posts = mysql.fetch(return_query)
    return render_template('partials/post_partial.html', posts=posts)

# if __name__ == "__main__":
#     app.run(port=5000, debug=True)

app.run(debug=True)
