import json
import os
import subprocess

from duckduckgo_search import ddg


def execute_command(command_name, arguments):
    """
    Execute a command with optional arguments.
    """
    command_mapping = {
        "google": lambda: google_search(arguments["query"]),
        "add_simple_task": lambda: add_simple_task(arguments["task"]),
        "add_complex_task": lambda: add_complex_task(arguments["task"]),
        "list_tasks": lambda: list_tasks(),
        "read_from_file": lambda: read_from_file(arguments["file"]),
        "write_to_file": lambda: write_to_file(arguments["file"], arguments["text"]),
        "append_to_file": lambda: append_to_file(arguments["file"], arguments["text"]),
        "delete_file": lambda: delete_file(arguments["file"]),
        "search_files": lambda: search_files(arguments["text"]),
        "execute_shell": lambda: execute_shell(arguments["command_line"]) if cfg.execute_local_commands else "You are not allowed to run local shell commands. To execute shell commands, EXECUTE_LOCAL_COMMANDS must be set to 'True' in your config. Do not attempt to bypass the restriction.",
        "task_complete": lambda: shutdown(),
        "do_nothing": lambda: "No action performed."
    }

    try:
        if command_name in command_mapping:
            return command_mapping[command_name]()
        else:
            return f"Unknown command '{command_name}'. Please refer to the 'COMMANDS' list for available commands and only respond in the specified JSON format."
    except Exception as e:
        return f"Error: {str(e)}"

def google_search(query, num_results=8):
    """
    Perform a Google search and return the top 5 results.
    """
    search_results = list(ddg(query, max_results=num_results))
    return json.dumps(search_results, ensure_ascii=False, indent=4)


def add_simple_task(task):
    """
    Add a simple task to the task list.
    """
    with open("simple_task_list.txt", "a") as f:
        f.write(task + "\n")

    return f"Added task '{task}' to the simple task list."

def add_complex_task(task):
    """
    Add a complex task to the task list.
    """
    with open("complex_task_list.txt", "a") as f:
        f.write(task + "\n")

    return f"Added task '{task}' to the complex task list."

def list_tasks():
    """
    List all tasks in the task list.
    """
    try:
        with open("simple_task_list.txt", "r") as f:
            simple_tasks = f.read()
    except FileNotFoundError:
        simple_tasks = ""

    try:
        with open("complex_task_list.txt", "r") as f:
            complex_tasks = f.read()
    except FileNotFoundError:
        complex_tasks = ""

    return f"Simple tasks:\n{simple_tasks}\nComplex tasks:\n{complex_tasks}"

def read_from_file(file):
    """
    Read a file.
    """
    with open(file, "r") as f:
        return f"File {file}. Content: {f.read()}"

def write_to_file(file, text):
    """
    Write text to a file.
    """
    with open(file, "w") as f:
        f.write(text)

    return f"File {file}. Content: {text}"

def append_to_file(file, text):
    """
    Append text to a file.
    """
    with open(file, "a") as f:
        f.write(text)

    return f"File {file}. Appended: {text}"

def delete_file(file):
    """
    Delete a file.
    """
    os.remove(file)
    return f"Deleted file {file}."

def search_files(text):
    """
    Search all files for a string.
    """
    files = os.listdir()
    results = []
    for file in files:
        with open(file, "r") as f:
            if text in f.read():
                results.append(file)

    return f"Search results: {results}"

def execute_shell(command_line):
    """
    Execute a shell command.
    """
    result = subprocess.run(command_line, capture_output=True, shell=True)
    return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def shutdown():
    """
    Task is done. Stop the agent.
    """
    exit(0)

