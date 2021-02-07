from flask import Flask, jsonify, request


app = Flask(__name__)

# стартовый список с вложенными словарями
users = [
    {
        'id': 1,
        'user_name': 'John Doe',
    },
    {
        'id': 2,
        'user_name': 'Ivan Ivanovich Ivanov',
    },
    {
        "id": 3,
        "user_name": "Alex Pro"
    }
]


#  отображение всех пользователей
@app.route('/user', methods=['GET'])
def get_user():
    return jsonify(users)


#  отображение определенного пользователя по id
@app.route('/user/<int:user_id>', methods=['GET'])
def get_task(user_id):
    user = list(filter(lambda t: t['id'] == user_id, users))

    return jsonify(user[0])


#  добавление пользователя
@app.route('/user', methods=['POST'])
def post_user():
    new_user = {
        'id': users[-1]['id'] + 1,
        'user_name': request.json['user_name']
    }
    users.append(new_user)

    return jsonify(users)


#  изменение определенного пользователя по id
@app.route('/user/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    update_user = list(filter(lambda x: x['id'] == user_id, users))
    update_user[0]['user_name'] = request.json.get(
        'user_name', update_user[0]['user_name'])

    return jsonify({'user_name': update_user[0]})


#  удаление определенного пользователя по id
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    del_user = list(filter(lambda x: x['id'] == user_id, users))
    users.remove(del_user[0])

    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)

# curl для проверки
# curl -i -H "Content-Type: application/json" -X POST -d "{\"user_name\":\"Jesse Pinkman\"}" http://localhost:5000/user
# curl -i http://localhost:5000/user
# curl -i http://localhost:5000/user/3
# curl -i -H "Content-Type: application/json" -X PUT -d "{\"user_name\":\"Saul Goodman\"}" http://localhost:5000/user/3
# curl -X DELETE http://localhost:5000/user/2
