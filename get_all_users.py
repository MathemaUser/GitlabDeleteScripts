import requests
from dotenv import load_dotenv
import os
import csv

"""
This file gets all users from Gitlab and creates a processable csv file to use it in other script. An admin token is required.
"""

# GitLab API URL and Token
GITLAB_API_URL = 'https://gitlab.example.com/api/v4'
PRIVATE_TOKEN = 'your_private_token'

# return all gitlab users in an array to process them
def get_all_users():
    users = []
    page = 1
    per_page = 100  # Number of users per page

    while True:
        url = f"{GITLAB_API_URL}/users?page={page}&per_page={per_page}&without_project_bots=true&exclude_external=true&blocked=false&access_token={PRIVATE_TOKEN}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if not data:
                break
            users.extend(data)
            page += 1
        else:
            print(f"Error requesting users: {response.status_code}")
            break

    return users


def main():
    users = get_all_users()

    with open('gitlab_users.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'username', 'email', 'external', 'blocked', 'to_block']) # the to_block column must be filled manually with 1, to mark the users you want to block
        # example rows for users to block and not to block
        # id,username,email,external,blocked,toblock
        # 1,user1,user1@example.de,0,0,1    -> block user
        # 2,user2,user2@example.de,0,0      -> do not block user
        # 3,user3,user3@example.de,0,0,0    -> do not block user
        for user in users:
            if "bot" in user['username']:                                       # exclude bots
                writer.writerow([user['id'], user['username'], "none", 0, 0])
                continue
            if "email" in user:
                email = user['email']
            else:
                email = "none"
            state = user['state']
            is_blocked = '1' if state == 'blocked' else '0'
            if "external" in user:
                is_external = '1' if user['external'] else '0'
            else:
                is_external = 1

            # write all users into the csv file
            writer.writerow([user['id'], user['username'], email, is_external, is_blocked])

            print(f"id: {user['id']}, username: {user['username']}, email: {email}, external: {is_external}, blocked: {is_blocked}")


if __name__ == "__main__":
    load_dotenv()
    GITLAB_API_URL = os.getenv('GITLAB_URL')
    PRIVATE_TOKEN = os.getenv('GITLAB_TOKEN')
    main()