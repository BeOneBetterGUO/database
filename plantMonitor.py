import pyodbc
import plantdesign
from queue import Queue, Empty

def init():
    connection_pool = plantdesign.ConnectionPool('127.0.0.1',"plantdesign",'chosen','123456')
    create_table_plant_info = """
        CREATE TABLE PlantInfo (
        plant_id varchar(50) PRIMARY KEY,
        plant_name VARCHAR(255) NOT NULL,
        alias VARCHAR(255),
        scientific_family VARCHAR(255),
        scientific_species VARCHAR(255),
        morphological_features TEXT,
        cultivation_points TEXT,
        pest_control_measures TEXT,
        application_value TEXT
    );"""
    connection_pool.exec_sql_with_commit(create_table_plant_info)

class ConnectionPool:
    def __init__(self, server, database, pool_size=5):
        self.server = server
        self.database = database
        self.pool_size = pool_size
        self.conn_queue = Queue()
        self._create_connections()

    def _create_connections(self):
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
        conn = self.conn_queue.get()
        if conn is None:
            self._create_new_conn()
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

    def exec_sql2(self, sql, values=None):
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
                    return None  # For non-SELECT queries, return None
        finally:
            self._put_conn(conn)

    def get_connection(self):
        try:
            conn = self.conn_queue.get(timeout=5)
        except Empty:
            print("Connection pool is empty")
            conn = self._create_new_conn()
        return conn

    def return_connection(self, conn):
        self.conn_queue.put(conn)
class MonitoringData:
    def __init__(self, monitoring_id, plant_id, abnormal_condition, creator, creation_time, update_time, light,
                 temperature, humidity):
        self.monitoring_id = monitoring_id             #监测数据编号
        self.plant_id = plant_id                       #植物编号
        self.abnormal_condition = abnormal_condition   #异常情况
        self.creator = creator                         #创建人员
        self.creation_time = creation_time             #创建时间
        self.update_time = update_time                 #更新时间
        self.light = light                             #光照
        self.temperature = temperature                 #温度


# 监测人员
class MonitoringPersonnel:
    def __init__(self, personnel_id, personnel_name):
        self.personnel_id = personnel_id               #工号
        self.personnel_name = personnel_name           #姓名
# 监测
class Monitoring:
    def __init__(self, check_id, monitoring_id, monitoring_time, monitoring_location, detection_device):
        self.monitoring_id = monitoring_id             #监测记录编号
        self.check_id = check_id                       #监测数据编号
        self.monitoring_time = monitoring_time         #监测时间
        self.monitoring_location = monitoring_location #监测地点
        self.detection_device = detection_device       #监测设备

class MonitoringDataDao:
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool

    def get_monitoring_data_by_id(self, monitoring_id):
        query = f"SELECT * FROM 监测数据 WHERE 监测数据编号 = {monitoring_id}"
        result = self.connection_pool.exec_sql(query)

        # 检查 result 是否是列表且非空
        if isinstance(result, list) and result:
            # 假设列表中只有一条数据
            row = result[0]

            if row:
                monitoring_data = MonitoringData(
                    monitoring_id=row[0],
                    plant_id=row[1],
                    abnormal_condition=row[2],
                    creator=row[3],
                    creation_time=row[4],
                    update_time=row[5],
                    light=row[6],
                    temperature=row[7],
                    humidity=row[8]
                )
            return monitoring_data
        else:
            return None

    def display_all_monitoring_data_from_db(self):
        query = "SELECT * FROM 监测数据"
        result = self.connection_pool.exec_sql(query)

        monitoring_data_list = []
        for row in result:
            monitoring_data = MonitoringData(
                monitoring_id=row[0],
                plant_id=row[1],
                abnormal_condition=row[2],
                creator=row[3],
                creation_time=row[4],
                update_time=row[5],
                light=row[6],
                temperature=row[7],
                humidity=row[8]
            )
            monitoring_data_list.append(monitoring_data)

        return monitoring_data_list

    # 插入
    def add_monitoring_data(self, monitoring_data):
        query = f"INSERT INTO 监测数据 (植物编号, 异常情况, 创建人员, 创建时间, 更新时间, 光照, 温度, 湿度) VALUES ( '{monitoring_data.plant_id}', '{monitoring_data.abnormal_condition}', '{monitoring_data.creator}', '{monitoring_data.creation_time}', '{monitoring_data.update_time}', '{monitoring_data.light}', '{monitoring_data.temperature}', '{monitoring_data.humidity}')"
        self.connection_pool.exec_sql2(query)

    # 删除
    def delete_monitoring_data(self, monitoring_id):
        query = f"DELETE FROM 监测数据 WHERE 监测数据编号 = '{monitoring_id}'"
        self.connection_pool.exec_sql2(query)

    # 更新
    def update_monitoring_data(self, monitoring_data):
        query = "UPDATE 监测数据 SET "

        if monitoring_data.abnormal_condition is not None:
            query += f"异常情况 = '{monitoring_data.abnormal_condition}', "

        if monitoring_data.update_time is not None:
            query += f"更新时间 = '{monitoring_data.update_time}', "

        if monitoring_data.light is not None:
            query += f"光照 = '{monitoring_data.light}', "

        if monitoring_data.temperature is not None:
            query += f"温度 = '{monitoring_data.temperature}', "

        if monitoring_data.humidity is not None:
            query += f"湿度 = '{monitoring_data.humidity}' "

        # 移除最后一个逗号和空格
        query = query.rstrip(', ')

        # 添加 WHERE 子句
        query += f"WHERE 监测数据编号 = {monitoring_data.monitoring_id}"

        self.connection_pool.exec_sql2(query)

    # 查询
    def search_monitoring_data(self, **search_criteria):
        query = "SELECT * FROM 监测数据 WHERE"

        for attribute, keyword in search_criteria.items():
            if keyword:
                query += f" {attribute} LIKE '%{keyword}%' AND"

        # 移除最后一个 AND
        query = query.rstrip(' AND')

        result = self.connection_pool.exec_sql(query)

        monitoring_data_list = []
        for row in result:
            monitoring_data = MonitoringData(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            monitoring_data_list.append(monitoring_data)

        return monitoring_data_list

    def get_temperature_aggregated_values(self):
        query = "SELECT MAX(温度) AS 最高温度, AVG(温度) AS 平均温度 FROM 监测数据"
        result = self.connection_pool.exec_sql(query)
        # 处理查询结果...
        return result  # 返回的是一个包含温度聚合值的结果集



    def get_light_aggregated_values(self):
        query = "SELECT MAX(光照) AS 最大光照, AVG(光照) AS 平均光照 FROM 监测数据"
        result = self.connection_pool.exec_sql(query)
        # 处理查询结果...
        return result  # 返回的是一个包含光照聚合值的结果集

class MonitoringPersonnelDao:
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool

    # 插入
    def add_personnel_data(self, personnel_data):
        query = f"INSERT INTO 监测人员 (工号, 名称) VALUES ('{personnel_data.personnel_id}', '{personnel_data.personnel_name}')"
        self.connection_pool.exec_sql2(query)

    # 显示信息
    def get_all_personnel_data(self):
        query = "SELECT * FROM 监测人员"
        result = self.connection_pool.exec_sql(query)

        personnel_data_list = []
        for row in result:
            personnel_data = MonitoringPersonnel(row[0], row[1])
            personnel_data_list.append(personnel_data)

        return personnel_data_list

    # 工号查询
    def get_personnel_data_by_id(self, personnel_id):
        query = f"SELECT * FROM 监测人员 WHERE 工号 = '{personnel_id}'"
        result = self.connection_pool.exec_sql(query)

        if result:
            row = result[0]
            personnel_data = MonitoringPersonnel(row[0], row[1])
            return personnel_data
        else:
            return None  # 没有找到对应工号的监测人员信息

    # 删除
    def delete_personnel_data(self, personnel_id):
        query = f"DELETE FROM 监测人员 WHERE 工号 = '{personnel_id}'"
        self.connection_pool.exec_sql2(query)

class MonitoringDao:
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool

    def get_monitoring_by_id(self, monitoring_id):
        query = f"SELECT * FROM 监测 WHERE 监测数据编号 = {monitoring_id}"
        result = self.connection_pool.exec_sql(query)

        # 检查 result 是否是列表且非空
        if isinstance(result, list) and result:
            # 假设列表中只有一条数据
            row = result[0]

            if row:
                monitoring_data = Monitoring(
                    check_id=row[0],
                    monitoring_id=row[1],
                    monitoring_time=row[2],
                    monitoring_location=row[3],
                    detection_device=row[4]
                )
                return monitoring_data
        else:
            return None

    def add_monitoring(self, monitoring_data):
        query = f"INSERT INTO 监测 (监测数据编号, 监测时间, 监测地点, 监测设备) VALUES ('{monitoring_data.monitoring_id}', '{monitoring_data.monitoring_time}', '{monitoring_data.monitoring_location}', '{monitoring_data.detection_device}')"
        self.connection_pool.exec_sql2(query)

    # 显示信息
    def display_all_monitoring_data(self):
        query = "SELECT * FROM 监测"
        result = self.connection_pool.exec_sql(query)

        monitoring_data_list = []
        for row in result:
            monitoring_data = Monitoring(
                check_id=row[0],
                monitoring_id=row[1],
                monitoring_time=row[2],
                monitoring_location=row[3],
                detection_device=row[4]

            )
            monitoring_data_list.append(monitoring_data)

        return monitoring_data_list

    # 更新
    def update_monitoring(self, monitoring):
        query = "UPDATE 监测 SET "

        if monitoring.monitoring_time is not None:
            query += f"监测时间 = '{monitoring.monitoring_time}', "

        if monitoring.monitoring_location is not None:
            query += f"监测地点 = '{monitoring.monitoring_location}', "

        if monitoring.detection_device is not None:
            query += f"监测设备 = '{monitoring.detection_device}', "

        # 移除最后一个逗号和空格
        query = query.rstrip(', ')

        # 添加 WHERE 子句，根据你的数据模型修改条件
        query += f"WHERE 监测数据编号 = '{monitoring.monitoring_id}'"

        self.connection_pool.exec_sql2(query)

    # 查询
    def search_monitoring(self, **search_criteria):
        query = "SELECT * FROM 监测 WHERE"

        for attribute, keyword in search_criteria.items():
            if keyword:
                query += f" {attribute} LIKE '%{keyword}%' AND"
        # 移除最后一个 AND
        query = query.rstrip(' AND')

        result = self.connection_pool.exec_sql(query)

        monitoring_data_list = []
        for row in result:
            monitoring_data = Monitoring(row[0], row[1], row[2], row[3], row[4])
            monitoring_data_list.append(monitoring_data)

        return monitoring_data_list

    # 删除
    def delete_monitoring(self, monitoring_id):
        query = f"DELETE FROM 监测 WHERE 监测数据编号 = '{monitoring_id}'"
        self.connection_pool.exec_sql2(query)

class Factory:
    def __init__(self, server, database, pool_size=5):
        self.connection_pool = ConnectionPool(server, database, pool_size)


    def create_monitoring_data_dao(self):
        return MonitoringDataDao(self.connection_pool)

    def create_personnel_data_dao(self):
        return MonitoringPersonnelDao(self.connection_pool)

    def create_monitoring_dao(self):
        return MonitoringDao(self.connection_pool)

if __name__ == "__main__":
    # 创建DAO工厂对象
    factory = Factory("localhost", "plantdesign")

    # 获取Dao对象
    monitoring_data_dao = factory.create_monitoring_data_dao()
    personnel_data_dao = factory.create_personnel_data_dao()
    monitoring_dao = factory.create_monitoring_dao()


while True:
    print("\n请选择操作:")
    print("1. 查看监测数据表")
    print("2. 查看监测表")
    print("3. 查看监测人员表")
    print("4. 查询")
    print("5. 统计")
    print("6. 退出")

    try:
        operation_choice = int(input("请输入数字选择您要执行的操作: "))

        if operation_choice == 1:
        #显示所有监测数据信息
            all_monitoring_data = monitoring_data_dao.display_all_monitoring_data_from_db()
            print("所有监测数据信息:")
            for monitoring_data in all_monitoring_data:
                            print("\n监测数据信息:")
                            print(f"监测数据编号: {monitoring_data.monitoring_id}")
                            print(f"植物编号: {monitoring_data.plant_id}")
                            print(f"异常情况: {monitoring_data.abnormal_condition}")
                            print(f"创建人员: {monitoring_data.creator}")
                            print(f"创建时间: {monitoring_data.creation_time}")
                            print(f"更新时间: {monitoring_data.update_time}")
                            print(f"光照: {monitoring_data.light}")
                            print(f"温度: {monitoring_data.temperature}")
            pass
        elif operation_choice == 2:
        #执行查看监测表操作
            all_monitoring_data = monitoring_dao.display_all_monitoring_data()

            # 打印显示的监测数据信息
            for monitoring_data in all_monitoring_data:
                print(f"监测记录编号: {monitoring_data.check_id}")
                print(f"监测数据编号: {monitoring_data.monitoring_id}")
                print(f"监测时间: {monitoring_data.monitoring_time}")
                print(f"监测地点: {monitoring_data.monitoring_location}")
                print(f"监测设备: {monitoring_data.detection_device}")

            pass
        elif operation_choice == 3:
            # 执行查看监测人员表操作
            # 显示所有监测人员信息
            all_personnel_data = personnel_data_dao.get_all_personnel_data()
            print("所有监测人员信息:")
            for personnel_data in all_personnel_data:
                print(f"工号: {personnel_data.personnel_id}, 姓名: {personnel_data.personnel_name}")
            pass

        elif operation_choice == 4:
            # 执行查询操作
            print("请选择要查询的表:")
            print("1.监测数据表")
            print("2.监测表")
            print("3.监测人员表")

            table_choice = int(input("请输入表的选择(1/2/3): "))

            if table_choice == 1:
                # 查询监测数据表
                # 查询条件选择
                print("请选择查询条件:")
                print("1.监测数据编号")
                print("2.植物编号")
                print("3.异常情况")
                print("4.创建人员")
                print("5.创建时间")
                print("6.更新时间")
                print("7.光照")
                print("8.温度")

                # 获取用户选择
                search_choice = int(input("请输入查询条件的选择(1-8): "))

                # 根据用户选择构建查询条件
                attribute_names = ["监测数据编号", "植物编号", "异常情况", "创建人员", "创建时间",
                                   "更新时间", "光照", "温度"]
                if 1 <= search_choice <= len(attribute_names):
                    attribute_name = attribute_names[search_choice - 1]
                else:
                    print("无效的查询条件选择，请重新选择。")
                # 结束或其他处理

                # 获取用户输入的查询值
                search_value = input(f"请输入要查询的{attribute_name}值: ")

                # 执行查询
                result = monitoring_data_dao.search_monitoring_data(**{attribute_name: search_value})

                # 显示查询结果
                print("查询结果:")
                for monitoring_data in result:
                    print(f"监测数据编号: {monitoring_data.monitoring_id}")
                    print(f"植物编号: {monitoring_data.plant_id}")
                    print(f"异常情况: {monitoring_data.abnormal_condition}")
                    print(f"创建人员: {monitoring_data.creator}")
                    print(f"创建时间: {monitoring_data.creation_time}")
                    print(f"更新时间: {monitoring_data.update_time}")
                    print(f"光照: {monitoring_data.light}")
                    print(f"温度: {monitoring_data.temperature}")
                    print("-" * 20)  # 用横线分隔每个数据对象的输出



            elif table_choice == 2:
                # 查询监测表
                # 查询条件选择
                print("请选择查询条件:")
                print("1.监测数据编号")
                print("2.监测时间")
                print("3.监测地点")
                print("4.检测设备")

                # 获取用户选择
                search_choice = int(input("请输入查询条件的选择(1-4): "))

                # 根据用户选择构建查询条件
                attribute_names = ["监测数据编号", "监测时间", "监测地点", "检测设备"]
                if 1 <= search_choice <= len(attribute_names):
                    attribute_name = attribute_names[search_choice - 1]
                else:
                    print("无效的查询条件选择，请重新选择。")
                    # 结束或其他处理

                # 获取用户输入的查询值
                search_value = input(f"请输入要查询的{attribute_name}值: ")

                # 执行查询
                result = monitoring_dao.search_monitoring(**{attribute_name: search_value})

                # 显示查询结果
                print("查询结果:")
                for monitoring_info in result:
                    print(f"监测记录编号: {monitoring_info.check_id}")
                    print(f"监测数据编号: {monitoring_info.monitoring_id}")
                    print(f"监测时间: {monitoring_info.monitoring_time}")
                    print(f"监测地点: {monitoring_info.monitoring_location}")
                    print(f"检测设备: {monitoring_info.detection_device}")
                    print("-" * 20)  # 用横线分隔每个数据对象的输出


            elif table_choice == 3:
                # 查询监测人员表
                # 查询监测人员表
                print("请输入监测人员工号进行查询:")
                personnel_id = input("监测人员工号: ")

                result_by_id = personnel_data_dao.get_personnel_data_by_id(personnel_id)

                if result_by_id:
                    print(f"通过工号 {personnel_id} 查询到的监测人员信息:")
                    print(f"工号: {result_by_id.personnel_id}, 姓名: {result_by_id.personnel_name}")
                else:
                    print(f"未找到工号为 {personnel_id} 的监测人员信息")

            else:
                print("无效的表选择，请重新选择。")

        elif operation_choice == 5:
            # 统计指标选择
            print("请选择要统计的指标:")
            print("1.温度")
            print("2.光照")

            # 获取用户选择
            aggregated_choice = int(input("请输入要统计的指标选择(1-2): "))

            # 根据用户选择执行统计操作
            if aggregated_choice == 1:
                temperature_values = monitoring_data_dao.get_temperature_aggregated_values()
                print("温度聚合值（最大值/平均值）:")
                print(temperature_values)

            elif aggregated_choice == 2:
                light_values = monitoring_data_dao.get_light_aggregated_values()
                print("光照聚合值（最大值/平均值）:")
                print(light_values)
            else:
                print("无效的指标选择，请重新选择。")
                # 结束或其他处理

            pass
        elif operation_choice == 6:
            print("退出系统管理员操作。")
            break
        else:
            print("无效的选择，请输入有效的数字。")

    except ValueError:
        print("请输入有效的数字。")


