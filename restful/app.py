from flask import Flask
from db import SQLite
from storage import Storage

app = Flask(__name__)
app.config.from_object('config.Development')
database = app.config['DATABASE']
database = eval(database)()


#  отображение всех пользователей
@app.route('/user', methods=['GET'])
def display_users():
    return database.get_users()


#  отображение определенного пользователя по id
@app.route("/user/<int:user_id>", methods=["GET"])
def display_user(user_id):
    return database.get_user(user_id)


#  добавление пользователя
@app.route('/user', methods=['POST'])
def creature_user():
    return database.post_user()


#  изменение определенного пользователя по id
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return database.put_user(user_id)


#  удаление определенного пользователя по id
@app.route('/user/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    return database.delete_user(user_id)


if __name__ == '__main__':
    app.run(debug=True)


# curl для проверки
# curl -i -H "Content-Type: application/json" -X POST -d "{\"user_name\":\"Jesse Pinkman\"}" http://localhost:5000/user
# curl -i -H "Content-Type: application/json" -X POST -d "{\"user_name\":\"John Doe\"}" http://localhost:5000/user
# curl -i -H "Content-Type: application/json" -X POST -d "{\"user_name\":\"Ivan Ivanovich Ivanov\"}" http://localhost:5000/user
# curl -i -H "Content-Type: application/json" -X POST -d "{\"user_name\":\"Alex Pro\"}" http://localhost:5000/user
# curl -i http://localhost:5000/user
# curl -i http://localhost:5000/user/3
# curl -i -H "Content-Type: application/json" -X PUT -d "{\"user_name\":\"Saul Goodman\"}" http://localhost:5000/user/3
# curl -X DELETE http://localhost:5000/user/2