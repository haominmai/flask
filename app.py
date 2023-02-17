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