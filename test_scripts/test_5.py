from evaluate.test_abstract import TestScript
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TaskScript(TestScript):
    def __init__(self, driver, env_config):
        self.driver = driver
        self.env_config = env_config
        self.wait = WebDriverWait(self.driver, 10)

    def _ensure_login(self):
        self.driver.get(f"{self.env_config['__GHOST_ADMIN__']['url']}/")
        time.sleep(1)
        if "signin" in self.driver.current_url:
            print("Logging in...")
            try:
                self.driver.find_element(By.NAME, "identification").send_keys("admin@example.com")
                self.driver.find_element(By.NAME, "password").send_keys("VeryAwesomeAdminGuy123@")
                self.driver.find_element(By.CSS_SELECTOR, "button.login").click()
                self.wait.until(EC.url_contains("/dashboard"))
            except:
                pass

    def action(self):
        """
        Task: Create a new static page with title 'About Us'.
        """
        self._ensure_login()
        
        # Navigate to Pages
        print("Navigating to Pages...")
        self.driver.get(f"{self.env_config['__GHOST_ADMIN__']['url']}/#/pages")
        
        # Click New Page
        print("Looking for 'New page' button...")
        try:
            new_page_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#/editor/page/']")))
            new_page_btn.click()
        except:
            print("Primary selector failed. Trying by text 'New page'...")
            new_page_btn = self.driver.find_element(By.XPATH, "//span[contains(text(), 'New page')]")
            new_page_btn.click()

        
        # Wait for editor
        print("Waiting for editor title...")
        title_area = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.gh-editor-title")))
        title_area.clear()
        title_area.send_keys("About Us")
        
        time.sleep(1) # Wait for url update/save

    def verify(self):
        """
        Verify: URL contains '/editor/page'
        """
        current_url = self.driver.current_url
        print(f"Current URL: {current_url}")
        return "/editor/page" in current_url
