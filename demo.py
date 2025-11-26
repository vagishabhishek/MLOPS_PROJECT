from mlops_project.logger import get_logger

def demo_logger():
    logger =get_logger("Demo Logger")
    logger.info("Logging works perfectly.")

demo_logger()
