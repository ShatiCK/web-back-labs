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