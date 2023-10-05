from flask import Flask, request, session, jsonify
from flask import Api, Resource

app = Flask(__name__)
app.secret_key = b'secret_key' 
api = Api(app)


users = [
    {'id': 1, 'username': 'user1', 'password': 'password1'},
    {'id': 2, 'username': 'user2', 'password': 'password2'},
]

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')

        user = next((user for user in users if user['username'] == username), None)

        if user:
            session['user_id'] = user['id']
            return jsonify(user), 200
        else:
            return {'message': 'User not found'}, 404

class LogoutResource(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

class CheckSessionResource(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = next((user for user in users if user['id'] == user_id), None)
            if user:
                return jsonify(user), 200
        return {}, 401


api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(CheckSessionResource, '/check_session')

if __name__ == '__main__':
    app.run(debug=True)
