import pyodbc
from queue import Queue, Empty
from threading import Lock

# 数据库名：plantdesign
# 创建连接池
class ConnectionPool:
    def __init__(self, server, database, UID, PWD, pool_size=5):
        self.server = server
        self.database = database
        self.pool_size = pool_size
        self.UID = UID
        self.PWD = PWD
        self.conn_queue = Queue(maxsize=pool_size)  # 使用 maxsize 限制队列大小
        self.lock = Lock()  # 添加锁以确保线程安全
        self._create_connections()

    def _create_connections(self):
        with self.lock:  # 使用锁确保线程安全
            for _ in range(self.pool_size):
                conn = self._create_new_conn()
                self.conn_queue.put(conn)

    def _create_new_conn(self):
        # return pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};'
        #                       f'UID={self.UID};PWD={self.PWD}')
        connectionString = f'DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.UID};PWD={self.PWD}'
        return pyodbc.connect(connectionString)

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


# 封装PlantInfo基本信息类
class PlantInfo:
    def __init__(self, plant_id, plant_name, alias, scientific_family, scientific_species, morphological_features,
                 cultivation_points, pest_control_measures, application_value):
        self.plant_id = plant_id  # 植物编号
        self.plant_name = plant_name  # 植物名称
        self.alias = alias  # 别名
        self.scientific_family = scientific_family  # 科名
        self.scientific_species = scientific_species  # 种名
        self.morphological_features = morphological_features  # 形态特征
        self.cultivation_points = cultivation_points  # 栽培技术要点
        self.pest_control_measures = pest_control_measures  # 病虫害防治措施
        self.application_value = application_value  # 应用价值




