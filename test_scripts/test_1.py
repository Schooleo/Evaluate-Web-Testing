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

    def action(self):
        """
        Task: Log in to the Ghost Admin panel.
        """
        # Navigate to Ghost Admin
        self.driver.get(f"{self.env_config['__GHOST_ADMIN__']['url']}/#/signin")
        
        # Check if already logged in
        if "signin" not in self.driver.current_url:
            print("Already logged in (or redirected).")
            return

        print("Navigated to Signin page.")
        
        # Enter Email
        email_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="identification"]')))
        email_input.clear()
        email_input.send_keys("admin@example.com")
        
        # Enter Password
        pass_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        pass_input.clear()
        pass_input.send_keys("VeryAwesomeAdminGuy123@")
        
        # Click Sign In
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button.login")
        submit_btn.click()
        
        # Wait for navigation
        self.wait.until(EC.url_contains("/dashboard"))
        print("Login submission complete.")
        time.sleep(2) # Stability wait

    def verify(self):
        """
        Verify: URL contains '/dashboard'
        """
        current_url = self.driver.current_url
        print(f"Current URL: {current_url}")
        
        # Success condition: We are on the dashboard
        if "/dashboard" in current_url:
            return True
        
        # Or if we were already logged in (tasks sometimes chain)
        return False
