import sqlite3
import os

# 获取正确的数据库路径
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
db_path = os.path.join(backend_dir, 'data', 'database', 'classnet.db')

# 连接到数据库
conn = sqlite3.connect(db_path)
c = conn.cursor()

print("=== 清除用户账户 ===")

# 检查当前用户数量
c.execute('SELECT COUNT(*) FROM users;')
user_count = c.fetchone()[0]
print(f"当前用户数量: {user_count}")

if user_count > 0:
    # 删除所有用户记录
    c.execute('DELETE FROM users;')
    conn.commit()
    
    # 验证删除结果
    c.execute('SELECT COUNT(*) FROM users;')
    new_user_count = c.fetchone()[0]
    print(f"删除后用户数量: {new_user_count}")
    print("所有用户账户已成功清除!")
else:
    print("数据库中没有用户账户，无需清除。")

# 关闭连接
conn.close()
