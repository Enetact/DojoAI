import json
from llm_manager import ask_agent

AGENT_TASKS = {
    "initializer": "Read all files and set up missing dependencies.",
    "planner": "Design the application structure and delegate tasks.",
    "frontend": "Create UI components using React.",
    "backend": "Develop backend APIs with Golang.",
    "database": "Optimize SQL queries and manage data storage.",
    "record_keeper": "Verify integration and learning accuracy."
}

def assign_task(agent):
    """Send a request to the correct LLM based on their role"""
    task = AGENT_TASKS.get(agent, "No task assigned.")
    response = ask_agent(agent, task)
    print(f" {agent} - Task: {task}\n📝 Response: {response}\n")

if __name__ == "__main__":
    for agent in AGENT_TASKS.keys():
        assign_task(agent)
