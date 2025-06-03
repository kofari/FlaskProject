import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret-key')
    # Если у MySQL есть пароль, добавьте его после root:
    # 'mysql+mysqlconnector://root:ВАШ_ПАРОЛЬ@localhost/restaurant_booking'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost/restaurant_booking'
    SQLALCHEMY_TRACK_MODIFICATIONS = False