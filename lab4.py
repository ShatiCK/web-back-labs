from flask import Blueprint, render_template, request, redirect, session
  

lab4 = Blueprint('lab4', __name__)


tree_count = 0

users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей Петров', 'gender': 'м'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Смит', 'gender': 'м'},
    {'login': 'mary', 'password': '999', 'name': 'Мария Иванова', 'gender': 'ж'},
    {'login': 'john', 'password': '777', 'name': 'Джон Доу', 'gender': 'м'}
]

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены')
    
    x1 = int(x1)
    x2 = int(x2)
    
    
    if x2 == 0:
        return render_template('lab4/div.html', error='Деление на ноль невозможно')
    
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)



@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum_operation():
    x1 = request.form.get('x1', '0')
    x2 = request.form.get('x2', '0')
    
    x1 = int(x1) if x1 != '' else 0
    x2 = int(x2) if x2 != '' else 0
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mult-form')
def mult_form():
    return render_template('lab4/mult-form.html')

@lab4.route('/lab4/mult', methods=['POST'])
def mult():
    x1 = request.form.get('x1', '1')
    x2 = request.form.get('x2', '1')
    
    x1 = int(x1) if x1 != '' else 1
    x2 = int(x2) if x2 != '' else 1
    
    result = x1 * x2
    return render_template('lab4/mult.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены')
    
    x1 = int(x1)
    x2 = int(x2)
    
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены')
    
    x1 = int(x1)
    x2 = int(x2)
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Оба числа не могут быть нулями')
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    
    operation = request.form.get('operation')
    
    if operation == 'plant' and tree_count < 10:
        tree_count += 1
    elif operation == 'cut' and tree_count > 0:
        tree_count -= 1
    
    
    return redirect('/lab4/tree')


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            name = session.get('name', '')
        else:
            authorized = False
            login = ''
            name = ''
        return render_template('lab4/login.html', authorized=authorized, login=login, name=name)
    
    login_input = request.form.get('login')
    password = request.form.get('password')
    
    
    if not login_input:
        return render_template('lab4/login.html', error='Не введён логин', login_input=login_input, authorized=False)
    if not password:
        return render_template('lab4/login.html', error='Не введён пароль', login_input=login_input, authorized=False)
    
    
    for user in users:
        if login_input == user['login'] and password == user['password']:
            session['login'] = user['login']
            session['name'] = user['name']
            return redirect('/lab4/login')
    
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, login_input=login_input, authorized=False)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)  
    return redirect('/lab4/login')  

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    error = None
    temperature = None
    snowflakes = 0
    
    if request.method == 'POST':
        temp_str = request.form.get('temperature')
        
        if not temp_str:
            error = 'Ошибка: не задана температура'
        else:
            try:
                temperature = int(temp_str)
                
                if temperature < -12:
                    error = 'Не удалось установить температуру — слишком низкое значение'
                elif temperature > -1:
                    error = 'Не удалось установить температуру — слишком высокое значение'
                elif -12 <= temperature <= -9:
                    snowflakes = 3
                elif -8 <= temperature <= -5:
                    snowflakes = 2
                elif -4 <= temperature <= -1:
                    snowflakes = 1
                    
            except ValueError:
                error = 'Ошибка: введите целое число'
    
    return render_template('lab4/fridge.html', 
                         error=error, 
                         temperature=temperature, 
                         snowflakes=snowflakes)


@lab4.route('/lab4/grain_order', methods=['GET', 'POST'])
def grain_order():
    error = None
    result = None
    discount = 0
    
    grains = {
        'barley': {'name': 'ячмень', 'price': 12000},
        'oats': {'name': 'овёс', 'price': 8500},
        'wheat': {'name': 'пшеница', 'price': 9000},
        'rye': {'name': 'рожь', 'price': 15000}
    }
    
    if request.method == 'POST':
        grain_type = request.form.get('grain_type')
        weight_str = request.form.get('weight')
        
        if not grain_type:
            error = 'Выберите тип зерна'
        elif not weight_str:
            error = 'Введите вес'
        else:
            try:
                weight = float(weight_str)
                
                if weight <= 0:
                    error = 'Вес должен быть больше 0'
                elif weight > 100:
                    error = 'Такого объёма сейчас нет в наличии'
                else:
                    grain = grains[grain_type]
                    total = weight * grain['price']
                    
                    # Скидка за большой объем
                    if weight > 10:
                        discount = total * 0.1
                        total -= discount
                    
                    result = {
                        'grain': grain['name'],
                        'weight': weight,
                        'total': total,
                        'discount': discount
                    }
                    
            except ValueError:
                error = 'Введите корректный вес'
    
    return render_template('lab4/grain_order.html', 
                         error=error, 
                         result=result, 
                         grains=grains)