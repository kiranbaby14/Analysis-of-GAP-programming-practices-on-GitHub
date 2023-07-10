# Only run this script if data/real_GAP_file.txt exists

import os
import csv
import requests
import joblib  # would need this library to load the preprocessing steps using NLP


def preprocess(content):
    """
    Preprocesses the content using a pre-trained NLP pipeline.

    :param content: The content to preprocess.
    :return: The processed content.
    """
    # Load the pre-trained NLP pipeline
    pipeline = joblib.load('nlp_pipeline.pkl')  # Replace 'nlp_pipeline.pkl' with the path of pre-trained pipeline file

    # Apply NLP pipeline to the content
    processed_content = pipeline.transform([content])
    return processed_content


def process_urls_and_store_features(file_path, output_file):
    """
    Retrieves URLs from a file, processes the content using a pre-trained NLP pipeline,
    and stores the processed feature vectors in a CSV file.

    :param file_path: The path to the file containing URLs.
    :param output_file: The path to the output CSV file.
    """

    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]  # Read non-empty lines into a list

    processed_features = []  # List to store processed feature vectors

    # Process URLs through the pipeline
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            content = response.text
            feature_vector = preprocess(content)
            processed_features.append(feature_vector)
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving content from {url}: {str(e)}")

    # Store processed feature vectors in a CSV file
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['URL', 'Feature'])  # Write header row
        writer.writerows(zip(urls, processed_features))  # Write URL and feature vector rows

    print(f"Processed feature vectors stored in: {output_file}")


def main():
    dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

    file_path = os.path.join(dir_path, 'real_GAP_files.txt')
    output_file = os.path.join(dir_path, 'processed_features.csv')  # Output file to store the processed feature vectors
    print(file_path, "\n", output_file)
    process_urls_and_store_features(file_path, output_file)


if __name__ == "__main__":
    main()
