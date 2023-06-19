import os


def get_access_token():
    token_file_path = os.path.expanduser('~') + '/.github_shell_token'
    if os.path.isfile(token_file_path):
        with open(token_file_path, 'r') as token_file:
            access_token = token_file.read().strip()
        if access_token:
            # return token
            return access_token
        else:
            print("Error: Empty access token in the file.")
    else:
        print("Error: Token file not found.")
