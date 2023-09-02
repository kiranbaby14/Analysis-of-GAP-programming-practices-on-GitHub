from dateutil.relativedelta import relativedelta
from datetime import datetime
from github import Github
import pickle
import requests
import calendar
import time
import sys
import os
import csv

# append the path of the
# parent directory
sys.path.append("..")
from utils.config import get_access_token
from utils.files import retrieve_matching_files, save_to_csv_file, get_unique_file_path
from utils.constants import LANGUAGE_DATA
from transformers.transformers import \
    NumberRemovalTransformer, \
    UrlToContentTransformer, \
    NonASCIIRemovalTransformer, \
    MultipleSpacesRemovalTransformer


def validate_date(date_str):
    """
    Function to validate date string

    :param date_str: date as a string
    :return: true if date is valid else return false
    """

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except Exception as e:
        return False


def load_pipeline():
    """
    Function to load the ML pipeline

    :return: ML pipeline
    """
    # Load the saved pipeline
    clf_folder_path = os.path.join(os.path.dirname(os.getcwd()), "model")
    clf_file_path = os.path.join(clf_folder_path, 'classifier1.pkl')
    # Load the saved pipeline
    with open(clf_file_path, 'rb') as file:
        loaded_pipeline = pickle.load(file)
    return loaded_pipeline


def get_github_files(access_token, query, output_file_path):
    """
    Function to scrape files from GitHub

    :param access_token: access token of the user
    :param query: GitHub query
    :return: scraped files
    """

    # Create a PyGithub instance using the access token
    g = Github(access_token)

    per_page = 100  # Number of results per page
    page = 1  # starting page number
    count = 0

    # Get the start and end dates from the user (YYYY-MM-DD)
    start_date = input("Enter start year (YYYY-MM-DD): ")
    end_date = input("Enter end year (YYYY-MM-DD): ")

    # Validate dates given by the user
    if not validate_date(start_date):
        print("Error: Invalid start date!")
        return

    if not validate_date(end_date):
        print("Error: Invalid end date!")
        return

    # Convert given dates to datetime format
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Validate dates given by the user
    if current_date > end_date:
        print("Error: Invalid start date and end date!")
        return

    date_range_of_data_collected = {
        "start_date": start_date,
        "end_date": datetime.strftime(end_date, "%Y-%m-%d"),
        "current_date": datetime.now().strftime("%Y-%m-%d")
    }

    # Process the current month
    start_month = current_date.strftime("%Y-%m-%d")

    # Iterate over the months until end date is reached
    while (current_date <= end_date) or (datetime.strptime(start_month, "%Y-%m-%d") <= end_date):

        if current_date.strftime("%Y-%m") != end_date.strftime("%Y-%m"):
            _, num_days = calendar.monthrange(current_date.year, current_date.month)
            end_month = current_date.replace(day=num_days).strftime("%Y-%m-%d")
        else:
            # edge case for when the end date is encountered as we want to
            # only get the files till the specified day by the user
            # and not the whole month
            end_month = end_date.strftime("%Y-%m-%d")

        # Construct the URL with the date range
        created_date_range = f'{start_month}..{end_month}'

        url = f"https://api.github.com/search/repositories?q={query}+" \
              f"created:{created_date_range}&" \
              f"per_page={per_page}&" \
              f"page={page}"

        # Header tags
        headers = {'User-Agent': 'request',
                   "Authorization": f"Bearer {access_token}"}
        while True:
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                break
            except KeyboardInterrupt:
                print("Execution interrupted by user.")
                break
            except Exception as e:
                print("\nRate limit exceeded (Wait for a few minutes...!)\n", e)
                time.sleep(300)
                continue
            # write exception for when the pagination number is not valid

        # Process the repositories on the current page
        items = data.get("items", [])

        for item in items:
            repo_name = item["full_name"]

            while True:
                try:
                    # Get the repository object using PyGithub
                    repo = g.get_repo(repo_name)
                    break
                except KeyboardInterrupt:
                    print("Execution interrupted by user.")
                    break
                except Exception as e:
                    print("\nRate limit exceeded (Wait for a few minutes...!)\n")
                    time.sleep(300)
                    continue

            pipeline = load_pipeline()

            # Get the matching files in the repository
            matching_files = retrieve_matching_files("GAP", repo, LANGUAGE_DATA["GAP"]["extensions"], "", pipeline)

            # Save repositories with matching files
            if matching_files:
                # ----------code to save repo here----------------
                print("Real: " + repo_name)
                count += 1
                field_names = list(matching_files[0].keys())
                save_to_csv_file(output_file_path, field_names, matching_files)

        # Check if there are more pages
        if len(items) < per_page:
            page = 1
            current_date += relativedelta(months=1)
            start_month = current_date.strftime("%Y-%m-01")  # start-month after the first iteration starts from day 1
            continue

        # Increment the page number
        page += 1

    print(f"\nTotal repositories having (.g, .gi, .gd) extensions: {count}\n")
    return date_range_of_data_collected


def main():
    access_token = get_access_token()
    query = "language:GAP"

    # Specify the output folder path
    output_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

    base_filename = "gap_files"  # csv file name to be saved
    output_file_path = get_unique_file_path(output_folder, base_filename)

    date_range_of_data_collected = get_github_files(access_token, query, output_file_path)

    date_column_names = ['start_date', 'end_date', 'current_date']
    date_values_for_first_row = [date_range_of_data_collected['start_date'], date_range_of_data_collected['end_date'],
                                 date_range_of_data_collected['current_date']]

    # Check if the file exists before trying to read it
    if os.path.exists(output_file_path):

        # Read the existing content
        existing_content = []
        with open(output_file_path, 'r') as csv_in:
            reader = csv.reader(csv_in)
            existing_content = list(reader)

        # Modify the header
        header = existing_content[0]
        header.extend(date_column_names)

        # Modify the first row
        first_row = existing_content[1]
        first_row.extend(date_values_for_first_row)

        # Write the updated content back to the file
        with open(output_file_path, 'w', newline='') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerows(existing_content)

        print(f"Classified data saved to {output_file_path}.")

    else:
        print("No CSV file was created as no matching repositories were found.")


if __name__ == "__main__":
    main()
