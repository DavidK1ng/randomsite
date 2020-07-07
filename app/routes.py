from flask import render_template, flash, redirect, url_for,request
from app import app
from app.forms import LoginForm
from app.models import User, Post, Category, User_, query_user
from flask_login import login_user, logout_user, current_user, login_required
import markdown
from random import shuffle,randint



@app.route('/blog/',methods=['GET'])
@login_required
def index():

    page = 1

    posts=[]
    
    if request.args.get('page'):
        page = int(request.args.get('page'))
        
    if request.args.get('search'):
        search = request.args.get('search')
        paginate_ = Post.query.filter(Post.body.like(f'%{search}%')).paginate(page,10,error_out=False)

        posts = paginate_.items
    else:
        paginate_ = Post.query.order_by(Post.timestamp.desc()).paginate(page,10,error_out=False)

        if request.args.get('page'):
            posts = paginate_.items
        else:

            posts = Post.query.all()

            shuffle(posts)

            posts = posts[:10]

    current_post = Post.query.order_by(Post.timestamp.desc()).all()[:5]    

    return render_template('index.html',posts=posts, current_post=current_post,paginate=paginate_,en=False)

@app.route('/blog/en')
@login_required
def en():
    page = 1

    if request.args.get('page'):
        page = int(request.args.get('page'))

    if request.args.get('search'):
        search = request.args.get('search')
        paginate_ = Post.query.filter(Post.body.like(f'%{search}%')).paginate(page,10,error_out=False)
    else:
        paginate_ = Post.query.order_by(Post.timestamp.desc()).filter_by(is_en=True).paginate(page,10,error_out=False)

    posts = paginate_.items

    current_post = Post.query.order_by(Post.timestamp.desc()).all()[:5]

    return render_template('index.html', posts=posts, current_post=current_post, paginate=paginate_, en=True)



@app.route('/blog/yoga')
@login_required
def yoga():

    page = 1

    if request.args.get('page'):
        page = int(request.args.get('page'))

    c = Category.query.filter_by(name="Yoga").first_or_404()


    if request.args.get('search'):
        search = request.args.get('search')
        paginate_ = Post.query.filter_by(category=c).filter(Post.body.like(f'%{search}%')).paginate(page,10,error_out=False)
    else:
        paginate_ = Post.query.filter_by(category=c).paginate(page,10,error_out=False)

    posts = paginate_.items

    current_post = Post.query.order_by(Post.timestamp.desc()).all()[:5]

    return render_template('index.html',posts=posts,current_post=current_post,paginate=paginate_,en=False)

@app.route('/blog/eventos')
@login_required
def eventos():
    page = 1

    if request.args.get('page'):
        page = int(request.args.get('page'))

    c = Category.query.filter_by(name="Eventos").first_or_404()


    if request.args.get('search'):
        search = request.args.get('search')
        paginate_ = Post.query.filter_by(category=c).filter(Post.body.like(f'%{search}%')).paginate(page,10,error_out=False)
    else:
        paginate_ = Post.query.filter_by(category=c).paginate(page,10,error_out=False)

    posts = paginate_.items

    current_post = Post.query.order_by(Post.timestamp.desc()).all()[:5]

    return render_template('index.html',posts=posts,current_post=current_post,paginate=paginate_,en=False)


@app.route('/blog/meditacion')
@login_required
def meditacion():
    page = 1

    if request.args.get('page'):
        page = int(request.args.get('page'))

    c = Category.query.filter_by(name="Meditación").first_or_404()


    if request.args.get('search'):
        search = request.args.get('search')
        paginate_ = Post.query.filter_by(category=c).filter(Post.body.like(f'%{search}%')).paginate(page,10,error_out=False)
    else:
        paginate_ = Post.query.filter_by(category=c).paginate(page,10,error_out=False)

    posts = paginate_.items

    current_post = Post.query.order_by(Post.timestamp.desc()).all()[:5]

    return render_template('index.html',posts=posts,current_post=current_post,paginate=paginate_,en=False)


@app.route('/blog/mindfulness')
@login_required
def mindfulness():
    page = 1

    if request.args.get('page'):
        page = int(request.args.get('page'))

    c = Category.query.filter_by(name="Mindfulness").first_or_404()


    if request.args.get('search'):
        search = request.args.get('search')
        paginate_ = Post.query.filter_by(category=c).filter(Post.body.like(f'%{search}%')).paginate(page,10,error_out=False)
    else:
        paginate_ = Post.query.filter_by(category=c).paginate(page,10,error_out=False)

    posts = paginate_.items

    current_post = Post.query.order_by(Post.timestamp.desc()).all()[:5]

    return render_template('index.html',posts=posts,current_post=current_post,paginate=paginate_,en=False)


@app.route('/blog/yogis')
@login_required
def yogis():
    page = 1

    if request.args.get('page'):
        page = int(request.args.get('page'))

    c = Category.query.filter_by(name="Yogis").first_or_404()


    if request.args.get('search'):
        search = request.args.get('search')
        paginate_ = Post.query.filter_by(category=c).filter(Post.body.like(f'%{search}%')).paginate(page,10,error_out=False)
    else:
        paginate_ = Post.query.filter_by(category=c).paginate(page,10,error_out=False)

    posts = paginate_.items

    current_post = Post.query.order_by(Post.timestamp.desc()).all()[:5]

    return render_template('index.html',posts=posts,current_post=current_post,paginate=paginate_,en=False)



@app.route('/blog/<postname>')
@login_required
def post_detail(postname):

    post = Post.query.filter_by(title=postname).first_or_404()

    post.body = markdown.markdown(post.body,
		extensions=[
			#包含 缩写，表格等常用扩展
			'markdown.extensions.extra'
		])

    current_post = Post.query.order_by(Post.timestamp.desc()).all()[:5]

    return render_template('post.html', post=post, current_post=current_post,en=False)





@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('userid')
        user = query_user(user_id)
        if user is not None and request.form['password'] == user['password']:

            curr_user = User_()

            curr_user.id = user_id

            login_user(curr_user)

            return redirect(url_for('index'))

        flash('Wrong username or password')

    return render_template('login_.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully'



@app.errorhandler(404)
def miss(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error(e):
    return render_template('500.html'), 500