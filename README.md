# Agentic Web Testing Framework

This repository hosts the evaluation infrastructure for testing web agents against **Ghost CMS**. It uses a robust, modular **Automation Tester** architecture designed for End-to-End (E2E) verification.

## 📂 Directory Structure

*   `app/`: Docker Compose configuration for the Ghost CMS target application.
*   `dataset/`: Contains `tasks.json` (The source of truth for task definitions).
*   `evaluate/`: Core framwork logic.
    *   `automation_tester.py`: The test runner engine.
    *   `evaluator.py`, `matchers.py`: Helper classes for verification.
*   `test_scripts/`: **[WORK AREA]** Contains the Python automation scripts (`test_<id>.py`).
*   `run_tests.py`: CLI entry point to execute tests.
*   `env_config.json`: Environment URLs configuration.

## 🚀 Setup

### 1. Start the Target Application (Ghost CMS)
```bash
cd app
docker compose up -d
```
*   **Frontend**: [http://localhost:2368](http://localhost:2368)
*   **Admin Panel**: [http://localhost:2368/ghost](http://localhost:2368/ghost)
    *   *Credentials*: `admin@example.com` / `VeryAwesomeAdminGuy123@`

### 2. Install Dependencies
```bash
pip install selenium
```

## 🛠️ Usage

### Running Tests
The framework uses `run_tests.py` to discover and execute scripts.

**Run All Tests:**
```bash
python3 run_tests.py --task_id all
```

**Run Specific Test(s):**
```bash
# Single ID
python3 run_tests.py --task_id 20

# Multiple IDs
python3 run_tests.py --task_id "1, 20"
```

**Debug Mode (Visible Browser):**
```bash
python3 run_tests.py --task_id 20 --no-headless
```

## ✍️ Contribution Workflow

### Anatomy of a Test
Each task in `dataset/tasks.json` must have a corresponding script in `test_scripts/` with the filename format `test_<id>.py`.

**Example: `test_scripts/test_20.py`**
```python
class TaskScript:
    def __init__(self, driver, env_config):
        self.driver = driver
        self.env_config = env_config

    def action(self):
        # 1. Perform the task (e.g., Logout)
        self.driver.get(...)
        self.driver.find_element(...).click()

    def verify(self):
        # 2. Verify the result
        return "/signin" in self.driver.current_url
```

### Creating a New Test
1.  Read the task requirement in `dataset/tasks.json`.
2.  Create `test_scripts/test_<id>.py`.
3.  Implement the `scan -> action -> verify` logic.
4.  Run `python3 run_tests.py --task_id <id>` to validate.
