import os
import json
import requests
import logging
from tqdm import tqdm

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('download_models')

# Set the logger to print to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)


# Function to download a file from a URL
def download_file(url: str, out_path: str):
    """
    Download a file from a URL
    :param url: URL to download the file from
    :param out_path: Path to save the downloaded file
    """
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        # Sizes in bytes.
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024
        with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
            with open(out_path, "wb") as file:
                for chunk in response.iter_content(block_size):
                    progress_bar.update(len(chunk))
                    file.write(chunk)
            logger.info(f"Downloaded: {out_path}")
        if total_size != 0 and progress_bar.n != total_size:
            raise RuntimeError("Could not download file")
    else:
        logger.info(f"Failed to download: {url}")


# Rest of the code remains the same


def main(json_path: str):
    """
    Download the models listed in the JSON file
    :param json_path: Path to the JSON file containing the models
    """
    models = json.load(open(json_path, "r"))
    # Loop through the models and download if not exist
    for model in models:
        dir_path = model["dir"]
        file_path = os.path.join(dir_path, model["out"])

        # Create the directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)

        # Check if the file exists
        if not os.path.exists(file_path):
            logger.info(f"File does not exist. Downloading: {file_path}")
            download_file(model["url"], file_path)
        else:
            logger.warn(f"File already exists: {file_path}")


if __name__ == "__main__":
    # Parse the JSON data
    json_path = "model_list.json"
    main(json_path)
    logger.info("Downloaded model files")
