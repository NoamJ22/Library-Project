from flask import Flask, request, jsonify, session
from flask_cors import CORS
from models import db
from models.Admin import Admin
from models.Game import Game

app = Flask(__name__)  # Create a Flask instance
app.secret_key = 'your_secret_key_here'  # Secret key for session handling

# Enable all routes, allow requests from anywhere (not recommended for production)
CORS(app, resources={r"/*": {"origins": "*"}})

# Specifies the database connection URL (SQLite in this case)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)  # Initialize the database with the Flask application


# Define the login route
@app.route('/login', methods=['POST'])
def login():
    data = request.json  # Get JSON data from the request
    username = data.get('username')
    password = data.get('password')

    # Check if both username and password are provided
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Find the admin by username
    admin = Admin.query.filter_by(username=username).first()

    if admin and admin.password == password:  # Verify the password (simple comparison for now)
        session['user_id'] = admin.id  # Store user ID in session
        session['username'] = admin.username  # Store username in session
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


# Route to register a new admin (for simplicity, this is assuming admin registration)
@app.route('/register', methods=['POST'])
def register():
    data = request.json  # Parse incoming JSON request data
    username = data.get('username')
    password = data.get('password')

    # Check if username and password are provided
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Check if the username already exists
    existing_admin = Admin.query.filter_by(username=username).first()
    if existing_admin:
        return jsonify({'error': 'Username already exists'}), 400

    # Create new admin user
    new_admin = Admin(username=username, password=password)
    db.session.add(new_admin)
    db.session.commit()

    # Log the user in automatically after registration
    session['user_id'] = new_admin.id
    session['username'] = new_admin.username

    return jsonify({'message': 'Registration successful, logged in automatically'}), 201


# Define a route for adding a game (requires login)
@app.route('/games', methods=['POST'])
def add_game():
    if 'user_id' not in session:  # Check if the user is logged in (session exists)
        return jsonify({'error': 'You must log in to perform this action'}), 403

    data = request.json  # Parse JSON data from the request body
    new_game = Game(
        title=data['title'],
        genre=data['genre'],
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(new_game)
    db.session.commit()
    return jsonify({'message': 'Game added to database.'}), 201


# Define a route to get all games (requires login)
@app.route('/games', methods=['GET'])
def get_games():
    if 'user_id' not in session:  # Check if the user is logged in (session exists)
        return jsonify({'error': 'You must log in to perform this action'}), 403

    try:
        games = Game.query.all()
        game_list = []

        for game in games:
            game_data = {
                'id': game.id,
                'title': game.title,
                'price': game.price,
                'quantity': game.quantity,
                'loan_status': game.loan_status
            }
            game_list.append(game_data)

        return jsonify({
            'message': 'Games retrieved successfully',
            'games': game_list
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve games', 'message': str(e)}), 500


# Route to log out (clear session)
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear the session to log the user out
    return jsonify({'message': 'Logged out successfully'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist already
    app.run(debug=True)
