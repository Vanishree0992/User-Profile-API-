from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.exceptions import NotFound

app = Flask(__name__)
api = Api(app)

# In-memory user storage
users = []
user_id_counter = 1

class UserList(Resource):
    def get(self):
        return {'users': users}, 200

    def post(self):
        global user_id_counter
        data = request.get_json()
        if not data or 'name' not in data or 'email' not in data:
            return {'message': 'Name and Email are required.'}, 400

        new_user = {
            'id': user_id_counter,
            'name': data['name'],
            'email': data['email']
        }
        users.append(new_user)
        user_id_counter += 1
        return new_user, 201

class User(Resource):
    def get(self, id):
        user = next((u for u in users if u['id'] == id), None)
        if not user:
            raise NotFound('User not found')
        return user, 200

    def put(self, id):
        data = request.get_json()
        user = next((u for u in users if u['id'] == id), None)
        if not user:
            raise NotFound('User not found')

        user['name'] = data.get('name', user['name'])
        user['email'] = data.get('email', user['email'])
        return user, 200

    def delete(self, id):
        global users
        user = next((u for u in users if u['id'] == id), None)
        if not user:
            raise NotFound('User not found')

        users = [u for u in users if u['id'] != id]
        return {'message': f'User with id {id} deleted'}, 200

# Routes
api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
