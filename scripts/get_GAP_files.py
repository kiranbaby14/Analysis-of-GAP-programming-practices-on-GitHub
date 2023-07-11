from github import Github

import time
import os
import sys

# append the path of the
# parent directory
sys.path.append("..")

from utils.files import retrieve_matching_files, save_to_csv_file
from utils.config import get_access_token


def get_real_prgm_lang_files(access_token, repo_dict, output_file_path):
    """
    Retrieve matching files from a list of GitHub repositories.

    :param output_file_path: file path to save the retrieved files to
    :param access_token: github access token
    :param repo_dict: dictionary with programming language as key and list of repositories as values
    :return:
    """

    # Create a PyGithub instance using the access token
    g = Github(access_token)

    # iterate over the dictionary
    for language_name, repo_list in repo_dict.items():
        # Iterate over the repositories
        for repo_path in repo_list:
            try:
                # Get the repository object using PyGithub
                repo = g.get_repo(repo_path)

                # Retrieve all matching files in the repository
                matching_files = retrieve_matching_files(language_name, repo, "")
                field_names = list(matching_files[0].keys())

                save_to_csv_file(output_file_path, field_names, matching_files)

            except Exception as e:
                print("\nRate limit exceeded (Wait for a few minutes...!)\n")
                time.sleep(10)

                continue


def main():
    # Get the GitHub access token
    access_token = get_access_token()

    # Specify the repository list
    repo_dict = {"GAP": ["gap-system/gap", ], }  # add more repositories to this list of various other pgm languages

    # Specify the output folder path
    output_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist
    output_file_path = os.path.join(output_folder, "real_GAP_files.csv")

    get_real_prgm_lang_files(access_token, repo_dict, output_file_path)


if __name__ == "__main__":
    main()
