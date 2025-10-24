from flask import Blueprint, render_template, request, make_response, redirect, session

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    
    
    if name is None:
        name = "неизвестный пользователь"
    
    
    if age is None:
        age = "не указан"
    
    return render_template('lab3/lab3.html', 
                         name=name, 
                         name_color=name_color, 
                         age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '25')  
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')  
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')
    
    if user == '':
        errors['user'] = 'Заполните поле!'
    if age == '':
        errors['age'] = 'Заполните возраст!'
    
    return render_template('lab3/form1.html', 
                         user=user, age=age, sex=sex, 
                         errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    
    drink = request.args.get('drink')
    milk = request.args.get('milk')
    sugar = request.args.get('sugar')
    
    
    price = 120  
    if drink == 'black-tea':
        price = 80
    elif drink == 'green-tea':
        price = 70
    
    if milk:  
        price += 30
    if sugar:  
        price += 10
    
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success', methods=['POST'])
def success():
    price = request.form.get('price')
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    
    if color or bg_color or font_size:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        return resp
    
    color = request.cookies.get('color', '#000000')
    bg_color = request.cookies.get('bg_color', '#ffffff')
    font_size = request.cookies.get('font_size', '16')
    
    return render_template('lab3/settings.html', 
                         color=color, 
                         bg_color=bg_color, 
                         font_size=font_size)


@lab3.route('/lab3/ticket')
def ticket():
    errors = {}
    
    
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    baggage = request.args.get('baggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    
    if fio == '' or fio is None:
        errors['fio'] = 'Заполните ФИО пассажира'
    
    if shelf == '' or shelf is None:
        errors['shelf'] = 'Выберите тип полки'
    
    if age == '' or age is None:
        errors['age'] = 'Заполните возраст'
    elif age:
        try:
            age_int = int(age)
            if age_int < 1 or age_int > 120:
                errors['age'] = 'Возраст должен быть от 1 до 120 лет'
        except ValueError:
            errors['age'] = 'Возраст должен быть числом'
    
    if departure == '' or departure is None:
        errors['departure'] = 'Заполните пункт выезда'
    
    if destination == '' or destination is None:
        errors['destination'] = 'Заполните пункт назначения'
    
    if date == '' or date is None:
        errors['date'] = 'Выберите дату поездки'
    
    
    if errors or not any([fio, shelf, age, departure, destination, date]):
        return render_template('lab3/ticket_form.html', 
                             errors=errors,
                             fio=fio or '',
                             shelf=shelf or '',
                             linen=linen or '',
                             baggage=baggage or '',
                             age=age or '',
                             departure=departure or '',
                             destination=destination or '',
                             date=date or '',
                             insurance=insurance or '')
    
    
    age_int = int(age)
    
    
    if age_int < 18:
        base_price = 700  
        ticket_type = "Детский билет"
    else:
        base_price = 1000  
        ticket_type = "Взрослый билет"
    
    
    additions = []
    
    
    if shelf in ['lower', 'lower_side']:
        base_price += 100
        additions.append("+100 руб (нижняя полка)")
    
    
    if linen == 'on':
        base_price += 75
        additions.append("+75 руб (бельё)")
    
    
    if baggage == 'on':
        base_price += 250
        additions.append("+250 руб (багаж)")
    
    
    if insurance == 'on':
        base_price += 150
        additions.append("+150 руб (страховка)")
    
    return render_template('lab3/ticket_result.html',
                         fio=fio,
                         shelf=shelf,
                         linen=linen,
                         baggage=baggage,
                         age=age,
                         departure=departure,
                         destination=destination,
                         date=date,
                         insurance=insurance,
                         ticket_type=ticket_type,
                         base_price=base_price,
                         additions=additions)


@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    return resp


# Список товаров (компьютерные игры)
products = [
    {"name": "Cyberpunk 2077: Phantom Liberty", "price": 2999, "brand": "CD Projekt Red", "genre": "RPG", "platform": "PC/PS5/XSX"},
    {"name": "Baldur's Gate 3", "price": 3499, "brand": "Larian Studios", "genre": "RPG", "platform": "PC/PS5/XSX"},
    {"name": "Elden Ring", "price": 3999, "brand": "FromSoftware", "genre": "RPG", "platform": "PC/PS4/PS5/XBOX"},
    {"name": "Call of Duty: Modern Warfare III", "price": 4499, "brand": "Activision", "genre": "Шутер", "platform": "PC/PS4/PS5/XBOX"},
    {"name": "Starfield", "price": 3799, "brand": "Bethesda", "genre": "RPG", "platform": "PC/XSX"},
    {"name": "The Legend of Zelda: Tears of the Kingdom", "price": 4999, "brand": "Nintendo", "genre": "Приключения", "platform": "Switch"},
    {"name": "Marvel's Spider-Man 2", "price": 4599, "brand": "Insomniac", "genre": "Экшен", "platform": "PS5"},
    {"name": "Hogwarts Legacy", "price": 3299, "brand": "Avalanche", "genre": "RPG", "platform": "PC/PS4/PS5/XBOX/Switch"},
    {"name": "Diablo IV", "price": 4199, "brand": "Blizzard", "genre": "RPG", "platform": "PC/PS4/PS5/XBOX"},
    {"name": "Resident Evil 4 Remake", "price": 3699, "brand": "Capcom", "genre": "Хоррор", "platform": "PC/PS4/PS5/XSX"},
    {"name": "God of War Ragnarök", "price": 4799, "brand": "Santa Monica", "genre": "Экшен", "platform": "PS4/PS5"},
    {"name": "Forza Motorsport", "price": 3899, "brand": "Turn 10", "genre": "Гонки", "platform": "PC/XSX"},
    {"name": "Alan Wake 2", "price": 3199, "brand": "Remedy", "genre": "Хоррор", "platform": "PC/PS5/XSX"},
    {"name": "Street Fighter 6", "price": 3499, "brand": "Capcom", "genre": "Файтинг", "platform": "PC/PS4/PS5/XBOX"},
    {"name": "Dead Space Remake", "price": 3999, "brand": "Motive", "genre": "Хоррор", "platform": "PC/PS5/XSX"},
    {"name": "Final Fantasy XVI", "price": 4699, "brand": "Square Enix", "genre": "RPG", "platform": "PS5"},
    {"name": "Armored Core VI: Fires of Rubicon", "price": 3799, "brand": "FromSoftware", "genre": "Экшен", "platform": "PC/PS4/PS5/XBOX"},
    {"name": "Star Wars Jedi: Survivor", "price": 4299, "brand": "Respawn", "genre": "Экшен", "platform": "PC/PS5/XSX"},
    {"name": "The Last of Us Part I", "price": 4599, "brand": "Naughty Dog", "genre": "Экшен", "platform": "PC/PS5"},
    {"name": "Red Dead Redemption 2", "price": 2999, "brand": "Rockstar", "genre": "Экшен", "platform": "PC/PS4/XBOX"},
    {"name": "The Witcher 3: Wild Hunt", "price": 1499, "brand": "CD Projekt Red", "genre": "RPG", "platform": "PC/PS4/PS5/XBOX/Switch"},
    {"name": "Grand Theft Auto V", "price": 1999, "brand": "Rockstar", "genre": "Экшен", "platform": "PC/PS4/PS5/XBOX"},
    {"name": "Minecraft", "price": 999, "brand": "Mojang", "genre": "Песочница", "platform": "PC/PS4/XBOX/Switch/Mobile"},
    {"name": "Stray", "price": 1799, "brand": "BlueTwelve", "genre": "Приключения", "platform": "PC/PS4/PS5"},
    {"name": "It Takes Two", "price": 2199, "brand": "Hazelight", "genre": "Приключения", "platform": "PC/PS4/PS5/XBOX/Switch"}
]


@lab3.route('/lab3/products')
def products_search():
    # Получаем параметры из запроса
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    reset = request.args.get('reset')
    
    # Если нажата кнопка сброс, очищаем куки и параметры
    if reset:
        resp = make_response(redirect('/lab3/products'))
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
        return resp
    
    # Фильтрация товаров
    filtered_products = []
    
    if min_price or max_price:
        try:
            # Преобразуем в числа, если поля не пустые
            min_val = float(min_price) if min_price else 0
            max_val = float(max_price) if max_price else float('inf')
            
            # Если пользователь перепутал min и max, меняем местами
            if min_price and max_price and min_val > max_val:
                min_val, max_val = max_val, min_val
                min_price, max_price = str(max_val), str(min_val)
            
            # Фильтруем товары
            for product in products:
                if min_val <= product['price'] <= max_val:
                    filtered_products.append(product)
                    
            # Сохраняем в куки
            resp = make_response(render_template('lab3/products.html',
                                               products=products,
                                               min_price=min_price,
                                               max_price=max_price,
                                               filtered_products=filtered_products,
                                               min_all_price=min([p['price'] for p in products]),
                                               max_all_price=max([p['price'] for p in products])))
            if min_price:
                resp.set_cookie('min_price', min_price)
            if max_price:
                resp.set_cookie('max_price', max_price)
            return resp
            
        except ValueError:
            # Если введены некорректные числа, показываем все товары
            filtered_products = products
    else:
        # Проверяем куки
        min_price_cookie = request.cookies.get('min_price')
        max_price_cookie = request.cookies.get('max_price')
        
        if min_price_cookie or max_price_cookie:
            # Используем значения из куки для поиска
            min_price = min_price_cookie
            max_price = max_price_cookie
            
            try:
                min_val = float(min_price) if min_price else 0
                max_val = float(max_price) if max_price else float('inf')
                
                if min_price and max_price and min_val > max_val:
                    min_val, max_val = max_val, min_val
                    min_price, max_price = str(max_val), str(min_val)
                
                for product in products:
                    if min_val <= product['price'] <= max_val:
                        filtered_products.append(product)
            except ValueError:
                filtered_products = products
    
    # Рассчитываем минимальную и максимальную цену
    all_prices = [p['price'] for p in products]
    min_all_price = min(all_prices)
    max_all_price = max(all_prices)
    
    return render_template('lab3/products.html',
                         products=products,
                         min_price=min_price,
                         max_price=max_price,
                         filtered_products=filtered_products,
                         min_all_price=min_all_price,
                         max_all_price=max_all_price)