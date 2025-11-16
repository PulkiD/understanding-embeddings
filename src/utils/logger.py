import logging
import sys
from pathlib import Path
from .config_loader import ConfigLoader, SingletonMeta

class Logger(metaclass=SingletonMeta):
    """
    Singleton class for application logging.

    Configures a logger based on settings from the ConfigLoader.
    It sets up a console handler and a file handler.
    The log format is:
    date time: module name: python script name: code line: LEVEL: message
    """
    def __init__(self):
        # Get configuration from the singleton config loader
        config_data = ConfigLoader().get_section('Logging')
        
        log_level = config_data.get('level', 'INFO').upper()
        log_file_name = config_data.get('file', 'logs/app.log')
        
        # Define project root
        project_root: Path = Path(__file__).resolve().parent.parent.parent
        self.log_file_path: Path = project_root / log_file_name
        
        # Ensure log directory exists
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create the logger
        project_name = config_data.get('project_name', 'UnderstandingEmbeddings')
        self.logger = logging.getLogger(project_name)
        self.logger.setLevel(getattr(logging, log_level, logging.INFO))
        
        # Prevent logs from propagating to the root logger
        self.logger.propagate = False 

        # Define the log format
        log_format = '%(asctime)s: %(module)s: %(filename)s: %(lineno)d: %(levelname)s: %(message)s'
        formatter = logging.Formatter(log_format)

        # Only add handlers if they don't already exist
        if not self.logger.handlers:
            # Create Console Handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            # Create File Handler
            file_handler = logging.FileHandler(self.log_file_path)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """
        Returns the configured logger instance.
        """
        return self.logger

# Creating a single instance to be imported by other modules
logger = Logger().get_logger()