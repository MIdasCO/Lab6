import sqlite3

def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS turnover_overall
                 (id INTEGER PRIMARY KEY,
                  total_revenue REAL,
                  total_profit REAL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS turnover_product
                 (id INTEGER PRIMARY KEY,
                  product TEXT,
                  supply_qty INTEGER,
                  sales_qty INTEGER,
                  remaining INTEGER,
                  revenue REAL,
                  profit_loss REAL,
                  taxes REAL,
                  net_profit REAL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS turnover_category
                 (id INTEGER PRIMARY KEY,
                  category TEXT,
                  supply_qty INTEGER,
                  sales_qty INTEGER,
                  remaining INTEGER,
                  revenue REAL,
                  profit_loss REAL,
                  taxes REAL,
                  net_profit REAL)''')

    # Add more tables for other accountant routes...

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully")
