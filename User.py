import pyodbc as pyodbc

from plantPest import PestManager
import plantPest

class User:
    def __init__(self, number, password, type):
        self.number = number
        self.password = password
        self.type = type


class UserDAO:
    def __init__(self, conn):
        self.conn = conn

    def insert_user(self, user):
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO 用户(账号, 密码, 类型) VALUES (?, ?, ?)"
            values = (user.number, user.password, user.type)
            cursor.execute(query, values)
            self.conn.commit()
        except Exception as e:
            print(f"Error fetching pests: {e}")
        finally:
            cursor.close()  # 关闭游标

    def delete_user(self, number):
        try:
            cursor = self.conn.cursor()
            query = "DELETE FROM 用户 WHERE 账号 = ?"
            values = (number,)
            cursor.execute(query, values)
            self.conn.commit()
        except Exception as e:
            print(f"Error fetching pests: {e}")
        finally:
            cursor.close()  # 关闭游标

    def update_user(self, number, property_name, property_value):
        try:
            cursor = self.conn.cursor()
            query = f"UPDATE 用户 SET {property_name} = ? WHERE 账号 = ?"
            values = (property_value, number)
            cursor.execute(query, values)
            self.conn.commit()
        except Exception as e:
            print(f"Error fetching pests: {e}")
        finally:
            cursor.close()  # 关闭游标

    def get_number(self):
        try:
            cursor = self.conn.cursor()
            query = "SELECT 账号 FROM 用户"
            cursor.execute(query)

            # 使用列表推导式获取账号列表
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching pests: {e}")
        finally:
            cursor.close()  # 关闭游标

    def get_password(self, number):
        try:
            cursor = self.conn.cursor()
            query = "SELECT 密码 FROM 用户 WHERE 账号 = ?"
            values = (number,)
            cursor.execute(query, values)
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error fetching pests: {e}")
        finally:
            cursor.close()  # 关闭游标

    def get_type(self, number):
        try:
            cursor = self.conn.cursor()
            query = "SELECT 类型 FROM 用户 WHERE 账号 = ?"
            values = (number,)
            cursor.execute(query, values)
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error fetching pests: {e}")
        finally:
            cursor.close()  # 关闭游标

    def get_all(self):
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM 用户"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Error fetching pests: {e}")
        finally:
            cursor.close()  # 关闭游标

    def initialization(self):
        try:
            user_list = [
                User("systemadmin", "123456", "系统管理员"),
                User("superior", "123456", "上级管理部门"),
                User("maintenance", "123456", "养护人员"),
                User("guardians", "123456", "监护人员")
            ]
            self.insert_user(user_list[0])
            self.insert_user(user_list[1])
            self.insert_user(user_list[2])
            self.insert_user(user_list[3])
            print("初始化成功!")
        except Exception as e:
            print(f"Error initializing: {e}")


    def system_run(self):
        print("您的身份是系统管理员，您可以进行以下操作：")
        print("1. 基本信息管理")
        print("2. 分类管理")
        print("3. 退出")
        while True:
            choice = input("请选择：")
            if choice == '1':
                print("\n您正在进行基本信息管理，您可以进行以下操作：")

            elif choice == '2':
                print("\n您正在进行分类管理，您可以进行以下操作：")

            elif choice == '3':
                break
            else:
                print("输入错误，请重新输入")

    def superior_run(self):
        print("\n您的身份是上级管理部门，您可以进行以下操作：")
        print("1. 添加用户")
        print("2. 删除用户")
        print("3. 展示用户")
        print("4. 退出")
        choice = input("请输入你的选择")
        while True:
            if choice == '1':
                print("1. 添加养护人员\n2. 添加监护人员")
                choice2 = input("请选择：")
                if choice2 == '1':
                    number = input("请输入账号：")
                    password = input("请输入密码：")
                    user = User(number, password, "养护人员")
                    self.insert_user(user)
                elif choice2 == '2':
                    number = input("请输入账号：")
                    password = input("请输入密码：")
                    user = User(number, password, "监护人员")
                    self.insert_user(user)
                else:
                    print("输入有误，请重新输入")
                print("添加成功！")
            elif choice == '2':
                number = input("请输入账号：")
                values = self.get_type(number)
                if values not in ("养护人员", "监护人员"):
                    print("抱歉，您只能对养护人员和监护人员进行操作")
                else:
                    self.delete_user(number)
                    print("删除成功！")
            elif choice == '3':
                number = input("请输入账号")
                values = self.get_type(number)
                if values not in ("养护人员", "监护人员"):
                    print("抱歉，您只能对养护人员和监护人员进行操作")
                else:
                    print("1.修改账号\n2.修改密码\n3.修改身份\n4.退出")
                    choice2 = input("请选择：")
                    values2 = input("请输入修改后的值:")
                    if choice2 == '1':
                        self.update_user(number,"账号", values)
                    elif choice2 == '2':
                        self.update_user(number, "密码", values)
                    elif choice2 == '3':
                        if values2 not in ("养护人员", "监护人员"):
                            print("抱歉，您只能对养护人员和监护人员进行操作")
                        else:
                            self.update_user(number, "类型", values)
            elif choice == '4':
                break
            else:
                print("输入错误，请重新输入；")

    def maintenance_run(self):
        print("\n您的身份是养护人员，您可以进行以下操作：")
        print("1.养护管理\n2.病虫害管理\n3.退出")
        choice = input("请选择：")
        while True:
            if choice == '1':
                print("\n您正在进行养护管理，您可以进行以下操作：")

            elif choice == '2':
                print("\n您正在进行病虫害防治管理，您可以进行以下操作：")
               # pest_manage = PestManager()
                pest_manage.manage()
            elif choice == '3':
                break
            else:
                print("输入错误，请重新输入；")

    def guardians_run(self):
        print("\n您的身份是养护人员，您可以进行以下操作：")
        print("1.检测管理\n2.退出")
        choice = input("请选择：")
        while True:
            if choice == '1':
                print("\n您正在进行检测管理，您可以进行以下操作：")

            elif choice == '2':
                break
            else:
                print("输入错误，请重新输入；")

    def user_run(self):
        print("请输入账号密码进行登录(输入exit退出)")
        flag = False
        while True:
            number = input("账号: ")
            if number == "exit":
                break
            rows = self.get_number()
            if number in rows:
                correct_password = self.get_password(number)
                while True:
                    password = input("密码:")
                    if password == correct_password:
                        print("登录成功")
                        correct_type = self.get_type(number)
                        if correct_type == "系统管理员":
                            self.system_run()
                        elif correct_type == "上级管理部门":
                            self.superior_run()
                        elif correct_type == "养护人员":
                            self.maintenance_run()
                        elif correct_type == "监护人员":
                            self.guardians_run()
                        else:
                            print("程序错误，退出")
                            break
                    elif password == "exit":
                        break
                    else:
                        print("密码错误,请重新输入")
            else:
                print("账号不存在,请重新输入")


class Factory:
    def __init__(self):
        pass

    def create_pest_dao(self):
        return plantPest.PestDiseaseDAO

    def create_pesticide_dao(self):
        return plantPest.PesticideDAO

    def create_pest_pesticide_dao(self):
        return plantPest.PestDiseasePesticideDAO


if __name__ == "__main__":
    factory = Factory()

    pest_dao = factory.create_pest_dao()
    pesticide_dao = factory.create_pesticide_dao()
    pest_pesticide_dao = factory.create_pest_pesticide_dao()

    pest_manage = plantPest.PestManager(pest_dao, pesticide_dao, pest_pesticide_dao)

    server = 'localhost'
    database = 'plantdesign'
    conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database}'
    try:
        conn = pyodbc.connect(conn_str)
        print('数据库连接成功')
    except Exception as e:
        print("数据库连接失败", e)

    user = UserDAO(conn)
    # user.initialization()
    user.user_run()