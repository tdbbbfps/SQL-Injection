from routers.database import create_db, create_user, user_login
from routers.models import User
import hashlib

def main():
    create_db()
    username = str(input("請輸入欲建立的使用者名稱: "))
    password = str(input("請輸入欲建立的使用者密碼: "))
    print(hashlib.sha256(password.encode('utf-8')).hexdigest())
    # assert create_user(new_user)
    # print("繼續執行程式...")
    if not create_user(username, password):
        return
    print("使用者建立成功!")

    print("--- 測試登入 ---")

    # username 輸入: ' ' OR '1'='1' 因為密碼不等於''，程式會檢查OR後面 '1'='1' 必然是true，會導致 SQL Injection(如果後端直接將字串帶入 SQL 查詢)
    login_username = str(input("請輸入使用者名稱: "))
    login_password = str(input("請輸入使用者密碼: "))
    if not user_login(login_username, login_password):
        return
    print("登入成功!")


if __name__ == "__main__":
    main()
