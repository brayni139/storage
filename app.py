import logging
from flask import Flask
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Настройка уровня логирования Flask
app.logger.setLevel(logging.DEBUG)

# Инициализация Firebase Admin SDK с логированием
cred = credentials.Certificate('/opt/render/project/src/reygame-af213-firebase-adminsdk-5dlkj-a2d1fe06e4.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://reygame-af213-default-rtdb.europe-west1.firebasedatabase.app'
})

# Получение объекта логгера Firebase
firebase_logger = logging.getLogger('firebase_admin')
firebase_logger.setLevel(logging.DEBUG)

@app.route('/')
def index():
    app.logger.info('Это информационное сообщение')
    app.logger.warning('Это предупреждение')

    # Пример использования Firebase SDK с логированием
    try:
        ref = db.reference('/')
        snapshot = ref.get()
        app.logger.debug(f'Получено значение: {snapshot}')
    except Exception as e:
        app.logger.error(f'Ошибка при получении данных из Firebase: {e}')

    return 'Пример логирования'

if __name__ == '__main__':
    app.run(debug=True)
