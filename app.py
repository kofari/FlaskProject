from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Booking
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')

from datetime import datetime, timedelta
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Генерация хеша с указанием метода
        password = generate_password_hash(
            request.form['password'],
            method='pbkdf2:sha256',
            salt_length=16
        )

        if User.query.filter_by(email=email).first():
            flash('Email уже зарегистрирован', 'danger')
            return redirect(url_for('register'))

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация успешна! Войдите в систему', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user:
            # Проверка пароля с отладочным выводом
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                print(f"Password check failed for user: {email}")
                print(f"Stored hash: {user.password}")
                print(f"Input password: {password}")

        flash('Неверный email или пароль', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


from datetime import datetime, timedelta  # Добавьте timedelta

# Добавьте список залов с изображениями
HALLS = [
    {"name": "Hampton by Hilton",
     "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
    {"name": "Ritz Carlton",
     "image": "https://i.pinimg.com/originals/44/25/32/442532e41baf740bf00067089df1f232.jpg"},
    {"name": "La Datcha",
     "image": "https://avatars.mds.yandex.net/i?id=4c6c4d58488cdd6f3cf5448137f24603_l-4566892-images-thumbs&n=13"},
    {"name": "Hilton London",
     "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"},
    {"name": "Liverpool",
     "image": "https://i.pinimg.com/736x/fa/4d/78/fa4d7887a1f41be1edc5367514b6bb55.jpg"}
]


@app.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    today = datetime.now().date()
    max_date = today + timedelta(days=90)

    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        time = datetime.strptime(request.form['time'], '%H:%M').time()
        guests = int(request.form['guests'])
        name = request.form['name']
        phone = request.form['phone']
        hall = request.form['hall']  # Новое поле: зал
        comments = request.form.get('comments', '')  # Новое поле: комментарии

        new_booking = Booking(
            user_id=current_user.id,
            date=date,
            time=time,
            guests=guests,
            name=name,
            phone=phone,
            hall=hall,  # Сохраняем зал
            comments=comments  # Сохраняем комментарии
        )

        db.session.add(new_booking)
        db.session.commit()

        flash('Бронирование успешно создано!', 'success')
        return redirect(url_for('index'))

    # Передаем список залов в шаблон
    return render_template('booking.html', halls=HALLS, today=today, max_date=max_date)
# Расширяем данные о залах для галереи
HALLS = [
    {
        "name": "Hampton by Hilton",
        "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        "description": "Элегантный зал в классическом стиле с панорамными окнами. Идеально подходит для свадеб и торжественных мероприятий.",
        "capacity": "до 100 гостей",
        "features": ["Сцена", "Дансинг", "Панорамные окна", "VIP-ложа"],
        "more_images": [
            "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
            "https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"
        ]
    },
    {
        "name": "Ritz Carlton",
        "image": "https://i.pinimg.com/originals/44/25/32/442532e41baf740bf00067089df1f232.jpg",
        "description": "Современный зал с уникальным дизайном и передовой технологией освещения. Прекрасное место для конференций и коктейльных вечеринок.",
        "capacity": "до 150 гостей",
        "features": ["3D-проекция", "Светодиодные стены", "Балкон", "Собственный бар"],
        "more_images": [
            "https://images.unsplash.com/photo-1513694203232-719a280e022f?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
            "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"
        ]
    },
{
        "name": "Hilton London",
        "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        "description": "Современный зал с уникальным дизайном и передовой технологией освещения. Прекрасное место для конференций и коктейльных вечеринок.",
        "capacity": "до 100 гостей",
        "features": ["3D-проекция", "Светодиодные стены", "Балкон", "Собственный бар"],
        "more_images": [
            "",
            ""
        ]
    },
{
        "name": "Liverpool",
        "image": "https://i.pinimg.com/736x/fa/4d/78/fa4d7887a1f41be1edc5367514b6bb55.jpg",
        "description": "Современный зал с уникальным дизайном и передовой технологией освещения. Прекрасное место для конференций и коктейльных вечеринок.",
        "capacity": "до 80 гостей",
        "features": ["3D-проекция", "Светодиодные стены", "Балкон", "Собственный бар"],
        "more_images": [
            "",
            ""
        ]
    },
    # ... аналогично для остальных залов ...
]

# Маршрут для галереи
@app.route('/gallery')
def gallery():
    return render_template('gallery.html', halls=HALLS)

# Маршрут для детальной страницы зала
@app.route('/hall/<hall_name>')
def hall(hall_name):
    # Найдем зал по имени
    hall_data = next((h for h in HALLS if h['name'] == hall_name), None)
    if not hall_data:
        flash('Зал не найден', 'danger')
        return redirect(url_for('gallery'))
    return render_template('hall.html', hall=hall_data)
@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('index'))

    bookings = Booking.query.all()
    return render_template('admin.html', bookings=bookings)


@app.route('/admin/delete/<int:id>')
@login_required
def delete_booking(id):
    if not current_user.is_admin:
        return redirect(url_for('index'))

    booking = Booking.query.get(id)
    if booking:
        db.session.delete(booking)
        db.session.commit()
        flash('Бронирование удалено', 'success')
    else:
        flash('Бронирование не найдено', 'danger')

    return redirect(url_for('admin'))


if __name__ == '__main__':
    with app.app_context():
        # Создаем таблицы, если они не существуют
        db.create_all()

        # Создаем администратора по умолчанию, если его нет
        if not User.query.filter_by(email='admin@example.com').first():
            admin_user = User(
                name='Admin',
                email='admin@example.com',
                password=generate_password_hash('adminpassword'),
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Создан администратор по умолчанию: admin@example.com / adminpassword")

    app.run(debug=True)


