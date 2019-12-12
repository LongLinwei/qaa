from flask import Flask, render_template, request, redirect, url_for, g
import config
from models import User, Question, Answer
from exts import db

from decorators import *
from sqlalchemy import or_

app = Flask(__name__)
db.init_app(app)
app.config.from_object(config)


@app.route('/')
def index():
    return render_template('index.html', questions=Question.query.order_by(db.desc('publish_time')).all())
@app.route('/eggshell/')
def eggshell():
    return render_template('eggshell.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')

        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', msg='账号或密码错误')


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        user = request.form.get('user')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if User.query.filter(User.telephone == telephone).first():
            return render_template('regist.html', msg='手机已被注册，请更换手机')
        if password1 != password2:
            return render_template('regist.html', msg='两次密码输入不相等，请重新输入')
        else:

            user = User(telephone=telephone, user=user, password=password1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/loginout/')
def loginout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        # author_id=session.get('user_id')
        # author=User.query.filter(User.id==author_id).first()
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>')
def detail(question_id):
    question_detail = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question_detail=question_detail)


@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    answer_content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(answer_content=answer_content, question_id=question_id)
    # user_id=session.get('user_id')
    # user=User.query.filter(User.id==user_id).first()
    answer.author = g.user
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


@app.route('/search')
def search():
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q), Question.content.contains(q)))
    return render_template('index.html', questions=questions)


@app.before_request
def get_user():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    if user:
        g.user = user


@app.context_processor
def my_context_processor():
    # userid =session.get('user_id')
    # user= User.query.filter(User.id==userid).first()
    if hasattr(g, 'user'):
        return {'user': g.user.user}
    else:
        return {}


if __name__ == '__main__':
    app.run(Debug=True)
