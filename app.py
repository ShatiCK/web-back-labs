from flask import Flask, url_for, request, redirect, abort, render_template
from datetime import datetime
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4

app = Flask(__name__)

app.secret_key = 'секретно-секретный ключ'
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)




@app.route("/")
@app.route("/index")
def index():
    return '''<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>
        <main>
            <menu>
                <li><a href="''' + url_for('lab1.lab') + '''">Первая лабораторная</a></li>
                <li><a href="''' + url_for('lab2.lab') + '''">Вторая лабораторная</a></li>
                <li><a href="''' + url_for('lab3.lab') + '''">Третья лабораторная</a></li>
                <li><a href="''' + url_for('lab4.lab') + '''">Четвертая лабораторная</a></li>
                
            </menu>
        </main>
        <footer>
            Шатравский Никита Дмитриевич, ФБИ-33, 3 курс, 2025
        </footer>
    </body>
</html>'''




not_found_logs = []

@app.errorhandler(404)
def not_found(err):
    client_ip = request.remote_addr
    access_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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



@app.route("/400")
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


@app.route("/401")
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


@app.route("/402")
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


@app.route("/403")
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


@app.route("/405")
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


@app.route("/418")
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
