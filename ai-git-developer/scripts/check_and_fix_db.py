import sqlite3
import os
import json

DB_PATH = "C:/DeepSeekAI/ai-git-developer/memory/ai_memory.db"
BACKUP_PATH = "C:/DeepSeekAI/ai-git-developer/memory/ai_memory_backup.db"

EXPECTED_TABLES = {
    "agents": """
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
    """,
    "conversations": """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            agent_id INTEGER,
            message TEXT NOT NULL,
            embedding_id INTEGER,
            FOREIGN KEY (agent_id) REFERENCES agents(id),
            FOREIGN KEY (embedding_id) REFERENCES embeddings(id)
        );
    """,
    "embeddings": """
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vector BLOB NOT NULL,
            metadata JSON
        );
    """,
    "api_requests": """
        CREATE TABLE IF NOT EXISTS api_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            request JSON NOT NULL,
            response JSON NOT NULL
        );
    """,
}

def backup_database():
    """Creates a backup of the database before modifying anything."""
    if os.path.exists(DB_PATH):
        os.makedirs(os.path.dirname(BACKUP_PATH), exist_ok=True)
        os.replace(DB_PATH, BACKUP_PATH)
        print(f"Backup created: {BACKUP_PATH}")

def check_and_fix_database():
    """Ensures all required tables exist in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = {row[0] for row in cursor.fetchall()}

    missing_tables = [table for table in EXPECTED_TABLES if table not in existing_tables]

    if missing_tables:
        print(f"Missing tables detected: {', '.join(missing_tables)}")
        for table in missing_tables:
            cursor.execute(EXPECTED_TABLES[table])
            print(f"Created missing table: {table}")

        conn.commit()
    else:
        print("All required tables exist.")

    conn.close()

def check_agents():
    """Ensures that at least one AI agent exists in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM agents")
    count = cursor.fetchone()[0]

    if count == 0:
        print("No AI agents found. Adding default agent.")
        cursor.execute("INSERT INTO agents (name) VALUES ('initializer')")
        conn.commit()

    conn.close()

if __name__ == "__main__":
    print("Checking AI Memory Database...")

    # Step 1: Backup the database
    backup_database()

    # Step 2: Ensure the schema is correct
    check_and_fix_database()

    # Step 3: Ensure AI agents exist
    check_agents()

    print("AI Database Check & Fix Completed!")
