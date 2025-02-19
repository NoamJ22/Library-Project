from flask import Flask, request, jsonify, session
import csv
from flask_cors import CORS
from models import db
from models.Admin import Admin
from models.Game import Game
from models.Customer import Customer
from werkzeug.security import generate_password_hash

app = Flask(__name__)  # Create a Flask instance
app.secret_key = 'your_secret_key_here'  # Secret key for session handling

# Enable all routes, allow requests from anywhere (not recommended for production)
CORS(app, resources={r"/*": {"origins": "*"}})
#CORS(app)

# Specifies the database connection URL (SQLite in this case)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Game.db'
db.init_app(app)  # Initialize the database with the Flask application


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    print(f"Received data: {data}")  # Log the incoming data

    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    admin = Admin.query.filter_by(username=username).first()
    if admin:
        print(f"Found admin: {admin.username}")
    else:
        print("Admin not found")

    if admin and admin.password == password:
        session['user_id'] = admin.id
        session['username'] = admin.username
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


def add_games_from_csv():
    try:
        with open(r'C:\Users\noame\Desktop\pypro\Library-Project\backend\game_data.csv', mode='r') as file:
            # Manually define the headers, because there is no header in the CSV file
            column_headers = ['title', 'genre', 'price', 'quantity']
            csv_reader = csv.reader(file)  # Use csv.reader instead of DictReader
            
            games_added = 0
            for row in csv_reader:
                if len(row) == 4:  # Ensure there are exactly 4 values in the row
                    # Create a dictionary to map each value to the correct header
                    game_data = dict(zip(column_headers, row))
                    print(f"Reading row: {game_data}")  # Debug log

                    new_game = Game(
                        title=game_data['title'],
                        genre=game_data['genre'],
                        price=int(game_data['price']),  # Convert to integer
                        quantity=int(game_data['quantity']),  # Convert to integer
                        loan_status=False  # Default loan status
                    )
                    db.session.add(new_game)
                    games_added += 1

            db.session.commit()

        return jsonify({'message': f'{games_added} games added from CSV successfully!'}), 201

    except Exception as e:
        db.session.rollback()  # Rollback any changes if there is an error
        print(f"Error occurred: {str(e)}")  # Log the error to console
        return jsonify({'error': 'Failed to add games from CSV', 'message': str(e)}), 500


# Route to get all games (requires login)
@app.route('/games', methods=['GET'])
def get_games():
    # if 'user_id' not in session:  # Check if the user is logged in (session exists)
    #     return jsonify({'error': 'You must log in to perform this action'}), 403

    try:
        games =  Game.query.filter_by(loan_status=False).all()
        game_list = []

        for game in games:
            game_data = {
                'id': game.id,
                'title': game.title,
                'genre':game.genre,
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
    

# this is a decorator from the flask module to define a route for for adding a book, supporting POST requests.(check the decorator summary i sent you and also the exercises)
@app.route('/add', methods=['POST'])
def add_game():
    data = request.json  # this is parsing the JSON data from the request body
    new_game = Game(
        title=data['title'],  # Set the title of the new book.
        genre=data['genre'],  # Set the author of the new book.
        price=data['price'],
        # Set the types(fantasy, thriller, etc...) of the new book.
        quantity=data['quantity'],
        loan_status= False
    )
    db.session.add(new_game)  # add the bew book to the database session
    db.session.commit()  # commit the session to save in the database
    return jsonify({'message': 'Book added to database.'}), 201


@app.route('/delete', methods=['POST'])
def delete_game():
    data = request.json
    title = data['title']
    
    # Query the database for the game with the given title
    game = Game.query.filter_by(title=title).first()  # Use filter_by for simpler equality queries
    if game.loan_status == True:
        return jsonify({"message": "Cannot delete a loaned game"}), 201

    if game:
        # If the game is found, delete it
        db.session.delete(game)
        db.session.commit()
        return jsonify({"message": "Game deleted successfully!"}), 200
    else:
        return jsonify({"message": "Game not found!"}), 404



# Route to get all games (requires login)
@app.route('/loaned', methods=['GET'])
def get_loaned_games():
    # if 'user_id' not in session:  # Check if the user is logged in (session exists)
    #     return jsonify({'error': 'You must log in to perform this action'}), 403

    try:
        loaned_games = Game.query.filter_by(loan_status=True).all()
        game_list = []

        for game in loaned_games:
            game_data = {
                'id': game.id,
                'title': game.title,
                'genre':game.genre,
                'price': game.price,
                'quantity': game.quantity,
                'loan_status': game.loan_status
            }
            game_list.append(game_data)

        return jsonify({
            'message': 'loaned Games retrieved successfully',
            'games': game_list
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve loaned games', 'message': str(e)}), 500

# Route to log out (clear session)
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()  # Clear the session to log the user out
    return jsonify({'message': 'Logged out successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all database tables defined in your models

        # Call the add_games_from_csv() function to load the games from the CSV
        add_games_from_csv()  # This will add games from the CSV to the database
    
    app.run(debug=True, port=5000)  # Start the Flask application in debug mode
