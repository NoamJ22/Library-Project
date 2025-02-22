# Import statements
from models.Game import Game
from models import db
from models.Admin import Admin
from selenium import webdriver  # Main Se
import csv
from flask import Flask, request, jsonify, session

# lenium package for browser automation
# Manages ChromeDriver service
from selenium.webdriver.chrome.service import Service

# Chrome-specific configuration options
from selenium.webdriver.chrome.options import Options

# Provides locator strategies (ID, CLASS, etc.)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # Implements explicit waits

# Conditions for WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time  # For adding delays between actions

# Create the Flask app instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Game.db'
db.init_app(app)

with app.app_context():
    db.create_all()



# Function to set up the Chrome WebDriver
def setup_driver():
    chrome_options = Options()  # Create a new Options object for Chrome
    service = Service()  # Create a new Service object to manage ChromeDriver
    chrome_options.add_experimental_option('detach', True)  # Add this option to keep browser open after script finishes
    # Initialize Chrome with our settings
    return webdriver.Chrome(service=service, options=chrome_options)


def interact_with_form():
    driver = setup_driver()

    try:
        print("Opening website...")
        driver.get("http://127.0.0.1:5500/Library-Project/frontend/index.html")
        time.sleep(3)

        wait = WebDriverWait(driver, 3)

        # Wait and interact with the username field
        print("Waiting for the username field...")
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys("roei")
        print("Username entered.")
        time.sleep(1)

        # Wait and interact with the password field
        print("Waiting for the password field...")
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys("1234")
        print("Password entered.")
        time.sleep(1)

        # Wait for the login button to become clickable and click it
        print("Waiting for the login submit button...")
        log_submit = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "auth-action")))
        log_submit.click()
        print("Login button clicked.")
        time.sleep(2)  # Add a brief wait after clicking the login button to ensure the next page is loaded

        # log_submit.click()
        # print("Login button clicked.")
        # time.sleep(2)

        # Process CSV and add games
        with app.app_context():
            print("Opening CSV file and processing games...")
            with open(r'C:\Users\noame\Desktop\pypro\games.csv', mode='r') as file:
                column_headers = ['title', 'genre', 'price', 'quantity']
                csv_reader = csv.reader(file)  # Use csv.reader instead of DictReader
                print("column headers")
                
                games_added = 0
                games_skipped = 0  # To count how many games are skipped because they already exist
                for row in csv_reader:
                    print("starting loop")
                    if len(row) == 4:  # Ensure there are exactly 4 values in the row
                        game_data = dict(zip(column_headers, row))
                        print(f"Reading row: {game_data}")  # Debug log

                        # Check if a game with this title already exists in the database
                        existing_game = Game.query.filter_by(title=game_data['title']).first()

                        if existing_game:
                            print(f"Game '{game_data['title']}' already exists, skipping.")
                            games_skipped += 1
                        else:
                            # If the game doesn't exist, add it to the database
                            new_game = Game(
                                title=game_data['title'],
                                genre=game_data['genre'],
                                price=int(game_data['price']),
                                quantity=int(game_data['quantity']),
                                loan_status=False  # Default loan status
                            )
                            print(f"Adding game: {new_game.title}")

                            # Wait for the game title input field and send data
                            print("Waiting for game title field...")
                            title_field = wait.until(EC.presence_of_element_located((By.ID, "game-title")))
                            title_field.send_keys(new_game.title)
                            print(f"Entered game title: {new_game.title}")
                            time.sleep(1)

                            # Wait for the game genre input field and send data
                            print("Waiting for game genre field...")
                            genre_field = wait.until(EC.presence_of_element_located((By.ID, "game-genre")))
                            genre_field.send_keys(new_game.genre)
                            print(f"Entered game genre: {new_game.genre}")
                            time.sleep(1)

                            # Wait for the game price input field and send data
                            print("Waiting for game price field...")
                            price_field = wait.until(EC.presence_of_element_located((By.ID, "game-price")))
                            price_field.send_keys(new_game.price)
                            print(f"Entered game price: {new_game.price}")
                            

                            # Wait for the game quantity input field and send data
                            print("Waiting for game quantity field...")
                            quantity_field = wait.until(EC.presence_of_element_located((By.ID, "game-quantity")))
                            quantity_field.send_keys(new_game.quantity)
                            print(f"Entered game quantity: {new_game.quantity}")
                            time.sleep(1)

                            # Wait for the submit button and click it to add the game
                            print("Waiting for submit button to add game...")
                            # Locate the "Add Game" button using XPath
                            game_submit = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Add Game"]')))
                            game_submit.click()
                            print(f"Game '{new_game.title}' added.")
                            time.sleep(1)

                            games_added += 1

                print(f"Finished processing CSV: {games_added} games added, {games_skipped} games skipped.")

                return jsonify({
                'message': f'{games_added} games added from CSV successfully, {games_skipped} games were skipped (already exist in the database).'
                }), 201

    except Exception as e:
        print(f"An error occurred: {str(e)}")  # Print any errors that occur
        return jsonify({'error': str(e)}), 500

    finally:
        # Close the browser to clean up
        if driver:
            print("Closing the browser...")
            driver.quit()


# Script entry point
if __name__ == "__main__":
    interact_with_form()  # Start the form interaction process
