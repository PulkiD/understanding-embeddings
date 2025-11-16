"""
Module to prepare ChEMBL data for downstream tasks. This script performs:
    1) Downloads the latest ChEMBL compound data from the FTP server as txt file.
        Eg, https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/chembl_<latest_chembl_version>_chemreps.txt.gz
    2) Parses the downloaded file to extract relevant fields such as compound identifiers and SMILES strings.
    3) Cleans and formats the data into a structured format (e.g., JSONL) suitable for downstream tasks.
"""

import os
import gzip
import requests
import pandas as pd
#
from src.utils.logger import logger

URL_CHEMBL_FTP = "https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/chembl_CHEMBL_VERSION_chemreps.txt.gz"

class ChEMBLDataPreparer:
    """
    Class to handle the preparation of ChEMBL data.
    """
    def __init__(self, version: str, download_dir: str, output_dir: str):
        """
        Initializes the ChEMBLDataPreparer.

        Args:
            version (str): The ChEMBL version to download.
            download_dir (str): Directory to download the data file.
            output_dir (str): Directory to save the prepared JSONL file.
        """
        self.version = version
        self.download_dir = download_dir
        self.output_dir = output_dir

    def _download_chembl_data(self) -> str:
        """
        Downloads the ChEMBL compound data file from the FTP server.

        Returns:
            str: Path to the downloaded file.
        """
        output_filename = os.path.join(self.download_dir, f"chembl_{self.version}_chemreps.txt.gz")
        #
        if os.path.exists(output_filename):
            logger.debug(f"ChEMBL data file already exists at {output_filename}. Skipping download.")
            return output_filename

        # Download the file
        url = URL_CHEMBL_FTP.replace("CHEMBL_VERSION", self.version)
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
        
        response = requests.get(url)
        response.raise_for_status()
        
        with open(output_filename, 'wb') as f:
            f.write(response.content)
        
        return output_filename
    
    def _parse_chembl_file(self, file_path: str) -> pd.DataFrame:
        """
        Parses the ChEMBL compound data file to extract relevant fields.

        Args:
            file_path (str): Path to the downloaded ChEMBL data file.

        Returns:
            pd.DataFrame: DataFrame containing cleaned compound identifiers and SMILES strings.
        """
        with gzip.open(file_path, 'rt') as f:
            df = pd.read_csv(f, sep='\t')
        
        cleaned_data = df[['chembl_id', 'canonical_smiles']].dropna().reset_index(drop=True)
        
        return cleaned_data
    
    def prepare_data(self):
        """
        Prepares the ChEMBL data by downloading, parsing, and saving it.
        """
        output_file = os.path.join(self.output_dir, f"chembl_{self.version}_data.jsonl")

        # Step 1: Download the ChEMBL data file
        logger.debug(f"Downloading ChEMBL data for version {self.version}...")
        downloaded_file = self._download_chembl_data()
        
        # Step 2: Parse and clean the data
        logger.debug(f"Parsing ChEMBL data from {downloaded_file}...")
        data = self._parse_chembl_file(downloaded_file)
        
        # Step 3: Save the cleaned data to JSONL format
        logger.debug(f"Saving prepared data to {self.output_dir}...")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        data.to_json(output_file, orient='records', lines=True)

