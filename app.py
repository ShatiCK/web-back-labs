from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)



@app.route("/")
@app.route("/index")
def index():
    return '''<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>
        <main>
            <menu>
                <li><a href="''' + url_for('lab1') + '''">Первая лабораторная</a></li>
            </menu>
        </main>
        <footer>
            Шатравский Никита Дмитриевич, ФБИ-33, 3 курс, 2025
        </footer>
    </body>
</html>'''

@app.route("/lab1")
def lab1():
    return '''<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
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
                <li><a href="''' + url_for('web') + '''">Web-сервер на Flask</a></li>
                <li><a href="''' + url_for('author') + '''">Об авторе</a></li>
                <li><a href="''' + url_for('image') + '''">Изображение</a></li>
                <li><a href="''' + url_for('counter') + '''">Счетчик посещений</a></li>
                <li><a href="''' + url_for('info') + '''">Перенаправление</a></li>
                <li><a href="''' + url_for('created') + '''">Создано</a></li>
                <li><a href="''' + url_for('unauthorized') + '''">401</a></li>
                <li><a href="''' + url_for('payment_required') + '''">402</a></li>
                <li><a href="''' + url_for('forbidden') + '''">403</a></li>
                <li><a href="''' + url_for('method_not_allowed') + '''">405</a></li>
                <li><a href="''' + url_for('teapot') + '''">418</a></li>
            </ul>
        </main>
        <footer>
            Шатравский Никита Дмитриевич, ФБИ-33, 3 курс, 2025
        </footer>
    </body>
</html>'''


@app.route("/lab1/web")
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


@app.route("/lab1/author")
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

@app.route("/lab1/image")
def image():
    image_path = url_for("static", filename="fish.jpg")
    css_path = url_for("static", filename="lab1.css")
    
    return '''<!doctype html>
<html>
    <head>
        <title>Рыбка Годжо</title>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <div class="container">
            <h1>Рыбка Годжо</h1>
            <img src="''' + image_path + '''" alt="Рыбка Годжо">
            <p class="description">Lobotomy Kaisen</p>
        </div>
    </body>
</html>'''

count = 0
@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = str(datetime.datetime.today())
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + time + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP адрес: ''' + client_ip + '''<br>
        <hr>
        <a href="''' + url_for('reset_counter') + '''">Сбросить счетчик</a>
    </body>
</html>'''

@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return redirect(url_for('counter'))

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
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

@app.errorhandler(404)
def not_found(err):
    return "Нет такой страницы", 404


@app.route("/lab1/400")
def bad_request():
    return '''
<!doctype html>
<html>
    <head><title>400 Bad Request</title></head>
    <body>
        <h1>400 Bad Request</h1>
        <p>Сервер не понимает запрос из-за неверного синтаксиса.</p>
    </body>
</html>
''', 400


@app.route("/lab1/401")
def unauthorized():
    return '''
<!doctype html>
<html>
    <head><title>401 Unauthorized</title></head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Требуется аутентификация для доступа к ресурсу.</p>
    </body>
</html>
''', 401


@app.route("/lab1/402")
def payment_required():
    return '''
<!doctype html>
<html>
    <head><title>402 Payment Required</title></head>
    <body>
        <h1>402 Payment Required</h1>
        <p>Требуется оплата для доступа к ресурсу.</p>
    </body>
</html>
''', 402


@app.route("/lab1/403")
def forbidden():
    return '''
<!doctype html>
<html>
    <head><title>403 Forbidden</title></head>
    <body>
        <h1>403 Forbidden</h1>
        <p>Доступ к запрошенному ресурсу запрещен.</p>
    </body>
</html>
''', 403


@app.route("/lab1/405")
def method_not_allowed():
    return '''
<!doctype html>
<html>
    <head><title>405 Method Not Allowed</title></head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Метод запроса не поддерживается для данного ресурса.</p>
    </body>
</html>
''', 405


@app.route("/lab1/418")
def teapot():
    return '''
<!doctype html>
<html>
    <head><title>418 I'm a teapot</title></head>
    <body>
        <h1>418 I'm a teapot</h1>
        <p>Я чайник и не могу заваривать кофе. Это шуточный код ошибки.</p>
    </body>
</html>
''', 418