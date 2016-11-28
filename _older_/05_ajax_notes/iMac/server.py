from flask import Flask, render_template, redirect, request
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app, 'notes_db')

# routes to landing page
@app.route('/')
def index():
    # get all notes currently in database
    query = "SELECT id, title, note, DATE_FORMAT(updated_at, '%b %e, %Y at %l:i %p') AS last_change FROM notes ORDER BY updated_at DESC"
    notes = mysql.query_db(query)
    return render_template('index.html', notes=notes)

# handles ajax request for partials
@app.route('/index_html')
def index_html():
    query = "SELECT id, title, note, DATE_FORMAT(updated_at, '%b %e, %Y at %l:i %p') AS last_change FROM notes ORDER BY updated_at DESC"
    notes = mysql.query_db(query)
    return render_template('partials/notes_partial.html', notes=notes)

# handles new note form
@app.route('/new_note', methods=['POST'])
def new_note():
    # take user input from form and add to database
    query = "INSERT INTO notes (title, note, created_at, updated_at) VALUES ('{}', '{}', NOW(), NOW())".format(request.form['note_title'], request.form['note_text'])
    mysql.query_db(query)

    # requery to avoid refresh or redirect
    requery = "SELECT id, title, note, DATE_FORMAT(updated_at, '%b %e, %Y at %l:i %p') AS last_change FROM notes ORDER BY updated_at DESC"
    notes = mysql.query_db(requery)

    return render_template('partials/notes_partial.html', notes=notes)

# handles update form
@app.route('/update_note', methods=['POST'])
def update_note():
    # take user input and update corresponding note
    query = "UPDATE notes SET title = '{}', note = '{}', updated_at = NOW() WHERE id = '{}'".format(request.form['update_title'], request.form['update_text'], request.form['note_id'])
    mysql.query_db(query)

    return redirect('/')

# handles delete form
@app.route('/delete_note', methods=['POST'])
def delete_note():
    query = "DELETE FROM notes where id = '{}'".format(request.form['delete_id'])
    mysql.query_db(query)

    requery = "SELECT id, title, note, DATE_FORMAT(updated_at, '%b %e, %Y at %l:i %p') AS last_change FROM notes ORDER BY updated_at DESC"
    notes = mysql.query_db(requery)

    return render_template('partials/notes_partial.html', notes=notes)

app.run(debug=True)
