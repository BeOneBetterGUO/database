import pyodbc
import plantdesign
from queue import Queue, Empty

from plantCategory import Category


# 封装PlantInfo基本信息类
class PlantInfo:
    def __init__(self,plant_id, plant_name, scientific_name, cultivation_points, application_value, morphological_features):
        self.plant_id = plant_id
        self.plant_name = plant_name
        self.scientific_name = scientific_name
        self.cultivation_points = cultivation_points
        self.application_value = application_value
        self.morphological_features = morphological_features

    def display_info(self):
        print(f"植物编号: {self.plant_id}")
        print(f"植物名称: {self.plant_name}")
        print(f"学名: {self.scientific_name}")
        print(f"栽培技术要点: {self.cultivation_points}")
        print(f"应用价值: {self.application_value}")
        print(f"形态特征: {self.morphological_features}")
        print("\n")

class PlantDAO:
    # ... 其他方法 ...
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool

    def get_plant_by_id(self, plant_id):
        sql = f"SELECT * FROM 植物基本信息 WHERE 植物编号 = {plant_id}"
        result = self.connection_pool.exec_sql(sql)
        if result:
            plant_data = result[0]
            return PlantInfo(plant_data[0], plant_data[1], plant_data[2], plant_data[3], plant_data[4], plant_data[5])
        return None

    def getallplant(self):
        sql = f"SELECT * FROM 植物基本信息"
        result = self.connection_pool.exec_sql(sql)
        plants = []
        for plant_data in result:
            plants.append(
                PlantInfo(plant_data[0], plant_data[1], plant_data[2], plant_data[3], plant_data[4], plant_data[5]))
        return plants

    def add_plant(self, plant):#增加
        sql = f"INSERT INTO 植物基本信息 VALUES ('{plant.plant_id}', '{plant.plant_name}', '{plant.scientific_name}', '{plant.cultivation_points}', '{plant.application_value}', '{plant.morphological_features}')"
        self.connection_pool.exec_sql(sql)

    def delete_plant(self, plant_id):#删除
        sql = f"DELETE FROM 植物基本信息 WHERE 植物编号 = '{plant_id}'"
        self.connection_pool.exec_sql(sql)

        def update_plant(self, plant):
            sql = f"UPDATE 植物基本信息 SET 植物名称 = '{plant.plant_name}', 学名 = '{plant.scientific_name}', 栽培技术要点 = '{plant.cultivation_points}', 应用价值 = '{plant.application_value}', 形态特征 = '{plant.morphological_features}' WHERE 植物编号 = '{plant.plant_id}'"
            self.connection_pool.exec_sql(sql)

    def update_plant_name(self, plant_id, new_name):
        sql = f"UPDATE 植物基本信息 SET 植物名称 = '{new_name}' WHERE 植物编号 = '{plant_id}'"
        self.connection_pool.exec_sql(sql)

    def update_scientific_name(self, plant_id, new_scientific_name):
        sql = f"UPDATE 植物基本信息 SET 学名 = '{new_scientific_name}' WHERE 植物编号 = '{plant_id}'"
        self.connection_pool.exec_sql(sql)

    def update_cultivation_points(self, plant_id, new_cultivation_points):
        sql = f"UPDATE 植物基本信息 SET 栽培技术要点 = '{new_cultivation_points}' WHERE 植物编号 = '{plant_id}'"
        self.connection_pool.exec_sql(sql)

    def update_application_value(self, plant_id, new_application_value):
        sql = f"UPDATE 植物基本信息 SET 应用价值 = '{new_application_value}' WHERE 植物编号 = '{plant_id}'"
        self.connection_pool.exec_sql(sql)

    def update_morphological_features(self, plant_id, new_morphological_features):
        sql = f"UPDATE 植物基本信息 SET 形态特征 = '{new_morphological_features}' WHERE 植物编号 = '{plant_id}'"
        self.connection_pool.exec_sql(sql)

    def get_all_plants(self):
        sql = "SELECT * FROM 植物基本信息"
        result = self.connection_pool.exec_sql(sql)
        plants = []
        for plant_data in result:
            plants.append(PlantInfo(plant_data[0], plant_data[1], plant_data[2], plant_data[3], plant_data[4], plant_data[5]))
        return plants

    def count_plants_by_family(self, family_name):#根据科名统计植物数量
        sql = f"SELECT COUNT(*) FROM 植物分类信息 WHERE 科名 = '{family_name}'"
        result = self.connection_pool.exec_sql(sql)
        if result:
            return result[0][0]
        return 0

    def query_plants2(self, **kwargs):#根据任意属性组合查询所需植物
        conditions = []
        params = []

        for key, value in kwargs.items():
            if key in ["学名", "植物名称"]:
                conditions.append(f"植物基本信息.{key} = ?")
                params.append(value)
            elif key in ["栽培技术要点", "应用价值", "形态特征"]:
                conditions.append(f"植物基本信息.{key} LIKE ?")
                params.append(f"%{value}%")
            elif key in ["科名", "属名", "种名", "别名"]:
                conditions.append(f"植物分类信息.{key} = ?")
                params.append(value)
            elif key in ["分布区域", "生长环境"]:
                conditions.append(f"植物分类信息.{key} LIKE ?")
                params.append(f"%{value}%")

            #params.append(f"%{value}%")  # 使用 % 进行模糊匹配
            #params.append(value)

        join_clause = "INNER JOIN 植物分类信息 ON 植物基本信息.植物编号 = 植物分类信息.植物编号"
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        sql = f"SELECT 植物基本信息.* FROM 植物基本信息 {join_clause} {where_clause}"

        result = self.connection_pool.exec_sql_with_params(sql, params)
        print(len(result))

        plants = []
        for plant_data in result:
            plants.append(
                PlantInfo(plant_data[0], plant_data[1], plant_data[2], plant_data[3], plant_data[4], plant_data[5]))

        return plants

    #根据植物名称查看监测人员信息
    def get_monitoring_personnel_by_plant_name(self, plant_name):
        sql = """
            SELECT DISTINCT MP.人员名称,MP.人员工号
            FROM 植物基本信息 P
            JOIN 监测数据 MD ON P.植物编号 = MD.植物编号
            JOIN 监测人员 MP ON MD.创建人员 = MP.人员名称
            WHERE P.植物名称 = ?
        """

        params = (plant_name,)
        result = self.connection_pool.exec_sql_with_params(sql, params)

        monitoring_personnel = [row for row in result]
        return monitoring_personnel
# 管理功能部分
class PlantManager:
    def __init__(self, plant_dao):
        self.plant_dao = plant_dao

    def manage(self):
        while True:
            print("\n植物管理")
            print("1. 添加植物")
            print("2. 删除植物")
            print("3. 更新植物")
            print("4. 查询植物")
            print("5. 统计植物数量")
            print("6. 查询监测人员信息")
            print("7. 查看所有植物信息")
            print("8. 上级菜单")

            choice = input("请输入选项 (1-8): ")

            if choice == "1":
                # 添加植物
                new_plant_id = input("请输入植物编号： ")
                new_plant_name = input("请输入植物名称: ")
                new_scientific_name = input("请输入学名: ")
                new_cultivation_points = input("请输入栽培技术要点: ")
                new_application_value = input("请输入应用价值: ")
                new_morphological_features = input("请输入形态特征: ")

                new_plant = PlantInfo(
                    plant_id=new_plant_id,
                    plant_name=new_plant_name,
                    scientific_name=new_scientific_name,
                    cultivation_points=new_cultivation_points,
                    application_value=new_application_value,
                    morphological_features=new_morphological_features
                )

                self.plant_dao.add_plant(new_plant)
                print("植物添加成功。")

            elif choice == "2":
                # 删除植物
                plant_id_to_delete = int(input("请输入要删除的植物编号: "))
                self.plant_dao.delete_plant(plant_id_to_delete)
                print("植物删除成功。")

            elif choice == "3":
                # 更新植物
                plant_id_to_update = input("请输入要更新的植物编号: ")
                print("选择要更新的属性:")
                print("1. 植物名称")
                print("2. 学名")
                print("3. 栽培技术要点")
                print("4. 应用价值")
                print("5. 形态特征")
                property_choice = input("请输入选项 (1-5): ")
                if property_choice == "1":
                    new_value = input("请输入新的植物名称: ")
                    self.plant_dao.update_plant_name(plant_id_to_update, new_value)
                elif property_choice == "2":
                    new_value = input("请输入新的学名: ")
                    self.plant_dao.update_scientific_name(plant_id_to_update, new_value)
                elif property_choice == "3":
                    new_value = input("请输入新的栽培技术要点: ")
                    self.plant_dao.update_cultivation_points(plant_id_to_update, new_value)
                elif property_choice == "4":
                    new_value = input("请输入新的应用价值: ")
                    self.plant_dao.update_application_value(plant_id_to_update, new_value)
                elif property_choice == "5":
                    new_value = input("请输入新的形态特征: ")
                    self.plant_dao.update_morphological_features(plant_id_to_update, new_value)
                else:
                    print("无效的选项，请重新输入。")
                print("植物更新成功。")

            elif choice == "4":
                # 查询植物
                query_attributes = input("请输入查询属性（用逗号分隔，如：植物名称,学名）: ").split(',')
                # 如果用户输入两个属性，则分别获取属性和值
                if len(query_attributes) == 2:
                    query_attribute1, query_attribute2 = query_attributes
                    query_value1 = input(f"请输入{query_attribute1}的值: ")
                    query_value2 = input(f"请输入{query_attribute2}的值: ")
                    plants = self.plant_dao.query_plants2(**{query_attribute1: query_value1, query_attribute2: query_value2})
                elif len(query_attributes) == 1:
                    query_attribute = query_attributes[0]
                    query_value = input(f"请输入{query_attribute}的值: ")
                    plants = self.plant_dao.query_plants2(**{query_attribute: query_value})
                else:
                    print("无效的输入，请输入一个或两个属性。")
                    continue
                if plants:
                    for plant in plants:
                        plant.display_info()
                else:
                    print("未找到符合条件的植物。")

            elif choice == "5":
                # 统计植物数量
                family_name_to_count = input("请输入科名: ")
                count = self.plant_dao.count_plants_by_family(family_name_to_count)
                print(f"{family_name_to_count}中植物的数量是： {count}")

            elif choice == "6":
                # 查询监测人员信息
                plant_name_to_query = input("请输入植物名称: ")
                monitoring_personnel = self.plant_dao.get_monitoring_personnel_by_plant_name(plant_name_to_query)
                if monitoring_personnel:
                    print(f"{plant_name_to_query}的监测人员信息:")
                    for personnel in monitoring_personnel:
                        print(f"人员名称: {personnel[0]}, 人员工号: {personnel[1]}")
                else:
                    print("未找到相关监测人员信息。")

            elif choice == "7":
                plantslist = self.plant_dao.getallplant()
                if plantslist:
                        for i in plantslist:
                            i.display_info()
            elif choice == "8":
                print("退出程序。")
                break

            else:
                print("无效的选项，请重新输入。")

