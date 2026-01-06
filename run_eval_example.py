import json
import time
import os
import sys
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Add current directory to path
sys.path.append(os.getcwd())

from evaluate.evaluator import Evaluator

def print_summary(results):
    print("\n" + "="*80)
    print(f"{'ID':<5} | {'Result':<10} | {'Description'}")
    print("-" * 80)
    for res in results:
        status_icon = "✅ PASS" if res['success'] else "❌ FAIL"
        # Truncate description if too long
        desc = (res['description'][:60] + '..') if len(res['description']) > 60 else res['description']
        print(f"{res['id']:<5} | {status_icon:<10} | {desc}")
    print("="*80)
    
    total = len(results)
    passed = sum(1 for r in results if r['success'])
    print(f"Total: {total} | Passed: {passed} | Section Completion Rate: {(passed/total)*100:.1f}%")

def perform_task_action(driver, task, env_config):
    """
    Automates the actions for a given task using Selenium.
    """
    task_id = task['task_id']
    print(f"Automating Task {task_id}...")
    
    try:
        if task_id == "1": # Login
            wait = WebDriverWait(driver, 30)
            
            # Find and fill email
            email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="identification"]')))
            email_input.clear()
            email_input.send_keys("admin@example.com")
            
            # Find and fill password
            pass_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
            pass_input.clear()
            pass_input.send_keys("VeryAwesomeAdminGuy123@")
            pass_input.send_keys(Keys.RETURN)
            
            print("Submitted credentials...")
            
            # Wait for dashboard
            try:
                 wait.until(EC.url_contains("/dashboard"))
                 print("Successfully redirected to dashboard.")
            except:
                 print("Warning: Did not detect dashboard redirection within timeout.")
            time.sleep(3) # Extra buffer

        elif task_id == "2": # Create Post
            wait = WebDriverWait(driver, 10)
            driver.get(f"{env_config['__GHOST_ADMIN__']['url']}/#/editor/post/")
            print(f"Task 2: Navigated to {driver.current_url}")
            
            # Title
            title_area = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-test-editor-title-input], textarea.gh-editor-title")))
            title_area.clear()
            title_area.send_keys("My First Post")
            
            # Body
            # Use Tabbing to reach body as selectors can be flaky
            title_area.send_keys(Keys.TAB)
            actions = webdriver.ActionChains(driver) 
            actions.send_keys("Hello Ghost").perform()
            time.sleep(2)

        elif task_id == "3": # Publish Post
            wait = WebDriverWait(driver, 10)
            # Must navigate to the post first
            driver.get(f"{env_config['__GHOST_ADMIN__']['url']}/#/posts/")
            
            # Find post and click 
            print("Task 3: Searching for post...")
            post_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(@class, 'gh-content-entry-title') and contains(., 'My First Post')]")))
            post_link.click()
            print("Task 3: Post clicked. Finding publish trigger...")
            
            # Click Publish
            publish_trigger = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.gh-publish-trigger, [data-test-button='publish-flow']")))
            publish_trigger.click()
            print("Task 3: Publish flow triggered.")
            time.sleep(1)
            
            # Click Continue
            continue_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.gh-btn-black, [data-test-button='continue']")))
            continue_btn.click()
            print("Task 3: Continue clicked.")
            time.sleep(1)
            
            # Click Confirm
            confirm_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.gh-btn-pulse, [data-test-button='confirm-publish']")))
            confirm_btn.click()
            print("Task 3: Confirm clicked.")
            time.sleep(3)
            
            # Wait for UI to update/modal to settle
            time.sleep(3)


        elif task_id == "4": # Verify Home Page
            # Navigation is handled by run_task default logic, no specific action beyond navigation needed
            time.sleep(3)

        elif task_id == "5": # Create Page
            wait = WebDriverWait(driver, 10)
            driver.get(f"{env_config['__GHOST_ADMIN__']['url']}/#/editor/page/")
            title_area = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.gh-editor-title")))
            title_area.clear()
            title_area.send_keys("About Us")
            # Wait for autosave
            time.sleep(2)

        elif task_id == "6": # Update Site Title
            wait = WebDriverWait(driver, 10)
            driver.get(f"{env_config['__GHOST_ADMIN__']['url']}/#/settings/")
            time.sleep(2)
            
            # Click General (edit) - Usually the first "Edit" button corresponds to Title & Description
            try:
                # Wait for any Edit button to be present - use . (dot) to check recursive text
                wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Edit')]")))
                edit_btns = driver.find_elements(By.XPATH, "//button[contains(., 'Edit')]")
                if edit_btns:
                    # Click the first one (Title & description)
                    edit_btns[0].click()
                else:
                    print("Task 6 Warning: Could not find 'Edit' button.")
            except Exception as e:
                print(f"Task 6 Error finding Edit button: {e}")

            time.sleep(1)
            
            # Find Title Input
            title_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Site title']")))
            
            # Use Ctrl+A -> Backspace for full clear
            title_input.send_keys(Keys.CONTROL + "a")
            title_input.send_keys(Keys.BACKSPACE)
            time.sleep(0.5) 
            
            title_input.send_keys("Agentic Web")
            
            # Trigger input event just in case
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", title_input)
            time.sleep(1)
            
            # Find and Click Save
            # Save button appears/becomes enabled after change
            try:
                # Use . for nested text here too for consistency
                save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save')]")))
                save_btn.click()
                print("Task 6: Save button clicked.")
                
                # Wait for save to complete (button text might change to 'Saved' or disable)
                time.sleep(2)
            except Exception as e:
                print(f"Task 6 Error clicking Save: {e}")

        elif task_id == "7": # Update Site Description
             wait = WebDriverWait(driver, 10)
             driver.get(f"{env_config['__GHOST_ADMIN__']['url']}/#/settings/")
             time.sleep(2)
             
             try:
                 # Wait for any Edit button - corresponds to Title & Description
                 wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Edit')]")))
                 edit_btns = driver.find_elements(By.XPATH, "//button[contains(., 'Edit')]")
                 if edit_btns:
                     edit_btns[0].click()
                 else:
                     print("Task 7 Warning: Could not find 'Edit' button.")
             except Exception as e:
                 print(f"Task 7 Error finding Edit button: {e}")

             try:
                 desc_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Site description']")))
                 # Clear input reliably
                 desc_input.send_keys(Keys.CONTROL + "a")
                 desc_input.send_keys(Keys.BACKSPACE)
                 time.sleep(0.5)
                 
                 desc_input.send_keys("Testing Ghost CMS")
                 
                 # Save
                 save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Save')]")))
                 save_btn.click()
                 time.sleep(2)
             except Exception as e:
                print(f"Task 7 automation error: {e}")

        elif task_id == "8": # Invite Staff
            wait = WebDriverWait(driver, 10)
            driver.get(f"{env_config['__GHOST_ADMIN__']['url']}/#/settings/staff/")
            invite_people_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Invite people')]")))
            invite_people_btn.click()
            
            email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='email@example.com']")))
            email_input.send_keys("editor@example.com")
            
            # Role selection (default might be Author, need Editor)
            # Usually just click "Send invitation" for now as default is likely OK or simple
            send_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Send invitation')]")
            send_btn.click()
            time.sleep(2)

        elif task_id == "9": # Create Tag
            wait = WebDriverWait(driver, 10)
            driver.get(f"{env_config['__GHOST_ADMIN__']['url']}/#/tags/new/")
            
            name_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-test-input='tag-name']")))
            name_input.send_keys("Tech")
            
            save_btn = driver.find_element(By.CSS_SELECTOR, "button[data-test-button='save']")
            save_btn.click()
            time.sleep(2)

        elif task_id == "10": # Add Tag to Post
            wait = WebDriverWait(driver, 10)
            # Navigate to the post editor for 'My First Post'
            driver.get(f"{env_config['__GHOST_ADMIN__']['url']}/#/posts/")
            
            # Find post and click 
            post_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(@class, 'gh-content-entry-title') and contains(., 'My First Post')]")))
            post_link.click()
            
            # Click Settings/Side menu
            settings_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Settings']"))) 
            settings_btn.click()
            
            # Tag input
            tag_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#tag-input input")))
            tag_input.send_keys("Tech")
            tag_input.send_keys(Keys.RETURN)
            
            # Close settings and Save/Update
            settings_btn.click() # toggle close
            
            # Update/Publish
            # If already published, button is "Update"
            update_btn = driver.find_element(By.CSS_SELECTOR, "[data-test-button='publish-save']") # or generic save
            if update_btn: update_btn.click()
            time.sleep(2)

        elif task_id == "11": # Create Member
            wait = WebDriverWait(driver, 10)
            driver.get(f"{env_config['__GHOST_ADMIN__']['url']}/#/members/new/")
            
            name_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-test-input='member-name']")))
            name_input.send_keys("John Doe")
            
            email_input = driver.find_element(By.CSS_SELECTOR, "input[data-test-input='member-email']")
            email_input.send_keys("john@example.com")
            
            save_btn = driver.find_element(By.CSS_SELECTOR, "button[data-test-button='save']")
            save_btn.click()
            time.sleep(2)

        elif task_id == "12": # Edit Member Note
             wait = WebDriverWait(driver, 10)
             driver.get(f"{env_config['__GHOST_ADMIN__']['url']}/#/members/")
             member_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(text(), 'John Doe')]")))
             member_link.click()
             
             note_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='note']")))
             note_input.send_keys("VIP")
             
             save_btn = driver.find_element(By.CSS_SELECTOR, "button[data-test-button='save']")
             save_btn.click()
             time.sleep(2)

        elif task_id == "13": # Delete Member
             wait = WebDriverWait(driver, 10)
             # Assuming already on member page or navigate
             actions_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-button='member-actions']")))
             actions_btn.click()
             
             del_btn = driver.find_element(By.CSS_SELECTOR, "button[data-test-button='delete-member']")
             del_btn.click()
             
             confirm_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.gh-btn-red")))
             confirm_btn.click()
             time.sleep(2)

        elif task_id == "14": # Add Navigation
             wait = WebDriverWait(driver, 10)
             driver.get(f"{env_config['__GHOST_ADMIN__']['url']}/#/settings/navigation/")
             
             # Inputs are typically last row
             # Placeholder 'New item label'
             label_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='New item label']")))
             label_input.send_keys("Portfolio")
             
             url_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='/']")
             url_input.send_keys("portfolio") # auto-formatted
             
             add_btn = driver.find_element(By.CSS_SELECTOR, "button.bg-green")
             add_btn.click()
             
             save_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]")
             save_btn.click()
             time.sleep(2)

        elif task_id == "15": # Unpublish Post
             wait = WebDriverWait(driver, 10)
             driver.get(f"{env_config['__GHOST_ADMIN__']['url']}/#/posts/")
             post_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(@class, 'gh-content-entry-title') and contains(., 'My First Post')]")))
             post_link.click()
             
             # Click Update menu
             trigger = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test-button='publish-flow']")))
             trigger.click()
             
             # Revert to draft button
             revert_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test-button='revert-to-draft']")))
             revert_btn.click()
             time.sleep(2)

        elif task_id == "16": # Change Profile Name
             wait = WebDriverWait(driver, 10)
             # User menu
             menu = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".gh-user-avatar")))
             menu.click()
             
             profile_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test-nav='user-profile']"))) 
             profile_link.click()
             
             name_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='user-name']"))) # likely id
             name_input.clear()
             name_input.send_keys("Admin User")
             
             save_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]")
             save_btn.click()
             time.sleep(2)

        elif task_id == "17": # Global Search
             wait = WebDriverWait(driver, 10)
             btn = driver.find_element(By.CSS_SELECTOR, "button.gh-nav-search-button")
             btn.click()
             
             search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.gh-input-with-select")))
             search_input.send_keys("About Us")
             time.sleep(2)
             search_input.send_keys(Keys.RETURN)
             time.sleep(3)

        elif task_id == "18": # Delete Post
             wait = WebDriverWait(driver, 10)
             driver.get(f"{env_config['__GHOST_ADMIN__']['url']}/#/posts/")
             # Assuming 'My First Post' exists
             
             # Might need to ensure we don't pick up 'My First Post' if there are multiples or if status differs
             # Logic same as before but wrapped in try-catch for safety
             try:
                 post_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[contains(@class, 'gh-content-entry-title') and contains(., 'My First Post')]")))
                 post_link.click()
                 
                 # Settings
                 settings_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Settings']"))) 
                 settings_btn.click()
                 
                 # Delete
                 del_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.settings-menu-delete-button")))
                 del_btn.click()
                 
                 confirm_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.gh-btn-red")))
                 confirm_btn.click()
                 time.sleep(2)
             except: pass


    except Exception as e:
        print(f"Error during automation: {e}")
        try:
            driver.save_screenshot(f'failure_task_{task_id}.png')
            print(f"Saved failure screenshot: failure_task_{task_id}.png")
        except: pass


def run_task(task, evaluator, driver, env_config, manual=False):
    print(f"\n--- Task {task['task_id']} ---")
    print(f"Description: {task['task_description']}")
    
    # Resolve start URL
    start_url_key = task['start_url']
    start_url = start_url_key
    if start_url_key in env_config:
         start_url = env_config[start_url_key]['url']

    print(f"Start URL: {start_url}")

    try:
        # Navigate
        if start_url.startswith("http"):
             driver.get(start_url)
        else:
             print(f"Warning: Could not resolve valid start URL from {start_url_key}")
        
        if task.get("require_login"):
            print("(!) Note: This task requires login.")

        # ACTION
        print(f"\n[ACTION REQUIRED] Perform: {task['task_description']}")
        # input("Press Enter when done...")
        if manual:
            input("Press Enter when done...")
        else:
            perform_task_action(driver, task, env_config)

        # EVAL
        print("Evaluating...")
        success = evaluator.evaluate_with_selenium(task['task_id'], browser=driver)
        
        if success:
             print("[PASS] Web App Evaluation passed.")
             return True
        else:
             print("[FAIL] Web App Evaluation failed.")
             try:
                 driver.save_screenshot(f'eval_fail_task_{task["task_id"]}.png')
                 print(f"Saved evaluation failure screenshot: eval_fail_task_{task['task_id']}.png")
             except: pass
             return False

    except Exception as e:
        print(f"Error executing task {task['task_id']}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Run a specific task or sequence of tasks.')
    parser.add_argument('--task_id', type=str, help='Task IDs to run, separated by commas or spaces, or "all" to run sequence')
    parser.add_argument('--manual', action='store_true', help='Run tasks manually (press Enter when done)')
    parser.add_argument('--auto_proceed', action='store_true', help='Auto proceed to next task after evaluation')
    args = parser.parse_args()

    try:
        with open('env_config.json', 'r') as f:
            env_config = json.load(f)
        with open('dataset/tasks.json', 'r') as f:
            tasks = json.load(f)
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    evaluator = Evaluator(tasks)
    
    print(f"Loaded {len(tasks)} tasks.")
    if len(sys.argv) > 1:
        choice = args.task_id
        print(f"Auto-selecting Task ID: {choice}")
    else:
        choice = input("Enter Task ID to run, or 'all' to run sequence: ").strip()

    tasks_to_run = []
    if choice.lower() == 'all':
        tasks_to_run = tasks
    else:
        split_choice = choice
        if ',' in choice:
            split_choice = choice.split(',')
        elif ' ' in choice:
            split_choice = choice.split(' ')
        ids = [x.strip() for x in split_choice]
        tasks_to_run = [t for t in tasks if t['task_id'] in ids]

    # Check if manual
    manual = args.manual

    # Check dependencies (Login)
    requires_login = any(t.get('require_login', False) for t in tasks_to_run)
    has_login_task = any(t['task_id'] == '1' for t in tasks_to_run)
    
    auto_login = False
    if requires_login and not has_login_task:
        print("Note: Selected tasks require login. Auto running login script.")
        login_task = next((t for t in tasks if t['task_id'] == '1'), None)
        if login_task:
            auto_login = True

    if not tasks_to_run:
        print(f"No tasks found for input: {choice}")
        return

    # Init Browser Once
    print("\nLaunching Browser...")
    chrome_options = Options()
    # chrome_options.add_argument("--headless") 
    driver = webdriver.Chrome(options=chrome_options)

    results = []

    try:
        for task in tasks_to_run:
            # Login first if required
            if auto_login:
                run_task(login_task, evaluator, driver, env_config)
                auto_login = False

            success = run_task(task, evaluator, driver, env_config, manual=manual)
            results.append({
                "id": task['task_id'],
                "description": task['task_description'],
                "success": success
            })
            
            if not args.auto_proceed and len(tasks_to_run) > 1 and task != tasks_to_run[-1]:
               cont = input("\nProceed to next task? (Y/n): ")
               if cont.lower() == 'n':
                   break
            elif args.auto_proceed and len(tasks_to_run) > 1 and task != tasks_to_run[-1]:
                print("Auto-proceeding to next task...")
                time.sleep(1)
            else:
                print("\n[FINISH] All tasks completed. Printing summary...")
                break
    
    finally:
        # driver.quit() # Optional: close browser
        pass
    
    # Print Summary Table
    print_summary(results)

    # Save results to file
    with open('results.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    main()
