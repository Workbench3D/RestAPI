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


# создаем класс баз данных
class SQLite:
    def get_users(self):
        all_users = User.query.all()
        user_schema = UserSchema(many=True)
        user = user_schema.dump(all_users)

        return jsonify(user)

    def get_user(self, user_id):
        user = User.query.get(user_id)

        return user_schema.jsonify(user)

    def post_user(self):
        user_name = request.json['user_name']
        new_user = User(user_name)

        db.session.add(new_user)

        db.session.commit()
        return user_schema.jsonify(new_user)

    def put_user(self, user_id):
        user = User.query.get(user_id)
        user_name = request.json['user_name']
        user.user_name = user_name

        db.session.commit()
        return user_schema.jsonify(user)

    def delete_user(self, user_id):
        user = User.query.get(user_id)

        db.session.delete(user)

        db.session.commit()
        return user_schema.jsonify(user)
