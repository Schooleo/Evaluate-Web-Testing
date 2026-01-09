# Agent Instruction Prompt: Automated Web Testing Framework

## 1. Repository Purpose

This repository hosts an **Automated Web Testing Framework** for the Ghost CMS application.
The goal is **NOT** to manually perform tests, but to **engineer automated Python scripts** that perform and verify these tests.

**Key Components:**

- `dataset/tasks.json`: The source of truth for all test definitions (Description, Start URL, ID).
- `evaluate/automation_tester.py`: The core engine that runs the scripts.
- `run_tests.py`: The CLI entry point to execute the suite.
- `test_scripts/`: The directory where YOU will populate `test_<id>.py` files.

## 2. Global Evaluation Rules (Authoritative)

### 1. Retry Limit and Failure Handling

- **Constraint**: You may attempt to fix a failing test script a maximum of **3 times**.
- **Action**: After 3 failed attempts, the task **MUST** be marked as FAILED in your internal tracking.
- **Action**: You **MUST** immediately move on to the next task.

### 2. Verification Authority

- **Constraint**: The `verify()` method **MUST** use ONLY evaluation logic provided by `evaluate.evaluator` and `evaluate.matchers`.
- **Constraint**: Ad-hoc assertions, manual comparisons, `assert` statements, or custom validation logic are **STRICTLY FORBIDDEN**.
- **Constraint**: Verification **MUST** delegate to `matcher.match(page, config)`.

### 3. Dynamic Evaluation Configuration

- **Constraint**: Measurement values (text, selectors, URLs) **MUST** be read dynamically from `dataset/tasks.json` at runtime.
- **Constraint**: Hardcoding expected values, selectors, or URLs in the test script is **STRICTLY FORBIDDEN**.
- **Action**: You **MUST** locate the task by its ID in `dataset/tasks.json` and extract its `eval` configuration.

### 4. Credentials Handling

- **Constraint**: Credentials **MUST** be retrieved from `env_config.json` (available as `self.env_config`).
- **Constraint**: Hardcoding usernames, passwords, or tokens is **STRICTLY FORBIDDEN**.

### 5. Script Cleanliness

- **Constraint**: Test scripts **MUST** contain **ZERO COMMENTS**.
- **Constraint**: Docstrings are allowed only for the class and methods standardly defined in `REQUIREMENTS.md`.
- **Constraint**: Inline comments, explanations, or commented-out code are **FORBIDDEN**.

### 6. Environment Constraints

- **Constraint**: Tests **MUST** be executed inside the provided virtual environment.
- **Constraint**: Usage of global Python environment is **FORBIDDEN**.

### 7. Script Scope and Isolation

- **Constraint**: Each script **MUST** be fully self-contained.
- **Constraint**: If login/setup is required, it **MUST** be performed within the `action()` method of that specific script.
- **Constraint**: Shared state, external dependencies, or reliance on previous test runs is **FORBIDDEN**.

### 8. Structural Compliance

- **Constraint**: You **MUST** create **exactly one** Playwright script per task named `test_scripts/test_<TASK_ID>.py`.
- **Constraint**: You **MUST** strictly adhere to the class structure defined in `test_scripts/REQUIREMENTS.md`.
- **Constraint**: The class **MUST** be named `TaskScript`.
- **Constraint**: The class **MUST** implement **exactly two** methods: `action(self)` and `verify(self)`.
- **Constraint**: The `__init__` method **MUST** accept `(self, page, env_config)`.

### 9. Browser Interaction and Logic Separation

- **Constraint**: The `action(self)` method **MUST** contain **all** browser automation logic (navigation, login, interactions).
- **Constraint**: The `action(self)` method **MUST NOT** perform any validation or verification.
- **Constraint**: You **MUST** use `page.wait_for_load_state("networkidle")` or `page.wait_for_selector(...)` after any action that triggers navigation or DOM updates.
- **Constraint**: Reliance on implicit waits is **FORBIDDEN**.

## 3. Mandatory Agent Workflow

**constraint**: This workflow **MUST** be followed exactly for every task.

### Step 1: Task Analysis

1.  **Action**: Open `dataset/tasks.json`.
2.  **Action**: Locate the task by its **Task ID**.
3.  **Action**: Extract and understand:
    - **Start URL**
    - **Task description**
    - **Evaluation configuration**
4.  **Critical**: Identify the success criteria **strictly** from the `eval` configuration.

### Step 2: Explore & Research (Browser Tool Required)

1.  **Action**: Use the **Browser Control subagent** to manually navigate the Ghost CMS UI.
2.  **Action**: Perform the task manually to understand the real user flow.
3.  **Action**: Inspect the DOM to identify **stable selectors**:
    - **Prefer**: element IDs.
    - **Then**: data-attributes.
    - **Avoid**: fragile or positional selectors.
4.  **Determine**:
    - **Required login state**
    - **Proper wait times between page loads**
    - **Trigger actions**
    - **Observable success signals** (DOM changes, URL changes, messages)

### Step 3: Script Implementation

1.  **Constraint**: Create **exactly one** Playwright script: `test_scripts/test_<TASK_ID>.py`.
2.  **Constraint**: Follow `test_scripts/REQUIREMENTS.md` **exactly**.
3.  **Constraint**: Implement **exactly two** methods:
    - `action(self)`
    - `verify(self)`
4.  `action(self)`:
    - **Content**: Contains **all** browser automation logic.
    - **Responsibility**: Handles navigation, login (if required), and user interactions.
    - **Prohibition**: **MUST NOT** perform validation.
    - **CRITICAL**: **MUST** use `page.wait_for_load_state("networkidle")` or `page.wait_for_selector(...)` after any action that triggers navigation or DOM updates (including "signin" redirection). Do NOT rely on implicit waits.
5.  `verify(self)`:
    - **Content**: Uses **ONLY** `evaluate.matchers`.
    - **Input**: Reads evaluation configuration **dynamically** from `dataset/tasks.json` via `self.env_config` or passed arguments (via `Evaluator`).
    - **Output**: Performs final validation returning `True` or `False`.
6.  **Ensure**:
    - **CRITICAL**: **No comments**.
    - **CRITICAL**: **No hardcoded values**.
    - **CRITICAL**: **No logic outside required methods**.

### Step 4: Execute Test

**Action**: Run the test using:

```bash
python run_tests.py --task_id <TASK_ID>
```

### Step 5: Self-Correction (If FAIL)

1.  **Action**: Inspect the error trace (Note: script timeouts after 30s).
2.  **Analyze**: Identify the root cause:
    - Missing authentication step?
    - Incorrect vs unstable selector?
    - Insufficient wait vs timing issue?
3.  **Action**: Modify the script to fix the issue.
4.  **Action**: Re-run the test.
5.  **Constraint**: You may repeat this process up to **3 total attempts**.

### Step 6: Completion

- **If PASS**:
  - **Action**: Proceed to the next task.
- **If FAIL** after 3 attempts:
  - **Action**: Mark the task as **FAILED**.
  - **Action**: Proceed to the next task.

## 4. Useful Commands

- Run a specific test: `python3 run_tests.py --task_id 20`
- Run all tests: `python3 run_tests.py --task_id all`
- Run with visible browser (debug): `python3 run_tests.py --task_id 20 --no-headless`
