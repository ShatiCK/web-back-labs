from flask import Blueprint, render_template, request, redirect, url_for, abort

lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')

@lab2.route('/lab2/a')
def a():
    return 'без слэша'

@lab2.route('/lab2/a/')
def a2():
    return 'со слэшом'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return "цветок: " + flower_list[flower_id]

@lab2.route('/lab2/add_flower/<name>')
def add_flower_by_url(name):
    flower_list.append(name)
    return f'''
<!DOCTYPE html>
<html>
    <body>
        <h1>Добавлен цветок</h1>
        <p>Название нового цветка: {name}</p>
        <p>Всего цветов: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

@lab2.route('/lab2/example')
def example():
    name = 'Шатравский Никита'
    lab_num = '2'
    group = 'ФБИ-33'
    kurs = '3'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('lab2/example.html', 
                         name=name, 
                         lab_num=lab_num, 
                         group=group, 
                         kurs=kurs,
                         fruits=fruits)

@lab2.route('/lab2/filters')
def filters():
    phrase = "О сколько нам открытий чудных..."
    return render_template('lab2/filters.html', phrase=phrase)

@lab2.route('/lab2/add_flower/')
def add_flower_no_name():
    return '''
<!DOCTYPE html>
<html>
    <body>
        <h1>Ошибка 400</h1>
        <p style="color:red;">Вы не задали имя цветка!</p>
        <p><a href="/lab2/flowers_list">Посмотреть все цветы</a></p>
    </body>
</html>
''', 400

@lab2.route('/lab2/flowers_list')
def show_flowers():
    flowers_html = "<ul>" + "".join([f"<li>{f}</li>" for f in flower_list]) + "</ul>"
    return f'''
<!DOCTYPE html>
<html>
    <body>
        <h1>Список всех цветов</h1>
        <p>Всего цветов: {len(flower_list)}</p>
        {flowers_html}
        <p><a href="/lab2/clear_flowers">Очистить все цветы</a></p>
    </body>
</html>
'''

@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return '''
<!DOCTYPE html>
<html>
    <body>
        <h1>Список цветов очищен</h1>
        <p><a href="/lab2/flowers_list">Посмотреть все цветы</a></p>
    </body>
</html>
'''

@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@lab2.route('/lab2/calc/<int:a>')
def calc_one_arg(a):
    return redirect(f'/lab2/calc/{a}/1')

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    if b == 0:
        div_result = "Ошибка: деление на ноль"
    else:
        div_result = a / b
    
    return f'''
<!DOCTYPE html>
<html>
    <body>
        <h1>Калькулятор</h1>
        <p>Первое число: {a}</p>
        <p>Второе число: {b}</p>
        <ul>
            <li>Сумма: {a + b}</li>
            <li>Разность: {a - b}</li>
            <li>Произведение: {a * b}</li>
            <li>Деление: {div_result}</li>
            <li>Возведение в степень: {a ** b}</li>
        </ul>
        <p><a href="/lab2/calc/">Попробовать снова с 1 и 1</a></p>
    </body>
</html>
'''

books = [
    {"author": "Анджей Сапковский", "title": "Ведьмак: Последнее желание", "genre": "Фэнтези", "pages": 320},
    {"author": "Анджей Сапковский", "title": "Ведьмак: Меч Предназначения", "genre": "Фэнтези", "pages": 384},
    {"author": "Сергей Минаев", "title": "Духless: Повесть о ненастоящем человеке", "genre": "Роман", "pages": 320},
    {"author": "Сергей Минаев", "title": "The Тёлки", "genre": "Роман", "pages": 416},
    {"author": "Джозеф Кэмпбелл", "title": "Тысячеликий герой", "genre": "Мифология", "pages": 384},
    {"author": "Джозеф Кэмпбелл", "title": "Сила мифа", "genre": "Мифология", "pages": 272},
    {"author": "Айзек Азимов", "title": "Я, робот", "genre": "Научная фантастика", "pages": 320},
    {"author": "Айзек Азимов", "title": "Основание", "genre": "Научная фантастика", "pages": 256},
    {"author": "Рэй Брэдбери", "title": "451° по Фаренгейту", "genre": "Антиутопия", "pages": 256},
    {"author": "Джордж Оруэлл", "title": "1984", "genre": "Антиутопия", "pages": 320}
]

@lab2.route('/lab2/books')
def show_books():
    return render_template('lab2/books.html', books=books)

berries = [
    {"name": "Арбуз", "img": "lab2/berry1.jpg", "desc": "Крупная сладкая ягода с красной мякотью и чёрными семенами."},
    {"name": "Черника", "img": "lab2/berry2.jpg", "desc": "Сине-фиолетовая ягода с кисло-сладким вкусом и массой витаминов."},
    {"name": "Клубника", "img": "lab2/berry3.jpg", "desc": "Сочный и ароматный ягода, популярный по всей стране."},
    {"name": "Клюква", "img": "lab2/berry4.jpg", "desc": "Кислая болотная ягода, используется при простуде и воспалениях."},
    {"name": "Смородина", "img": "lab2/berry5.jpg", "desc": "Чёрная или красная ягода с кисло-сладким вкусом, богата витамином С."},
    {"name": "Красная смородина", "img": "lab2/berry6.jpg", "desc": "Мелкие ярко-красные ягоды с освежающим кисловатым вкусом."},
    {"name": "Малина", "img": "lab2/berry7.jpg", "desc": "Нежная и ароматная ягода, часто используется при простуде."},
    {"name": "Облепиха", "img": "lab2/berry8.jpg", "desc": "Оранжевая ягода с терпким вкусом и мощными лечебными свойствами."},
    {"name": "Земляника", "img": "lab2/berry9.jpg", "desc": "Сорт садовой земляники, крупная и ароматная."},
    {"name": "Ежевика", "img": "lab2/berry10.jpg", "desc": "Тёмно-фиолетовая ягода с насыщенным вкусом и антоцианами."}
]

@lab2.route('/lab2/berries')
def show_berries():
    return render_template('lab2/berries.html', berries=berries)

flowers_with_prices = [
    {"name": "роза", "price": 300},
    {"name": "тюльпан", "price": 310},
    {"name": "незабудка", "price": 320},
    {"name": "ромашка", "price": 330}
]

@lab2.route('/lab2/flowers_dop')
def show_flowers_dop():
    return render_template('lab2/flowers.html', flowers=flowers_with_prices)

@lab2.route('/lab2/flowers_dop/delete/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flowers_with_prices):
        abort(404)
    
    flowers_with_prices.pop(flower_id)
    return redirect(url_for('lab2.show_flowers_dop'))

@lab2.route('/lab2/flowers_dop/clear')
def clear_flowers_dop():
    flowers_with_prices.clear()
    return redirect(url_for('lab2.show_flowers_dop'))

@lab2.route('/lab2/flowers_dop/add', methods=['POST'])
def add_flower_dop():
    name = request.form.get('name')
    price = request.form.get('price')
    
    if not name:
        return "Вы не задали имя цветка", 400
    if not price or not price.isdigit():
        return "Цена должна быть числом", 400
        
    flowers_with_prices.append({"name": name, "price": int(price)})
    return redirect(url_for('lab2.show_flowers_dop'))