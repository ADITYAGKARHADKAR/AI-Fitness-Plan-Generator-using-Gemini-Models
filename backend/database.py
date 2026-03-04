import sqlite3
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_PATH = "database/fitbuddy.db"


def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def initialize_database():
    """Create tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            weight REAL NOT NULL,
            goal TEXT NOT NULL,
            intensity TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Plans table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            workout_plan TEXT NOT NULL,
            nutrition_tip TEXT,
            feedback TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()
    logger.info("✅ Database initialized successfully!")


# ─────────────────────────────────────────────
# USER CRUD OPERATIONS
# ─────────────────────────────────────────────

def insert_user(name: str, age: int, weight: float, goal: str, intensity: str) -> int:
    """Insert a new user and return the user ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (name, age, weight, goal, intensity, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, age, weight, goal, intensity, datetime.now().isoformat()))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    logger.info(f"✅ User inserted with ID: {user_id}")
    return user_id


def get_user(user_id: int) -> dict:
    """Fetch a user by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


# ─────────────────────────────────────────────
# PLAN CRUD OPERATIONS
# ─────────────────────────────────────────────

def insert_plan(user_id: int, workout_plan: str, nutrition_tip: str = None) -> int:
    """Insert a new plan and return the plan ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO plans (user_id, workout_plan, nutrition_tip, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, workout_plan, nutrition_tip,
          datetime.now().isoformat(), datetime.now().isoformat()))
    conn.commit()
    plan_id = cursor.lastrowid
    conn.close()
    logger.info(f"✅ Plan inserted with ID: {plan_id}")
    return plan_id


def get_plan_by_user(user_id: int) -> dict:
    """Fetch the latest plan for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM plans WHERE user_id = ?
        ORDER BY created_at DESC LIMIT 1
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def update_plan(plan_id: int, new_plan: str, feedback: str) -> bool:
    """Update an existing plan with feedback and regenerated content."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE plans
        SET workout_plan = ?, feedback = ?, updated_at = ?
        WHERE id = ?
    """, (new_plan, feedback, datetime.now().isoformat(), plan_id))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    logger.info(f"✅ Plan {plan_id} updated successfully!")
    return updated