
def check_matching_files(repo, directory):
    """
    Recursive function to check for matching files in all directories

    :param repo: repository link
    :param directory: directory path
    :return: matching files
    """
    matching_files = []
    contents = repo.get_contents(directory)
    for content in contents:
        if content.type == 'dir':
            matching_files.extend(check_matching_files(repo, content.path))
        else:
            file_name = content.name
            if file_name.endswith((".g", ".gi", ".gd")):
                print(content)
                matching_files.append(file_name)
    return matching_files
