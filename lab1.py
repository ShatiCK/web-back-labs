from flask import Blueprint, url_for, redirect, request
from datetime import datetime

lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1")
def lab():  
    return '''<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>
        <main>
            <h1>Первая лабораторная работа</h1>
            
            <p>Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые ба-
            зовые возможности.</p>
            
            <a href="''' + url_for('index') + '''">Вернуться на главную</a>
            
            <h2>Список роутов</h2>
            <ul>
                <li><a href="''' + url_for('lab1.web') + '''">Web-сервер на Flask</a></li>
                <li><a href="''' + url_for('lab1.author') + '''">Об авторе</a></li>
                <li><a href="''' + url_for('lab1.image') + '''">Изображение</a></li>
                <li><a href="''' + url_for('lab1.counter') + '''">Счетчик посещений</a></li>
                <li><a href="''' + url_for('lab1.info') + '''">Перенаправление</a></li>
                <li><a href="''' + url_for('lab1.created') + '''">Создано</a></li>
                <!-- УДАЛЕНЫ НЕСУЩЕСТВУЮЩИЕ ССЫЛКИ -->
            </ul>
        </main>
        <footer>
            Шатравский Никита Дмитриевич, ФБИ-33, 3 курс, 2025
        </footer>
    </body>
</html>'''


@lab1.route("/lab1/web")
def web():
    return '''<!doctype html>
        <html>
            <body>
                <h1>web-cервер на flask</h1>
                <a href="/lab1/author">author</a>
            <body>
        </html>''', 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }


@lab1.route("/lab1/author")
def author():
    name = "Шатравский Никита Дмитриевич"
    group = "ФБИ-33"
    faculty = "ФБ"

    return '''<!doctype html>
        <html>
            <body>
                <p>Студент: ''' + name + '''</p>
                <p>Группа: ''' + group + '''</p>
                <p>Факультет: ''' + faculty + '''</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>'''

@lab1.route("/lab1/image")
def image():
    image_path = url_for("static", filename="fish.jpg")
    css_path = url_for("static", filename="lab1.css")
    
    html_content = f'''<!doctype html>
<html>
    <head>
        <title>Рыбка Годжо</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>Рыбка Годжо</h1>
            <img src="{image_path}" alt="Рыбка Годжо">
            <p class="description">Lobotomy Kaisen</p>
        </div>
    </body>
</html>'''
    
    
    return html_content, 200, {
        "Content-Language": "ru",              
        "X-Author": "Shatravskiy Nikita",       
        "X-Project": "LAB1",         
        "Content-Type": "text/html; charset=utf-8"
    }

count = 0

@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url
    client_ip = request.remote_addr
    
    return f'''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: {count}
        <hr>
        Дата и время: {current_time}<br>
        Запрошенный адрес: {url}<br>
        Ваш IP адрес: {client_ip}<br>
        <hr>
        <a href="{url_for('lab1.reset_counter')}">Сбросить счетчик</a>
    </body>
</html>'''

@lab1.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return redirect(url_for('lab1.counter'))

@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@lab1.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано</i></div>
    </body>
</html>
''', 201