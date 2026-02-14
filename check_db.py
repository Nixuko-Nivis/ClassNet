import sqlite3
import os

# 获取正确的数据库路径
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
db_path = os.path.join(backend_dir, 'data', 'database', 'classnet.db')

# 连接到数据库
conn = sqlite3.connect(db_path)
c = conn.cursor()

print("=== 数据库表结构 ===")
# 检查表结构
c.execute('PRAGMA table_info(users);')
columns = c.fetchall()
for col in columns:
    print(f"字段名: {col[1]}, 类型: {col[2]}, 是否为空: {col[3]}, 默认值: {col[4]}, 主键: {col[5]}")

print("\n=== 用户数据 ===")
# 检查用户数据
c.execute('SELECT id, username, real_name, email FROM users LIMIT 10;')
users = c.fetchall()
for user in users:
    print(f"ID: {user[0]}, 用户名: {user[1]}, 真实姓名: {user[2]}, 邮箱: {user[3]}")

# 关闭连接
conn.close()
