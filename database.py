import sqlite3
from .database import User

def create_db():
    """初始化資料庫和資料表"""
    try:
        # with 可以自動管理資源與清理
        with sqlite3.connect("test.db") as conn:
            cursor = conn.cursor()
            # 使用 IF NOT EXISTS 避免在資料表已存在時發生錯誤
            # 使用 INTEGER PRIMARY KEY 讓 id 成為自動遞增的主鍵
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS USERS(
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )
                    """)
    except sqlite3.Error as e:
        print(f"資料庫操作發生錯誤: {e}")

def create_user(user : User):
    """新增一位使用者到資料庫。"""
    try:
        # with 可以自動管理資源與清理
        with sqlite3.connect("test.db") as conn:
            cursor = conn.cursor()
            # 將要插入的數值作為 execute 方法的第二個參數傳遞
            # 這可以安全地處理使用者輸入，防止 SQL 注入
            cursor.execute("""
                           INSERT INTO USERS (username, password)
                           VALUES (?, ?)
                        """, (user.username, user.password))
    except sqlite3.Error as e:
        print(f"資料庫操作發生錯誤: {e}")

def user_login(username : str, password : str):
    try:
        with sqlite3.connect("test.db") as conn:
            cursor = conn.cursor()
            # 錯誤示範：使用 f-string 直接組合 SQL 字串，會導致 SQL Injection
            # cursor.execute(f"SELECT * FROM USERS WHERE username = '{username}' AND password = '{password}'")
            
            # 正確做法：使用參數化查詢，將變數作為元組傳入
            cursor.execute("""
                           SELECT * FROM USERS
                           WHERE username = ? AND password = ?
                        """, (username, password))
            user = cursor.fetchone()
            if user:
                return True
            else:
                return False
    except sqlite3.Error as e:
        print(f"資料庫操作發生錯誤: {e}")

if __name__ == "__main__":
    create_db()
