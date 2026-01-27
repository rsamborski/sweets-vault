from dotenv import load_dotenv
import os
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HardwareInterface:
    def __init__(self, user_names: list[str]):
        """
        Initialize the HardwareInterface.
        This will attempt to lock all drawers (sections 0 and 1) upon instantiation.
        """
        # Default to port 8001 as seen in the running process, but allow override
        load_dotenv()
        self.api_url = os.getenv("LED_MATRIX_API_HOST", "http://localhost")
        self.api_port = os.getenv("LED_MATRIX_API_PORT", "8000")
        self.api_key = os.getenv("LED_MATRIX_API_SECRET", "your-secret-key")
        self.headers = {"X-API-Key": self.api_key}

        # Number of sections in the LED matrix (2 sections: 0 and 1)
        self.sections = [0, 1]

        # Validate user names
        if len(user_names) != 2:
            raise ValueError("HardwareInterface requires exactly 2 user names.")
        self.user_names = user_names
        
        # Lock all drawers on startup
        self.lock_all_drawers()

    def _set_section_state(self, section_id: int, locked: bool) -> bool:
        """
        Helper method to set the state of a specific section.
        """
        try:
            url = f"http://{self.api_url}:{self.api_port}/section/{section_id}"
            char = self.user_names[section_id][0].upper()
            payload = {"char": char, "locked": locked}
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            logger.info(f"Successfully set section {section_id} to char='{char}', locked={locked}")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to set section {section_id} state: {e}")
            return False

    def lock_all_drawers(self):
        """
        Locks all drawers (sections).
        """
        logger.info("Attempting to lock all drawers...")
        for section in self.sections:
            self._set_section_state(section, locked=True)

    def unlock_drawer(self, drawer_id: int):
        """
        Unlocks a specific drawer.
        Args:
            drawer_id (int): The ID of the drawer (section) to unlock (0 or 1).
        """
        logger.info(f"Attempting to unlock drawer {drawer_id}...")
        if drawer_id not in self.sections:
            logger.error(f"Invalid drawer_id {drawer_id}. Valid IDs are {self.sections}")
            return

        self._set_section_state(drawer_id, locked=False)

    def clear_display(self):
        """
        Clears the entire LED matrix.
        """
        try:
            url = f"http://{self.api_url}:{self.api_port}/clear"
            requests.post(url, headers=self.headers)
            logger.info("Cleared LED matrix display")
        except requests.RequestException as e:
            logger.error(f"Failed to clear display: {e}")
