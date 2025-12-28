from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
import random
import hashlib
import json

lab9 = Blueprint('lab9', __name__)

# Хранилища
boxes_state = {}
boxes_positions = {}
users_db = {
    'test': hashlib.sha256('test123'.encode()).hexdigest(),  # тестовый пользователь
    'user': hashlib.sha256('password'.encode()).hexdigest()   # еще один пользователь
}

# Поздравления и подарки
congratulations = [
    "С Новым годом! Пусть сбудутся все мечты!",
    "Желаю здоровья, счастья и успехов!",
    "Пусть новый год принесёт много радости!",
    "Желаю исполнения всех желаний!",
    "Счастья, любви и благополучия в новом году!",
    "Радостного настроения каждый день!",
    "Финансового благополучия и стабильности!",
    "Удачи во всех начинаниях и проектах!",
    "Новых достижений и громких побед!",
    "Светлого и волшебного нового года!"
]

# Подарки: первые 5 для всех, остальные 5 только для авторизованных
gifts = [
    "/static/lab9/gift1.png",    
    "/static/lab9/gift2.png",   
    "/static/lab9/gift3.png",    
    "/static/lab9/gift4.png",    
    "/static/lab9/gift5.png",    
    "/static/lab9/special1.png", 
    "/static/lab9/special2.png", 
    "/static/lab9/special3.png", 
    "/static/lab9/special4.png", 
    "/static/lab9/special5.png" 
]

def init_boxes_positions():
    """Инициализирует случайные позиции коробок"""
    if not boxes_positions:
        for i in range(10):
            boxes_positions[i] = {
                'top': random.randint(10, 75),
                'left': random.randint(5, 85)
            }

@lab9.route('/lab9/')
def lab():
    init_boxes_positions()
    return render_template('lab9/index.html')

@lab9.route('/lab9/login', methods=['GET', 'POST'])
def login():
    """Страница входа"""
    if request.method == 'GET':
        return render_template('lab9/login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return render_template('lab9/login.html', error='Заполните все поля')
    
    # Проверка пользователя
    if username not in users_db:
        return render_template('lab9/login.html', error='Пользователь не найден')
    
    # Проверка пароля
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if users_db[username] != password_hash:
        return render_template('lab9/login.html', error='Неверный пароль')
    
    # Авторизация успешна
    session['username'] = username
    session['logged_in'] = True
    
    # Создаем уникальный session_id для хранения состояния коробок
    if 'session_id' not in session:
        session['session_id'] = f"{username}_{random.randint(1000, 9999)}"
    
    return redirect(url_for('lab9.lab'))

@lab9.route('/lab9/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации"""
    if request.method == 'GET':
        return render_template('lab9/register.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return render_template('lab9/register.html', error='Заполните все поля')
    
    if len(username) < 3:
        return render_template('lab9/register.html', error='Имя пользователя должно быть не менее 3 символов')
    
    if len(password) < 4:
        return render_template('lab9/register.html', error='Пароль должен быть не менее 4 символов')
    
    # Проверка существования пользователя
    if username in users_db:
        return render_template('lab9/register.html', error='Имя пользователя уже занято')
    
    # Регистрация
    users_db[username] = hashlib.sha256(password.encode()).hexdigest()
    session['username'] = username
    session['logged_in'] = True
    session['session_id'] = f"{username}_{random.randint(1000, 9999)}"
    
    return redirect(url_for('lab9.lab'))

@lab9.route('/lab9/logout')
def logout():
    """Выход из системы"""
    session.pop('username', None)
    session.pop('logged_in', None)
    session.pop('session_id', None)
    return redirect(url_for('lab9.lab'))

@lab9.route('/lab9/api/boxes')
def get_boxes():
    """API: Получение информации о коробках"""
    init_boxes_positions()
    
    # Получаем или создаем session_id
    session_id = session.get('session_id')
    if not session_id:
        session_id = f"guest_{random.randint(1000, 9999)}"
        session['session_id'] = session_id
    
    # Инициализация состояния для этой сессии
    if session_id not in boxes_state:
        boxes_state[session_id] = {
            'opened_boxes': [],
            'opened_count': 0
        }
    
    state = boxes_state[session_id]
    is_logged_in = session.get('logged_in', False)
    username = session.get('username', 'Гость')
    
    # Формируем информацию о коробках
    boxes_list = []
    for i in range(10):
        is_opened = i in state['opened_boxes']
        is_available = True
        
        # Коробки с 5 по 9 (индексы 5-9) только для авторизованных
        if i >= 5 and not is_logged_in:
            is_available = False
        
        boxes_list.append({
            'id': i,
            'top': boxes_positions[i]['top'],
            'left': boxes_positions[i]['left'],
            'opened': is_opened,
            'available': is_available
        })
    
    return jsonify({
        'boxes': boxes_list,
        'opened_count': state['opened_count'],
        'remaining_count': 10 - len(state['opened_boxes']),
        'logged_in': is_logged_in,
        'username': username
    })

@lab9.route('/lab9/api/open', methods=['POST'])
def open_box():
    """API: Открытие коробки"""
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'success': False, 'message': 'Ошибка сессии'})
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Нет данных'})
    
    box_id = data.get('box_id')
    
    if box_id is None or box_id < 0 or box_id >= 10:
        return jsonify({'success': False, 'message': 'Неверный номер коробки'})
    
    # Проверка авторизации для специальных коробок (5-9)
    if box_id >= 5 and not session.get('logged_in', False):
        return jsonify({
            'success': False, 
            'message': 'Эта коробка только для авторизованных пользователей. Пожалуйста, войдите в систему.'
        })
    
    # Инициализация состояния
    if session_id not in boxes_state:
        boxes_state[session_id] = {'opened_boxes': [], 'opened_count': 0}
    
    state = boxes_state[session_id]
    
    # Проверка, не открыта ли уже коробка
    if box_id in state['opened_boxes']:
        return jsonify({'success': False, 'message': 'Эта коробка уже открыта'})
    
    # Проверка лимита (максимум 3 коробки)
    if state['opened_count'] >= 3:
        return jsonify({
            'success': False, 
            'message': 'Вы уже открыли максимальное количество коробок (3)'
        })
    
    # Открываем коробку
    state['opened_boxes'].append(box_id)
    state['opened_count'] = len(state['opened_boxes'])
    
    return jsonify({
        'success': True,
        'congratulation': congratulations[box_id],
        'gift': gifts[box_id],
        'opened_count': state['opened_count'],
        'remaining_count': 10 - state['opened_count']
    })

@lab9.route('/lab9/api/reset', methods=['POST'])
def reset_boxes():
    """API: Сброс всех коробок (Дед Мороз)"""
    if not session.get('logged_in', False):
        return jsonify({
            'success': False, 
            'message': 'Эта функция доступна только авторизованным пользователям'
        })
    
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'success': False, 'message': 'Ошибка сессии'})
    
    # Сбрасываем состояние коробок
    boxes_state[session_id] = {
        'opened_boxes': [],
        'opened_count': 0
    }
    
    # Перегенерируем позиции коробок
    init_boxes_positions()
    
    return jsonify({
        'success': True,
        'message': '🎅 Дед Мороз наполнил все коробки заново! Теперь вы можете открыть новые подарки.'
    })

@lab9.route('/lab9/api/user')
def get_user_info():
    """API: Информация о текущем пользователе"""
    return jsonify({
        'logged_in': session.get('logged_in', False),
        'username': session.get('username', 'Гость')
    })