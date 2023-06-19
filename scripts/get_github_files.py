from github import Github, RateLimitExceededException, BadCredentialsException, BadAttributeException, \
    GithubException, UnknownObjectException, BadUserAgentException
import time
import config
import requests


def get_github_files(access_token, query):
    """
    Function to scrape files from GitHub

    :param access_token: acces token of the user
    :param query: GitHub query
    :return: scraped files
    """
    while True:
        try:
            g = Github(access_token)
            print("Rate Limit is: ", g.rate_limiting)
            files = g.search_code(query=query)
            print("Total files found: ", files.totalCount)
        except RateLimitExceededException as e:
            print(e.status)
            print('Rate limit exceeded')
            time.sleep(300)
            continue
        except BadCredentialsException as e:
            print(e.status)
            print('Bad credentials exception')
            break
        except UnknownObjectException as e:
            print(e.status)
            print('Unknown object exception')
            break
        except GithubException as e:
            print(e.status)
            print('General exception')
            break
        except requests.exceptions.ConnectionError as e:
            print('Retries limit exceeded')
            print(str(e))
            time.sleep(10)
            continue
        except requests.exceptions.Timeout as e:
            print(str(e))
            print('Time out exception')
            time.sleep(10)
            continue
        break


def main():
    access_token = config.get_access_token()
    query = "extension:g OR extension:gi OR extension:gd"
    get_github_files(access_token, query)


if __name__ == "__main__":
    main()
