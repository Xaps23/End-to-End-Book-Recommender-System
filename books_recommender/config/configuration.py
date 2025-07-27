import os
import sys
from books_recommender.logger.log import logging
from books_recommender.utils.util import read_yaml_file
from books_recommender.exception.exception_handler import AppException
from books_recommender.entity.config_entity import DataIngestionConfig
from books_recommender.constant import *


class AppConfiguration:
    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        try:
            self.configs_info = read_yaml_file(file_path=config_file_path)
        except Exception as e:
            raise AppException(e, sys) from e

    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            data_ingestion_config = self.configs_info.get('data_ingestion_config', {})
            artifacts_config = self.configs_info.get('artifacts_config', {})
            artifacts_dir = artifacts_config.get('artifacts_dir', '')
            dataset_dir = data_ingestion_config.get('dataset_dir', '')

            ingested_data_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config.get('ingested_dir', ''))
            raw_data_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config.get('raw_data_dir', ''))

            response = DataIngestionConfig(
                dataset_download_url = data_ingestion_config.get('dataset_download_url', ''),
                raw_data_dir = raw_data_dir,
                ingested_dir = ingested_data_dir
            )

            logging.info(f"Data Ingestion Config: {response}")
            return response

        except Exception as e:
            raise AppException(e, sys) from e
