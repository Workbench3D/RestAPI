from flask import jsonify, request
import sqlite3


# создаю функцию чтобы работать с словарем а не кортежем
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# команды для создания или подключения базы данных
conn = sqlite3.connect('users.db', check_same_thread=False)
conn.row_factory = dict_factory
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   id INT PRIMARY KEY,
   user_name TEXT);
""")
conn.commit()


# класс рабатающий с базой данных
class SQLite:
    def get_users(self):
        cur.execute("SELECT * FROM users;")
        all_users = cur.fetchall()

        return jsonify(all_users)

    def get_user(self, user_id):
        cur.execute("SELECT * FROM users;")
        all_users = cur.fetchall()
        user = list(filter(lambda x: x['id'] == user_id, all_users))

        return jsonify(user[0])

    def post_user(self):
        cur.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1;")
        last_users = cur.fetchall()
        if not last_users:
            new_user = {
                'id': 1,
                'user_name': request.json['user_name']
            }
        else:
            new_user = {
                'id': last_users[-1]['id'] + 1,
                'user_name': request.json['user_name']
            }
        cur.execute("INSERT INTO users VALUES (:id, :user_name);", new_user)
        conn.commit()

        return jsonify('Create new user')

    def put_user(self, user_id):
        cur.execute("SELECT * FROM users;")
        all_users = cur.fetchall()
        update_user = list(filter(lambda x: x['id'] == user_id, all_users))
        update_user[0]['user_name'] = request.json.get(
            'user_name', update_user[0]['user_name'])
        user_name = update_user[0].get('user_name')
        cur.execute("UPDATE users SET user_name=? WHERE id=?;", (user_name, user_id))
        conn.commit()

        return jsonify('Update user' + ' ' + update_user[0].get('user_name'))

    def delete_user(self, user_id):
        cur.execute("DELETE FROM users WHERE id=?;", (user_id, ))
        conn.commit()

        return jsonify('Delete user')
