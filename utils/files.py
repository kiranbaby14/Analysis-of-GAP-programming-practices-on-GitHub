import csv
import time
import sys



def check_matching_files(repo, directory):
    """
    Recursive function to check for matching files in all directories

    :param repo: repository link
    :param directory: directory path
    :return: matching files
    """
    matching_files = []
    contents = repo.get_contents(directory)
    processed_files = 0

    # Define the loading animation characters
    animation_chars = ["|", "/", "-", "\\"]

    for content in contents:
        processed_files += 1

        if content.type == 'dir':
            matching_files.extend(check_matching_files(repo, content.path))
        else:
            file_name = content.download_url
            if file_name.endswith((".g", ".gi", ".gd")):
                matching_files.append(file_name)

        # Display loading animation
        loading_animation = f"Processing files: {animation_chars[processed_files % len(animation_chars)]}"
        sys.stdout.write(loading_animation)
        sys.stdout.flush()
        # move the cursor back by the length
        # of the loading_animation string
        sys.stdout.write("\b" * len(loading_animation))
        sys.stdout.flush()
        time.sleep(0.1)  # for smooth visual effects of the animation

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
