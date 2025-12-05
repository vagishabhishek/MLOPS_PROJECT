from mlops_project.pipeline.training_pipeline import TrainPipeline

from mlops_project.logger import get_logger

import logging
logging.getLogger("pymongo").setLevel(logging.CRITICAL)

pipeline = TrainPipeline()
pipeline.run_pipeline()