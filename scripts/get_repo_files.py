from github import Github

access_token = config.get_access_token()

# Create a GitHub client object
g = Github(access_token)

start_date = '2022-12-01'
end_date = '2022-12-31'
count = 0

# Construct the search query
search_query = f"created:{start_date}..{end_date} language:GAP"

# Retrieve repositories matching the search query
repositories = g.search_repositories(query=search_query)

# Filter repositories based on the file extension query
filtered_repos = []
for repo in repositories:
    print(repo.name)
    count=count+1
    if count == 10:
        break
    files = repo.get_contents("")
    contents = repo.get_contents("")
    for content_file in contents:
        print(content_file)
    has_matching_files = any(file.name.endswith((".g", ".gi", ".gd")) for file in files)
    if has_matching_files:
        filtered_repos.append(repo.name)

# Print the names of the filtered repositories
for repo_name in filtered_repos:
    print(repo_name)
