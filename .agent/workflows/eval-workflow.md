---
description: Mandatory workflow for task analysis, browser research, script implementation, execution, and self-correction for Ghost CMS automated testing.
---

## Mandatory Agent Workflow

**constraint**: This workflow **MUST** be followed exactly for every task.

---

### Step 1: Task Analysis

1.  **Action**: Open `dataset/tasks.json`.
2.  **Action**: Locate the task by its **Task ID**.
3.  **Action**: Extract and understand:
    - **Start URL**
    - **Task description**
    - **Evaluation configuration**
4.  **Critical**: Identify the success criteria **strictly** from the `eval` configuration.

---

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

---

### Step 3: Script Implementation

1.  **Constraint**: Create **exactly one** Playwright script: `test_scripts/test_<TASK_ID>.py`.
2.  **Constraint**: Follow `test_scripts/REQUIREMENTS.md` **exactly**.
3.  **Constraint**: Implement **exactly one** method:
    - `action(self)`
4.  `action(self)`:
    - **Content**: Contains **all** browser automation logic.
    - **Responsibility**: Handles navigation, login (**CRITICAL** if require_login equals true), and user interactions.
    - **Prohibition**: **MUST NOT** perform validation.
    - **CRITICAL**: **MUST** use `page.wait_for_load_state("networkidle")` or `page.wait_for_selector(...)` after any action that triggers navigation or DOM updates (**including starting "signin" redirection**). Do NOT rely on implicit waits.
5.  `verify(self)`:
    - **Content**: Uses the **EXACT SAME SETUP** as `test_scripts/REQUIREMENTS.md`.
6.  **Ensure**:
    - **CRITICAL**: **No comments**.
    - **CRITICAL**: **No hardcoded values**.
    - **CRITICAL**: **No logic outside required methods**.

---

### Step 4: Execute Test

**Action**: Run the test using:

```bash
python run_tests.py --task_id <TASK_ID>
```

---

### Step 5: Self-Correction (If FAIL)

1.  **Action**: Inspect the error trace (Note: script timeouts after 30s).
2.  **Analyze**: Identify the root cause:
    - Missing authentication step?
    - Incorrect vs unstable selector?
    - Insufficient wait vs timing issue?
3.  **Action**: Modify the script to fix the issue.
4.  **Action**: Re-run the test.
5.  **Constraint**: You may repeat this process up to **3 total attempts**.

---

### Step 6: Completion

- **If PASS**:
  - **Action**: Proceed to the next task.
- **If FAIL** after 3 attempts:
  - **Action**: Mark the task as **FAILED**.
  - **Action**: Proceed to the next task.
