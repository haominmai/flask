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
        name, message = insert_message(request)
                
        return render_template('submit.html', message = message, name = name, submit = True)


import sqlite3

from flask import g


def get_message_db():
    """
    A function get message from database
    """
    try:
        
        # check if there is a database called message_db in the g attribute of the app
        return g.message_db
    
    except:
        
        # if there is no database, connect that database
        g.message_db = sqlite3.connect("messages_db.sqlite")
        
        # create table called message if it's not exists in database
        # in this table, we have three columns: handle, message
        cmd = \
        """
        CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        message TEXT) 
        
        """
        # get a cursor object
        cursor = g.message_db.cursor()
        
        # execute sql command
        cursor.execute(cmd)
        
        return g.message_db


def insert_message(request):
    """
    Extract message and handle from request, 
    and save user message into database
    """
    
    # extract message and name from request
    message = request.form['message']
    name = request.form['name']

    # open connection to database
    conn = get_message_db()
    cursor = conn.cursor()
    
    # insert into our database
    cmd = \
    f"""
    INSERT INTO messages (name, message) 
    VALUES ('{name}', '{message}')
    """
    
    cursor.execute(cmd)
    
    # ensure our row insertion has been saved
    conn.commit()
    
    # close the database connection 
    conn.close()
    
    return name, message


def random_messages(n):
    """
    Return a collection of n random messages
    from the message_db database
    """
    
    # open connection to database
    conn = get_message_db()
    cursor = conn.cursor()
    
    # select message from database
    cmd = \
    f"""
    SELECT name ,message FROM messages ORDER BY RANDOM() LIMIT {n}
    """

    # get the message
    cursor.execute(cmd)
    messages = cursor.fetchall()
    
    # close the database connection
    conn.close()

    return  messages


@app.route('/view/')
def view():
    
    return render_template('view.html', messages = random_messages(5))