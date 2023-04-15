import json
import os

import openai
from commands import execute_command
from dotenv import load_dotenv
from prompt import get_prompt


def test_api_key(api_key):
    try:
        openai.api_key = api_key
        openai.Engine.list()
        print("API key is valid.")
    except openai.error.AuthenticationError:
        print("API key is invalid. Please check your OpenAI API key.")
        exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit()


class GPTAgent:
    def __init__(self, api_key, model, goals, temperature=0.5, max_tokens=2000,
                 n=1, stop=None):
        openai.api_key = api_key
        self.model = model
        self.goals = goals
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.n = n
        self.stop = stop
        self.conversation_history = []
        self.memory = []

    def generate_response(self):
        prompt = get_prompt()
        prompt = (
            f"{prompt} Your conversation history is: "
            f"{self.conversation_history}"
        )
        prompt = f"{prompt} Your memory is: {self.memory}"
        prompt = f"{prompt} Your goals are: {self.goals}"

        messages = [{"role": "system", "content": prompt}]
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                n=self.n,
                stop=self.stop
            )
        except Exception as e:
            print(f"An error occurred: {e}")

        if response is None:
            raise RuntimeError("Failed to get response from OpenAI API.")

        self.conversation_history.append(response)
        return response.choices[0].message.content

    def memory(self, action, memory=None):
        if action == "list":
            return self.memory
        elif action == "add":
            self.memory.append(memory)
        elif action == "remove":
            self.memory.remove(memory)
        elif action == "clear":
            self.memory = []


if __name__ == "__main__":
    # Load default environment variables (.env)
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    assert OPENAI_API_KEY, (
        "OPENAI_API_KEY environment variable is missing from .env"
    )

    FAST_MODEL = os.getenv("FAST_MODEL", "gpt-3.5-turbo")
    SMART_MODEL = os.getenv("SMART_MODEL", "gpt-4")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")

    test_api_key(OPENAI_API_KEY)

    goals = [
        "Maximize profit",
        "Minimize cost",
        "Run multiple online businesses",
    ]

    task_list = []

    gpt_agent = GPTAgent(OPENAI_API_KEY, SMART_MODEL, goals)

    while True:
        response = gpt_agent.generate_response()
        print(f"{response}")

        response = json.loads(response)
        print(f"{response}")

        # Execute command
        if response["command"] is not None:
            result = execute_command(response["command"]["name"],
                                     response["command"]["args"])
            print(f"Command result: {result}")
            gpt_agent.conversation_history.append(result)
