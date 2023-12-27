import pyodbc
import plantdesign
from queue import Queue, Empty

from plantCategory import CategoryService
from plantConservation import ConservationService
import PlantInfo

server = "localhost"
database = "plantdesign"

# 创建工厂
factory = plantdesign.Factory(server, database)
category_dao = factory.create_category_dao()
plant_dao = factory.create_plant_dao()
conservation_dao = factory.create_conservation_dao()

# 创建用户管理器
user_manager = plantdesign.UserManager(factory.connection_pool)
plant_manager = PlantInfo.PlantManager(plant_dao)
category_manager = CategoryService(category_dao)
conservation_manager = ConservationService(conservation_dao)
# 用户登录

while True:
    # 显示菜单
    plantdesign.plantMenu.menu()

    # 获取用户选择
    choice = plantdesign.plantMenu.choice()

    if choice == 1:
        # 这里可以添加植物基本信息管理的相关代码
        pass
    elif choice == 2:
        # 进入植物分类管理
        category_manager.manageMenu()
    elif choice == 3:
        #进入植物养护管理
        conservation_manager.manageMenu()

