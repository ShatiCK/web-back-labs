// Основная функция для заполнения списка фильмов
function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        
        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');
            let tdTitleRus = document.createElement('td'); // Русское название ПЕРВОЕ
            let tdTitle = document.createElement('td');    // Английское название ВТОРОЕ
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');
            
            // Русское название (основное)
            tdTitleRus.innerText = films[i].title_ru;
            
            // Английское название (второстепенное)
            if (films[i].title && films[i].title !== films[i].title_ru) {
                let span = document.createElement('span');
                span.className = 'original-name';
                span.innerText = films[i].title;
                tdTitle.appendChild(span);
            }
            
            tdYear.innerText = films[i].year;
            
            // Создаем кнопки
            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.onclick = function() {
                editFilm(i);
            };
            
            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.onclick = function() {
                deleteFilm(i, films[i].title_ru);
            };
            
            // Добавляем кнопки в ячейку действий
            tdActions.appendChild(editButton);
            tdActions.appendChild(delButton);
            
            // Добавляем ячейки в строку в правильном порядке
            tr.append(tdTitleRus);  // 1. Русское название
            tr.append(tdTitle);     // 2. Английское название
            tr.append(tdYear);      // 3. Год
            tr.append(tdActions);   // 4. Действия
            
            // Добавляем строку в таблицу
            tbody.append(tr);
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
    });
}

// Функция удаления фильма
function deleteFilm(id, title) {
    if(!confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;
    
    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
    .then(function() {
        fillFilmList();
    })
    .catch(function(error) {
        console.error('Ошибка при удалении:', error);
    });
}

// Показываем модальное окно для добавления нового фильма
function addFilm() {
    // Очищаем все поля
    document.getElementById('id').value = '';
    document.getElementById('title_ru').value = '';
    document.getElementById('title').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    
    // Очищаем все ошибки
    document.querySelectorAll('.error').forEach(el => el.innerText = '');
    
    document.querySelector('.modal').style.display = 'block';
}

// Показываем модальное окно для редактирования существующего фильма
function editFilm(id) {
    // Очищаем все ошибки
    document.querySelectorAll('.error').forEach(el => el.innerText = '');
    
    // Загружаем данные фильма с сервера
    fetch(`/lab7/rest-api/films/${id}`)
    .then(response => response.json())
    .then(film => {
        document.getElementById('id').value = id;
        document.getElementById('title_ru').value = film.title_ru;
        document.getElementById('title').value = film.title;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        
        document.querySelector('.modal').style.display = 'block';
    })
    .catch(error => {
        console.error('Ошибка при загрузке фильма:', error);
        alert('Ошибка при загрузке данных фильма');
    });
}

// Отправка данных фильма (добавление или редактирование)
function sendFilm() {
    const id = document.getElementById('id').value;
    const title_ru = document.getElementById('title_ru').value;
    const title = document.getElementById('title').value;
    const year = document.getElementById('year').value;
    const description = document.getElementById('description').value;
    
    // Очищаем все ошибки
    document.querySelectorAll('.error').forEach(el => el.innerText = '');
    
    // Проверка обязательных полей
    if (!title_ru.trim() || !year.trim() || !description.trim()) {
        alert('Пожалуйста, заполните все обязательные поля');
        return;
    }
    
    const filmData = {
        title_ru: title_ru,
        title: title || title_ru, // Если оригинальное название пустое, используем русское
        year: parseInt(year),
        description: description
    };
    
    let url = '/lab7/rest-api/films/';
    let method = 'POST';
    
    // Если есть ID, то редактируем существующий фильм
    if (id !== '') {
        url = `/lab7/rest-api/films/${id}`;
        method = 'PUT';
    }
    
    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(filmData)
    })
    .then(function(resp){  
        if(resp.ok){  
            fillFilmList();  
            cancel();
            return {};  
        }  
        return resp.json();  
    })  
    .then(function(errors){  
        if(errors) {
            // Показываем все ошибки
            for(const field in errors) {
                const errorElement = document.getElementById(field + '_error');
                if(errorElement) {
                    errorElement.innerText = errors[field];  
                }
            }
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
        alert('Ошибка при сохранении фильма');
    });
}

// Закрытие модального окна
function cancel() {
    document.querySelector('.modal').style.display = 'none';
    // Очищаем все ошибки
    document.querySelectorAll('.error').forEach(el => el.innerText = '');
}

// Добавляем нормальные CSS стили без выделения строк
const style = document.createElement('style');
style.textContent = `
    /* Таблица - нормальная */
    table {
        width: 100%;
        border: 2px solid #333;
        border-collapse: collapse;
        margin: 20px 0;
        font-family: Arial, Helvetica, sans-serif;
    }
    
    th {
        background: #4a6fa5;
        color: white;
        padding: 12px;
        text-align: left;
        border: 1px solid #333;
        font-weight: bold;
    }
    
    td {
        padding: 10px 12px;
        border: 1px solid #ccc;
    }
    
    /* Кнопки - нормальные */
    button {
        padding: 8px 16px;
        margin: 4px;
        background: #4a6fa5;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
        font-weight: bold;
    }
    
    button:hover {
        background: #3a5a8a;
    }
    
    /* Кнопка добавления выделенная */
    button[onclick="addFilm()"] {
        background: #28a745;
        padding: 10px 20px;
        font-size: 16px;
    }
    
    button[onclick="addFilm()"]:hover {
        background: #218838;
    }
    
    /* Кнопки действий в таблице */
    button:not([onclick="addFilm()"]) {
        background: #6c757d;
        font-size: 13px;
        padding: 6px 12px;
    }
    
    button:not([onclick="addFilm()"]):hover {
        background: #5a6268;
    }
    
    /* Кнопка удаления красная */
    button[onclick^="deleteFilm"] {
        background: #dc3545;
    }
    
    button[onclick^="deleteFilm"]:hover {
        background: #c82333;
    }
    
    /* Модальное окно - нормальное */
    .modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        z-index: 1000;
    }
    
    .modal > div {
        background: white;
        width: 500px;
        margin: 50px auto;
        padding: 25px;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        border: 2px solid #333;
    }
    
    .modal h2 {
        margin: 0 0 20px 0;
        color: #333;
        border-bottom: 2px solid #4a6fa5;
        padding-bottom: 10px;
    }
    
    .modal label {
        display: block;
        margin: 15px 0 5px;
        font-weight: bold;
        color: #333;
    }
    
    .modal input, .modal textarea {
        width: 100%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 14px;
        box-sizing: border-box;
    }
    
    .modal input:focus, .modal textarea:focus {
        border-color: #4a6fa5;
        outline: none;
        box-shadow: 0 0 0 2px rgba(74, 111, 165, 0.2);
    }
    
    .modal-buttons {
        margin-top: 25px;
        text-align: right;
    }
    
    .modal-buttons button {
        margin-left: 10px;
        min-width: 80px;
    }
    
    .modal-buttons button:first-child {
        background: #28a745;
    }
    
    .modal-buttons button:first-child:hover {
        background: #218838;
    }
    
    .modal-buttons button:last-child {
        background: #6c757d;
    }
    
    .modal-buttons button:last-child:hover {
        background: #5a6268;
    }
    
    /* Оригинальное название */
    .original-name {
        font-style: italic;
        color: #311ebfff;
        font-size: 0.9em;
    }
    
    /* Ошибки */
    .error {
        color: #dc3545;
        font-size: 12px;
        margin-top: 3px;
        font-weight: normal;
    }
    
    /* Обязательные поля */
    .required::after {
        content: " *";
        color: #dc3545;
    }
`;
document.head.appendChild(style);

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    fillFilmList();
});