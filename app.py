from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webform import LoginForm, PostForm, UserForm, PasswordForm, NamerForm, PasswordField , SearchForm
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import uuid as uuid
import os
import psycopg2

#create a flask instances
app = Flask(__name__)
#add ckeditor
ckeditor = CKEditor(app)
#-------------------old-SQLite DB (users)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#-------------------new MYSQL DB (our_user)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Cable360224@localhost/our_users' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jxwyrzntznmgea:c70bd233b264ad7a650f5e06b4e3aa859ffe99c80fe41fc3b893d12a2e6db0c0@ec2-34-236-199-229.compute-1.amazonaws.com:5432/daehgh3q6l9hlo'

#secret key-------------------------------
app.config['SECRET_KEY']= "my supa soldia" 
UPLOAD_FOLDER = "static/images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.logger.debug("Debug message")
#initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#-------------------Create Login page
#Flask Login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
#Pass Stuff To Navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

#create admin page
@app.route('/admin')
@login_required
def admin(): 
    id = current_user.id
    if id == 1:
        return render_template("admin.html")
    else:
        flash("Sorry You must be the Admin to access the Admin page")
        return redirect(url_for('dashboard'))
    


#Create Search Function
@app.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        #Get data from submitted form
        post.searched = form.searched.data
        #Query the Database
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()
        
        
        
        return render_template("search.html", form=form, searched=post.searched, posts=posts)
 
    
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            #check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Success")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password")
        else:
            flash("That User doesn't exist ")
                
        
    return render_template("login.html", form=form)
#Create Dashboard page
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        name_to_update.about_author = request.form['about_author']
        name_to_update.profile_pic = request.files['profile_pic']
        
        
        
        
        # Grab Image Name
        pic_filename = secure_filename(name_to_update.profile_pic.filename)
        # Set UUID 輸入檔案撞名就給予編號
        pic_name = str(uuid.uuid1()) + "-" + pic_filename
        #Save That Image
        saver = request.files['profile_pic']
        
        #change it to a string to save to db
        name_to_update.profile_pic = pic_name
        try:
            db.session.commit()
            saver.save(os.path.join(app.config['UPLOAD_FOLDER']), pic_name)
            flash("User Updated Successfully")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error!! Got some problem, try again Please~")
            return render_template("dashboard.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("dashboard.html", form=form, name_to_update=name_to_update, id=id)
    
    
    return render_template("dashboard.html")
#-------------------Create logout Page
@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You Have Been logout! Thanks for Stopping by...")
    return redirect(url_for('login'))

#Json Thing
@app.route('/date')
def get_current_date():
    favorite_pizza = {
        "John": "Pepperoni",
        
        "Mike": "Cheese"
    }
    return favorite_pizza
    #return {"Date": date.today()}

@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
        
            #Return a message
            flash("Blog Post Was Deleted!")
        
            #Grab all the posts from 
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("Post.html", Post=posts)
        except:
            #Return error message
            flash("Whoops! There was a problem on deleting post, Try again...")
            
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("Post.html", Post=posts)
    else:
        #Return a message
            flash("You are not authorized to Delete that Post")
        
            #Grab all the posts from 
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("Post.html", Post=posts)
        
    
@app.route('/posts')
def posts():
    #從資料夾抓出所有的posts
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("Post.html", Post=posts) 
@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template("post2.html", post=post)

@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        #post.author = form.author.data 
        post.slug = form.slug.data
        post.content = form.content.data
        # Update Database
        db.session.add(post)
        db.session.commit()
        flash("Post Has Been Updated!")
        return redirect(url_for("post", id=post.id))
    
    if current_user.id == post.poster_id:
        form.title.data = post.title
        #form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template("edit_post.html", form=form)
    else:
        flash("You Aren't authorized to edit this post.")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("Post.html", Post=posts)
    
    
#Add Post Page
@app.route('/add-post', methods=['GET','POST'])
@login_required
def add_post():
    form = PostForm()
    
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form.title.data, content=form.content.data, poster_id=poster, slug=form.slug.data)
        #Clear the form 
        form.title.data = ''
        form.content.data = ''
        #form.author.data = ''
        form.slug.data = ''
        
        #Add post data to database
        db.session.add(post)
        db.session.commit()
        #return message
        flash("Blog post submit successfully!")
    #Redirect to the webpage
    return render_template("add_post.html", form=form)
        



#delete record
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User Deleted Successfylly')
        our_users=Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form=form, name=name, our_users=our_users)
    except:
        flash("THere is a problem happened")
        return render_template("add_user.html",form=form , name=name, our_user=our_users)
        
#update database record
@app.route('/update/<int:id>', methods=['GET','POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template("update.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error!! Got some problem, try again")
            return render_template("update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update, id=id)
        
            


#create a route decorator
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:  #if 資料庫沒有這位user就將此user添加進資料庫
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(username=form.username.data ,name=form.name.data ,email=form.email.data ,favorite_color=form.favorite_color.data, password_hash=hashed_pw)  
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data=''
        flash("User being add successfully ")
    our_users=Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

@app.route('/')
def index(): #定義 屬於index.html
    first_name = "Jilly"
    stuff = "this is bold text"
    the_list = [1,2,3,4,5,6]
    pizza = ["pinapple", "guava", "tomato", 66]
    return render_template("index.html", first_name = first_name, stuff_index = stuff, favorite_pizza = pizza, the_list = the_list)

@app.route('/user/<name>') #屬於user.html
def user(name): #定義 變數
    return render_template("user.html", user_name = name)
#Invalid url------------------------------------- 錯誤頁面測試
@app.errorhandler(404)
def page_not_found(e):
    return render_template("666.html"), 404
@app.errorhandler(505)
def page_not_found(e):
    return render_template("555.html"), 505

#create Password Test page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None 
    pw_to_check = None
    passed = None
    form = PasswordForm()
    #validate form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        #clear the form
        form.email.data = ''
        form.password_hash.data = ''
        
        #Lookup User By Email Address 
        pw_to_check = Users.query.filter_by(email=email).first()
        #Check Hashed password 檢查hashed的密碼
        passed = check_password_hash(pw_to_check.password_hash, password) 
        
    return render_template("test_pw.html", email = email, password = password, pw_to_check = pw_to_check, passed = passed ,form = form )

#create a name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("From submitted Successfully")
        
    return render_template("name.html", name = name, form = form )

#----------------------------------Database
#create a blog post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    title = db.Column(db.String(255)) 
    content = db.Column(db.Text)
    #author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    #Foreign key to link users (refer to primary key of the user)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#Create Model (注意大小寫)
class Users(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("Username", db.String(20), nullable=False, unique=True)
    name = db.Column("name", db.String(200), nullable=False)
    email = db.Column("email", db.String(200), nullable=False, unique=True )
    favorite_color = db.Column(db.String(120))
    about_author = db.Column(db.Text(), nullable=True)
    password_hash = PasswordField()
    password_hash2 = PasswordField() 
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    profile_pic = db.Column(db.String(), nullable=True)
    #Doing some password stuff
    password_hash = db.Column(db.String(128))
    #Users can have many Posts
    posts = db.relationship('Posts', backref='poster')
    
    
    @property 
    def password(self):
        raise AttributeError('password is not readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    #create a string 
    def __repr__(self):
        return '<Name %r>' % self.name

#attention walter's posts=Post , walter's post=post2 