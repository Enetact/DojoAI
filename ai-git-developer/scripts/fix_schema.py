import sqlite3

DB_PATH = "C:/DeepSeekAINonGit/ai-git-developer/ai_memory.db"

def fix_conversations_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Check for table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'")
        if not cursor.fetchone():
            print("Creating missing 'conversations' table...")
            cursor.execute("""
                CREATE TABLE conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id INTEGER,
                    message TEXT,
                    response TEXT
                );
            """)
        else:
            # Check for missing columns
            cursor.execute("PRAGMA table_info(conversations);")
            existing_columns = {col[1] for col in cursor.fetchall()}
            required_columns = {"agent_id", "message", "response"}

            missing = required_columns - existing_columns
            for col in missing:
                print(f"Adding missing column: {col}")
                cursor.execute(f"ALTER TABLE conversations ADD COLUMN {col} TEXT")

        conn.commit()
        print("✅ Schema verified and fixed.")

if __name__ == "__main__":
    fix_conversations_table()
