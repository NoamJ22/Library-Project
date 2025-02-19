# import csv
# import app
# from flask import Flask, request, jsonify
# from models import db
# from models.Game import Game

# # Route to add games from a CSV file
# @app.route('/add_games_from_csv', methods=['POST'])
# def add_games_from_csv():
#     try:
#         with open('games_data.csv', mode='r') as file:
#             csv_reader = csv.DictReader(file)
#             for row in csv_reader:
#                 new_game = Game(
#                     title=row['title'],  # From column 'title'
#                     genre=row['genre'],  # From column 'genre'
#                     price=int(row['price']),  # Convert to integer
#                     quantity=int(row['quantity']),  # Convert to integer
#                     loan_status=False  # Default loan status
#                 )
#                 db.session.add(new_game)
        
#         db.session.commit()

#         return jsonify({'message': 'Games added from CSV successfully!'}), 201
    
#     except Exception as e:
#         return jsonify({'error': 'Failed to add games from CSV', 'message': str(e)}), 500
