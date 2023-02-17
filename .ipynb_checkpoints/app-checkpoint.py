from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("base.html")


@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    
    if request.method == "GET":
        
        return render_template("submit.html")
    
    else: 
        
        print(request.form['message'], request.form['name'])
        
        return render_template("view.html",
                               message = request.form['message'],
                               name = request.form['name']
                               ) 

@app.route('/view/')
def view():
    return render_template("view.html")


import sqlite3


def get_message_db():
    """
    A function get message from database
    """
    try:
        
        #check if there is a database called message_db in the g attribute of the app
        return g.message_db
    
    except:
        
        #if there is no database, connect that database
        g.message_db = sqlite3.connect("messages_db.sqlite")
        
        # create table called message if it's not exists in database
        # in this table, we have three columns: id, handle, message
        cmd = 'CREATE TABLE IF NOT EXISTS messages (id integer, handle text, message text)' 
        
        # get a cursor object
        cursor = g.message_db.cursor()
        
        #Execute sql command
        cursor.execute(cmd)
        
        return g.message_db


