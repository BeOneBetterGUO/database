class PestDisease:
    def __init__(self, pest_id, control_method):
        self.pest_id = pest_id
        self.control_method = control_method


class PestDiseaseDAO:
    def __init__(self, conn):
        self.conn = conn

    def get_all_pests(self):
        try:
            query = "SELECT * FROM 病虫害"
            rows = self.conn.exec_sql(query)
            for row in rows:
                print(f"病虫害名称：{row[0]}")
                print(f"病虫害防治方法：{row[1]}\n")
        except Exception as e:
            print(f"Error fetching pests: {e}")

    def get_pests_by_id(self, pest_id):
        try:
            query = "SELECT * FROM 病虫害 WHERE 病虫害名称 = ?"
            rows = self.conn.exec_sql_with_params(query, pest_id)
            for row in rows:
                print(f"病虫害名称：{row[0]}")
                print(f"病虫害防治方法：{row[1]}\n")
        except Exception as e:
            print(f"Error fetching pests by ID: {e}")

    def delete_pest_by_id(self, pest_id):
        try:
            query = "DELETE FROM 病虫害 WHERE 病虫害名称 = ?"
            self.conn.exec_sql_with_commit(query, pest_id)
        except Exception as e:
            print(f"Error deleting pest by ID: {e}")

    def insert_pest(self, pest):
        try:
            query = "INSERT INTO 病虫害 (病虫害名称, 防治方法) VALUES (?, ?)"
            values = (pest.pest_id, pest.control_method)
            self.conn.exec_sql_with_params(query, values)
        except Exception as e:
            print(f"Error inserting pest: {e}")

    def update_pest(self, pest_id, property_name, property_value):
        try:
            print("yes")
            query = f"UPDATE 病虫害 SET {property_name} = ? WHERE 病虫害名称 = ?"
            value = (property_value, pest_id)
            self.conn.exec_sql_with_commit(query, value)
        except Exception as e:
            print(f"Error updating pest: {e}")


class Pesticide:
    def __init__(self, pesticide_id, dosage, effective_period):
        self.pesticide_id = pesticide_id
        self.dosage = dosage
        self.effective_period = effective_period


class PesticideDAO:
    def __init__(self, conn):
        self.conn = conn

    def get_all_pesticide(self):
        try:
            query = "SELECT * FROM 药剂"
            rows = self.conn.exec_sql(query)
            for row in rows:
                print(f"药剂名称：{row[0]}")
                print(f"作用期限：{row[1]}")
                print(f"药剂范围：{row[2]}\n")
        except Exception as e:
            print(f"Error getting all pesticide: {e}")

    def get_pesticide_by_id(self, pesticide_id):
        try:
            query = "SELECT * FROM 药剂 WHERE 药剂名称 = ?"
            rows = self.conn.exec_sql(query,query)
            for row in rows:
                print(f"药剂名称：{row[0]}")
                print(f"作用期限：{row[1]}")
                print(f"药剂范围：{row[2]}\n")
        except Exception as e:
            print(f"Error getting pesticide by id: {e}")

    def delete_pesticide_by_id(self, pesticide_id):
        try:
            query = "DELETE FROM 药剂 WHERE 药剂名称 = ?"
            self.conn.exec_sql_with_commit(query, pesticide_id)
        except Exception as e:
            print(f"Error deleting pesticide by id: {e}")

    def insert_pesticide(self, pesticide):
        try:
            query = f"INSERT INTO  药剂 (药剂名称, 作用期限, 药剂范围) VALUES (?, ?, ?)"
            values = (pesticide.pesticide_id, pesticide.dosage, pesticide.effective_period)
            self.conn.exec_sql_with_commit(query, values)
        except Exception as e:
            print(f"Error inserting pesticide: {e}")

    def update_pesticide(self, pesticide_id, property_name, property_value):
        try:
            query = f"UPDATE 药剂 SET {property_name} = ? WHERE 药剂名称 = ?"
            values = (property_value, pesticide_id)
            self.conn.exec_sql_with_commit(query, values)
        except Exception as e:
            print(f"Error updating pesticide: {e}")


class PestDiseasePesticide:
    def __init__(self, pest_disease_id, pesticide_id):
        self.pest_disease_id = pest_disease_id
        self.pesticide_id = pesticide_id


class PestDiseasePesticideDAO:
    def __init__(self, conn):
        self.conn = conn

    def get_all(self):
        try:
            query = "SELECT * FROM 防治"
            rows = self.conn.exec_sql(query)
            for row in rows:
                print(f"病虫害名称：{row[0]}")
                print(f"药剂：{row[1]}")
        except Exception as e:
            print(f"Error fetching all relations: {e}")

    def get_by_pest_disease_id(self, pest_disease_id):
        try:
            query = "SELECT * FROM 防治 WHERE 病虫害名称 = ?"
            rows = self.conn.exec_sql_with_params(query, pest_disease_id)
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Error fetching relations by PestDiseaseID: {e}")

    def get_by_pesticide_id(self, pesticide_id):
        try:
            query = "SELECT * FROM 药剂 WHERE 药剂名称 = ?"
            rows = self.conn.exec_sql_with_params(query, pesticide_id)
            for row in rows:
                print(f"药剂名称：{row[0]}")
                print(f"作用期限：{row[1]}")
                print(f"药剂范围：{row[2]}\n")
        except Exception as e:
            print(f"Error fetching relations by PesticideID: {e}")
            return []

    def insert_relation(self, pest_id, pesticide_id):
        try:
            query = "INSERT INTO 防治 (病虫害名称, 药剂名称) VALUES (?, ?)"
            values = (pest_id, pesticide_id)
            self.conn.exec_sql_with_commit(query, values)
        except Exception as e:
            print(f"Error inserting relation: {e}")

    def delete_relation_by_pest_id(self, pest_disease_id):
        try:
            query = "DELETE FROM 防治 WHERE 病虫害名称 = ?"
            self.conn.exec_sql_with_commit(query, pest_disease_id)
        except Exception as e:
            print(f"Error deleting relation: {e}")

    def delete_relation_by_pesticide_id(self, pesticide_id):
        try:
            query = "DELETE FROM 防治 WHERE 药剂名称 = ?"
            self.conn.exec_sql_with_commit(query, pesticide_id)
        except Exception as e:
            print(f"Error deleting relation by pesticide id: {e}")

    def update_pest_id(self, pest_disease_id, new_pest_disease_id):
        try:
            query = "UPDATE 防治 SET 病虫害名称 = ? WHERE 病虫害名称 = ?"
            values = (pest_disease_id, new_pest_disease_id)
            self.conn.exec_sql_with_commit(query, values)
        except Exception as e:
            print(f"Error updating pest id: {e}")

    def update_pesticide_id(self, pesticide_id, new_pesticide_id):
        try:
            query = "UPDATE 防治 SET 药剂名称 = ? WHERE 药剂名称 = ?"
            values = (pesticide_id, new_pesticide_id)
            self.conn.exec_sql_with_commit(query, values)
        except Exception as e:
            print(f"Error updating pesticide id: {e}")


class PestManager:
    def __init__(self, pest_disease_dao, pesticide_dao, pest_disease_pesticide_dao):
        self.pest_disease_dao = pest_disease_dao
        self.pesticide_dao = pesticide_dao
        self.pest_disease_pesticide_dao = pest_disease_pesticide_dao

    def add_pest(self):
        print("\n添加病虫害信息")
        pest_id = input("请输入病虫害名称：")
        control_method = input("请输入防治方法")
        new_pest = PestDisease(pest_id, control_method)
        # print(new_pest.pest_id, new_pest.control_method)
        self.pest_disease_dao.insert_pest(new_pest)
        print("添加成功")

    def add_pesticide(self):
        print("\n 添加药剂信息")
        pesticide_id = input("请输入药剂名称：")
        dosage = input("请输入作用期限")
        effective = input("请输入药剂范围")
        new_pesticide = Pesticide(pesticide_id, dosage, effective)
        self.pesticide_dao.insert_pesticide(new_pesticide)
        print("添加成功")

    def add_pest_pesticide(self):
        print("\n 添加防治方法信息")
        pest_id = input("请输入病虫害名称：")
        pesticide_id = input("请输入药剂名称：")
        self.pest_disease_pesticide_dao.insert_relation(pest_id, pesticide_id)
        print("添加成功")

    def delete_pest(self):
        print("\n删除病虫害信息")
        pest_id = input("请输入病虫害名称：")
        self.pest_disease_dao.delete_pest_by_id(pest_id)
        self.pest_disease_pesticide_dao.delete_relation_by_pest_id(pest_id)
        print("删除成功")

    def delete_pesticide(self):
        print("\n删除药剂信息")
        pesticide_id = input("请输入药剂名称：")
        self.pesticide_dao.delete_pesticide_by_id(pesticide_id)
        self.pest_disease_pesticide_dao.delete_relation_by_pesticide_id(pesticide_id)
        print("删除成功")

    def update_pest(self):
        print("\n修改病虫害信息")
        pest_id = input("请输入病虫害名称：")
        print("1.修改名称\n2.修改防治方法")
        choice = input("请输入选择：")
        property_name = '病虫害名称'
        value = input("请输入修改后的值：")
        if choice == "1":
            self.pest_disease_pesticide_dao.update_pest_id(pest_id, value)
        elif choice == "2":
            property_name = '防治方法'
        else:
            print("输入错误")
        self.pest_disease_dao.update_pest(pest_id, property_name, value)
        print("修改成功")

    def update_pesticide(self):
        print("\n修改药剂信息")
        pesticide_id = input("请输入药剂名称：")
        print("1.修改名称\n2.修改作用期限\n3.修改药剂范围")
        choice = input("请输入选择：")
        property_name = '药剂名称'
        value = input("请输入修改后的值：")
        if choice == '1':
            self.pest_disease_pesticide_dao.update_pesticide_id(pesticide_id, value)
        elif choice == '2':
            property_name = '作用期限'
        elif choice == '3':
            property_name = '药剂范围'
        else:
            print("输入错误")
        self.pesticide_dao.update_pesticide(pesticide_id, property_name, value)
        print("修改成功")

    def search_all_pest(self):
        print("\n查询所有病虫害信息")
        self.pest_disease_dao.get_all_pests()

    def search_by_id(self):
        print("\n按名称查询病虫害信息")
        pest_id = input("请输入病虫害名称： ")
        self.pest_disease_dao.get_pests_by_id(pest_id)

    def search_all_pesticide(self):
        print("\n查询所有药剂信息")
        self.pesticide_dao.get_all_pesticide()

    def search_by_id_pesticide(self):
        print("\n按名称药剂信息")
        pesticide_id = input("请输入药剂名称： ")
        self.pest_disease_pesticide_dao.get_by_pesticide_id(pesticide_id)

    def show_pest_pesticide(self):
        print("\n显示所有防治关系")
        self.pest_disease_pesticide_dao.get_all()

    def manage_menu(self):
        while True:
            print("\n植物防治管理")
            print("1. 植物病虫害管理")
            print("2. 植物药剂管理")
            print("3. 查看所有防治信息")
            print("4. 添加防治信息")
            print("5. 返回上级菜单")
            choice = input("请输入选择：")
            if choice == '1':
                self.pest_run()
            elif choice == '2':
                self.pesticide_run()
            elif choice == '3':
                self.show_pest_pesticide()
            elif choice == '4':
                self.add_pest_pesticide()
            elif choice == '5':
                break
            else:
                print("输入错误，请重新输入")

    def pest_run(self):
        while True:
            print("病虫害管理")
            print("\n1.添加病虫害\n2.修改病虫害\n3.删除病虫害\n4.查询病虫害信息\n5.返回上级菜单")
            choice = input("请输入选择：")
            if choice == '1':
                self.add_pest()
            elif choice == '2':
                self.update_pest()
            elif choice == '3':
                self.delete_pest()
            elif choice == '4':
                choice2 = input("请输入选择：\n1.按病虫害名称查询\n2.全部查询")
                if choice2 == '1':
                    self.search_by_id()
                elif choice2 == '2':
                    self.search_all_pest()
            elif choice == '5':
                break
            else:
                print("输入有误，请重新输入！")

    def pesticide_run(self):
        while True:
            print("药剂管理")
            print("\n1.添加药剂\n2.修改药剂\n3.删除药剂\n4.查询药剂信息\n5.返回上级菜单")
            choice = input("请输入选择：")
            if choice == '1':
                self.add_pesticide()
            elif choice == '2':
                self.update_pesticide()
            elif choice == '3':
                self.delete_pesticide()
            elif choice == '4':
                choice2 = input("请输入选择：\n1.按药剂名称查询\n2.全部查询")
                if choice2 == '1':
                    self.search_by_id_pesticide()
                elif choice2 == '2':
                    self.search_all_pesticide()
            elif choice == '5':
                break
            else:
                print("输入有误，请重新输入！")