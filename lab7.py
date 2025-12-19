from flask import Blueprint, render_template, request, jsonify

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/index.html')

films = [
    {
        "title": "Reservoir Dogs",
        "title_ru": "Бешеные псы",
        "year": 1992,
        "description": "Шесть преступников, не знающих имен друг друга, собираются для ограбления ювелирного магазина. После провала операции они пытаются выяснить, кто среди них предатель."
    },
    {
        "title": "Pulp Fiction",
        "title_ru": "Криминальное чтиво",
        "year": 1994,
        "description": "Переплетающиеся истории гангстеров, боксера, грабителей и бандитов в Лос-Анджелесе. Один из самых влиятельных фильмов в истории кинематографа."
    },
    {
        "title": "Jackie Brown",
        "title_ru": "Джеки Браун",
        "year": 1997,
        "description": "Стюардесса, занимающаяся контрабандой денег для торговца оружием, попадает под давление полиции и решает обмануть обе стороны."
    },
    {
        "title": "Kill Bill: Volume 1",
        "title_ru": "Убить Билла. Фильм 1",
        "year": 2003,
        "description": "Невеста, бывшая убийца, выходит из комы и начинает кровавый путь мести против команды наемников, которые предали ее."
    },
    {
        "title": "Kill Bill: Volume 2",
        "title_ru": "Убить Билла. Фильм 2",
        "year": 2004,
        "description": "Продолжение истории Невесты, которая продолжает свой путь мести, чтобы добраться до главной цели — Билла."
    },
    {
        "title": "Death Proof",
        "title_ru": "Доказательство смерти",
        "year": 2007,
        "description": "История каскадера, который использует свою 'смертоносную' машину для убийства молодых девушек, пока не встречает достойных соперниц."
    },
    {
        "title": "Inglourious Basterds",
        "title_ru": "Бесславные ублюдки",
        "year": 2009,
        "description": "Во время Второй мировой войны группа еврейских солдат-мстителей планирует уничтожить нацистское руководство во Франции."
    },
    {
        "title": "Django Unchained",
        "title_ru": "Джанго освобожденный",
        "year": 2012,
        "description": "Освобожденный раб вместе с охотником за головами путешествует по Америке, чтобы спасти свою жену у жестокого плантатора."
    },
    {
        "title": "The Hateful Eight",
        "title_ru": "Омерзительная восьмерка",
        "year": 2015,
        "description": "Вскоре после Гражданской войны восемь незнакомцев оказываются в запертой лавке во время метели в Вайоминге, где раскрываются их темные секреты."
    },
    {
        "title": "Once Upon a Time in Hollywood",
        "title_ru": "Однажды в Голливуде",
        "year": 2019,
        "description": "История актера и его дублера, пытающихся найти свое место в стремительно меняющемся Голливуде 1969 года."
    }
]
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return '', 404
    return films[id]

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return '', 404
    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    
    # Если оригинальное название пустое, а русское задано - используем русское
    if (not film.get('title') or film['title'].strip() == '') and film.get('title_ru'):
        film['title'] = film['title_ru']
    
    # Проверка обязательных полей
    required_fields = ['title_ru', 'year', 'description']
    for field in required_fields:
        if field not in film or not str(film[field]).strip():
            return {field: 'Это поле обязательно для заполнения'}, 400
    
    # Проверка на существующий ID
    if id < 0 or id >= len(films):
        return '', 404
    
    films[id] = film
    return films[id]

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    data = request.get_json()
    
    if not data:
        return '', 400
    
    # Если оригинальное название пустое, а русское задано - используем русское
    if (not data.get('title') or data['title'].strip() == '') and data.get('title_ru'):
        data['title'] = data['title_ru']
    
    # Проверка обязательных полей
    required_fields = ['title_ru', 'year', 'description']
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            return {field: 'Это поле обязательно для заполнения'}, 400
    
    # Проверка года (должен быть числом)
    try:
        year = int(data['year'])
        if year < 1888 or year > 2100:
            return {'year': 'Некорректный год выпуска'}, 400
    except ValueError:
        return {'year': 'Год должен быть числом'}, 400
    
    new_film = {
        'title': data.get('title', ''),
        'title_ru': data['title_ru'],
        'year': year,
        'description': data['description']
    }
    
    films.append(new_film)
    return str(len(films) - 1), 201