from flask import Flask,render_template, url_for,flash, redirect,request,abort
from uccworks import app,db,bcrypt,mail
from uccworks import app
from uccworks.models import User,Post
from uccworks.forms import *
from flask_login import login_user,current_user,logout_user,login_required
from flask_mail import Message





@app.route("/") # Root page of the web
@app.route("/home")
def index():
    return render_template('index.html')




@app.route("/Impact")
def impact():
    return render_template('impact.html')


@app.route("/Areas Of Growth")
def growth():
    return render_template('growth.html')


@app.route("/game")
def game():
    return render_template('game.html')





@app.route("/Reviews")
@login_required
def reviews():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page,per_page=5)
    return render_template('reviews.html',posts=posts)

@app.route("/Reviews/New",methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content= form.content.data, author= current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created", 'success')
        return redirect(url_for('reviews'))
    return render_template('create_post.html',form = form, legend = "New Review")


@app.route("/Reviews/<int:post_id>/update",methods = ['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id) # if the post dosent exists it will give a 404, if there
    # is a post then simply render a template that returns that post(we creat this template)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post Has been Updated', 'success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',
                        form=form, legend = "Update Review")


@app.route("/Reviews/<int:post_id>/delete",methods = ['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  # if the post dosent exists it will give a 404, if there
    # is a post then simply render a template that returns that post(we creat this template)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post Has been Deleted', 'success')
    return redirect(url_for('reviews'))


@app.route("/Contact")
def contact():
    return render_template('contacts.html')


@app.route("/register",methods = ['GET','POST'] )
def register():
    if current_user.is_authenticated:
        flash(f'{current_user.username}!, You are already logged In ', 'success')
        return redirect(url_for('index'))
    form = registrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email= form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data}!, Your are successfully Registered ','success')
        return  redirect(url_for('login')) # where index is the name of the function
    return render_template('register.html',title = 'Register', form = form)




@app.route("/login",methods = ['GET','POST'])
def login():

    if current_user.is_authenticated:
        flash(f'{current_user.username}!, You are already logged In ', 'success')
        return redirect(url_for('index'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # return non if no user with the same email
        # if there is on it returns the first email
        if user and bcrypt.check_password_hash(user.password, form.password.data): # checking if the password provided #
            # is equal to one in the db
            # so now if the user exist and the password that they enter is valid with whats in the db
            # so we wan to log the user in we go
            login_user(user)
            next_page = request.args.get('next') # getting the route in the url) args is a dictionary


            # if the user has logged in successfully we redirect them to the homepage
            flash(f'{user.username}!, Welcome ', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
            # redirct to nextpage if it is not none else redirect to homepage

        else:
            flash('Invalid email or Password')
    return render_template('login.html',title = 'Login', form = form)


@app.route("/logout")
def logout():
    logout_user()
    flash('You are successfully Logged Out')
    return redirect(url_for('index'))



@app.route("/Reviews/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id) # if the post dosent exists it will give a 404, if there
    # is a post then simply render a template that returns that post(we creat this template)

    return  render_template('post.html',title = post.title,post=post)



@app.route("/user/<string:username>")
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_post.html', posts=posts,user = user)



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender= 'noreply@uccworks2021.com',recipients=[user.email])

    msg.body= f""" To reset your password please click the following link:
    
    {url_for('reset_token', token = token, _external=True)}
    if you didn't make this request please ignore this email
    
    """
    mail.send(msg)


@app.route("/reset_password",methods = ['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent to your email with instructions to reset your password, If not found check spam folder",'success')
        return  redirect(url_for('login'))
    return render_template('reset_request.html', form = form)


@app.route("/reset_password/<token>",methods = ['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Token is invalid or expired')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your Password is now updated ','success')
        return  redirect(url_for('login')) # where index is the name of the function
    return render_template('reset_token.html', form=form)















