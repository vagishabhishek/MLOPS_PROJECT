import sys
from mlops_project.exception import MyException
from mlops_project.logger import get_logger
from mlops_project.components.data_ingestion import DataIngetion

from mlops_project.entity.config_entity import DataIngestionConfig
from mlops_project.entity.artifact_entity import DataIngestionArtifact

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def start_data_ingestion(self) ->DataIngestionArtifact:

        try:
            logger = get_logger("Pipeline")
            logger.info("Entered the start data_ingestion method of TrainingPipeline")
            logger.info("Getting the data from mongoDB")

            data_ingestion = DataIngetion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logger.info("Got the train set and test set from mongoDB data")
            logger.info("Exited start_data_ingestion of Pipeline Class")

            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e,sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()

        except MyException as e:
            raise MyException(e,sys) 

