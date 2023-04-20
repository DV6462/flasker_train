from flask import Flask, render_template

app = Flask(__name__)
@app.route('/user/<name>')

def user(name):
    return render_template("user01.html",user_name=name)

@app.route('/')
#localhost:5000/user/john
def index():
    firstname = "holallolu"
    stuff = "This is <strong>Bold</strong> Text"
    favorate_pizza = ["cheese", "pepper", "juicy", 69]
    return render_template("01.html",first_name=firstname,stuff=stuff,favorate_pizza=favorate_pizza)

#create custom error page-------------------------------
#Invalid URL----------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal Server Error------------
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

#---------------------------------





