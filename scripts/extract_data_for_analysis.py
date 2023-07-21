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

# Function to extract details
def extract_github_details(file_url, g):
    parsed_url = urlparse(file_url)
    path_parts = parsed_url.path.split('/')
    owner = path_parts[1]
    repository_name = path_parts[2]
    repository_path = owner+'/'+repository_name
    file_path = '/'.join(path_parts[3:])
    
    repo = g.get_repo(repository_path)
            
    # Extract the repository details
    repo_name = repo.name
    repo_url = repo.html_url
    repo_created_at = repo.created_at
    repo_updated_at = repo.updated_at
    
    # Extract commit history
    commits = repo.get_commits()
    
    # Create a list to store commit details
    commit_details = []

    # Iterate over each commit and extract relevant information
    for commit in commits:
        commit_sha = commit.sha
        commit_message = commit.commit.message
        commit_author_name = commit.commit.author.name
        commit_author_email = commit.commit.author.email
        commit_date = str(commit.commit.author.date)

        # Create a dictionary for each commit
        commit_dict = {
            'Commit SHA': commit_sha,
            'Commit Message': commit_message,
            'Author Name': commit_author_name,
            'Author Email': commit_author_email,
            'Commit Date': commit_date
        }

        # Append the commit dictionary to the list
        commit_details.append(commit_dict)

    # Get the number of commits
    number_of_commits = len(commit_details)

    # Get the number of distinct authors
    distinct_authors = set(commit['Author Email'] for commit in commit_details)
    number_of_distinct_authors = len(distinct_authors)

    # Print the results
    print("Number of Commits:", number_of_commits)
    print("Number of Distinct Authors:", number_of_distinct_authors)

    # Extract collaborator details
    #collaborators = repo.get_collaborators()
    #collaborator_usernames = [collaborator.login for collaborator in collaborators]
    #num_collaborators = len(collaborator_usernames)
    
    return {"Owner": owner, "Repository name": repository_name, "Repository url": repo_url, "Repository created": repo_created_at, "Repository updated": repo_updated_at, "No of commits": number_of_commits, "No of authors": number_of_distinct_authors, "File path": file_url}

def main():
    # Get the GitHub access token
    access_token = get_access_token()
    g = Github(access_token)

    # List to store the extracted details
    data = []

    # Read the URLs from the input CSV file
    with open('../data/real_GAP_files1.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            url = row['URL']  
            details = extract_github_details(url, g)
            data.append(details)

    # Define the CSV column headers
    fields = ["Owner", "Repository name", "Repository url", "Repository created", "Repository updated", "No of commits", "No of authors", "File path"]

    # Write the extracted details into the output CSV file
    with open('../data/data_for_analysis.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
        

if __name__ == "__main__":
    main()