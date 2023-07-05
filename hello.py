from flask import Flask, render_template

app = Flask(__name__)

#create a route decorator
@app.route('/')

def index(): #定義 屬於index.html
    first_name = "haha"
    stuff = "this is bold text"
    the_list = [1,2,3,4,5,6]
    pizza = ["pinapple", "guava", "tomato", 66]
    return render_template("index.html", first_name = first_name, stuff_index = stuff, favorite_pizza = pizza, the_list = the_list)

@app.route('/user/<name>') #屬於user.html
def user(name): #定義 變數
    return render_template("user.html",user_name = name)
#Invalid url
@app.errorhandler(404)
def page_not_found(e):
    return render_template("666.html"), 404
@app.errorhandler(505)
def page_not_found(e):
    return render_template("555.html"), 505

    

