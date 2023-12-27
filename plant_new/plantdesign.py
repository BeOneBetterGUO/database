import pyodbc
from queue import Queue, Empty
from threading import Lock

from plantCategory import CategoryDao
from plantConservation import PlantConservationDAO


# 数据库名：plantdesign
# 创建连接池
class ConnectionPool:
    def __init__(self, server, database, pool_size=5):
        self.server = server
        self.database = database
        self.pool_size = pool_size
        self.conn_queue = Queue(maxsize=pool_size)  # 使用 maxsize 限制队列大小
        self.lock = Lock()  # 添加锁以确保线程安全
        self._create_connections()

    def _create_connections(self):
        with self.lock:  # 使用锁确保线程安全
            for _ in range(self.pool_size):
                conn = self._create_new_conn()
                self.conn_queue.put(conn)

    def _create_new_conn(self):
        return pyodbc.connect(
            'DRIVER={SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + ';Trusted_Connection=yes;'
        )
    def _put_conn(self, conn):
        self.conn_queue.put(conn)

    def _get_conn(self):
        try:
            # 使用锁确保在获取连接时的线程安全
            with self.lock:
                conn = self.conn_queue.get(timeout=5)
        except Empty:
            print("Connection pool is empty")
            conn = self._create_new_conn()
        return conn

    def exec_sql(self, sql, values=None):
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                if values:
                    cur.execute(sql, values)
                elif "SELECT" in sql.upper():
                    cur.execute(sql)
                    return cur.fetchall()
                else:
                    cur.execute(sql)
                    return None  # 对于非 SELECT 查询，返回 None
        finally:
            self._put_conn(conn)

    def exec_sql_with_commit(self, sql, values=None):
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                if values:
                    cur.execute(sql, values)
                else:
                    cur.execute(sql)
            conn.commit()  # 提交事务
        finally:
            self._put_conn(conn)

    def exec_sql_with_params(self, sql, params):
        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                if "SELECT" in sql.upper():
                    return cur.fetchall()
                else:
                    return None  # 对于非 SELECT 查询，返回 None
        finally:
            self._put_conn(conn)

    def get_connection(self):
        return self._get_conn()  # 直接调用 _get_conn 方法

    def return_connection(self, conn):
        self._put_conn(conn)  # 直接调用 _put_conn 方法

class Factory:
    def __init__(self, server, database, pool_size=5):
        self.connection_pool = ConnectionPool(server, database, pool_size)

    def create_category_dao(self):
        return CategoryDao(self.connection_pool)

    def create_conservation_dao(self):
        return PlantConservationDAO(self.connection_pool)

#菜单
class plantMenu:
    @staticmethod
    def menu():
        print("植物管理系统")
        print("1. 植物基本信息管理")
        print("2. 植物分类管理")
        print("3. 植物养护管理")
        print("4. 植物监测测管理")
        print("5. 植物病虫害防治管理 ")
    @staticmethod
    def choice():
        try:
            choice=int(input("请选择要执行的业务："))
            return choice
        except ValueError:
            print('请输入有效指令！')
            return None


class User:
    def __init__(self, username, password, role='普通用户'):
        self.username = username
        self.password = password
        self.role = role

    def __str__(self):
        return f"User: {self.username}, Role: {self.role}"

# Global variable to store the current user
current_user = None

class UserManager:
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool

    def login(self, username, password):
        global current_user
        # 在用户表中验证用户名和密码
        query = f"SELECT * FROM 用户 WHERE 账户名='{username}' AND 密码='{password}'"
        result = self.connection_pool.exec_sql(query)

        if result:
            # 登录成功，创建User对象
            user_info = result[0]  # 假设查询结果只有一条记录
            role = user_info.身份  # Assuming 身份 is a column in the table

            # if role == '管理员':
            #    role = '管理员'
            # elif role == '主管':
            #   role = '主管'
            # elif role == '养护人员':
            #    role = '养护人员'
            # elif role == '监测人员':
            #   role = '监测人员'

            current_user = User(username, password, role)
            print(f"用户 {username} 登录成功！角色：{role}")
            return True
        else:
            print("用户名或密码错误。登录失败。")
            return False
