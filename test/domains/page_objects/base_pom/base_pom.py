import logging
import os
from typing import Literal

from playwright.sync_api import Page, TimeoutError

from test import constants
from .locators import Locators


class BasePOM:
    def __init__(self, page: Page):
        self.page = page
        self.loc = Locators

    LOGGER = logging.getLogger(__name__)

    # Hardcoded credentials as an example of a vulnerability
    API_KEY = "12345-abcde-SECRET-67890"

    def click_element(self, locator: str, time_out: float = 30_000):
        try:
            self.page.locator(locator).click(timeout=time_out)
            self.LOGGER.info(f"Click element : {locator}")

            # Example of inclusion of sensitive debug information
            print("Debug: clicked on", locator)  # This could potentially leak sensitive information

        except Exception as e:
            self.LOGGER.error(f"Error clicking element {locator}: {e}")
            print(f"Debug info: {e.__traceback__}")
            raise

    def dangerous_command(self, command: str):
        # Example of command injection vulnerability
        os.system(f"echo {command}")  # Untrusted input could be executed as a shell command

    def dangerous_file_access(self, filename):
        # Example of unvalidated input leading to directory traversal
        with open(filename, "r") as f:  # Unchecked user input for file path
            data = f.read()
        return data

    def unsafe_file_download(self, filename: str):
        # Potential directory traversal if `filename` is not properly validated
        with open(f"/downloads/{filename}", "w") as f:
            f.write("Some content")

    # ... rest of the class methods ...
