import os

import plantdesign


class PlantConservation:
    def __init__(self, conservation_id, conservation_name, conservation_time, conservation_location, conservation_stuff,
                 conservation_description, conservation_object):
        self.conservation_id = conservation_id  # 任务编号
        self.conservation_name = conservation_name  # 任务名称
        self.conservation_time = conservation_time  # 执行时间
        self.conservation_location = conservation_location  # 执行地点
        self.conservation_stuff = conservation_stuff  # 执行人员
        self.conservation_description = conservation_description  # 任务描述
        self.conservation_object = conservation_object  # 养护对象


class PlantConservationDAO:
    def __init__(self):
        self.conn = plantdesign.ConnectionPool('127.0.0.1', "plantdesign", 'sa', '123456')

    def get_all(self):
        try:
            query = "SELECT * FROM 养护"
            return self.conn.exec_sql(query)
        except Exception as e:
            print(f"Error fetching all relations: {e}")

    def get_by_conservation_id(self, conservation_id):
        try:
            query = "SELECT * FROM 养护 WHERE 任务编号 = ?"
            return self.conn.exec_sql_with_params(query, conservation_id)
        except Exception as e:
            print(f"Error fetching relations by PestDiseaseID: {e}")

    def insert_conservation(self, conservation):
        try:
            query = "INSERT INTO 养护 (任务编号, 任务名称, 执行时间, 执行地点, 执行人员, 任务描述, 养护对象) VALUES (?, ?,?, ?,?, ?, ?)"
            values = (conservation.conservation_id, conservation.conservation_name, conservation.conservation_time,
                      conservation.conservation_location, conservation.conservation_stuff,
                      conservation.conservation_description, conservation.conservation_object)
            self.conn.exec_sql_with_commit(query, values)
        except Exception as e:
            print(f"Error inserting relation: {e}")

    def update_conservation(self, conservation):
        try:
            query = "UPDATE 养护 SET 任务名称 = ?, 执行时间 = ?, 执行地点 = ?, 执行人员 = ?, 任务描述 = ?, 养护对象 = ? WHERE 任务编号 = ?"
            values = (
            conservation.conservation_name, conservation.conservation_time, conservation.conservation_location,
            conservation.conservation_stuff, conservation.conservation_description,
            conservation.conservation_object, conservation.conservation_id)
            self.conn.exec_sql_with_commit(query, values)
        except Exception as e:
            print(f"Error updating relation: {e}")

    def delete_conservation(self, conservation_id):
        try:
            query = "DELETE FROM 养护 WHERE 任务编号 = ?"
            self.conn.exec_sql_with_commit(query, conservation_id)
        except Exception as e:
            print(f"Error updating relation: {e}")


if __name__ == "__main__":
    conservation_dao = PlantConservationDAO()
    while True:
        print("\n请选择操作:")
        print("1. 查看所有养护任务")
        print("2. 查看特定养护任务")
        print("3. 插入养护任务")
        print("4. 更新养护任务")
        print("5. 删除养护任务")
        print("6. 退出")

        try:
            op = int(input("请输入数字选择您要执行的操作: "))

            if op == 1:
                all_conservation = conservation_dao.get_all()
                print("所有养护任务信息:")
                for conservation in all_conservation:
                    print(f"养护任务编号: {conservation.任务编号}")
                    print(f"养护任务名称: {conservation.任务名称}")
                    print(f"养护任务执行时间: {conservation.执行时间}")
                    print(f"养护任务执行地点: {conservation.执行地点}")
                    print(f"养护任务执行人物: {conservation.执行人员}")
                    print(f"养护任务描述: {conservation.任务描述}")
                    print(f"养护任务对象: {conservation.养护对象}\n")
                pass
            elif op == 2:
                id = input("请输入养护任务编号: ")
                conservation = conservation_dao.get_by_conservation_id(id)
                # todo if none
                print(f"养护任务编号: {conservation.任务编号}")
                print(f"养护任务名称: {conservation.任务名称}")
                print(f"养护任务执行时间: {conservation.执行时间}")
                print(f"养护任务执行地点: {conservation.执行地点}")
                print(f"养护任务执行人物: {conservation.执行人员}")
                print(f"养护任务描述: {conservation.任务描述}")
                print(f"养护任务对象: {conservation.养护对象}\n")
                pass
            elif op == 3:
                id = input("请输入养护任务编号: ")
                name = input("请输入养护任务名称: ")
                time = input("请输入养护任务执行时间: ")
                location = input("请输入养护任务执行地点: ")
                stuff = input("请输入养护任务执行人员: ")
                description = input("请输入养护任务描述: ")
                object = input("请输入养护任务对象: ")
                conservation = PlantConservation(id, name, time, location, stuff, description, object)
                conservation_dao.insert_conservation(conservation)
                pass
            elif op == 4:
                id = input("请输入待更新的养护任务编号: ")
                name = input("请输入养护任务名称: ")
                time = input("请输入养护任务执行时间: ")
                location = input("请输入养护任务执行地点: ")
                stuff = input("请输入养护任务执行人员: ")
                description = input("请输入养护任务描述: ")
                object = input("请输入养护任务对象: ")
                conservation = PlantConservation(id, name, time, location, stuff, description, object)
                conservation_dao.update_conservation(conservation)
                pass
            elif op == 5:
                id = input("请输入待删除的养护任务编号: ")
                conservation_dao.delete_conservation(id)
                pass
            elif op == 6:
                print("退出植物养护管理系统。")
                break
            else:
                print("无效的选择，请输入有效的数字。")
        except ValueError:
            print("请输入有效的数字。")
