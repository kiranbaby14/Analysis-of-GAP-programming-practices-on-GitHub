from dateutil.relativedelta import relativedelta
from datetime import datetime
from github import Github
import requests
import calendar
import time
import sys

# append the path of the
# parent directory
sys.path.append("..")
from utils.config import get_access_token
from utils.files import retrieve_matching_files
from utils.constants import LANGUAGE_DATA


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


def get_github_files(access_token, query):
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

    # List to store repositories with matching files
    repositories_with_files = []

    # Iterate over the months until end date is reached
    while current_date <= end_date:
        try:
            # Process the current month
            start_month = current_date.strftime("%Y-%m-01")
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
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Process the repositories on the current page
            items = data.get("items", [])
            for item in items:
                repo_url = item["html_url"]
                repo_name = item["full_name"]

                # Get the repository object using PyGithub
                repo = g.get_repo(repo_name)

                # Get the matching files in the repository
                matching_files = retrieve_matching_files("GAP", repo, LANGUAGE_DATA["GAP"]["extensions"], "")

                # Save repositories with matching files
                if matching_files:
                    repositories_with_files.append((repo_url, matching_files))
                    count += 1

            # Check if there are more pages
            if len(items) < per_page:
                page = 1
                current_date += relativedelta(months=1)
                continue

            # Increment the page number
            page += 1

        except KeyboardInterrupt:
            print("Execution interrupted by user.")
            break

        except Exception as e:
            print("\nRate limit exceeded (Wait for a few minutes...!)\n", e)
            time.sleep(300)
            continue

    print(f"\nTotal repositories having (.g, .gi, .gd) extensions: {count}\n")

    # Print repositories with matching files
    # for repo_url, matching_files in repositories_with_files:
    #     print("Repository:", repo_url)
    #     print("Matching Files:", matching_files)
    #     print("")


def main():
    access_token = get_access_token()
    query = "language:GAP"
    get_github_files(access_token, query)


if __name__ == "__main__":
    main()
