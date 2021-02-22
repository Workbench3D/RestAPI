from flask import jsonify, request

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


# класс работающий с словарем
class Storage:
    def get_users(self):
        return jsonify(users)

    def get_user(self, user_id):
        user = list(filter(lambda x: x['id'] == user_id, users))

        return jsonify(user[0])

    def post_user(self):
        new_user = {
            'id': users[-1]['id'] + 1,
            'user_name': request.json['user_name']
        }
        users.append(new_user)

        return jsonify('Create new user')

    def put_user(self, user_id):
        update_user = list(filter(lambda x: x['id'] == user_id, users))
        update_user[0]['user_name'] = request.json.get(
            'user_name', update_user[0]['user_name'])

        return jsonify('Update user' + ' ' + update_user[0].get('user_name'))

    def delete_user(self, user_id):
        del_user = list(filter(lambda x: x['id'] == user_id, users))
        users.remove(del_user[0])

        return jsonify('Delete user' + ' ' + del_user[0].get('user_name'))
