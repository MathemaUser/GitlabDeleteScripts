# GitlabDeleteScripts

## Description
These script are useful to cleanup Gitlab from users who left the company.
In the first step you need to identify the users, you want to block.
Blocking users means, that they can no longer login to their account and you cannot access their profiles.

## Prerequesites
You need an Admin Token for Gitlab to retrieve all nescessary information and perform all required actions.
Fill your URL and token into the ```.env``` file.

Python 3.12.7 was used at time of development.
run ```pip install -r requirements.txt``` to install the required packages.

## Instructions
### Get all users
To mark the users you want to delete, run the script ```get_all_users.py```
 to get a list of all gitlab users in a csv file (gitlab_users.csv). Then fill the column ```to_block``` with a 1 if you want to block the user.

### Block all marked users
 In the second step run ```block_user.py``` to block all marked users in the csv file.
 This will block all marked users.

### Remove blocked users
 In the third step run ```remove_users.py```. this will remove all blocked users from all groups and all projects.

 Every successfull deletion will be logged in a log file, except when an error occurs, then you should investigate, why a deletion was not possible. In any case consult the Gitlab documentation.

### !!Attention!!
 Please read the code before running the script, to make sure it behaves as you expect and need it.

 No warranty for success, be carefull before deleting anything and make sure to have backups in place before running the scripts.
