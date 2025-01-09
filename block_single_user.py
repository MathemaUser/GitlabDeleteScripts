import requests
from dotenv import load_dotenv
import os
import datetime
import sys

"""
This script should block a single user, for example if he or she leaves the company.
An admin token is required.
"""

# GitLab API URL and Token
GITLAB_API_URL = 'https://gitlab.example.com/api/v4'
PRIVATE_TOKEN = 'your_private_token'

def get_user_by_name(username):
    headers = {'PRIVATE-TOKEN': PRIVATE_TOKEN}
    response = requests.get(f"{GITLAB_API_URL}/users?username={username}", headers=headers)
    if response.status_code == 200:
        users = response.json()
        if users:
            return users[0]  # Assuming the first result is the correct user
        else:
            print(f'User {username} not found.')
            return None
    else:
        print(f'Error: {response.status_code}')
        return None

# Function to block a user in Gitlab
def block_user(user_id):
    headers = {'PRIVATE-TOKEN': PRIVATE_TOKEN}
    response = requests.post(f"{GITLAB_API_URL}/users/{user_id}/block", headers=headers)
    print(f"Block user {user_id}")
    return response.status_code

# Main function to block users, which are marked to_block in the csv file
def block_users_by_username(username):
    now = datetime.datetime.now()
    filename = f"Block-user {username}-" + now.strftime("%Y-%m-%d_%H-%M-%S.txt")
    with open(filename, "w") as file:
        user = get_user_by_name(username)
        if user is not None:
            file.write(f"Blocking user {user['name']} with id {user['id']}\n")
            status_code = block_user(user['id'])

            if 200 <= status_code < 300:
                print(f"User {user['email']} has been blocked.")
                file.write(f"{user['email']} has been blocked\n")
            else:
                print(f"User {user['email']} could not be blocked, status code {status_code}")
                file.write(f"{user['email']} could not be blocked, status code {status_code}\n")
        else:
            print("An error occurred")
            file.write(f"{username} not found\n")
            return

if __name__ == "__main__":
    sys.argv.append('test3')
    if len(sys.argv) > 1:
        load_dotenv()
        GITLAB_API_URL = os.getenv('GITLAB_URL')
        PRIVATE_TOKEN = os.getenv('GITLAB_TOKEN')
        csv_file = 'gitlab_users.csv'

        block_users_by_username(sys.argv[1])
    else:
        print("Please provide a username which should be blocked and removed from projects an groups in Gitlab.")

