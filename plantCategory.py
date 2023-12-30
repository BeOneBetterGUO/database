class Category:
    def __init__(self, plant_id, family, genus, species, alias, distribution, growth_environment):
        self.plant_id = plant_id  # 编号
        self.family = family  # 科名
        self.genus = genus  # 属名
        self.species = species  # 种名
        self.alias = alias  # 别名
        self.distribution = distribution  # 分布区域
        self.growth_environment = growth_environment  # 生长环境


class CategoryDao:
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool

    # 插入分类信息
    def add_category(self, category):
        query = f"insert into 植物分类信息 (植物编号, 科名, 属名, 种名, 别名, 分布区域, 生长环境) VALUES " \
                f"('{category.plant_id}', '{category.family}', '{category.genus}', '{category.species}', " \
                f"'{category.alias}', '{category.distribution}', '{category.growth_environment}')"

        self.connection_pool.exec_sql(query)

    # 更新分类信息
    def update_category(self, plant_id, parameter_name, parameter_value):
        # 使用参数化查询
        query = f"update 植物分类信息 set {parameter_name}=? WHERE 植物编号=?"
        values = (parameter_value, plant_id)
        self.connection_pool.exec_sql(query, values)

    def delete_category(self, plant_id):
        query = f"DELETE FROM 植物分类信息 WHERE 植物编号 = '{plant_id}'"
        self.connection_pool.exec_sql(query)

    # 获取所有植物分类信息
    def get_all_categories(self):
        query = "SELECT * FROM 植物分类信息"
        result = self.connection_pool.exec_sql(query)

        categories = []
        for row in result:
            category = Category(
                row[0],  # plant_id
                row[1],  # family
                row[2],  # genus
                row[3],  # species
                row[4],  # alias
                row[5],  # distribution
                row[6]  # growth_environment
            )
            categories.append(category)
        return categories

    # 根据指定属性查找下属的植物信息
    def get_subcategories_by_property(self, property_name, property_value):
        query = f"SELECT [植物].[植物编号], [植物].[植物名称], [植物].[学名], [植物].[栽培技术要点], [植物].[应用价值], [植物].[形态特征] " \
                f"FROM [plantdesign].[dbo].[植物分类信息] AS [分类] " \
                f"JOIN [plantdesign].[dbo].[植物基本信息] AS [植物] ON [分类].[植物编号] = [植物].[植物编号] " \
                f"WHERE [分类].{property_name}='{property_value}'"
        result = self.connection_pool.exec_sql(query)

        subcategories = []
        for row in result:
            subcategory = {
                "植物编号": row[0],
                "植物名称": row[1],
                "学名": row[2],
                "栽培技术要点": row[3],
                "应用价值": row[4],
                "形态特征": row[5],
            }
            subcategories.append(subcategory)
        if not subcategories:
            print("未找到相关的植物信息！")
        else:
            print("找到相关的植物信息:")
            for subcategory in subcategories:
                print(
                    f"植物编号: {subcategory['植物编号']}, 植物名称: {subcategory['植物名称']}, 学名: {subcategory['学名']}, "
                    f"栽培技术要点: {subcategory['栽培技术要点']}, 应用价值: {subcategory['应用价值']}, "
                    f"形态特征: {subcategory['形态特征']}")
        # 根据生长环境进行模糊查询

    def search_by_growth_environment(self, keyword):
        query = f"SELECT * FROM 植物分类信息 WHERE 生长环境 LIKE '%{keyword}%'"
        result = self.connection_pool.exec_sql(query)

        categories = []
        for row in result:
            category = Category(
                row[0],  # plant_id
                row[1],  # family
                row[2],  # genus
                row[3],  # species
                row[4],  # alias
                row[5],  # distribution
                row[6]  # growth_environment
            )
            categories.append(category)
        return categories


class CategoryService:
    def __init__(self, category_dao):
        self.category_dao = category_dao

    def add_category(self):
        print("\n添加植物分类信息")
        # 获取用户输入
        plant_id = input("请输入植物编号: ")
        family = input("请输入科名: ")
        genus = input("请输入属名: ")
        species = input("请输入种名: ")
        alias = input("请输入别名: ")
        distribution = input("请输入分布区域: ")
        growth_environment = input("请输入生长环境: ")

        # 创建 Category 对象
        new_category = Category(
            plant_id=plant_id,
            family=family,
            genus=genus,
            species=species,
            alias=alias,
            distribution=distribution,
            growth_environment=growth_environment
        )

        self.category_dao.add_category(new_category)
        print("植物分类信息添加成功！")

    def get_all_categories(self):
        # 获取所有分类信息
        all_categories = self.category_dao.get_all_categories()
        if not all_categories:
            print("没有可用的分类信息。")
        else:
            print("所有分类信息:")
            for category in all_categories:
                print(f"植物编号: {category.plant_id}, 科名: {category.family}, 属名: {category.genus}, "
                      f"种名: {category.species}, 别名: {category.alias}, 分布区域: {category.distribution}, "
                      f"生长环境: {category.growth_environment}")

    def update_category(self):
        print("\n更新植物分类信息")

        plant_id = str(input("请输入要更新的植物编号: "))
        print("选择要更新的属性:")
        print("1. 科名")
        print("2. 属名")
        print("3. 种名")
        print("4. 别名")
        print("5. 分布区域")
        print("6. 生长环境")

        choice = int(input("请选择要执行的业务："))
        # 判断输入是否合法
        if choice not in range(1, 7):
            print("无效的选项，请重新选择。")
            return

        properties = ['科名', '属名', '种名', '别名', '分布区域', '生长环境']
        property_name = properties[choice - 1]
        property_value = input(f"请输入新的{property_name}: ")

        # 调用 DAO 更新分类属性
        self.category_dao.update_category(plant_id, property_name, property_value)
        print("植物分类信息更新成功！")

    def delete_category(self):
        print("\n删除分类")
        # 获取用户输入
        plant_id = str(input("请输入要删除的植物编号: "))

        # 调用 DAO 删除分类
        self.category_dao.delete_category(plant_id)
        print("分类删除成功！")

    def search_by_property(self):
        print("\n根据属性查找下属植物")
        print("选择要查找的属性:")
        print("1. 科名")
        print("2. 属名")
        print("3. 种名")
        print("4. 别名")

        choice = int(input("请选择要执行的业务："))
        if choice not in range(1, 7):
            print("无效的选项，请重新选择。")
            return

        properties = ['科名', '属名', '种名', '别名']
        property_name = properties[choice - 1]
        property_value = input(f"请输入要查找的{property_name}: ")

        self.category_dao.get_subcategories_by_property(property_name, property_value)

    def search_by_growth_environment(self):
        print("\n根据生长环境查找植物")
        keyword = input("请输入要查找的生长环境关键词: ")

        matching_categories = self.category_dao.search_by_growth_environment(keyword)

        if not matching_categories:
            print("未找到匹配的植物。")
        else:
            print("找到的植物:")
            for matching_category in matching_categories:
                print(
                    f"植物编号: {matching_category['植物编号']}, 植物名称: {matching_category['植物名称']}, "
                    f"学名: {matching_category['学名']}, 栽培技术要点: {matching_category['栽培技术要点']}, "
                    f"应用价值: {matching_category['应用价值']}, 形态特征: {matching_category['形态特征']}")

    def manage_menu(self):
        while True:
            print("\n植物分类管理")
            print("1. 添加分类")
            print("2. 更新分类")
            print("3. 删除分类")
            print("4. 根据属性查找下属植物")
            print("5. 根据生长环境查找植物")
            print("6. 查看所有分类信息")
            print("7. 返回上级菜单")
            choice = int(input("请选择要执行的业务："))

            if choice == 1:
                # 添加分类
                self.add_category()
            elif choice == 2:
                # 更新分类
                self.update_category()
            elif choice == 3:
                # 删除分类
                self.delete_category()
            elif choice == 4:
                # 根据属性查找下属植物
                self.search_by_property()
            elif choice == 5:
                self.search_by_growth_environment()
            elif choice == 6:
                # 获取所有分类信息
                self.get_all_categories()
            elif choice == 7:
                # 返回上级菜单
                break
            else:
                print("无效的选项，请重新选择。")