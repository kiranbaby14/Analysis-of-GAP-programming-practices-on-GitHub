import requests

import csv
import time
import sys
from datetime import datetime
from github import Github
from urllib.parse import urlparse
# append the path of the
# parent directory
sys.path.append("..")
from utils.config import get_access_token
from utils.constants import COUNTRIES_NAMES_SHORTCUTS
import re


repository_set = set()

def get_user_location(username, access_token):
    url = f'https://api.github.com/users/{username}'
    headers = {'Authorization': f'token {access_token}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_details = response.json()
        user_location = user_details.get('location', None)
        
        if user_location:
            # Clean the user_location by removing leading and trailing whitespace
            user_location = user_location.strip()

            # Check if the user_location matches a valid country name (key) or a valid country shortcut (value)
            for country_name, country_shortcut in COUNTRIES_NAMES_SHORTCUTS.items():
                if user_location.upper() == country_name.upper() or user_location.upper() == country_shortcut.upper():
                    return country_name

            # Check if the user_location appears as a whole word (not as part of other words)
            for country_name, country_shortcut in COUNTRIES_NAMES_SHORTCUTS.items():
                pattern = re.escape(country_name) + r"\s*,?\s*$|" + re.escape(country_shortcut) + r"\s*,?\s*$"
                if re.search(pattern, user_location, re.IGNORECASE):
                    return country_name
        
        return None

    return None

def get_repository_details(repo_full_name, access_token):
    url = f'https://api.github.com/repos/{repo_full_name}'
    headers = {'Authorization': f'token {access_token}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repo_details = response.json()
        repo_created_at = repo_details['created_at']
        repo_owner = repo_details['owner']['login']

        # Get the number of contributors and their locations
        contributors_url = f'https://api.github.com/repos/{repo_full_name}/contributors'
        contributors_response = requests.get(contributors_url, headers=headers)
        if contributors_response.status_code == 200:
            contributors = contributors_response.json()
            num_contributors = len(contributors)
            contributors_data = [{'User': contributor['login'], 'Location': get_user_location(contributor['login'], access_token)} for contributor in contributors]
        else:
            num_contributors = 0
            contributors_data = []

        # Get commit details
        commits_url = f'https://api.github.com/repos/{repo_full_name}/commits'
        commits_response = requests.get(commits_url, headers=headers)
        if commits_response.status_code == 200:
            commits_data = commits_response.json()
            commits_per_month = {}
            for commit in commits_data:
                date = commit['commit']['committer']['date'][:7]  # Extract year and month (YYYY-MM)
                commits_per_month[date] = commits_per_month.get(date, 0) + 1

            commits_info = [{'Month': date, 'Repository': repo_full_name, 'Owner': repo_owner, 'Commits Per Month': count}
                            for date, count in commits_per_month.items()]
        else:
            commits_info = []

        return repo_created_at, num_contributors, repo_owner, contributors_data, commits_info


    return None, None, None, [], []

def main():
    
    # Get the GitHub access token
    access_token = get_access_token()
    

    # List to store repository details
    repository_details = []
    user_details = []
    # List to store commit details
    commits_details = []
    
    
    
    # Read the URLs from the input CSV file
    with open('../data/real_GAP_files1.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            url = row['URL']  
            
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.split('/')
            owner = path_parts[1]
            repository_name = path_parts[2]
            repository_path = owner+'/'+repository_name
            
            if repository_path not in repository_set:
                repository_set.add(repository_path)  
                print("Extracting data from ",repository_path)

            
                repo_created_at, num_contributors, repo_owner, contributors_data, commits_info = get_repository_details(repository_path, access_token)
                if repo_created_at:
                    owner_location = get_user_location(repo_owner, access_token)
                    repository_details.append({
                        'Repository': repository_path,
                        'Created Date': repo_created_at,
                        'Number of Contributors': num_contributors,
                        'Repository Owner': repo_owner,
                        'Owner Location': owner_location
                    })

                    user_details.extend(contributors_data)
                    commits_details.extend(commits_info)

    # Save the repository details to a CSV file
    fields_repo = ['Repository', 'Created Date', 'Number of Contributors', 'Repository Owner', 'Owner Location']
    with open('repository_details.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields_repo)
        writer.writeheader()
        writer.writerows(repository_details)

    # Save the user details to a separate CSV file
    fields_user = ['User', 'Location']
    with open('user_details.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields_user)
        writer.writeheader()
        writer.writerows(user_details)

    # Save commit details to a CSV file
    fields_commits = ['Month', 'Repository', 'Owner', 'Commits Per Month']
    with open('commits_per_month.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields_commits)
        writer.writeheader()
        writer.writerows(commits_details)

if __name__ == "__main__":
    main()
