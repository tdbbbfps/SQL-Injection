from database import create_db, create_user, user_login
from models import User

def main():
    # 1. 初始化資料庫並建立一個範例使用者
    print("--- 系統初始化 ---")
    create_db()
    admin_user = User(id=0, username="admin", password="supersecretpassword")
    create_user(admin_user)
    print(f"已建立使用者: {admin_user.username}\n")

    # 2. 模擬正常但失敗的登入
    print("--- 測試 1: 正常但失敗的登入 ---")
    username_attempt = "admin"
    password_attempt = "wrongpassword"
    print(f"嘗試登入: username='{username_attempt}', password='{password_attempt}'")
    is_logged_in = user_login(username_attempt, password_attempt)
    print(f"登入結果: {'成功' if is_logged_in else '失敗'}\n")

    # 3. 模擬 SQL 注入攻擊
    print("--- 測試 2: SQL 注入攻擊 ---")
    # 注入的 payload，注意後面的 -- 用來註解掉密碼檢查
    malicious_username = "' OR '1'='1' --"
    dummy_password = "password_does_not_matter"
    print(f"嘗試登入: username=\"{malicious_username}\", password='{dummy_password}'")
    is_hacked = user_login(malicious_username, dummy_password)
    print(f"登入結果: {'成功 (被駭入!)' if is_hacked else '失敗'}")


if __name__ == "__main__":
    main()
