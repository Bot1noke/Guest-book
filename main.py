from data import db_session
from data import Articles
from data import Comments
from data import Users
import os
import flask_login
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, request, render_template, redirect
#from models import Article, Comment, User
from models import LoginForm
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh_no_cringe"
DATABASE_URL = r"C:\Users\Alexey\PycharmProjects\guest_book\oh_no.db"
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init(DATABASE_URL)

@app.route("/", methods=["GET"])
def index():
    session = db_session.create_session()
    articles = session.query(Articles.Articles).all()
    #query = 'SELECT * FROM Articles'
    #query_comment = 'SELECT * FROM Comments WHERE articleId = ?'
    #articles_raw = cursor.execute(query).fetchall()
    '''articles = []
    for article_raw in query:
        article = session.query(Articles.Articles).filter(Articles.Articles).one()
        query_comment = session.query(Comments.Comments).filter(Comments.Comments.articleId == article_raw[0]).all()
        #comments_raw = cursor.execute(query_comment, (article_raw[0],)).fetchall()
        comments = []
        for comment_raw in query_comment:
            comments.append(Comment(comment_raw[0], comment_raw[1], comment_raw[2]))
        articles.append(Article(article_raw[0], article_raw[1], article_raw[2], comments))'''
    print(articles)
    return render_template("index.html", articles=articles, page_name='index')


@app.route("/add_post", methods=["GET"])
@login_required
def add_post_page():
    return render_template("add_post.html", page_name='add_post')


@app.route("/api/add_post", methods=["POST"])
@login_required
def add_post():
    session = db_session.create_session()
    #con = sqlite3.connect(DATABASE_URL)
    #cursor = con.cursor()
    query = Articles.Articles(title= request.form['articleTitle'], content= request.form['articleContent'])
    session.add(query)
    #query = 'INSERT INTO Articles (title, content) VALUES (?, ?)'
    #cursor.execute(query, (request.form['articleTitle'], request.form['articleContent']))
    #con.commit()
    #con.close()
    session.commit()
    return redirect('/')


@app.route("/api/delete_post/<int:post_id>", methods=["GET"])
@login_required
def delete_post(post_id):
    session = db_session.create_session()
    #con = sqlite3.connect(DATABASE_URL)
    #cursor = con.cursor()
    query = session.query(Articles.Articles).filter(Articles.Articles.id == post_id).one()
    session.delete(query)
    #query = 'DELETE FROM Articles WHERE id = ?'
    #cursor.execute(query, (post_id,))
    #con.commit()
    #con.close()
    session.commit()
    return redirect('/')


@app.route("/api/add_comment/<int:post_id>", methods=["POST"])
@login_required
def add_comment(post_id):
    session = db_session.create_session()
    query = Comments.Comments(author= request.form['commentAuthor'], content= request.form['commentContent'], articleId= post_id)
    session.add(query)
    #con = sqlite3.connect(DATABASE_URL)
    #cursor = con.cursor()
    #query = 'INSERT INTO Comments (author, content, articleId) VALUES (?, ?, ?)'
    #cursor.execute(query, (request.form['commentAuthor'], request.form['commentContent'], post_id))
    #con.commit()
    #con.close()
    session.commit()
    return redirect('/')


@app.route("/api/delete_comment/<int:comment_id>", methods=["GET"])
@login_required
def delete_comment(comment_id):
    session = db_session.create_session()
    query = session.query(Comments.Comments).filter(Comments.Comments.id == comment_id).one()
    session.delete(query)
    session.commit()
    #con = sqlite3.connect(DATABASE_URL)
    #cursor = con.cursor()
    #query = 'DELETE FROM Comments WHERE id = ?'
    #cursor.execute(query, (comment_id,))
    #con.commit()
    #con.close()
    return redirect('/')


@app.route("/api/update_post/<int:post_id>", methods=["POST"])
@login_required
def update_post(post_id):
    session = db_session.create_session()
    articles = session.query(Articles.Articles).filter(Articles.Articles.id == post_id).one()
    articles.title = request.form['articleTitle']
    articles.content = request.form['articleContent']
    session.commit()
    #con = sqlite3.connect(DATABASE_URL)
    #cursor = con.cursor()
    #query = 'UPDATE Articles SET title = ?, content = ? WHERE id = ?'
    #cursor.execute(query, (request.form['articleTitle'], request.form['articleContent'], post_id))
    #con.commit()
    #con.close()
    return redirect('/')


@app.route("/update_post/<int:post_id>", methods=["GET"])
@login_required
def update_post_page(post_id):
    return render_template("update_post.html", page_name='update_post', post_id=post_id)


@app.route("/api/update_comment/<int:comment_id>", methods=["POST"])
@login_required
def update_comment(comment_id):
    session = db_session.create_session()
    comments = session.query(Comments.Comments).filter(Comments.Comments.id == comment_id).one()
    comments.author = request.form['commentAuthor']
    comments.content = request.form['commentContent']
    session.commit()
    #con = sqlite3.connect(DATABASE_URL)
    #cursor = con.cursor()
    #query = 'UPDATE Comments SET author = ?, content = ? WHERE id = ?'
    #cursor.execute(query, (request.form['commentAuthor'], request.form['commentContent'], comment_id))
    #con.commit()
    #con.close()
    return redirect('/')


@app.route("/update_comment/<int:comment_id>", methods=["GET"])
@login_required
def update_comment_page(comment_id):
    return render_template("update_comment.html", page_name='update_comment', comment_id=comment_id)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(Users.Users).filter(Users.Users.id == user_id).one_or_none()
    #if user_exists(user_id):
    #    return Users.Users.id
    #return None


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        given_password = form.password.data
        password = get_password(login)
        remember_me = form.remember_me.data
        if check_user(given_password, password):
            login_user(Users.Users.login, remember=remember_me)
            print("Success")
            return redirect("/")
        else:
            print("error")
            print(password, given_password)
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        given_password = form.password.data
        if not user_exists(get_id(login)):
            add_user(login, given_password)
            print("Success")
            return redirect("/")
        else:
            print("user exists")
    return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

def add_user(login, password):
    session = db_session.create_session()
    query = Users.Users(login= login, password= generate_password_hash(password))
    session.add(query)
    session.commit()
    #con = sqlite3.connect(DATABASE_URL)
    #cur = con.cursor()
    #cur.execute('''INSERT INTO Users(login, password)
    #                VALUES (?,?)''', (login, generate_password_hash(password)))
    #con.commit()
    #con.close()

def check_user(given_password, password):
    return check_password_hash(password, given_password)

def get_login(_id):
    session = db_session.create_session()
    return session.query(Users.Users).filter(Users.Users.id == _id).one()
    #con = sqlite3.connect(DATABASE_URL)
    #cur = con.cursor()
    #return cur.execute('''SELECT * FROM Users
    #                WHERE id = ?''', (_id,)).fetchone()

def get_logins():
    session = db_session.create_session()
    return session.query(Users.Users).all().Users.login
    #con = sqlite3.connect(DATABASE_URL)
    #cur = con.cursor()
    #return cur.execute('''SELECT login FROM Users''').fetchall()

def get_password(login):
    session = db_session.create_session()
    return session.query(Users.Users).filter(Users.Users.login == login).one().password
    #con = sqlite3.connect(DATABASE_URL)
    #cur = con.cursor()
    #return cur.execute('''SELECT password FROM Users
    #                        WHERE login = ?''', (login,)).fetchone()[0]

def get_user(login):
    session = db_session.create_session()
    return session.query(Users.Users).filter(Users.Users.login == login).one()
    #con = sqlite3.connect(DATABASE_URL)
    #cur = con.cursor()
    #return cur.execute('''SELECT * FROM Users
    #                        WHERE login = ?''', (login,)).fetchone()[0]

def user_exists(id):
    session = db_session.create_session()
    if session.query(Users.Users).filter(Users.Users.id == id).one_or_none().login:
        return True
    else:
        return False
    #con = sqlite3.connect(DATABASE_URL)
    #cur = con.cursor()
    #if cur.execute('''SELECT login FROM Users
    #                    WHERE id = ?''', (id,)).fetchone() == None:
    #    return False
    #else:
    #    return True

def get_id(login):
    session = db_session.create_session()
    if session.query(Users.Users).filter(Users.Users.login == login).one_or_none().id:
        return session.query(Users.Users).filter(Users.Users.login == login).one().id
    #con = sqlite3.connect(DATABASE_URL)
    #cur = con.cursor()
    #temp = cur.execute('''SELECT id FROM Users
    #                        WHERE login = ?''', (login,)).fetchone()
    #if temp != None:
    #    return cur.execute('''SELECT id FROM Users
    #                       WHERE login = ?''', (login,)).fetchone()[0]

def is_article_author(art_id, usr):
    session = db_session.create_session()
    query = session.query(Articles.Articles).filter(Articles.Articles.id == art_id).one_or_none().author
    if query == usr:
        return True
    else:
        return False
    #con = sqlite3.connect(DATABASE_URL)
    #cur = con.cursor()
    #temp = cur.execute('''SELECT author FROM Articles
    #                    WHERE id == ?''', (art_id,)).fetchone()
    #if temp != None and temp[0] == usr:
    #    return True
    #else:
    #    return False


def main():
    app.run(port=8888, debug=True)


if __name__ == '__main__':
    main()
