import pyodbc
from queue import Queue, Empty
from threading import Lock

from plantCategory import CategoryDao
from plantConservation import PlantConservationDAO
import plantPest, PlantInfo
from plantMonitor import MonitoringDataDao, MonitoringPersonnelDao, MonitoringDao


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


class Factory:
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool

    def create_pest_dao(self):
        return plantPest.PestDiseaseDAO(self.connection_pool)

    def create_pesticide_dao(self):
        return plantPest.PesticideDAO(self.connection_pool)

    def create_pest_pesticide_dao(self):
        return plantPest.PestDiseasePesticideDAO(self.connection_pool)

    def create_category_dao(self):
        return CategoryDao(self.connection_pool)

    def create_conservation_dao(self):
        return PlantConservationDAO(self.connection_pool)

    def create_plant_dao(self):
        return PlantInfo.PlantDAO(self.connection_pool)

    def create_monitoring_data_dao(self):
        return MonitoringDataDao(self.connection_pool)

    def create_personnel_data_dao(self):
        return MonitoringPersonnelDao(self.connection_pool)

    def create_monitoring_dao(self):
        return MonitoringDao(self.connection_pool)
