"""
Configuration loader for Playwright tests
Loads settings from commonui.properties and environment variables
"""
import os
from pathlib import Path
from typing import Optional, Dict


class ConfigLoader:
    """Loads and manages configuration from properties file and environment variables"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize config loader
        
        Args:
            config_file: Path to config file (defaults to commonui.properties in project root)
        """
        if config_file is None:
            # Default to commonui.properties in the project root
            config_file = Path(__file__).parent.parent / "commonui.properties"
        
        self.config_file = Path(config_file)
        if not self.config_file.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_file}\n"
                f"Please create commonui.properties in the project root."
            )
        
        # Load properties file
        self.properties = self._load_properties_file()
        
        # Base directory is the directory containing the config file
        self.BASE_DIR = self.config_file.parent
        
        # Load paths
        self._load_paths()
        
        # Load storybook settings
        self._load_storybook()
        
        # Load visual settings
        self._load_visual()
        
        # Load browser settings
        self._load_browser()
        
        # Create directories
        self._create_directories()
    
    def _load_properties_file(self) -> Dict[str, str]:
        """
        Load Java-style properties file (key=value format)
        
        Returns:
            Dictionary of property keys and values
        """
        properties = {}
        with open(self.config_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                # Handle key=value pairs
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    properties[key] = value
        return properties
    
    def _get_property(self, key: str, default: str = '') -> str:
        """
        Get property value, checking environment variables first
        
        Args:
            key: Property key (e.g., 'storybook.url', 'browser.browser')
            default: Default value if not found
            
        Returns:
            Property value (from env var if set, otherwise from properties file)
        """
        # Map property keys to environment variable names
        # Handle special cases for common env vars
        env_var_map = {
            'browser.browser': 'BROWSER',
            'browser.headless': 'HEADLESS',
            'browser.viewport_width': 'VIEWPORT_WIDTH',
            'browser.viewport_height': 'VIEWPORT_HEIGHT',
            'storybook.url': 'STORYBOOK_URL',
            'storybook.timeout': 'STORYBOOK_TIMEOUT',
            'visual.threshold': 'VISUAL_THRESHOLD',
            'visual.screenshot_mode': 'SCREENSHOT_MODE',
        }
        
        # Get environment variable name (use mapping or convert automatically)
        env_key = env_var_map.get(key)
        if env_key is None:
            # Convert property key to environment variable name
            # e.g., 'storybook.url' -> 'STORYBOOK_URL'
            env_key = key.upper().replace('.', '_')
        
        # Check environment variable first
        env_value = os.getenv(env_key)
        if env_value is not None:
            return env_value
        
        # Fall back to properties file
        return self.properties.get(key, default)
    
    def _load_paths(self):
        """Load directory paths"""
        self.SCREENSHOTS_DIR = self.BASE_DIR / self._get_property('paths.screenshots_dir', 'screenshots')
        self.SNAPSHOTS_DIR = self.BASE_DIR / self._get_property('paths.snapshots_dir', 'snapshots')
        self.REPORTS_DIR = self.BASE_DIR / self._get_property('paths.reports_dir', 'reports')
    
    def _load_storybook(self):
        """Load Storybook configuration"""
        self.STORYBOOK_URL = self._get_property('storybook.url', 'https://picarro.github.io/picarro-common-ui')
        self.STORYBOOK_TIMEOUT = int(self._get_property('storybook.timeout', '10000'))
    
    def _load_visual(self):
        """Load visual regression settings"""
        self.VISUAL_THRESHOLD = float(self._get_property('visual.threshold', '0.2'))
        self.SCREENSHOT_MODE = self._get_property('visual.screenshot_mode', 'full')
    
    def _load_browser(self):
        """Load browser settings"""
        self.BROWSER = self._get_property('browser.browser', 'firefox')
        
        # Headless: environment variable takes precedence, then config file
        headless_value = self._get_property('browser.headless', 'false').lower()
        self.HEADLESS = headless_value in ('true', '1', 'yes')
        
        self.VIEWPORT_WIDTH = int(self._get_property('browser.viewport_width', '1920'))
        self.VIEWPORT_HEIGHT = int(self._get_property('browser.viewport_height', '1080'))
    
    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        self.SCREENSHOTS_DIR.mkdir(exist_ok=True)
        self.SNAPSHOTS_DIR.mkdir(exist_ok=True)
        self.REPORTS_DIR.mkdir(exist_ok=True)


# Create a global config instance
_config_instance: Optional[ConfigLoader] = None


def get_config(config_file: Optional[str] = None) -> ConfigLoader:
    """
    Get or create the global config instance
    
    Args:
        config_file: Optional path to config file (only used on first call)
                     Defaults to commonui.properties in project root
        
    Returns:
        ConfigLoader instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigLoader(config_file)
    return _config_instance

