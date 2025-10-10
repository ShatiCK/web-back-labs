from flask import Flask, url_for, request, redirect, abort
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
                <li><a href="''' + url_for('server_error_test') + '''">Тест ошибки 500</a></li>
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


not_found_logs = []

@app.errorhandler(404)
def not_found(err):
    client_ip = request.remote_addr
    access_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    
    
    not_found_logs.append({
        'ip': client_ip,
        'time': access_time,
        'url': requested_url
    })
    
    
    if len(not_found_logs) > 20:
        not_found_logs.pop(0)
    
    
    log_html = '<h3>История 404 ошибок:</h3>'
    log_html += '<table border="1" style="width: 100%; border-collapse: collapse;">'
    log_html += '<tr><th>Время</th><th>IP-адрес</th><th>Запрошенный URL</th></tr>'
    for entry in reversed(not_found_logs):
        log_html += f'''
        <tr>
            <td style="padding: 5px;">{entry["time"]}</td>
            <td style="padding: 5px;">{entry["ip"]}</td>
            <td style="padding: 5px;">{entry["url"]}</td>
        </tr>
        '''
    log_html += '</table>'
    
    
    return f'''
<!doctype html>
<html>
<head>
    <title>404 - Страница не найдена</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 40px;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #d32f2f; }}
        p {{ font-size: 16px; }}
        table {{ margin-top: 20px; font-size: 14px; width: 100%; border-collapse: collapse; }}
        th {{ background: #e0e0e0; padding: 10px; text-align: left; }}
        td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
        a {{
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }}
        a:hover {{ background: #2980b9; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>404 - Страница не найдена</h1>
        <p>Ваш IP-адрес: <strong>{client_ip}</strong></p>
        <p>Дата и время доступа: <strong>{access_time}</strong></p>
        <p>Запрашиваемый адрес: <strong>{requested_url}</strong></p>
        <a href="{url_for('index')}">Вернуться на главную</a>
        {log_html}
    </div>
</body>
</html>
''', 404



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

@app.errorhandler(500)
def internal_server_error(err):
    return f'''
<!doctype html>
<html>
<head>
    <title>500 - Внутренняя ошибка сервера</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f8d7da;
            color: #721c24;
            text-align: center;
            padding: 50px;
        }}
        h1 {{
            font-size: 60px;
        }}
        p {{
            font-size: 20px;
        }}
        a {{
            display: inline-block;
            margin-top: 30px;
            padding: 12px 25px;
            background-color: #721c24;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }}
        a:hover {{
            background-color: #501217;
        }}
    </style>
</head>
<body>
    <h1>500</h1>
    <h2>Внутренняя ошибка сервера</h2>
    <p>Произошла непредвиденная ошибка на сервере.</p>
    <a href="{url_for('index')}">Вернуться на главную</a>
</body>
</html>
''', 500

@app.route("/server_error")
def server_error_test():
    
    result = 10 / 0
    return f"Результат: {result}"


@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшом'



flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return "цветок: " + flower_list[flower_id]