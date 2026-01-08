from abc import ABC, abstractmethod
from selenium.webdriver.support.ui import WebDriverWait

class TestScript(ABC):
    def __init__(self, driver, env_config):
        self.driver = driver
        self.env_config = env_config
        self.wait = WebDriverWait(self.driver, 10)

    @abstractmethod
    def action(self):
        """
        Perform the task steps (e.g., Navigate, Click, Type).
        """
        pass

    @abstractmethod
    def verify(self):
        """
        Verify the outcome.
        Returns:
            bool: True if pass, False if fail.
        """
        pass
