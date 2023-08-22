import csv
import time
import sys
import os


def retrieve_matching_files(language_name, repo, extensions, directory, pipeline=None):
    """
    Recursive function to check for matching files in all directories

    :param pipeline: the preprocessing and classifier pipeline
    :param language_name: name of the programming language
    :param repo: repository link
    :param extensions: extensions of the files
    :param directory: directory path
    :return: matching files
    """
    matching_files = []

    while True:
        try:
            contents = repo.get_contents(directory)
            break
        except Exception as e:
            print("\nRate limit exceeded (Wait for a few minutes...!)\n")
            time.sleep(10)
            continue

    processed_files = 0

    # Define the loading animation characters
    animation_chars = ["|", "/", "-", "\\"]

    for content in contents:
        processed_files += 1

        if content.type == 'dir':
            matching_files.extend(retrieve_matching_files(language_name, repo, extensions, content.path, pipeline))
        else:
            file_URL = content.download_url

            try:
                if file_URL.endswith(tuple(extensions)):
                    if pipeline is not None:
                        classified_language = pipeline.predict([file_URL])
                        if classified_language[0] == "GAP":
                            # print(classified_language, file_URL)
                            matching_files.append({"URL": file_URL, "Name": language_name})
                            return matching_files
                    else:
                        matching_files.append({"URL": file_URL, "Name": language_name})
                        
            except Exception:
                # print("URL: " + file_URL + ", File: " + content)
                continue

        # Display loading animation
        loading_animation = f"Processing files: {animation_chars[processed_files % len(animation_chars)]}"
        sys.stdout.write(loading_animation)
        sys.stdout.flush()
        # move the cursor back by the length
        # of the loading_animation string
        sys.stdout.write("\b" * len(loading_animation))
        sys.stdout.flush()
        #time.sleep(0.1)  # for smooth visual effects of the animation


    return matching_files


def save_to_csv_file(csv_file_path, fieldnames, data):
    """
    function to save the data into a csv file

    :param csv_file_path: path where the file is to be saved
    :param fieldnames: column names
    :param data: column values
    :return: None
    """
    # Write the data to a CSV file
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Check if the file is empty
        if file.tell() == 0:
            writer.writeheader()

        # Append the repository details
        writer.writerows(data)


def get_unique_file_path(output_folder, base_filename):
    """
    Generate a unique file path that doesn't already exist in the output folder.

    :param output_folder (str) - The path to the output folder where the file should be created.
    :param base_filename (str) - The base filename without the extension.
    :return: str - A unique file path that can be used to create a new file.
    """
    file_counter = 1
    output_file_name = f"{base_filename}.csv"
    output_file_path = os.path.join(output_folder, output_file_name)

    while os.path.exists(output_file_path):
        file_counter += 1
        output_file_name = f"{base_filename}({file_counter}).csv"
        output_file_path = os.path.join(output_folder, output_file_name)

    return output_file_path
