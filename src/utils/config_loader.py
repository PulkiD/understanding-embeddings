import os
import yaml
from pathlib import Path
from typing import Dict, Any


class SingletonMeta(type):
    """
    A metaclass for creating Singleton classes. Ensures only one instance
    of the class is ever created.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ConfigLoader(metaclass=SingletonMeta):
    """
    Singleton class to load and provide application configuration.

    It reads a YAML file from the 'configs/' directory in the project root.
    The specific file loaded depends on the 'APP_ENV' environment variable.
    If 'APP_ENV' is 'prod', it loads 'prod.yml'.
    If 'APP_ENV' is not set, it defaults to 'config.yml'.
    """
    def __init__(self):
        # Define the project root directory
        # This assumes config_loader.py is in src/utils/
        self.project_root: Path = Path(__file__).resolve().parent.parent.parent
        
        # Determine which config file to load
        env = os.environ.get('APP_ENV')
        if env:
            config_filename = f"{env}.yml"
        else:
            config_filename = "config.yml"
            
        self.config_path: Path = self.project_root / 'configs' / config_filename
        
        # Load the configuration
        self.config: Dict[str, Any] = self._load_config()
        # print(f"Config loaded...")

    def _load_config(self) -> Dict[str, Any]:
        """
        Loads the YAML configuration file.
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found at: {self.config_path}")
            
        try:
            with open(self.config_path, 'r') as f:
                config_data = yaml.safe_load(f)
            return config_data
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            raise
        except Exception as e:
            print(f"Error loading config: {e}")
            raise

    def get_config(self) -> Dict[str, Any]:
        """
        Returns the loaded configuration dictionary.
        """
        return self.config

    def get_section(self, section_name: str) -> Dict[str, Any]:
        """
        Helper method to get a specific section from the config.
        """
        return self.config.get(section_name, {})

# Creating a singleton instance of ConfigLoader to be used across the application
config_loader_instance = ConfigLoader()