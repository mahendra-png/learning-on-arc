from openai import OpenAI
from config import OPEN_API_KEY, MODEL
from memory import Memory
import tools
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MiniClawAgent:
    def __init__(self):
        self.memory = Memory()
    
    def think(self, goal):
        prompt = """
you are an autonomus CLI agent.
Goal: {goal}
Decide next action.
Respond in this format:

ACTION: tool_name
INPUT: tool_input

Available tools:
- read_file(path)
- write_file(path, content)
- run_shell(command)

If goal is complete:
ACTION: finish
"""
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content

    def execute(self, action_text):
        lines = action_text.split("\n")
        action = None
        input_data = None

        for line in lines:
            if line.startswith("ACTION:"):
                action = line.replace("ACTION:", "").strip()
            if line.startswith("INPUT:"):
                input_data = line.replace("INPUT:", "").strip()

        if action == "read_file":
            return tools.read_file(input_data)
        elif action == "write_file":
            return tools.write_file("output.txt", input_data)
        elif action == "run_shell":
            return tools.run_shell(input_data)
        elif action == "finish":
            return "DONE"
        else:
            return "Unknown action"

    def run(self, goal):
        print(" Goal:", goal)

        for step in range(5):  # limit loop
            thought = self.think(goal)
            print("\n Agent says:\n", thought)

            result = self.execute(thought)
            print("\n🔧 Tool result:\n", result)

            if result == "DONE":
                print("Task finished")
                break