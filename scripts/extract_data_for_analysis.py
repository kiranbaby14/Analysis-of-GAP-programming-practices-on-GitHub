import csv
import time
from datetime import datetime
from urllib.parse import urlparse

import requests
from github import Github
from geopy.geocoders import Nominatim
import pycountry

import sys
sys.path.append("..")

from utils.config import get_access_token
from utils.constants import HTTP_STATUS_CODES
import re


repository_set = set()
username_set = set()


def get_user_location(username, access_token):
    """
    Fetches the location of a GitHub user.

    Parameters:
        username (str): The GitHub username of the user whose location is to be fetched.
        access_token (str): The personal access token used for authentication with the GitHub API.

    Returns:
        str or None: The location of the user if available. If the location is not found or the API request fails,
        it returns None.
    """
    url = f'https://api.github.com/users/{username}'
    headers = {'Authorization': f'token {access_token}'}

    while True:
        try:
            # Send a GET request to the GitHub API to get user details
            response = requests.get(url, headers=headers)

            if response.status_code == HTTP_STATUS_CODES["SUCCESS"]:
                # Parse the JSON response to get user details
                user_details = response.json()
                # Get the location field from user details
                user_location = user_details.get('location', None)
                location = user_details.get('location', None)
                
                if user_location:
                    # Clean the user_location by removing leading and trailing whitespace
                    user_location = user_location.strip()

                    # Use Nominatim from geopy to geocode the location string and get detailed information
                    geolocator = Nominatim(user_agent="getCountry")
                    location_info = geolocator.geocode(location, exactly_one=True, language="en")

                    if location_info:
                        # Extract the country name from the geocoded information and return it
                        return location_info.address.split(',')[-1].strip()
                    else:
                        # Return None if the location is not found by the geocoder
                        return None
                
                # Return None if the user_location is not available
                return None
                
            elif response.status_code in [HTTP_STATUS_CODES["FORBIDDEN"], HTTP_STATUS_CODES["TOO_MANY_REQUESTS"]]:
                print("\nRate limit exceeded (Wait for a few minutes...!)\n")
                time.sleep(300)  # Wait for 5 minutes (300 seconds)
                continue  # Retry the API request

            else:
                # Handle other status codes or errors as needed
                print(f"Unexpected status code: {response.status_code}")
                break  # Break out of the loop if unexpected status code
                    
        except KeyboardInterrupt:
            print("Execution interrupted by user.")
            break
        except Exception as e:
            print("\nException Occurred!\n", e)
            break

    # Return None if the API request fails
    return None


def fetch_contributors_data(repo_full_name, access_token, username_set):
    """
    Fetches data of contributors for a GitHub repository.

    Parameters:
        repo_full_name (str): The full name of the repository in the format 'owner/repository_name'.
        access_token (str): The personal access token used for authentication with the GitHub API.

    Returns:
        list of dicts: A list containing data of contributors including their GitHub username and country location.
    """
    contributors_url = f'https://api.github.com/repos/{repo_full_name}/contributors'
    headers = {'Authorization': f'token {access_token}'}

    while True:
        try:
            # Send HTTP GET request to fetch contributors data for the repository
            response = requests.get(contributors_url, headers=headers)

            if response.status_code == HTTP_STATUS_CODES["SUCCESS"]:
                # Extract contributors data from the response JSON
                contributors = response.json()
                contributors_data = []

                # Process contributors data to retrieve usernames and countries
                for contributor in contributors:
                    login = contributor['login']
                    if login not in username_set:
                        # Add the username to the set to avoid duplicates
                        username_set.add(login)

                        # Get the country of the contributor using 'get_user_location' function
                        country = get_user_location(login, access_token)

                        # Append the contributor's data (username and country) to the list
                        contributors_data.append({'User': login, 'Country': country})

                # Return the list of dictionaries containing contributors' data
                return contributors_data
                
            elif response.status_code in [HTTP_STATUS_CODES["FORBIDDEN"], HTTP_STATUS_CODES["TOO_MANY_REQUESTS"]]:
                print("\nRate limit exceeded (Wait for a few minutes...!)\n")
                time.sleep(300)  # Wait for 5 minutes (300 seconds)
                continue  # Retry the API request

            else:
                # Handle other status codes or errors as needed
                print(f"Unexpected status code: {response.status_code}")
                break  # Break out of the loop if unexpected status code
                
        except KeyboardInterrupt:
            print("Execution interrupted by user.")
            break
        except Exception as e:
            print("\nException Occurred!\n", e)
            break

    # If the request is not successful, return an empty list
    return []

def fetch_activity_data(repo_full_name, access_token):
    """
    Fetches commit details for a GitHub repository.

    Parameters:
        repo_full_name (str): The full name of the repository in the format 'owner/repository_name'.
        access_token (str): The personal access token used for authentication with the GitHub API.

    Returns:
        list of dicts: A list containing commit details including the year, repository name, owner, commits per year,
        issues per year, and pull requests per year.
    """


    # Fetch activity data for commits, issues, and pull requests per year
    commits_per_year = fetch_activity_per_year(repo_full_name, access_token, 'commits')
    issues_per_year = fetch_activity_per_year(repo_full_name, access_token, 'issues')
    pull_requests_per_year = fetch_activity_per_year(repo_full_name, access_token, 'pulls')

    # Combine all unique dates (years) from commits, issues, and pull requests
    all_dates = set(list(commits_per_year.keys()) + list(issues_per_year.keys()) + list(pull_requests_per_year.keys()))

    # Sort the dates in ascending order (by year)
    sorted_dates = sorted(all_dates, key=lambda x: datetime.strptime(x, '%Y'))

    # Prepare a list of dictionaries containing commits, issues, and pull requests count for each year
    commits_info = []
    for date in sorted_dates:
        commits_count = commits_per_year.get(date, 0)
        issues_count = issues_per_year.get(date, 0)
        pull_requests_count = pull_requests_per_year.get(date, 0)
        commits_info.append({
            'Year': date,
            'Repository': repo_full_name,
            'Commits Per Year': commits_count,
            'Issues Per Year': issues_count,
            'Pull Requests Per Year': pull_requests_count
        })

    # Return the list of dictionaries containing commits, issues, and pull requests count for each year
    return commits_info

def fetch_activity_per_year(repo_full_name, access_token, activity_type):
    """
    Fetches activity data per year for a specific type (e.g., commits, issues, or pull requests) in a GitHub repository.

    Parameters:
        repo_full_name (str): The full name of the repository in the format 'owner/repository_name'.
        access_token (str): The personal access token used for authentication with the GitHub API.
        activity_type (str): The type of activity to fetch (e.g., 'commits', 'issues', 'pulls').

    Returns:
        dict: A dictionary containing activity data per year where the keys are the years in the format 'YYYY'
              and the values are the count of activities in that year.

    Raises:
        None.
    """
    url = f'https://api.github.com/repos/{repo_full_name}/{activity_type}'
    headers = {'Authorization': f'token {access_token}'}

    while True:
        try:
            # Send HTTP GET request to fetch activity data for the specified type
            response = requests.get(url, headers=headers, params={'state': 'all'})
            
            if response.status_code == HTTP_STATUS_CODES["SUCCESS"]:
                # Extract activity data from the response JSON
                activity_data = response.json()
                activity_per_year = {}

                # Process activity data to calculate count of activities per year
                for activity in activity_data:
                    if activity_type == 'commits':
                        created_at = activity['commit']['committer']['date'][:4]  # Extract year and year (YYYY)
                    else:
                        created_at = activity['created_at'][:4]  # Extract year and year (YYYY)
                    activity_per_year[created_at] = activity_per_year.get(created_at, 0) + 1

                # Return the activity data per year as a dictionary
                return activity_per_year
                
            elif response.status_code in [HTTP_STATUS_CODES["FORBIDDEN"], HTTP_STATUS_CODES["TOO_MANY_REQUESTS"]]:
                print("\nRate limit exceeded (Wait for a few minutes...!)\n")
                time.sleep(300)  # Wait for 5 minutes (300 seconds)
                continue  # Retry the API request

            else:
                # Handle other status codes or errors as needed
                print(f"Unexpected status code: {response.status_code}")
                break  # Break out of the loop if unexpected status code
                
        except KeyboardInterrupt:
            print("Execution interrupted by user.")
            break
        except Exception as e:
            print("\nException Occurred!\n", e)
            break

    # If the request is not successful, return an empty dictionary
    return {}

    
def get_repository_details(repo_full_name, access_token):
    """
    Fetches details of a GitHub repository.

    Parameters:
        repo_full_name (str): The full name of the repository in the format 'owner/repository_name'.
        access_token (str): The personal access token used for authentication with the GitHub API.

    Returns:
        tuple: A tuple containing repository details including:
            - Repository creation date (str).
            - Number of contributors (int).
            - Repository owner (str).
            - List of contributors' data (list of dicts).
            - List of commit details (list of dicts).
    """
    url = f'https://api.github.com/repos/{repo_full_name}'
    headers = {'Authorization': f'token {access_token}'}

    while True:
        try:
            # Send HTTP GET request to fetch the repository details
            response = requests.get(url, headers=headers)
            contributors_data = []
            commits_info = []

            if response.status_code == HTTP_STATUS_CODES["SUCCESS"]:
                # Extract repository details from the response JSON
                repo_details = response.json()
                repo_created_at = repo_details['created_at']
                repo_owner = repo_details['owner']['login']

                # Get the number of contributors and their locations
                contributors_data = fetch_contributors_data(repo_full_name, access_token, username_set)
                
                # Get commit details
                commits_info = fetch_activity_data(repo_full_name, access_token)

                # Return the repository details as a tuple
                return repo_created_at, len(contributors_data), repo_owner, contributors_data, commits_info
                
            elif response.status_code in [HTTP_STATUS_CODES["FORBIDDEN"], HTTP_STATUS_CODES["TOO_MANY_REQUESTS"]]:
                print("\nRate limit exceeded (Wait for a few minutes...!)\n")
                time.sleep(300)  # Wait for 5 minutes (300 seconds)
                continue  # Retry the API request

            else:
                # Handle other status codes or errors as needed
                print(f"Unexpected status code: {response.status_code}")
                break  # Break out of the loop if unexpected status code
                
        except KeyboardInterrupt:
            print("Execution interrupted by user.")
            break
        except Exception as e:
            print("\nException Occurred!\n", e)
            break

    # If the request is not successful, return None values
    return None, None, None, [], [] 
        

def main():
    """
    Main function to extract data from GitHub repositories based on URLs in a CSV file and save the results in separate CSV files.
    """
    
    # Get the GitHub access token
    access_token = get_access_token()  # Function call to get the GitHub access token

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
            
            # Parse the URL to extract repository details
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.split('/')
            owner = path_parts[1]
            repository_name = path_parts[2]
            repository_path = owner+'/'+repository_name
            
            # Check if the repository has already been processed to avoid duplicates
            if repository_path not in repository_set:
                repository_set.add(repository_path)  # Adding the repository path to the set to track processed repositories
                print("Extracting data from ", repository_path)

                # Get details of the repository, contributors, and commits using GitHub API
                repo_created_at, num_contributors, repo_owner, contributors_data, commits_info = get_repository_details(repository_path, access_token)

                # If the repository details are successfully retrieved
                if repo_created_at:
                    # Get the location of the repository owner
                    owner_location = get_user_location(repo_owner, access_token)

                    # Store the repository details in a list
                    repository_details.append({
                        'Repository': repository_path,
                        'Created Date': repo_created_at,
                        'Number of Contributors': num_contributors
                    })

                    # Extend the user_details list with contributors' data
                    user_details.extend(contributors_data)

                    # Extend the commits_details list with commit information
                    commits_details.extend(commits_info)

    # Save the repository details to a CSV file
    fields_repo = ['Repository', 'Created Date', 'Number of Contributors']
    with open('../data/repository_details.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields_repo)
        writer.writeheader()
        writer.writerows(repository_details)

    # Save the user details to a separate CSV file
    fields_user = ['User', 'Country']
    with open('../data/user_location.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields_user)
        writer.writeheader()
        writer.writerows(user_details)

    # Save commit details to a CSV file
    fields_commits = ['Year', 'Repository', 'Commits Per Year', 'Issues Per Year', 'Pull Requests Per Year']
    with open('../data/repository_activity.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields_commits)
        writer.writeheader()
        writer.writerows(commits_details)

if __name__ == "__main__":
    main()
