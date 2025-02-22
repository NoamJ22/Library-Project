import csv
import os

try:
    file_path = os.path.abspath('game_data.csv')
    print(f"Writing to file: {file_path}")

    with open('game_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ababababab"])
        writer.writerow(list("ababababab"))
    print("Data written successfully")
except Exception as e:
    print(f"Error occurred: {e}")