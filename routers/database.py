import sqlite3
from .models import User
import hashlib
import re
import os
 
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
                        salt TEXT NOT NULL,
                        password TEXT NOT NULL
                    )
                    """)
            return True
    except sqlite3.Error as e:
        print(f"資料庫操作發生錯誤: {e}")
        return False

def create_user(username : str, password : str):
    """新增一位使用者到資料庫。"""
    try:
        # with 可以自動管理資源與清理
        with sqlite3.connect("test.db") as conn:
            cursor = conn.cursor()
            # 檢查使用者是否已存在          用元組傳進去，否則會被當成字串(每個字元都當成一個參數傳進去導致錯誤)
            cursor.execute("SELECT * FROM USERS WHERE username = ?", (username,))
            is_user_exists  = cursor.fetchone()
            if is_user_exists:
                print(f"使用者 {username} 已存在，無法重複建立。")
                return False
            # 檢查密碼強度
            if not is_password_strong(password):
                print("密碼強度不足，必須包含數字、小寫字母、大寫字母，且長度介於8到16之間。")
                return False
            # 產生一個 salt 並將密碼轉換為雜湊值儲存
            salt = os.urandom(16).hex() # 產生一個 16-byte 的 salt
            hashed_password = get_hashed_password(password, salt)

            cursor.execute("""
                           INSERT INTO USERS (username, salt, password)
                           VALUES (?, ?, ?)
                        """, (username, salt, hashed_password))
            return True
    except sqlite3.Error as e:
        print(f"資料庫操作發生錯誤: {e}")
        return False

def user_login(username : str, password : str):
    """使用者登入   """
    try:
        with sqlite3.connect("test.db") as conn:
            cursor = conn.cursor()
            # 根據 username 取得 salt 和儲存的 hashed_password
            cursor.execute("SELECT salt, password FROM USERS WHERE username = ?", (username,))
            result = cursor.fetchone()
            if not result:
                print(f"使用者 {username} 不存在。")
                return False
            # 取得 salt 和儲存的雜湊密碼
            salt, stored_hash = result
            # 使用相同的 salt 和輸入的密碼計算雜湊值
            incoming_hash = get_hashed_password(password, salt)
 
            # 使用恆定時間比較演算法來比較輸入的雜湊密碼與儲存的雜湊密碼是否相同 (防範Timing Attack)
            return hashlib.timing_safe_compare(incoming_hash, stored_hash)
    except sqlite3.Error as e:
        print(f"資料庫操作發生錯誤: {e}")

def update_user_password(username : str, old_password : str, new_password : str):
    """更新使用者密碼"""
    try:
        with sqlite3.connect("test.db") as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT salt, password FROM USERS WHERE username = ?", (username,))
            result = cursor.fetchone()
            # 檢查使用者是否存在
            if (not result):
                print(f"使用者 {username} 不存在。")
                return False
            salt, stored_hash = result
            old_password_hash = get_hashed_password(old_password, salt)
            # 比對舊密碼是否正確
            if not hashlib.timing_safe_compare(old_password_hash, stored_hash):
                print("舊密碼不正確。")
                return False
            # 檢查新密碼強度
            if not is_password_strong(new_password):
                print("新密碼強度不足，必須包含數字、小寫字母、大寫字母，且長度介於8到16之間。")
                return False
            # 產生新的salt
            new_salt = os.urandom(16).hex()
            new_hashed_password = get_hashed_password(new_password, new_salt)
            
            cursor.execute("""
                            UPDATE USERS 
                            SET salt = ?, password = ?
                            WHERE username = ?
            """, (new_salt, new_hashed_password, username))
            return True
    except sqlite3.Error as e:
        print(f"資料庫操作發生錯誤: {e}")
        return False

def is_password_strong(password : str):
    """檢查密碼強度"""
    # 從頭檢查 *\d是否有數字、*[a-z]是否有小寫字母、*[A-Z]是否有大寫字母
    # .{8,16}表示長度介於8到16之間
    
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,16}$"
    if re.findall(pattern, password):
        return True
    else:
        return False

def get_hashed_password(password : str, salt : str):
    """產生密碼的雜湊值"""
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()

if __name__ == "__main__":
    create_db()