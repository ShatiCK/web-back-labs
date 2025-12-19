from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re
import os
import json
import tempfile

rgz = Blueprint("rgz", __name__, url_prefix="/rgz")

# ---- Параметры отображения (на каждой странице) ----
STUDENT_FIO = "Шатравский Никита Дмитриевич"
STUDENT_GROUP = "ФБИ-33"

# ---- Справочник услуг ----
SERVICE_TYPES = ["репетитор", "бухгалтер", "программист", "дизайнер", "юрист"]

# ---- JSON хранилище ----
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "storage", "data.json")


def load_data_from_file():
    if not os.path.exists(DATA_PATH):
        return None
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return None
        return data
    except Exception:
        # Если файл повреждён/пустой — игнорируем и пересоздадим данные
        return None


def save_data_to_file(data: dict):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    # атомарная запись: сначала во временный файл, затем replace
    fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(DATA_PATH), suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, DATA_PATH)
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass


DATA = {
    "users": [],
    "next_user_id": 1
}

# ---- Валидация логина/пароля (латиница, цифры, знаки) ----
LOGIN_RE = re.compile(r"^[A-Za-z0-9_!@#$%^&*().-]{3,32}$")
PASS_RE = re.compile(r"^[A-Za-z0-9_!@#$%^&*().-]{6,64}$")


def _recalc_next_user_id():
    if not DATA["users"]:
        DATA["next_user_id"] = 1
        return
    try:
        DATA["next_user_id"] = max(int(u.get("id", 0)) for u in DATA["users"]) + 1
    except Exception:
        DATA["next_user_id"] = len(DATA["users"]) + 1


def seed_if_empty():
    """
    Загрузка из storage/data.json; если файла нет — создаём стартовые данные (админ + 30)
    и сохраняем.
    """
    if DATA["users"]:
        return

    loaded = load_data_from_file()
    if loaded and loaded.get("users"):
        DATA["users"] = loaded["users"]

        # минимальная нормализация структуры
        for u in DATA["users"]:
            # на всякий: id/int
            try:
                u["id"] = int(u.get("id", 0))
            except Exception:
                pass

            # если вдруг кто-то сохранил password (не нужно) — убираем
            if "password" in u:
                u.pop("password", None)

            # гарантируем наличие ключей
            u.setdefault("role", "user")
            u.setdefault("name", "")
            u.setdefault("service", "")
            u.setdefault("experience", 0)
            u.setdefault("price", 0)
            u.setdefault("about", "")
            u.setdefault("is_hidden", False)
            u.setdefault("created_at", "")

        # next_user_id может отсутствовать — восстановим
        if loaded.get("next_user_id"):
            try:
                DATA["next_user_id"] = int(loaded["next_user_id"])
            except Exception:
                _recalc_next_user_id()
        else:
            _recalc_next_user_id()

        return

    # --- Если файла нет: создаём стартовые данные ---

    # Админ
    admin = {
        "id": DATA["next_user_id"],
        "login": "admin",
        "password_hash": generate_password_hash("admin123!"),
        "role": "admin",
        "name": "Администратор",
        "service": "",
        "experience": 0,
        "price": 0,
        "about": "",
        "is_hidden": False,
        "created_at": datetime.now().isoformat(timespec="seconds")
    }
    DATA["users"].append(admin)
    DATA["next_user_id"] += 1

    # 30 специалистов
    for i in range(1, 31):
        u = {
            "id": DATA["next_user_id"],
            "login": f"user{i}",
            "password_hash": generate_password_hash("User123!"),
            "role": "user",
            "name": f"Пользователь {i}",
            "service": SERVICE_TYPES[i % len(SERVICE_TYPES)],
            "experience": (i % 15) + 1,        # 1..15
            "price": 500 + (i % 10) * 250,     # 500..2750
            "about": "Краткое описание специалиста.",
            "is_hidden": False,
            "created_at": datetime.now().isoformat(timespec="seconds")
        }
        DATA["users"].append(u)
        DATA["next_user_id"] += 1

    save_data_to_file(DATA)


@rgz.before_request
def _seed():
    seed_if_empty()


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return next((u for u in DATA["users"] if u["id"] == uid), None)


def admin_required():
    u = current_user()
    return bool(u and u.get("role") == "admin")


def validate_credentials(login: str, password: str):
    if not login or not password:
        return "Логин и пароль не должны быть пустыми."
    if not LOGIN_RE.match(login):
        return "Логин: только латиница/цифры/знаки, длина 3–32."
    if not PASS_RE.match(password):
        return "Пароль: только латиница/цифры/знаки, длина 6–64."
    return None


def to_int(s, default=None):
    try:
        return int(s)
    except Exception:
        return default


def to_float(s, default=None):
    try:
        return float(s)
    except Exception:
        return default


@rgz.route("/")
def index():
    """Главная страница: поиск + выдача анкет (не более 5 за раз)."""

    # фильтры
    q_name = (request.args.get("name") or "").strip().lower()
    q_service = (request.args.get("service") or "").strip().lower()
    exp_from = to_int(request.args.get("exp_from"), None)
    exp_to = to_int(request.args.get("exp_to"), None)
    price_from = to_float(request.args.get("price_from"), None)
    price_to = to_float(request.args.get("price_to"), None)

    # пагинация
    page = max(to_int(request.args.get("page"), 1) or 1, 1)
    per_page = 5

    # список анкет: только user и не скрытые
    users = [u for u in DATA["users"] if u.get("role") == "user" and not u.get("is_hidden")]

    if q_name:
        users = [u for u in users if q_name in (u.get("name") or "").lower()]

    if q_service:
        users = [u for u in users if (u.get("service") or "").lower() == q_service]

    if exp_from is not None:
        users = [u for u in users if (u.get("experience") or 0) >= exp_from]

    if exp_to is not None:
        users = [u for u in users if (u.get("experience") or 0) <= exp_to]

    if price_from is not None:
        users = [u for u in users if (u.get("price") or 0) >= price_from]

    if price_to is not None:
        users = [u for u in users if (u.get("price") or 0) <= price_to]

    total = len(users)
    start = (page - 1) * per_page
    end = start + per_page
    chunk = users[start:end]
    has_next = end < total

    return render_template(
        "RGZ/index.html",
        student_fio=STUDENT_FIO,
        student_group=STUDENT_GROUP,
        user=current_user(),
        service_types=SERVICE_TYPES,
        results=chunk,
        page=page,
        has_next=has_next,
        filters=dict(
            name=request.args.get("name", ""),
            service=request.args.get("service", ""),
            exp_from=request.args.get("exp_from", ""),
            exp_to=request.args.get("exp_to", ""),
            price_from=request.args.get("price_from", ""),
            price_to=request.args.get("price_to", ""),
        ),
        total=total
    )


@rgz.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template(
            "RGZ/register.html",
            student_fio=STUDENT_FIO,
            student_group=STUDENT_GROUP,
            user=current_user()
        )

    login = (request.form.get("login") or "").strip()
    password = (request.form.get("password") or "").strip()

    err = validate_credentials(login, password)
    if err:
        return render_template(
            "RGZ/register.html",
            error=err,
            student_fio=STUDENT_FIO,
            student_group=STUDENT_GROUP,
            user=current_user()
        )

    if any(u.get("login") == login for u in DATA["users"]):
        return render_template(
            "RGZ/register.html",
            error="Логин уже занят.",
            student_fio=STUDENT_FIO,
            student_group=STUDENT_GROUP,
            user=current_user()
        )

    new_user = {
        "id": DATA["next_user_id"],
        "login": login,
        "password_hash": generate_password_hash(password),
        "role": "user",
        "name": "",
        "service": "",
        "experience": 0,
        "price": 0.0,
        "about": "",
        "is_hidden": False,
        "created_at": datetime.now().isoformat(timespec="seconds")
    }
    DATA["users"].append(new_user)
    DATA["next_user_id"] += 1

    save_data_to_file(DATA)

    session["user_id"] = new_user["id"]
    return redirect(url_for("rgz.profile_edit"))


@rgz.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template(
            "RGZ/login.html",
            student_fio=STUDENT_FIO,
            student_group=STUDENT_GROUP,
            user=current_user()
        )

    login_val = (request.form.get("login") or "").strip()
    password = (request.form.get("password") or "").strip()

    u = next((x for x in DATA["users"] if x.get("login") == login_val), None)
    if not u or not check_password_hash(u.get("password_hash", ""), password):
        return render_template(
            "RGZ/login.html",
            error="Неверный логин или пароль.",
            student_fio=STUDENT_FIO,
            student_group=STUDENT_GROUP,
            user=current_user()
        )

    session["user_id"] = u["id"]

    if u.get("role") == "admin":
        return redirect(url_for("rgz.admin_users"))

    return redirect(url_for("rgz.profile"))


@rgz.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("rgz.index"))


@rgz.route("/profile")
def profile():
    u = current_user()
    if not u:
        return redirect(url_for("rgz.login"))
    if u.get("role") == "admin":
        return redirect(url_for("rgz.admin_users"))

    return render_template(
        "RGZ/profile.html",
        student_fio=STUDENT_FIO,
        student_group=STUDENT_GROUP,
        user=u
    )


@rgz.route("/profile/edit", methods=["GET", "POST"])
def profile_edit():
    u = current_user()
    if not u:
        return redirect(url_for("rgz.login"))
    if u.get("role") != "user":
        abort(403)

    if request.method == "GET":
        return render_template(
            "RGZ/profile_edit.html",
            student_fio=STUDENT_FIO,
            student_group=STUDENT_GROUP,
            user=u,
            service_types=SERVICE_TYPES
        )

    name = (request.form.get("name") or "").strip()
    service = (request.form.get("service") or "").strip().lower()
    experience = to_int(request.form.get("experience"), 0)
    price = to_float(request.form.get("price"), 0.0)
    about = (request.form.get("about") or "").strip()

    if not name:
        err = "Имя не должно быть пустым."
    elif service not in SERVICE_TYPES:
        err = "Выберите корректный вид услуги."
    elif experience < 0 or experience > 60:
        err = "Стаж должен быть в диапазоне 0–60."
    elif price <= 0:
        err = "Цена должна быть положительной."
    else:
        err = None

    if err:
        return render_template(
            "RGZ/profile_edit.html",
            student_fio=STUDENT_FIO,
            student_group=STUDENT_GROUP,
            user=u,
            service_types=SERVICE_TYPES,
            error=err
        )

    u["name"] = name
    u["service"] = service
    u["experience"] = experience
    u["price"] = price
    u["about"] = about

    save_data_to_file(DATA)

    return redirect(url_for("rgz.profile"))


@rgz.route("/profile/toggle-hide", methods=["POST"])
def profile_toggle_hide():
    u = current_user()
    if not u:
        return redirect(url_for("rgz.login"))
    if u.get("role") != "user":
        abort(403)

    u["is_hidden"] = not u.get("is_hidden", False)

    save_data_to_file(DATA)

    return redirect(url_for("rgz.profile"))


@rgz.route("/account/delete", methods=["POST"])
def account_delete():
    u = current_user()
    if not u:
        return redirect(url_for("rgz.login"))
    if u.get("role") != "user":
        abort(403)

    DATA["users"] = [x for x in DATA["users"] if x.get("id") != u.get("id")]
    _recalc_next_user_id()

    save_data_to_file(DATA)

    session.clear()
    return redirect(url_for("rgz.index"))


# ---------------------- Админка ----------------------

@rgz.route("/admin/users")
def admin_users():
    if not admin_required():
        abort(403)

    q = (request.args.get("q") or "").strip().lower()
    users = DATA["users"]
    if q:
        users = [u for u in users if q in (u.get("login") or "").lower() or q in (u.get("name") or "").lower()]

    return render_template(
        "RGZ/admin_users.html",
        student_fio=STUDENT_FIO,
        student_group=STUDENT_GROUP,
        user=current_user(),
        users=users
    )


@rgz.route("/admin/users/<int:user_id>/delete", methods=["POST"])
def admin_user_delete(user_id):
    if not admin_required():
        abort(403)

    # запретим удалить самого себя
    if session.get("user_id") == user_id:
        abort(400)

    DATA["users"] = [u for u in DATA["users"] if u.get("id") != user_id]
    _recalc_next_user_id()

    save_data_to_file(DATA)

    return redirect(url_for("rgz.admin_users"))
