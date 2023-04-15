from promptgenerator import PromptGenerator


def get_prompt():
    """
    This function generates a prompt string that includes various constraints,
    commands, resources, and performance evaluations.

    Returns:
        str: The generated prompt string.
    """

    # Initialize the PromptGenerator object
    prompt_generator = PromptGenerator()

    # Add constraints to the PromptGenerator object
    prompt_generator.add_constraint(
        "~4000 word limit for short term memory. Your short term memory is "
        "short, so immediately save important information to files."
    )
    prompt_generator.add_constraint(
        "If you are unsure how you previously did something or want to recall "
        "past events, thinking about similar events will help you remember."
    )
    prompt_generator.add_constraint("No user assistance")
    prompt_generator.add_constraint(
        'Exclusively use the commands listed in '
        'double quotes e.g. "command name"'
    )

    # Define the command list
    commands = [
        ("Google Search", "google", {"query": "<search>"}),
        ("Add Simple Task", "add_simple_task", {"task": "<task>"}),
        ("Add Complex Task", "add_complex_task", {"task": "<task>"}),
        ("List Tasks", "list_tasks", {}),
        ("Write to file", "write_to_file",
            {"file": "<file>", "text": "<text>"}),
        ("Read from file", "read_from_file", {"file": "<file>"}),
        ("Append to file", "append_to_file",
            {"file": "<file>", "text": "<text>"}),
        ("Delete file", "delete_file", {"file": "<file>"}),
        ("Search Files", "search_files", {"text": "<text>"}),
        ("Execute Shell Command, non-interactive commands only",
            "execute_shell", {"command_line": "<command_line>"}),
        ("Task Complete (Shutdown)", "task_complete", {"reason": "<reason>"}),
        ("Do Nothing", "do_nothing", {}),
    ]

    # Add commands to the PromptGenerator object
    for command_label, command_name, args in commands:
        prompt_generator.add_command(command_label, command_name, args)

    # Add resources to the PromptGenerator object
    prompt_generator.add_resource(
        "Internet access for searches and information gathering."
    )
    prompt_generator.add_resource("Long Term memory management.")
    prompt_generator.add_resource(
        "A task list to add simple and complex tasks to."
    )
    prompt_generator.add_resource(
        "File system for storing and retrieving information."
    )
    prompt_generator.add_resource("A shell for executing commands.")

    # Add performance evaluations to the PromptGenerator object
    prompt_generator.add_performance_evaluation(
        "Continuously review and analyze your actions to ensure you are "
        "performing to the best of your abilities."
    )
    prompt_generator.add_performance_evaluation(
        "Constructively self-criticize your "
        "big-picture behavior constantly."
    )
    prompt_generator.add_performance_evaluation(
        "Reflect on past decisions and strategies to refine your approach."
    )
    prompt_generator.add_performance_evaluation(
        "Every command has a cost, so be smart and efficient. Aim to complete "
        "tasks in the least number of steps."
    )

    return prompt_generator.generate_prompt_string()
