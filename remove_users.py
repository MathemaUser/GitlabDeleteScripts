import requests
import json
from dotenv import load_dotenv
import os
import datetime

"""
This script will delete all users from groups and projects, if they have the state blocked.
"""

# GitLab API URL and Token
GITLAB_API_URL = 'https://gitlab.example.com/api/v4'
PRIVATE_TOKEN = 'your_private_token'

def flat_list(list):
    return [x for xs in list for x in xs]

def get_all_projects():
    headers = {'PRIVATE-TOKEN': PRIVATE_TOKEN}
    more_pages = True
    page = 1
    projects = []

    while more_pages:
        response = requests.get(f"{GITLAB_API_URL}/projects?archived=false&per_page=100&page={page}", headers=headers)
        if response.status_code == 200:
            content = json.loads(response.content)
            # parse content
            if len(content) > 0:
                projects.append(content)
                page = page + 1
            else:
                more_pages = False

    project_list = flat_list(projects)
    return project_list

def get_all_groups():
    headers = {'PRIVATE-TOKEN': PRIVATE_TOKEN}
    more_pages = True
    page = 1
    groups = []

    while more_pages:
        response = requests.get(f"{GITLAB_API_URL}/groups?per_page=100&page={page}", headers=headers)
        if response.status_code == 200:
            content = json.loads(response.content)
            # parse content
            if len(content) > 0:
                groups.append(content)
                page = page + 1
            else:
                more_pages = False

    groups_list = flat_list(groups)
    return groups_list

# Get all Users from a project
def get_project_users(project_id):
    headers = {'PRIVATE-TOKEN': PRIVATE_TOKEN}
    users = []
    page = 1
    more_pages = True

    while more_pages:
        response = requests.get(f"{GITLAB_API_URL}/projects/{project_id}/members/all?page={page}&per_page=100", headers=headers)
        data = response.json()
        if len(data) > 0:
            users.extend(data)
            page += 1
        else:
            more_pages = False

    return users

# Get all members from a group
def get_group_members(group_id):
    headers = {'PRIVATE-TOKEN': PRIVATE_TOKEN}
    users = []
    page = 1
    more_pages = True

    while more_pages:
        response = requests.get(f"{GITLAB_API_URL}/groups/{group_id}/members/all?page={page}&per_page=100", headers=headers)
        data = response.json()
        if len(data) > 0:
            users.extend(data)
            page += 1
        else:
            more_pages = False

    return users

# Function to delete a user from a project
def remove_user_from_project(project_id, user_id):
    headers = {'PRIVATE-TOKEN': PRIVATE_TOKEN}
    response = requests.delete(f"{GITLAB_API_URL}/projects/{project_id}/members/{user_id}", headers=headers)
    return response.status_code

# Function to delete a member from a group
def remove_user_from_group(group_id, user_id):
    headers = {'PRIVATE-TOKEN': PRIVATE_TOKEN}
    response = requests.delete(f"{GITLAB_API_URL}/groups/{group_id}/members/{user_id}", headers=headers)
    return response.status_code

def remove_users_from_projects():
    projects = get_all_projects()
    filename = "projects.txt"
    with open(filename, "w") as file:
        for project in projects:
            file.write(f"{project['id']},{project['name']}\n")

    now = datetime.datetime.now()
    filename = "removed-users-from-projects" + now.strftime("%Y-%m-%d_%H-%M-%S.txt")
    with open(filename, "w"):
        pass

    for project in projects:
        project_id = project['id']
        project_users = get_project_users(project_id)

        for user in project_users:
            if user['state'] == 'blocked':
                status_code = remove_user_from_project(project_id, user['id'])
                if 200 <= status_code < 300:
                    print(f"User {user['name']} has been removed from the project {project['name']}, Id {project['id']}")
                    with open(filename, "a") as file:
                        file.write(f"{user['name']},{project['name']},{project['id']}\n")
                else:
                    print(f"Error when removing the user {user['name']} from the project {project['name']}, Id {project['id']}")

def remove_users_from_groups():
    groups = get_all_groups()
    filename = "groups.txt"
    with open(filename, "w") as file:
        for group in groups:
            file.write(f"{group['id']},{group['name']}\n")

    now = datetime.datetime.now()
    filename = "removed-users-from-groups-" + now.strftime("%Y-%m-%d_%H-%M-%S.txt")
    with open(filename, "w"):
        pass

    for group in groups:
        group_id = group['id']
        group_members = get_group_members(group_id)

        for user in group_members:
            if user['state'] == 'blocked':
                status_code = remove_user_from_group(group_id, user['id'])
                if 200 <= status_code < 300:
                    print(f"User {user['name']} has been removed from the group {group['name']}, Id {group['id']}")
                    with open(filename, "a") as file:
                        file.write(f"{user['name']},{group['name']},{group['id']}\n")
                else:
                    print(f"Error when removing user {user['name']} from the group {group['name']}, Id {group_id}")

if __name__ == "__main__":
    load_dotenv()
    GITLAB_API_URL = os.getenv('GITLAB_URL')
    PRIVATE_TOKEN = os.getenv('GITLAB_TOKEN')

    remove_users_from_groups()
    remove_users_from_projects()
