import csv

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
                file_url = content.download_url
                matching_files.append({'file_name': file_name, 'file_url': file_url})
    return matching_files


def save_to_csv_file(csv_file_path, fieldnames, data):

    # Write the data to a CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()

        # Write the repository details
        writer.writerows(data)

    print(f"GAP files details saved to {csv_file_path}.")
