import os
import subprocess
import sys
import time
import ctypes
import logging

# Define paths
SCRIPTS_PATH = "C:\\DeepSeekAI\\ai-git-developer\\scripts"
WEB_UI_PATH = "C:\\DeepSeekAI\\ai-git-developer\\web_ui"
LOG_FILE = "C:\\DeepSeekAI\\logs\\deepseek_setup.log"

# Ensure script runs as admin
def is_admin():
    """Check if the script is running as an administrator."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_script(script_name, log_message):
    """Run a Python script and check for errors."""
    try:
        print(f"🔹 Running: {script_name} - {log_message}")
        result = subprocess.run([sys.executable, script_name], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f" Error in {script_name}: {e.stderr}")
        logging.error(f"Error running {script_name}: {e.stderr}")
        return False
    return True

def restart_service(service_name):
    """Restart a Windows service (if needed)."""
    try:
        subprocess.run(["net", "stop", service_name], check=True)
        time.sleep(2)
        subprocess.run(["net", "start", service_name], check=True)
        print(f" Restarted service: {service_name}")
    except subprocess.CalledProcessError as e:
        print(f" Failed to restart {service_name}: {e}")

def main():
    """Run all DeepSeek setup steps in order with troubleshooting."""
    if not is_admin():
        print(" DeepSeek Setup needs to be run as an administrator.")
        print(" Restarting script as admin...")
        subprocess.run(["powershell", "Start-Process", "python", f'"{sys.argv[0]}"', "-Verb", "RunAs"])
        sys.exit()

    print("\n Starting DeepSeek AI Full Setup...\n")

    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

    setup_steps = [
        (f"{SCRIPTS_PATH}\\create_folder_structure.py", "Creating necessary folders"),
        (f"{SCRIPTS_PATH}\\setup_environment.py", "Installing dependencies & setting up environment"),
        (f"{SCRIPTS_PATH}\\load_chat_history.py", "Embedding chat history into AI memory"),
        (f"{SCRIPTS_PATH}\\ai_initializer.py", "Initializing AI and executing setup"),
        (f"{SCRIPTS_PATH}\\task_scheduler.py", "Assigning tasks to AI agents"),
        (f"{SCRIPTS_PATH}\\api_server.py", "Starting local API for AI communication"),
        (f"{WEB_UI_PATH}\\chat.py", "Launching Chat UI for DeepSeek"),
        (f"{WEB_UI_PATH}\\dashboard.py", "Starting Web Dashboard for AI Monitoring")
    ]

    for script, description in setup_steps:
        if not run_script(script, description):
            print(f" Error detected in {script}. Attempting to troubleshoot...\n")
            restart_service("wuauserv")  # Restart Windows Update Service (if dependency issues occur)
            restart_service("Spooler")   # Restart Print Spooler (if Python dependencies need reloading)
            print(f" Setup paused due to an error in {script}. Please check {LOG_FILE} for details.")
            sys.exit(1)

    print("\n DeepSeek AI Setup Completed Successfully! 🚀")
    print(" Chat UI available at: http://localhost:8081")
    print(" Web Dashboard available at: http://localhost:8080")

if __name__ == "__main__":
    main()
