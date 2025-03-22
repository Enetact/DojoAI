import sqlite3
import json

DB_PATH = "C:\\DeepSeekAI\\ai-git-developer\\memory\\ai_memory.db"

def store_integration_idea(app_name, suggested_integrations):
    """Save integration ideas to AI memory"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS integration_memory 
                      (id INTEGER PRIMARY KEY, app_name TEXT, integrations TEXT)''')

    cursor.execute("INSERT INTO integration_memory (app_name, integrations) VALUES (?, ?)", 
                   (app_name, json.dumps(suggested_integrations)))
    conn.commit()
    conn.close()

def get_integration_suggestions(app_name):
    """Retrieve suggested integrations for an app"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT integrations FROM integration_memory WHERE app_name = ?", (app_name,))
    result = cursor.fetchone()
    conn.close()
    
    return json.loads(result[0]) if result else []

# Example Usage
store_integration_idea("Ticketing System", ["AI Chatbot for Support", "Automated SLA Tracker", "Customer Feedback Analysis"])
suggestions = get_integration_suggestions("Ticketing System")

print("🔗 Suggested Integrations:", suggestions)
