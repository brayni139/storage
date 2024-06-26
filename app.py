from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort
import firebase_admin
from firebase_admin import credentials, db
import logging

# Инициализация Flask приложения и API
app = Flask(__name__)
api = Api(app)

# Инициализация Firebase Admin SDK и логирование
cred = credentials.Certificate('/opt/render/project/src/reygame-af213-firebase-adminsdk-5dlkj-a2d1fe06e4.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://reygame-af213-default-rtdb.europe-west1.firebasedatabase.app'  # Замените на URL вашей базы данных Firebase
})
logging.basicConfig(level=logging.DEBUG)  # Устанавливаем уровень логирования

# Пример данных для базы Firebase
players = db.reference('players')

# Определение запросов, как описано в Swagger файле

class PlayerList(Resource):
    def get(self):
        # Получение списка всех игроков
        all_players = players.get()
        return jsonify(all_players)

    def post(self):
        # Создание нового игрока
        data = request.json
        logging.debug(f"Received POST request with data: {data}")  # Логируем данные запроса
        try:
            player_id = players.push(data)
            return jsonify({'id': player_id.key}), 201
        except Exception as e:
            logging.error(f"Failed to create player: {e}")
            return {'message': str(e)}, 500


class Player(Resource):
    def get(self, player_id):
        # Получение игрока по ID
        player = players.child(player_id).get()
        if player:
            return jsonify(player)
        abort(404, message=f"Player with id {player_id} not found")

    def put(self, player_id):
        # Обновление данных игрока по ID
        data = request.json
        logging.debug(f"Received PUT request for player ID {player_id} with data: {data}")  # Логируем данные запроса
        try:
            player = players.child(player_id)
            if player.get():
                player.update(data)
                return jsonify(data)
            abort(404, message=f"Player with id {player_id} not found")
        except Exception as e:
            logging.error(f"Failed to update player ID {player_id}: {e}")
            return {'message': str(e)}, 500

    def delete(self, player_id):
        # Удаление игрока по ID
        logging.debug(f"Received DELETE request for player ID {player_id}")  # Логируем данные запроса
        try:
            player = players.child(player_id)
            if player.get():
                player.delete()
                return '', 204
            abort(404, message=f"Player with id {player_id} not found")
        except Exception as e:
            logging.error(f"Failed to delete player ID {player_id}: {e}")
            return {'message': str(e)}, 500


# Регистрация ресурсов API
api.add_resource(PlayerList, '/players')
api.add_resource(Player, '/players/<string:player_id>')


# Запуск сервера Flask
if __name__ == '__main__':
    app.run(debug=True)
