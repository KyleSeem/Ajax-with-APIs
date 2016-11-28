from flask import Flask, request, render_template, redirect, session, jsonify
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "DGzwcg2TqZtCkHTQCBhPfrxQUw1KVQJg5fCwGNybpRPBC"
mysql = MySQLConnector(app,'ajax_notes')

@app.route('/')
def index():
    query = "SELECT * FROM notes ORDER BY updated_at DESC"
    notes = mysql.fetch(query)
    return render_template('index.html', notes=notes)

# this route renders all notes in database as json data
@app.route('/index_json')
def index_json():
    query = "SELECT * FROM notes"
    notes = mysql.fetch(query)
    return jsonify(notes)

# this route renders all notes in database as html in a partial
@app.route('/index_html')
def index_html():
    query = "SELECT * FROM notes ORDER BY updated_at DESC"
    notes = mysql.fetch(query)
    return render_template('/partials/notes.html', notes=notes)

# this route handles the create new note method and form
@app.route('/notes/create', methods=['POST'])
def create():
    title = request.form['title']
    description = request.form['create_description']

    query = "INSERT INTO notes (title, description, created_at, updated_at) VALUES ('{}', '{}', NOW(), NOW())".format(title, description)
    mysql.change(query)

    requery = "SELECT * FROM notes ORDER BY updated_at DESC"
    notes = mysql.fetch(requery)
    # return redirect('/')
    return render_template('/partials/notes.html', notes=notes)

# this route handles the update note method and form
@app.route('/notes/update/<id>', methods=['POST'])
def update(id):
    title = request.form['update_title']
    description = request.form['update_description']

    query = "UPDATE notes SET title = '{}', description = '{}', updated_at = NOW() WHERE id = '{}'".format(title, description, id)
    mysql.change(query)

    requery = "SELECT * FROM notes ORDER BY updated_at DESC"
    notes = mysql.fetch(requery)
    return redirect('/')
    # return render_template('/partials/notes.html', notes=notes)

# this route handles the delete method and form
@app.route('/notes/delete/<id>', methods=['POST'])
def delete(id):
    delete = "DELETE FROM notes WHERE id = '{}'".format(id)
    mysql.change(delete)
    return redirect('/')


app.run(debug=True)
