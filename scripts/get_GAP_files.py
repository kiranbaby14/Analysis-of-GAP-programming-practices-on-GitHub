from github import Github
import time
import sys

# append the path of the
# parent directory
sys.path.append("..")

from utils.files import check_matching_files
from utils.files import save_to_csv_file
from utils.config import get_access_token


def get_GAP_files(access_token, repo_list):
    """
    Retrieve matching files from a list of GitHub repositories.

    :param access_token: github access token
    :param repo_list: list containing repositories to be downloaded
    :return:
    """
    
    # Create a PyGithub instance using the access token
    g = Github(access_token)

    # Initialise csv file name
    csv_file_path = 'gap_files_details.csv'
    gap_files_details = []

    # Initialise column names in the csv file
    fieldnames = ['Repository Name', 'Repository URL', 'Created At', 'Updated At', 'File Name', 'File URL']

    # Iterate over the repositories
    for repo_path in repo_list:
        # Get the repository object using PyGithub
        try:
            repo = g.get_repo(repo_path)
            
            # Extract the repository details
            repo_name = repo.name
            repo_url = repo.html_url
            repo_created_at = repo.created_at
            repo_updated_at = repo.updated_at

            # Extract collaborator details
            #collaborators = repo.get_collaborators()
            #collaborator_usernames = [collaborator.login for collaborator in collaborators]
            #num_collaborators = len(collaborator_usernames)

            # Retrieve all matching files in the repository
            matching_files = check_matching_files(repo, "")

            print("Matching Files in", repo_path)
            for file in matching_files:
                print(file['file_name'])
                
                # Create a list of dictionaries with the repository and file details
                gap_files_details.append({
                        'Repository Name': repo_name,
                        'Repository URL': repo_url,
                        'Created At': repo_created_at,
                        'Updated At': repo_updated_at,
                        'File Name': file['file_name'],
                        'File URL': file['file_url']
                    })
            print()
        except Exception as e:
            print("Exception occurred. Wait for a few minutes...\nException details:",e)
            time.sleep(300)
            continue
    save_to_csv_file(csv_file_path, fieldnames, gap_files_details)


def main():
    # Get the GitHub access token
    access_token = get_access_token()

    # Specify the repository list
    repo_list = ["gap-system/gap"]  # add more repositories to this list if needed
    get_GAP_files(access_token, repo_list)


if __name__ == "__main__":
    main()
