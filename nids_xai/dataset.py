import subprocess
import zipfile
from pathlib import Path
import typer
from loguru import logger
from tqdm import tqdm

from config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()

KAGGLE_DATASET_URL = "https://www.kaggle.com/api/v1/datasets/download/solarmainframe/ids-intrusion-csv"
ZIP_FILE_NAME = "ids-intrusion-csv.zip"

def download_dataset(destination: Path):
    """Download dataset using curl."""
    destination.mkdir(parents=True, exist_ok=True)
    zip_path = destination / ZIP_FILE_NAME

    logger.info(f"Downloading dataset from Kaggle to {zip_path}...")

    try:
        # Run curl command to download dataset
        subprocess.run(["curl", "-L", "-o", str(zip_path), KAGGLE_DATASET_URL], check=True)
        logger.success(f"Dataset downloaded to {zip_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error downloading dataset: {e}")
        raise typer.Exit(code=1)

def extract_dataset(destination: Path):
    """Extract the downloaded ZIP file."""
    zip_path = destination / ZIP_FILE_NAME

    if not zip_path.exists():
        logger.error(f"ZIP file not found at {zip_path}. Download might have failed.")
        raise typer.Exit(code=1)

    logger.info(f"Extracting dataset to {destination}...")

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(destination)
        logger.success("Dataset extraction complete.")
    except zipfile.BadZipFile as e:
        logger.error(f"Error extracting dataset: {e}")
        raise typer.Exit(code=1)

@app.command()
def main():
    download_dataset(RAW_DATA_DIR)
    extract_dataset(RAW_DATA_DIR)

    logger.info("Processing dataset...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Processing dataset complete.")

if __name__ == "__main__":
    app()
