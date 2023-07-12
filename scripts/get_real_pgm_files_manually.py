from github import Github

import time
import os
import sys

# append the path of the
# parent directory
sys.path.append("..")

from utils.files import retrieve_matching_files, save_to_csv_file
from utils.config import get_access_token
from utils.constants import LANGUAGE_DATA


def get_real_prgm_lang_files(access_token, output_file_path):
    """
    Retrieve matching files from a list of GitHub repositories.

    :param output_file_path: file path to save the retrieved files to
    :param access_token: github access token
    :return:
    """

    # Create a PyGithub instance using the access token
    g = Github(access_token)

    # iterate over the dictionary
    for language, data in LANGUAGE_DATA.items():
        extensions = data["extensions"]
        repositories = data["repository"]
        
        # Iterate over the repositories
        for repo_path in repositories:
            try:
                # Get the repository object using PyGithub
                repo = g.get_repo(repo_path)

                # Retrieve all matching files in the repository
                matching_files = retrieve_matching_files(language, repo, extensions, "")
                field_names = list(matching_files[0].keys())

                save_to_csv_file(output_file_path, field_names, matching_files)

            except Exception as e:
                print("\nRate limit exceeded (Wait for a few minutes...!)\n")
                time.sleep(10)

                continue


def main():
    # Get the GitHub access token
    access_token = get_access_token()

    # Specify the output folder path
    output_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist
    output_file_path = os.path.join(output_folder, "data_files.csv")

    get_real_prgm_lang_files(access_token, output_file_path)
    print(f"Data saved to {output_file_path}.")


if __name__ == "__main__":
    main()
