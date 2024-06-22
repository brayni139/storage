from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort
import firebase_admin
from firebase_admin import credentials, db

# Инициализация Flask приложения и API
app = Flask(__name__)
api = Api(app)

# Инициализация Firebase Admin SDK
cred = credentials.Certificate('/opt/render/project/src/reygame-af213-firebase-adminsdk-5dlkj-a2d1fe06e4.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://reygame-af213-default-rtdb.europe-west1.firebasedatabase.app'  # Замените на URL вашей базы данных Firebase
})

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
        player_id = players.push(data)
        return jsonify({'id': player_id.key}), 201


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
        player = players.child(player_id)
        if player.get():
            player.update(data)
            return jsonify(data)
        abort(404, message=f"Player with id {player_id} not found")

    def delete(self, player_id):
        # Удаление игрока по ID
        player = players.child(player_id)
        if player.get():
            player.delete()
            return '', 204
        abort(404, message=f"Player with id {player_id} not found")


# Регистрация ресурсов API
api.add_resource(PlayerList, '/players')
api.add_resource(Player, '/players/<string:player_id>')


# Запуск сервера Flask
if __name__ == '__main__':
    app.run(debug=True)
