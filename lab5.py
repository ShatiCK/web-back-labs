from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='nikita_shatravskiy_knowledge_base',
            user='nikita_shatravskiy_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error='Заполните поля')
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, password FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login, password FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин или пароль неверный')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин или пароль неверный')
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    full_name = request.form.get('full_name')

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните логин и пароль')

    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))
    
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error="Такой пользователь уже существует")
    
    password_hash = generate_password_hash(password)
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password, full_name) VALUES (%s, %s, %s);", (login, password_hash, full_name))
    else:
        cur.execute("INSERT INTO users (login, password, full_name) VALUES (?, ?, ?);", (login, password_hash, full_name))
    
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))
    
    if not title or not article_text:
        return render_template('lab5/create_article.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()
    user_id = user["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) VALUES (%s, %s, %s, %s, %s);", 
                    (user_id, title, article_text, is_favorite, is_public))
    else:
        cur.execute("INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) VALUES (?, ?, ?, ?, ?);", 
                    (user_id, title, article_text, is_favorite, is_public))

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    
    conn, cur = db_connect()

    if login:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login=?;", (login,))
        
        user = cur.fetchone()
        user_id = user["id"]

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT a.id, a.title, a.article_text, a.is_favorite, a.is_public, u.login as author 
                FROM articles a 
                JOIN users u ON a.user_id = u.id 
                WHERE a.user_id = %s OR a.is_public = true 
                ORDER BY a.is_favorite DESC, a.id DESC;
            """, (user_id,))
        else:
            cur.execute("""
                SELECT a.id, a.title, a.article_text, a.is_favorite, a.is_public, u.login as author 
                FROM articles a 
                JOIN users u ON a.user_id = u.id 
                WHERE a.user_id = ? OR a.is_public = 1 
                ORDER BY a.is_favorite DESC, a.id DESC;
            """, (user_id,))
    else:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT a.id, a.title, a.article_text, a.is_favorite, a.is_public, u.login as author 
                FROM articles a 
                JOIN users u ON a.user_id = u.id 
                WHERE a.is_public = true 
                ORDER BY a.is_favorite DESC, a.id DESC;
            """)
        else:
            cur.execute("""
                SELECT a.id, a.title, a.article_text, a.is_favorite, a.is_public, u.login as author 
                FROM articles a 
                JOIN users u ON a.user_id = u.id 
                WHERE a.is_public = 1 
                ORDER BY a.is_favorite DESC, a.id DESC;
            """)
    
    articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles, login=login)

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()
    user_id = user["id"]

    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id, title, article_text, is_favorite, is_public FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
        else:
            cur.execute("SELECT id, title, article_text, is_favorite, is_public FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
        
        article = cur.fetchone()
        db_close(conn, cur)
        
        if not article:
            return redirect('/lab5/list')
        
        return render_template('lab5/edit_article.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))
    
    if not title or not article_text:
        article_data = {'id': article_id, 'title': title, 'article_text': article_text, 'is_favorite': is_favorite, 'is_public': is_public}
        return render_template('lab5/edit_article.html', article=article_data, error='Заполните все поля')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s, is_favorite=%s, is_public=%s WHERE id=%s AND user_id=%s;", 
                    (title, article_text, is_favorite, is_public, article_id, user_id))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=?, is_favorite=?, is_public=? WHERE id=? AND user_id=?;", 
                    (title, article_text, is_favorite, is_public, article_id, user_id))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()
    user_id = user["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("DELETE FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/users')
def users_list():
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, full_name FROM users ORDER BY login;")
    else:
        cur.execute("SELECT login, full_name FROM users ORDER BY login;")
    
    users = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('lab5/users.html', users=users)

@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login, full_name FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT login, full_name FROM users WHERE login=?;", (login,))
        
        user = cur.fetchone()
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user)
    
    full_name = request.form.get('full_name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if password and password != confirm_password:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login, full_name FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT login, full_name FROM users WHERE login=?;", (login,))
        
        user = cur.fetchone()
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user, error='Пароли не совпадают')
    
    if password:
        password_hash = generate_password_hash(password)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET full_name=%s, password=%s WHERE login=%s;", (full_name, password_hash, login))
        else:
            cur.execute("UPDATE users SET full_name=?, password=? WHERE login=?;", (full_name, password_hash, login))
    else:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET full_name=%s WHERE login=%s;", (full_name, login))
        else:
            cur.execute("UPDATE users SET full_name=? WHERE login=?;", (full_name, login))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return render_template('lab5/logout.html')