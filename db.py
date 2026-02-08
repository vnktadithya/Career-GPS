import sqlite3

def create_connection():
    return sqlite3.connect("users.db", check_same_thread=False)

# -------------------------
# User data management
# -------------------------
def create_user_table():
    conn = create_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        email TEXT,
                        password TEXT
                    )''')
    conn.commit()
    conn.close()

def register_user(username, email, password):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                       (username, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# -------------------------
# Progress tracking
# -------------------------
def create_progress_table():
    conn = create_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS progress (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        week INTEGER,
                        goal TEXT,
                        completed BOOLEAN DEFAULT 0,
                        suggestions TEXT,
                        UNIQUE(username, week, goal)
                    )''')
    conn.commit()
    conn.close()

def store_progress(username, week, goal, completed=False, suggestions=None):
    week = int(week)
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO progress (username, week, goal, completed, suggestions)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(username, week, goal)
            DO UPDATE SET completed=excluded.completed,
                          suggestions=COALESCE(excluded.suggestions, progress.suggestions)
        ''', (username, week, goal, completed, suggestions))
        conn.commit()
    except Exception as e:
        print("Error in store_progress:", e)
    finally:
        conn.close()

def get_progress(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT week, goal, completed, suggestions FROM progress WHERE username = ? ORDER BY week", (username,))
    progress = cursor.fetchall()
    conn.close()
    return [(int(week), goal, completed, suggestions) for week, goal, completed, suggestions in progress]

def delete_single_goal(username, week, goal):
    week = int(week)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM progress WHERE username = ? AND week = ? AND goal = ?", (username, week, goal))
    conn.commit()
    conn.close()