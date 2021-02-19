from flask import Flask
from db import SQLite
from storage import Storage

app = Flask(__name__)
conf = Storage()


#  отображение всех пользователей
@app.route('/user', methods=['GET'])
def display_users():
    return conf.get_users()


#  отображение определенного пользователя по id
@app.route("/user/<int:user_id>", methods=["GET"])
def display_user(user_id):
    return conf.get_user(user_id)


#  добавление пользователя
@app.route('/user', methods=['POST'])
def creature_user():
    return conf.post_user()


#  изменение определенного пользователя по id
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return conf.put_user(user_id)


#  удаление определенного пользователя по id
@app.route('/user/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    return conf.delete_user(user_id)


if __name__ == '__main__':
    app.run(debug=True)