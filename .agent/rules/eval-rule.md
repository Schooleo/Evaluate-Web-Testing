---
trigger: always_on
glob: "Evaluate-Web-Testing/**/*"
description: Non-negotiable rules governing automated web test generation, execution, and evaluation for Ghost CMS.
---

## Global Evaluation Rules (Authoritative)

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
