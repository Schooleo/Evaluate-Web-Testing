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

Your primary job is to systematically convert each task in `dataset/tasks.json` into a working Python automation script.

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
    - `verify(self)`: Selenium commands to return `True` or `False`.
- **Constraint**: The script must be self-contained. If the task requires login, the script must handle login (or check if already logged in) within `action()`.

### Step 4: Verify & Iterate
- Run the test: `python3 run_tests.py --task_id <ID>`
- If `❌ FAIL`:
    - Read the error/screenshot.
    - Debug using your Browser Tool.
    - Update the script.
- If `✅ PASS`:
    - Move to the next task.

## 3. Useful Commands
- Run a specific test: `python3 run_tests.py --task_id 20`
- Run all tests: `python3 run_tests.py --task_id all`
- Run with visible browser (debug): `python3 run_tests.py --task_id 20 --no-headless`
