from evaluate.test_abstract import TestScript
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TaskScript(TestScript):
    def __init__(self, driver, env_config):
        self.driver = driver
        self.env_config = env_config
        self.wait = WebDriverWait(self.driver, 10)

    def action(self):
        """
        Task: Navigate to home page.
        """
        url = self.env_config['__GHOST_FRONT__']['url']
        self.driver.get(url)

    def verify(self):
        """
        Verify: 'My First Post' is visible.
        """
        try:
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            return "My First Post" in body_text
        except:
            return False
