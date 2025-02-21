#home_page_content flex_cols
#class of the tab which holds all the games

#under tab_item_content:

#name: tab_item_name
#tab_item_details:
    #genre: top_tag


#price = discount_final_price

#note to mention that these are all CLASS names

import requests
from bs4 import BeautifulSoup

# URL for the Steam front page
url = "https://store.steampowered.com/"

# Send a request to the website and get the HTML content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all the game elements on the page
    games = soup.find_all('a', class_='tab_item')

    # Loop through each game element and extract the relevant information
    for game in games:
        # Get the name of the game
        game_name = game.find('div', class_='tab_item_name').text.strip() if game.find('div', class_='tab_item_name') else 'No name found'
        
        # Get the tags for the game
        tags = game.find_all('span', class_='top_tag')
        tag_list = [tag.text.strip() for tag in tags] if tags else ['No tags found']
        
        # Get the price of the game
        price = game.find('div', class_='discount_final_price').text.strip() if game.find('div', class_='discount_final_price') else 'Price not found'
        
        # Print out the details of each game if the script is being run directly
        if __name__ == "__main__":
            print(f"Game Name: {game_name}")
            print(f"Tags: {', '.join(tag_list)}")
            print(f"Price: {price}")
            print('-' * 40)
else:
    print(f"Failed to retrieve page, status code: {response.status_code}")
