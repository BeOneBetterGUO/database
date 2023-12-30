class MonitoringData:
    def __init__(self, monitoring_id, plant_id, abnormal_condition, creator, creation_time, update_time, light,
                 temperature):
        self.monitoring_id = monitoring_id  # 监测数据编号
        self.plant_id = plant_id  # 植物编号
        self.abnormal_condition = abnormal_condition  # 异常情况
        self.creator = creator  # 创建人员
        self.creation_time = creation_time  # 创建时间
        self.update_time = update_time  # 更新时间
        self.light = light  # 光照
        self.temperature = temperature  # 温度


# 监测人员
class MonitoringPersonnel:
    def __init__(self, personnel_id, personnel_name):
        self.personnel_id = personnel_id  # 工号
        self.personnel_name = personnel_name  # 姓名


# 监测
class Monitoring:
    def __init__(self, check_id, monitoring_id, monitoring_time, monitoring_location, detection_device):
        self.monitoring_id = monitoring_id  # 监测记录编号
        self.check_id = check_id  # 监测数据编号
        self.monitoring_time = monitoring_time  # 监测时间
        self.monitoring_location = monitoring_location  # 监测地点
        self.detection_device = detection_device  # 监测设备


class MonitoringManager:
    def __init__(self, monitoring_dao, monitoring_personnel_dao, monitoring_data_dao):
        self.monitoring_dao = monitoring_dao
        self.monitoring_personnel_dao = monitoring_personnel_dao
        self.monitoring_data_dao = monitoring_data_dao

    def manage_menu(self):
        while True:
            print("\n请选择操作:")
            print("1. 查看监测数据表")
            print("2. 查看监测表")
            print("3. 查看监测人员表")
            print("4. 查询")
            print("5. 统计")
            print("6. 管理监测数据表")
            print("7. 管理监测表")
            print("8. 管理监测人员表")
            print("9. 退出")

            try:
                operation_choice = int(input("请输入数字选择您要执行的操作: "))

                if operation_choice == 1:
                    # 显示所有监测数据信息
                    all_monitoring_data = self.monitoring_data_dao.display_all_monitoring_data_from_db()
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
                    # 执行查看监测表操作
                    all_monitoring_data = self.monitoring_dao.display_all_monitoring_data()

                    # 打印显示的监测数据信息
                    for monitoring_data in all_monitoring_data:
                        print(f"监测记录编号: {monitoring_data.check_id}")
                        print(f"监测数据编号: {monitoring_data.monitoring_id}")
                        print(f"监测时间: {monitoring_data.monitoring_time}")
                        print(f"监测地点: {monitoring_data.monitoring_location}")
                        print(f"监测设备: {monitoring_data.detection_device}\n")

                    pass
                elif operation_choice == 3:
                    # 执行查看监测人员表操作
                    # 显示所有监测人员信息
                    all_personnel_data = self.monitoring_personnel_dao.get_all_personnel_data()
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

                        while True:
                            # 获取用户选择
                            search_choice = int(input("请输入查询条件的选择(1-8): "))

                            # 根据用户选择构建查询条件
                            attribute_names = ["监测数据编号", "植物编号", "异常情况", "创建人员", "创建时间",
                                               "更新时间", "光照", "温度"]
                            if 1 <= search_choice <= len(attribute_names):
                                attribute_name = attribute_names[search_choice - 1]
                                break
                            else:
                                print("无效的查询条件选择，请重新选择。")
                            # 结束或其他处理

                        # 获取用户输入的查询值
                        search_value = str(input(f"请输入要查询的{attribute_name}值: "))

                        # 执行查询
                        result = self.monitoring_data_dao.search_monitoring_data(**{attribute_name: search_value})

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

                        while True:
                            # 获取用户选择
                            search_choice = int(input("请输入查询条件的选择(1-4): "))

                            # 根据用户选择构建查询条件
                            attribute_names = ["监测数据编号", "监测时间", "监测地点", "检测设备"]
                            if 1 <= search_choice <= len(attribute_names):
                                attribute_name = attribute_names[search_choice - 1]
                                break
                            else:
                                print("无效的查询条件选择，请重新选择。")
                            # 结束或其他处理

                        # 获取用户输入的查询值
                        search_value = input(f"请输入要查询的{attribute_name}值: ")

                        # 执行查询
                        result = self.monitoring_dao.search_monitoring(**{attribute_name: search_value})

                        # 显示查询结果
                        print("查询结果:")
                        for monitoring_info in result:
                            print(f"监测记录编号: {monitoring_info.check_id}")
                            print(f"监测数据编号: {monitoring_info.monitoring_id}")
                            print(f"监测时间: {monitoring_info.monitoring_time}")
                            print(f"监测地点: {monitoring_info.monitoring_location}")
                            print(f"检测设备: {monitoring_info.detection_device}\n")
                            print("-" * 20)  # 用横线分隔每个数据对象的输出

                    elif table_choice == 3:
                        # 查询监测人员表
                        print("请输入监测人员工号进行查询:")
                        personnel_id = input("监测人员工号: ")

                        result_by_id = self.monitoring_personnel_dao.get_personnel_data_by_id(personnel_id)

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
                        temperature_values = self.monitoring_data_dao.get_temperature_aggregated_values()
                        print("温度聚合值（最大值/平均值）:")
                        print(temperature_values)
                    elif aggregated_choice == 2:
                        light_values = self.monitoring_data_dao.get_light_aggregated_values()
                        print("光照聚合值（最大值/平均值）:")
                        print(light_values)
                    else:
                        print("无效的指标选择，请重新选择。")
                        # 结束或其他处理

                    pass
                elif operation_choice == 6:
                    # 用户选择管理方式
                    print("请选择管理方式:")
                    print("1.增加")
                    print("2.修改")
                    print("3.删除")

                    # 获取用户选择
                    management_choice = int(input("请输入管理方式选择(1-3): "))

                    if management_choice == 1:
                        # 获取用户输入的属性值

                        plant_id = int(input("请输入植物编号: "))
                        abnormal_condition = input("请输入异常情况描述: ")
                        creator = input("请输入创建人员: ")
                        creation_time = input("请输入创建时间: ")
                        update_time = input("请输入更新时间: ")
                        light = input("请输入光照数据: ")
                        temperature = input("请输入温度数据: ")

                        # 创建 MonitoringData 对象
                        new_monitoring_data = MonitoringData(
                            monitoring_id='1',
                            plant_id=plant_id,
                            abnormal_condition=abnormal_condition,
                            creator=creator,
                            creation_time=creation_time,
                            update_time=update_time,
                            light=light,
                            temperature=temperature
                        )

                        # 插入到数据库
                        self.monitoring_data_dao.add_monitoring_data(new_monitoring_data)
                        print("监测数据已成功添加。")

                        pass
                    elif management_choice == 2:

                        # 获取用户输入的监测数据编号
                        monitoring_id_to_update = int(input("请输入要更新的监测数据编号: "))

                        # 查询数据库获取当前监测数据的信息
                        monitoring_data_to_update = self.monitoring_data_dao.get_monitoring_data_by_id(
                            monitoring_id_to_update)

                        # 如果监测数据存在，允许用户选择要更新的属性
                        if monitoring_data_to_update:
                            print("请选择要更新的属性:")
                            print("1.异常情况描述")
                            print("2.更新时间")
                            print("3.光照数据")
                            print("4.温度数据")

                            # 获取用户选择
                            attribute_choice = int(input("请输入要更新的属性选择(1-4): "))

                            # 根据用户选择更新相应的属性
                            if attribute_choice == 1:
                                monitoring_data_to_update.abnormal_condition = input("请输入新的异常情况描述: ")
                            elif attribute_choice == 2:
                                monitoring_data_to_update.update_time = input("请输入新的更新时间: ")

                            elif attribute_choice == 3:
                                monitoring_data_to_update.light = input("请输入新的光照数据: ")
                            elif attribute_choice == 4:
                                monitoring_data_to_update.temperature = input("请输入新的温度数据: ")
                            else:
                                print("无效的属性选择，请重新选择。")
                                # 结束或其他处理

                            # 调用 update_monitoring_data 方法进行更新
                            self.monitoring_data_dao.update_monitoring_data(monitoring_data_to_update)
                            print("监测数据已成功更新。")
                        else:
                            print(f"监测数据编号 {monitoring_id_to_update} 不存在。")

                        pass
                    elif management_choice == 3:
                        monitoring_id_to_update = int(input("请输入要删除的监测数据编号: "))
                        monitoring_data_to_update = self.monitoring_data_dao.get_monitoring_data_by_id(
                            monitoring_id_to_update)

                        if monitoring_data_to_update:
                            self.monitoring_data_dao.delete_monitoring_data(monitoring_id_to_update)
                            print("监测数据已删除更新。")
                        else:
                            print(f"监测数据编号 {monitoring_id_to_update} 不存在。")
                        pass
                    else:
                        print("无效的管理方式选择，请重新选择。")

                # 结束或其他处理
                elif operation_choice == 7:
                    # 用户选择管理方式
                    print("请选择管理方式:")
                    print("1.增加")
                    print("2.修改")
                    print("3.删除")

                    # 获取用户选择
                    management_choice = int(input("请输入管理方式选择(1-3): "))
                    if management_choice == 1:
                        # 用户选择增加信息到监测表

                        # 获取用户输入的监测数据信息
                        monitoring_id = input("请输入监测数据编号: ")
                        monitoring_time = input("请输入监测时间: ")
                        monitoring_location = input("请输入监测地点: ")
                        detection_device = input("请输入检测设备: ")

                        # 创建 Monitoring 对象
                        new_monitoring_data = Monitoring(
                            check_id='1',
                            monitoring_id=monitoring_id,
                            monitoring_time=monitoring_time,
                            monitoring_location=monitoring_location,
                            detection_device=detection_device
                        )

                        # 插入到监测表
                        self.monitoring_dao.add_monitoring(new_monitoring_data)
                        print("监测数据已成功添加到监测表。")

                    if management_choice == 2:
                        # 获取用户输入的监测数据编号
                        monitoring_id_to_update = int(input("请输入要更新的监测数据编号: "))

                        # 查询数据库获取当前监测数据的信息
                        monitoring_data_to_update = self.monitoring_dao.get_monitoring_by_id(monitoring_id_to_update)

                        # 如果监测数据存在，允许用户选择要更新的属性
                        if monitoring_data_to_update:
                            print("请选择要更新的属性:")
                            print("1.监测时间")
                            print("2.监测地点")
                            print("3.检测设备")

                            # 获取用户选择
                            attribute_choice = int(input("请输入要更新的属性选择(1-3): "))

                            # 根据用户选择更新相应的属性
                            if attribute_choice == 1:
                                monitoring_data_to_update.monitoring_time = input("请输入新的监测时间: ")
                            elif attribute_choice == 2:
                                monitoring_data_to_update.monitoring_location = input("请输入新的监测地点: ")
                            elif attribute_choice == 3:
                                monitoring_data_to_update.detection_device = input("请输入新的检测设备: ")
                            else:
                                print("无效的属性选择，请重新选择。")
                                # 结束或其他处理

                                # 调用 update_monitoring 方法进行更新
                            self.monitoring_dao.update_monitoring(monitoring_data_to_update)
                            print("监测数据已成功更新。")
                        else:
                            print(f"监测数据编号 {monitoring_id_to_update} 不存在.")
                    if management_choice == 3:
                        monitoring_id_to_update = int(input("请输入要删除的监测数据编号: "))
                        monitoring_data_to_update = self.monitoring_dao.get_monitoring_by_id(monitoring_id_to_update)

                        if monitoring_data_to_update:
                            self.monitoring_dao.delete_monitoring(monitoring_id_to_update)
                            print("监测信息已删除更新。")
                        else:
                            print(f"监测数据编号 {monitoring_id_to_update} 不存在。")

                        pass
                    else:
                        print("无效的管理方式选择，请重新选择。")

                elif operation_choice == 8:
                    print("管理检测人员")
                    print("1.添加")
                    print("2.删除")
                    # 获取用户选择
                    attribute_choice = int(input("请输入要更新的属性选择(1-3): "))

                    # 根据用户选择更新相应的属性
                    if attribute_choice == 1:
                        personnel_name = input("请输入姓名：")
                        self.monitoring_personnel_dao.add_personnel_data(personnel_name)
                    elif attribute_choice == 2:
                        personnel_id = input("请输入工号：")
                        self.monitoring_personnel_dao.delete_personnel_data(personnel_id)
                    else:
                        print("无效的属性选择，请重新选择。")

                elif operation_choice == 9:
                    print("退出系统管理员操作。")
                    break
                else:
                    print("无效的选择，请输入有效的数字。")


            except ValueError:
                print("请输入有效的数字。")


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
            monitoring_data = MonitoringData(
                monitoring_id=row[0],
                plant_id=row[1],
                abnormal_condition=row[2],
                creator=row[3],
                creation_time=row[4],
                update_time=row[5],
                light=row[6],
                temperature=row[7],
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
            )
            monitoring_data_list.append(monitoring_data)

        return monitoring_data_list

    # 插入
    def add_monitoring_data(self, monitoring_data):
        query = (f"INSERT INTO 监测数据 (植物编号, 异常情况, 创建人员, 创建时间, 更新时间, 光照, 温度) VALUES "
                 f"('{monitoring_data.plant_id}', '{monitoring_data.abnormal_condition}', '{monitoring_data.creator}', "
                 f"'{monitoring_data.creation_time}', '{monitoring_data.update_time}', '{monitoring_data.light}', "
                 f"'{monitoring_data.temperature}')")
        self.connection_pool.exec_sql_with_commit(query)

    # 删除
    def delete_monitoring_data(self, monitoring_id):
        query = f"DELETE FROM 监测数据 WHERE 监测数据编号 = '{monitoring_id}'"
        self.connection_pool.exec_sql_with_commit(query)

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

        # 移除最后一个逗号和空格
        query = query.rstrip(', ')

        # 添加 WHERE 子句
        query += f"WHERE 监测数据编号 = {monitoring_data.monitoring_id}"

        self.connection_pool.exec_sql_with_commit(query)

    # 查询
    def search_monitoring_data(self, **search_criteria):
        query = "SELECT * FROM 监测数据 WHERE"

        for attribute, keyword in search_criteria.items():
            if keyword:
                query += f" {attribute} LIKE '%{keyword}%'"
                # query += f" {attribute} LIKE '%{keyword}%' AND"

        # 移除最后一个 AND
        # query = query.rstrip(' AND')

        result = self.connection_pool.exec_sql(query)

        monitoring_data_list = []
        for row in result:
            monitoring_data = MonitoringData(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
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
        query = (f"INSERT INTO 监测人员 (姓名) VALUES ('{personnel_data}')")
        self.connection_pool.exec_sql_with_commit(query)

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
        self.connection_pool.exec_sql_with_commit(query)


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
        query = (f"INSERT INTO 监测 (监测数据编号, 监测时间, 监测地点, 监测设备) VALUES ('{monitoring_data.monitoring_id}', "
                 f"'{monitoring_data.monitoring_time}', '{monitoring_data.monitoring_location}', "
                 f"'{monitoring_data.detection_device}')")
        self.connection_pool.exec_sql_with_commit(query)

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
        self.connection_pool.exec_sql_with_commit(query)