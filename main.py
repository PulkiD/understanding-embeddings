from src.utils.logger import logger
from src.utils.config_loader import ConfigLoader
from src.data_preprocessing.prepare_chembl_data import ChEMBLDataPreparer

def main():
    logger.info("Starting the Understanding Embeddings project.")
    config = ConfigLoader().get_config()
    logger.debug(f"Loaded configuration...")
    #
    config_chembl = config.get("ChEMBL", {})
    obj_chembl_preparer = ChEMBLDataPreparer(
        version=config_chembl.get("version", "36"),
        download_dir=config_chembl.get("download_chembl_file"),
        output_dir=config_chembl.get("parsed_chembl_file")
    )
    obj_chembl_preparer.prepare_data()
    logger.info("ChEMBL data preparation completed.")



if __name__ == "__main__":
    main()
