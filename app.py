from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


# создание класса пользователь
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, user_name):
        self.user_name = user_name


# создание схемы серилизации и десериализации данных
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_name')


user_schema = UserSchema()


# проверка на существование файла БД, и создание
file_path = os.path.isfile("user.db")
if not file_path:
    db.create_all()


#  отображение всех пользователей
@app.route('/user', methods=['GET'])
def get_user():
    all_users = User.query.all()
    user_schema = UserSchema(many=True)
    user = user_schema.dump(all_users)

    return jsonify(user)


#  отображение определенного пользователя по id
@app.route("/user/<user_id>", methods=["GET"])
def user_detail(user_id):
    user = User.query.get(user_id)

    return user_schema.jsonify(user)


#  добавление пользователя
@app.route('/user', methods=['POST'])
def post_user():
    user_name = request.json['user_name']
    new_user = User(user_name)

    db.session.add(new_user)

    db.session.commit()
    return user_schema.jsonify(new_user)


#  изменение определенного пользователя по id
@app.route('/user/<user_id>', methods=['PUT'])
def user_update(user_id):
    user = User.query.get(user_id)
    user_name = request.json['user_name']
    user.user_name = user_name

    db.session.commit()
    return user_schema.jsonify(user)


#  удаление определенного пользователя по id
@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    db.session.delete(user)

    db.session.commit()
    return user_schema.jsonify(user)


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
