# Evaluate-Web-Testing

This repository contains the evaluation infrastructure for testing web agents against **Ghost CMS**. It is based on the WebAppEval benchmark structure.

## Directory Structure

- `app/`: Contains the Docker Compose configuration for Ghost CMS.
- `dataset/`: Contains `tasks.json` with 20 evaluation tasks.
- `evaluate/`: Contains the evaluation logic (matchers, evaluator).
- `run_eval_example.py`: A helper script to interactively run and verify tasks.
- `env_config.json`: Configuration for target environment URLs.

## Prerequisites

- **Docker** & **Docker Compose**: To run the Ghost CMS application.
- **Python 3.x**: To run the evaluation script.
- **Selenium**: `pip install selenium`

## Setup

1.  **Start the Application Environment**:
    Navigate to the `app` directory and start the containers.

    ```bash
    cd app
    docker compose up -d
    ```

    Wait a moment for Ghost CMS to Initialize. You can access it at:

    - Frontend: [http://localhost:8080](http://localhost:8080)
    - Admin Panel: [http://localhost:8080/ghost](http://localhost:8080/ghost)
      - **Email**: `admin@example.com` (you may need to set this up on first run)
      - **Password**: `password` (you may need to set this up on first run)

    > **Note**: If this is the _very first time_ running Ghost, you might need to go to [http://localhost:8080/ghost](http://localhost:8080/ghost) and create the initial admin account manually to match the credentials expected by the tasks (User: `admin@example.com`, Pass: `password`), or update `dataset/tasks.json` to match your credentials.

2.  **Install Python Dependencies**:
    ```bash
    pip install selenium
    ```

## Running Evaluation

We provide an interactive script `run_eval_example.py` that allows you to act as the "Agent" (or hook up your own agent) to perform tasks and verify them.

1.  **Run the script**:

    ```bash
    python run_eval_example.py
    ```

2.  **Select a Task**:
    The script will prompt you for a **Task ID** (1-20). Refer to `dataset/tasks.json` for details.
3.  **Perform the Action**:
    A Chrome browser window will open controlled by Selenium.
    - Read the task description in your terminal.
    - Perform the required action manually in the browser.
4.  **Verify**:
    Return to your terminal and press **Enter**. The script will run the configured matchers (URL, String, DOM, etc.) and report `✅ PASSED` or `❌ FAILED`.

## Adding New Tasks

To add new tasks, edit `dataset/tasks.json`. Each task follows this schema:

```json
{
  "task_id": "21",
  "task_description": "Description of what to do",
  "task_type": "operation",
  "start_url": "__GHOST_ADMIN__",
  "eval": {
    "eval_type": ["dom_match"],
    "dom_match": {
      "url": "last",
      "dom_extractor": "document.body.innerText",
      "match_type": "contains",
      "match_value": "Success Message",
      "description": "Verify that the success message is visible."
    }
  }
}
```
