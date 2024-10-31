convert jupyter notebook to py
jupyter nbconvert --to script notebook.ipynb
# Database setup for feedback
conn = sqlite3.connect("feedback.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        thumbs_up BOOLEAN,
        comment TEXT
    )
""")