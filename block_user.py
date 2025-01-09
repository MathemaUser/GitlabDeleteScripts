import requests
from dotenv import load_dotenv
import os
import datetime
import csv

"""
This script should block all users which are marked to_block in the previously created file in the get_all_users.py file.
An admin token is required.
"""

# GitLab API URL and Token
GITLAB_API_URL = 'https://gitlab.example.com/api/v4'
PRIVATE_TOKEN = 'your_private_token'

def read_user_from_file(file_path):
    filtered_rows = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'to_block' in row and row['to_block'] == '1':
                filtered_rows.append(row)
    return filtered_rows

# Function to block a user in Gitlab
def block_user(user_id):
    headers = {'PRIVATE-TOKEN': PRIVATE_TOKEN}
    response = requests.post(f"{GITLAB_API_URL}/users/{user_id}/block", headers=headers)
    print(f"Block user {user_id}")
    return response.status_code

# Main function to block users, which are marked to_block in the csv file
def block_users_by_file(csv_file):
    email_list = read_user_from_file(csv_file)

    now = datetime.datetime.now()
    filename = now.strftime("%Y-%m-%d_%H-%M-%S.txt")
    with open(filename, "w"):
        pass

    for user in email_list:
        if user['email'] not in email_list:
            status_code = block_user(user['id'])
            if 200 <= status_code < 300:
                print(f"User {user['email']} has been blocked.")
                with open(filename, "a") as file:
                    file.write(f"{user['email']}\n")
            else:
                print(f"Error when blocking user {user['email']}.")


if __name__ == "__main__":
    load_dotenv()
    GITLAB_API_URL = os.getenv('GITLAB_URL')
    PRIVATE_TOKEN = os.getenv('GITLAB_TOKEN')
    csv_file = 'gitlab_users.csv'

    block_users_by_file(csv_file)