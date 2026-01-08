# Agent Instruction Prompt: Automated Web Testing Framework

## 1. Repository Purpose
This repository hosts an **Automated Web Testing Framework** for the Ghost CMS application.
The goal is **NOT** to manually perform tests, but to **engineer automated Python scripts** that perform and verify these tests.

**Key Components:**
- `dataset/tasks.json`: The source of truth for all test definitions (Description, Start URL, ID).
- `evaluate/automation_tester.py`: The core engine that runs the scripts.
- `run_tests.py`: The CLI entry point to execute the suite.
- `test_scripts/`: The directory where YOU will populate `test_<id>.py` files.

## 2. Agent Workflow Protocol

### ⚠️ Critical Constraints
1. **Retry Limit**: You have a maximum of **3 attempts** to fix a failing test script. If it fails 3 times, move on.
2. **Verification Standard**: The `verify()` method **MUST** strictly base its logic on `evaluate.evaluator.py` and `evaluate.matchers.py`.
    - Retrieve the `eval` object from `dataset/tasks.json` for the specific task.
    - Import the appropriate Matcher (e.g., `from evaluate.matchers import DOMMatcher`).
    - Use the matcher to validate the result. **Do NOT use ad-hoc assertions.**
3. **Credentials**: If a task requires login, you **MUST** retrieve the username and password from the `env_config.json` (available as `self.env_config` in the script). Do NOT hardcode credentials.
4. **Dynamic Evaluation**: Do NOT hardcode evaluation parameters (like `match_value`) in `verify()`. You **MUST** read `dataset/tasks.json`, find the current task by its ID, and extract the `eval` configuration dynamically.
5. **Clean test script**: Do NOT write any comments in the test script.
6. **Virtual Environment**: You **MUST** use a virtual environment to run the tests. Do NOT use a global environment.

### Step 1: Analyze the Task
- Read `dataset/tasks.json`.
- Identify the target Task ID (e.g., `20`).
- Understand the Goal (e.g., "Log out of the system") and the required verification.

### Step 2: Explore & Research
- Use your Browser Tool to navigate to the Ghost CMS instance.
- **Perform the task manually** to understand the user flow.
- **Inspect the DOM** to identify stable CSS selectors (IDs, Classes, Attributes) for every interaction (Click, Type, Wait).
- Note down:
    - Pre-requisites (Do I need to be logged in first?)
    - Trigger actions (Which button causes the change?)
    - Verification signals (What visual element confirms success? E.g., URL change, toaster message, modal).

### Step 3: Implement the Script
- Create a new file: `test_scripts/test_<ID>.py` (e.g., `test_scripts/test_20.py`).
- **Strictly Follow** the format defined in `test_scripts/REQUIREMENTS.md`.
- Implement two methods:
    - `action(self)`: All Selenium commands to reach the state.
    - `verify(self)`: **MUST** use `evaluate.matchers` as defined in Critical Constraints.
- **Constraint**: The script must be self-contained. If the task requires login, the script must handle login (or check if already logged in) within `action()`.

### Step 4: Verify & Iterate
- Run the test: `python3 run_tests.py --task_id <ID>`
- If `❌ FAIL`:
    - **Self-Correction Policy**: You are authorized to fix your own mistakes.
    - Read the error trace or failure screenshot (if available).
    - Analyze if the specific DOM selector failed or if the wait time was too short.
    - **Edit the script** to fix the issue.
    - **Retry Limit**: You may attempt to fix and re-run the test up to **3 times**.
    - If it still fails after 3 attempts, mark it as FAILED and move on.
- If `✅ PASS`:
    - Move to the next task.

## 3. Useful Commands
- Run a specific test: `python3 run_tests.py --task_id 20`
- Run all tests: `python3 run_tests.py --task_id all`
- Run with visible browser (debug): `python3 run_tests.py --task_id 20 --no-headless`
