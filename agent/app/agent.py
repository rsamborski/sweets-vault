# ruff: noqa
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import vertexai

from .app_utils.utils import load_prompt_from_file
from .app_utils.hw_interface import HardwareInterface
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models import Gemini
from google.adk.tools.tool_context import ToolContext
from google.genai import types

# Task configuration
TASKS_CONFIG = {
    "A": "Reading one page of a book",
    "B": "Calligraphy (writing letters in a workbook)",
}

# Pull variables from .env file
load_dotenv()
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = location
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# Initialize Vertex AI
vertexai.init(project=project_id, location=location)

# Initialize the HW interface and lock the drawers
AGENT_LANGUAGE = os.getenv("AGENT_LANGUAGE", "en")
user_names = ["Maria", "Jan"] if AGENT_LANGUAGE == "pl" else ["Mary", "James"]
hw_interface = HardwareInterface(user_names)

def unlock_drawer(id: int, user_name: str) -> str:
    """Unlock a drawer by its ID.

    Args:
        id: The ID of the drawer to unlock.
        user_name: The name of the user.

    Returns:
        A string with the drawer unlock status.
    """
    if id in [0, 1]:
        hw_interface.unlock_drawer(id)

        logging.info(f"Drawer {id} unlocked for {user_name}")
        return f"Drawer {id} unlocked for {user_name}"
    logging.error("Drawer not found")
    return "Drawer not found"


def _get_task_status(user_key: str, task_id: str, tool_context: ToolContext) -> bool:
    """Retrieves the completion status for a specific task from the flat state."""
    state_key = f"user_tasks_{user_key}_{task_id}"
    return tool_context.state.get(state_key, False)


def _set_task_status(user_key: str, task_id: str, is_done: bool, tool_context: ToolContext):
    """Saves the completion status for a specific task and ensures all user/task 
    combinations are explicitly represented in the flat tool_context.state.
    """
    # First, update the specific target task in the current tool state
    target_key = f"user_tasks_{user_key}_{task_id}"
    tool_context.state[target_key] = is_done
    
    # Now, ensure every possible combination for all known users exists in the flat state.
    all_sync_updates = {}
    for name in user_names:
        u_key = name.lower()
        for t_id in TASKS_CONFIG:
            key = f"user_tasks_{u_key}_{t_id}"
            # If the key isn't already in the current state, default it to False.
            # Otherwise, keep its existing value.
            all_sync_updates[key] = tool_context.state.get(key, False)
    
    # Apply all values back to the flat state
    tool_context.state.update(all_sync_updates)
    logging.info(f"Synchronized all task state values. Updated {target_key} to {is_done}")


def get_progress(user_name: str, tool_context: ToolContext) -> str:
    """Check the progress of tasks for a specific user.

    Args:
        user_name: The name of the user.

    Returns:
        A formatted string listing tasks and their completion status.
    """
    user_key = user_name.lower()
    logging.info(f"Checking progress for {user_name}")

    status_msg = f"Progress for {user_name}:\n"
    for task_id, desc in TASKS_CONFIG.items():
        is_done = _get_task_status(user_key, task_id, tool_context)
        state_str = "✅ DONE" if is_done else "❌ PENDING"
        status_msg += f"- [{task_id}] {desc}: {state_str}\n"

    return status_msg


def complete_task(user_name: str, task_id: str, tool_context: ToolContext) -> str:
    """Mark a task as completed for a user.

    Args:
        user_name: The name of the user.
        task_id: The ID of the task to mark as complete (e.g., 'A', 'B').

    Returns:
        A status message indicating success or showing remaining tasks.
    """
    user_key = user_name.lower()
    logging.info(f"Marking task {task_id} as complete for {user_name}")

    # Mark task as complete
    if task_id in TASKS_CONFIG:
        _set_task_status(user_key, task_id, True, tool_context)
    else:
        logging.error(f"Task ID '{task_id}' not found.")
        return f"Error: Task ID '{task_id}' not found."

    # Check if ALL tasks are complete
    all_complete = True
    remaining = []
    for t_id in TASKS_CONFIG:
        if not _get_task_status(user_key, t_id, tool_context):
            all_complete = False
            remaining.append(t_id)

    if all_complete:
        logging.info(f"All tasks completed for {user_name}")
        return (
            f"SUCCESS: All tasks completed for {user_name}! "
            "You may now unlock the drawer."
        )

    # If not all complete, show progress
    logging.info(f"Remaining tasks: {remaining}")
    return (
        f"Task {task_id} marked as DONE. "
        f"Remaining tasks: {', '.join(remaining)}."
    )


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        #model="gemini-live-2.5-flash-native-audio",   # for actual live-api
        model="gemini-2.5-flash",   # for testing with `adk web`
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=load_prompt_from_file(f"sweet-vault-agent-{AGENT_LANGUAGE}.txt"),
    tools=[get_progress, complete_task, unlock_drawer],
)

app = App(root_agent=root_agent, name="app")
