import requests
from bs4 import BeautifulSoup
import csv
import re
import os
import random

# URL for the Steam front page
url = "https://store.steampowered.com/"

# Send a request to the website and get the HTML content
response = requests.get(url)

# Function to clean the price (remove non-numeric characters)
def clean_price(price):
    # If the game is free, return 0
    if 'free' in price.lower():
        return 0
    # Keep only digits and periods (in case of decimal price)
    cleaned_price = re.sub(r'[^0-9.]', '', price)
    return int(float(cleaned_price)) if cleaned_price else 0

def remove_commas_from_tags(tag_list):
    # Join the list into a string, then replace commas
    tag_string = ' '.join(tag_list)
    return tag_string.replace(',', '')

# Function to scrape data and save it to CSV
def read_from_steam():
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all the game elements on the page
        games = soup.find_all('a', class_='tab_item')

        # Check if the file exists, if not, create it and write the header
        file_exists = os.path.isfile('games.csv')

        with open('games.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write the header only if the file does not exist (it's being created)
            if not file_exists:
                writer.writerow(['Game Name', 'Tags', 'Price', 'Quantity'])

            # Loop through each game element and extract the relevant information
            for game in games:
                # Get the name of the game
                game_name = game.find('div', class_='tab_item_name').text.strip() if game.find('div', class_='tab_item_name') else 'No name found'
                
                # Get the tags for the game
                tags = game.find_all('span', class_='top_tag')
                tag_list = [tag.text.strip() for tag in tags] if tags else ['No tags found']

                tag_list = remove_commas_from_tags(tag_list)
                
                # Get the price of the game
                price = game.find('div', class_='discount_final_price').text.strip() if game.find('div', class_='discount_final_price') else 'Price not found'
                clean_price_value = clean_price(price)

                # If there's no valid price, skip the game
                if clean_price_value == '':
                    continue

                # Replace commas with "and" in the tags
                tag_string = ''.join(tag_list)

                # Generate a random quantity
                quantity = random.randint(1, 1000)
                
                # Print out the details of each game if the script is being run directly
                print(f"Game Name: {game_name}")
                print(f"Tags: {tag_string}")
                print(f"Price: {clean_price_value}")
                print('-' * 40)

                # Write the game details to the CSV file
                writer.writerow([game_name, tag_string, clean_price_value, quantity])
                print("Game added to the CSV file")
    else:
        print(f"Failed to retrieve page, status code: {response.status_code}")

if __name__ == "__main__":
    print("Starting the scrape process...")
    read_from_steam()
    print(f"CSV file path: {os.path.abspath('games.csv')}")
