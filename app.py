from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the Flask Threat Detection App!'

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == 'admin' and password == 'password':
        app.logger.info(f"Successful login attempt: {username}")
        return jsonify({"message": "Login successful"}), 200
    else:
        app.logger.warning(f"Failed login attempt: {username}")
        return jsonify({"message": "Login failed"}), 401

if __name__ == '__main__':
    app.run(debug=True)
