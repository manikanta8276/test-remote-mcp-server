from fastmcp import FastMCP
import os
import sqlite3

DB_Path = os.path.join(os.path.dirname(__file__), "expense.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")  # Fix 5

mcp = FastMCP("Expense_tracker")

def init_db():
    with sqlite3.connect(DB_Path) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS expense(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT DEFAULT '',
            note TEXT DEFAULT ''
        )""")

init_db()

@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    """ADD a New expense entry to the database"""
    with sqlite3.connect(DB_Path) as c:
        cur = c.execute(
            "INSERT INTO expense(date, amount, category, subcategory, note) VALUES(?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
    return {"status": "ok", "id": cur.lastrowid}

@mcp.tool()
def list_expense(start_date, end_date):
    with sqlite3.connect(DB_Path) as c:
        cur = c.execute(
            "SELECT id,date,amount,category,subcategory,note FROM expense WHERE date BETWEEN ? AND ? ORDER BY id ASC",
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def summarize(start_date, end_date, category=None):
    """Summarize expense by category within an inclusive date range"""
    with sqlite3.connect(DB_Path) as c:
        query = """SELECT category, SUM(amount) AS total_amount 
                   FROM expense WHERE date BETWEEN ? AND ?"""  # Fix 4
        params = [start_date, end_date]
        if category:
            query += " AND category = ?"  # Fix 1: space before AND
            params.append(category)
        query += " GROUP BY category"  # Fix 4
        cur = c.execute(query, params)  # Fix 3: removed stray `c`
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]  # Fix 2: dict() not dict[]

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:  # Fix 5
        return f.read()




if __name__ == "__main__":
    mcp.run()