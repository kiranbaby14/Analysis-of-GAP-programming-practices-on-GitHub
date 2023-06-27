import requests
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
import config


def get_github_files(access_token, query):
    """
    Function to scrape files from GitHub

    :param access_token: access token of the user
    :param query: GitHub query
    :return: scraped files
    """
    per_page = 100  # Number of results per page
    page = 1  # starting page number
    count = 0

    # Get the start and end dates from the user (YYYY-MM-DD)
    start_date = input("Enter start year (YYYY-MM-DD): ")
    end_date = input("Enter end year (YYYY-MM-DD): ")

    # Convert given dates to datetime format
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

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
                print(item["html_url"])
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
            print("\nRate limit exceeded (Wait for a few minutes...!)\n")
            time.sleep(300)
            continue


def main():
    access_token = config.get_access_token()
    query = "language:GAP"
    get_github_files(access_token, query)


if __name__ == "__main__":
    main()
