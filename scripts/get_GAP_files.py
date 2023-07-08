from github import Github

import time
import os
import sys

# append the path of the
# parent directory
sys.path.append("..")

from utils.files import check_matching_files
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

    # Specify the output folder path
    output_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

    # Iterate over the repositories
    for repo_path in repo_list:
        # Get the repository object using PyGithub
        try:
            repo = g.get_repo(repo_path)

            # Retrieve all matching files in the repository
            matching_files = check_matching_files(repo, "")

            output_file = os.path.join(output_folder, "real_GAP_files.txt")

            with open(output_file, 'a') as file:
                for file_name in matching_files:
                    file.write(file_name + "\n")

        except Exception as e:
            print("\nRate limit exceeded (Wait for a few minutes...!)\n")
            time.sleep(10)
            continue


def main():
    # Get the GitHub access token
    access_token = get_access_token()

    # Specify the repository list
    repo_list = ["gap-system/gap"]  # add more repositories to this list if needed
    get_GAP_files(access_token, repo_list)


if __name__ == "__main__":
    main()
