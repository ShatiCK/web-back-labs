from flask import Blueprint, render_template, session, request, redirect, flash, current_app, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from os import path
import sqlite3

lab5 = Blueprint('lab5', __name__)



def db_connect():
    
    if current_app.config.get('DB_TYPE') == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='nikita_shatravskiy_knowledge_base',
            user='nikita_shatravskiy_knowledge_base',
            password='123',
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



@lab5.route('/lab5')
def lab():
    username = session.get('username', 'anonymous')
    return render_template('lab5/lab5.html', username=username)


@lab5.route('/lab5/logout')
def logout():
    session.pop('username', None)  
    return redirect(url_for('lab5.lab'))  


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    
    cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    
    password_hash = password

    
    cur.execute(
        "INSERT INTO users (login, password) VALUES (%s, %s);",
        (login, password_hash)
    )

    db_close(conn, cur)

    return render_template('lab5/success.html', login=login)




@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if not login or not password:
            return render_template('lab5/login.html', error="Заполните все поля")

        
        conn, cur = db_connect()
        
        
        cur.execute("SELECT login, password FROM users WHERE login = %s;", (login,))
        user = cur.fetchone()

        if user:
            if user['password'] == password:  
                session['username'] = login  
                db_close(conn, cur)
                return render_template('lab5/success_login.html', username=login)  
            else:
                db_close(conn, cur)
                return render_template('lab5/login.html', error="Неверный пароль")
        else:
            db_close(conn, cur)
            return render_template('lab5/login.html', error="Неверный логин")

    return render_template('lab5/login.html')




@lab5.route('/lab5/list')
def list_articles():
    return "Список статей — скоро будет реализован"


@lab5.route('/lab5/create')
def create_article():
    return "Создание статьи — скоро будет реализовано"
