from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TaskScript:
    def __init__(self, driver, env_config):
        self.driver = driver
        self.env_config = env_config
        self.wait = WebDriverWait(self.driver, 10)

    def action(self):
        """
        Logic to perform the logout.
        """
        # Prerequisite: Login (Helper function could be used here, but keeping it explicit for now)
        print("Pre-requisite: Logging in...")
        self.driver.get(f"{self.env_config['__GHOST_ADMIN__']['url']}/#/signin")
        
        # Check if already logged in
        if "signin" in self.driver.current_url:
            email_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="identification"]')))
            email_input.send_keys("admin@example.com")
            
            pass_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
            pass_input.send_keys("VeryAwesomeAdminGuy123@")
            
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()
            
            self.wait.until(EC.url_contains("/dashboard"))
            print("Logged in successfully.")
        
        # Actual Task: Log out
        print("Performing Task: Logging Out...")
        self.driver.get(f"{self.env_config['__GHOST_ADMIN__']['url']}/#/dashboard")
        time.sleep(1)
        
        # Click User Menu
        user_menu = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".gh-user-avatar")))
        user_menu.click()
        
        # Click Sign Out
        signout_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign out")))
        signout_link.click()
        time.sleep(2)

    def verify(self):
        """
        Verify we are redirected to the signin page.
        """
        current_url = self.driver.current_url
        print(f"Current URL after action: {current_url}")
        
        if "/signin" in current_url:
            print("[VERIFY] Success: URL contains '/signin'")
            return True
        else:
            print(f"[VERIFY] Failure: URL '{current_url}' does not contain '/signin'")
            return False
