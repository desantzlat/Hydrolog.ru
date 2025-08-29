# НЕ ИСПОЛЬЗУЕМ 'from replit import db'
import json  # ИМПОРТИРУЕМ БИБЛИОТЕКУ ДЛЯ РАБОТЫ С JSON

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'your_very_secret_key_12345'

    # --- НОВЫЕ ФУНКЦИИ ДЛЯ РАБОТЫ С БАЗОЙ ДАННЫХ ---
def load_db():
        """Загружает данные из JSON-файла."""
        try:
            with open('database.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Если файл пуст или не существует, возвращаем пустой словарь
            return {}

def save_db(data):
        """Сохраняет данные в JSON-файл."""
        with open('database.json', 'w') as f:
            json.dump(data, f, indent=4)
    # ------------------------------------------------

@app.route('/')
def index():
        return render_template('index.html')

    # ... (остальные маршруты '/calculators', '/library' и т.д. остаются без изменений) ...

@app.route('/calculators', methods=['GET', 'POST'])
def calculators_page():
        result = None
        if request.method == 'POST':
            area_str = request.form.get('area')
            velocity_str = request.form.get('velocity')
            if area_str and velocity_str:
                area = float(area_str)
                velocity = float(velocity_str)
                discharge = area * velocity
                result = discharge
        return render_template('calculators.html', result=result)

@app.route('/library')
def library_page():
        return render_template('library.html')

@app.route('/expert')
def expert_page():
        return render_template('expert.html')

@app.route('/climatology')
def climatology_page():
        climate_data = [
            {'year': 2000, 'avg_temp': 5.2, 'precipitation': 602},
            {'year': 2001, 'avg_temp': 5.5, 'precipitation': 630},
            {'year': 2002, 'avg_temp': 5.1, 'precipitation': 590},
            {'year': 2003, 'avg_temp': 5.6, 'precipitation': 655},
            {'year': 2004, 'avg_temp': 5.4, 'precipitation': 615},
        ]
        return render_template('climatology.html', records=climate_data)

@app.route('/hydrology')
def hydrology_page():
        sample_data = [
            {'year': 1980, 'avg_flow': 150.5, 'max_flow': 320.1, 'min_flow': 50.2},
            {'year': 1981, 'avg_flow': 145.2, 'max_flow': 310.8, 'min_flow': 48.9},
            {'year': 1982, 'avg_flow': 160.1, 'max_flow': 350.0, 'min_flow': 55.1},
            {'year': 1983, 'avg_flow': 155.7, 'max_flow': 335.5, 'min_flow': 52.3},
            {'year': 1984, 'avg_flow': 148.9, 'max_flow': 315.6, 'min_flow': 49.5},
        ]
        return render_template('hydrology.html', records=sample_data)

    # === МАРШРУТ ДЛЯ РЕГИСТРАЦИИ (ИЗМЕНЁН) ===
@app.route('/register', methods=['GET', 'POST'])
def register():
        if request.method == 'POST':
            name = request.form.get('name')
            username = request.form.get('username')
            password = request.form.get('password')

            if not name or not username or not password:
                flash('Все поля должны быть заполнены.', 'danger')
                return redirect(url_for('register'))

            users = load_db()
            if username in users:
                flash('Пользователь с таким email уже существует!', 'danger')
                return redirect(url_for('register'))

            hashed_password = generate_password_hash(password)
            users[username] = {
                'password': hashed_password,
                'name': name
            }
            save_db(users)

            flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html')

    # === МАРШРУТ ДЛЯ ВХОДА (ИЗМЕНЁН) ===
@app.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            users = load_db()
            if username in users and check_password_hash(users[username]['password'], password):
                session['user_email'] = username
                session['user_name'] = users[username]['name']
                flash('Вход выполнен успешно!', 'success')
                return redirect(url_for('index'))

            flash('Неверный email или пароль.', 'danger')
            return redirect(url_for('login'))

        return render_template('login.html')

    # === МАРШРУТ ДЛЯ ВЫХОДА ===
@app.route('/logout')
def logout():
        session.pop('user_email', None)
        session.pop('user_name', None)
        flash('Вы успешно вышли из системы.', 'info')
        return redirect(url_for('index'))

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=81)