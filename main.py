import plantMonitor
import plantdesign, plantPest, PlantInfo
from User import UserDAO
from plantCategory import CategoryService
from plantConservation import ConservationService
from plantdesign import Factory

if __name__ == "__main__":
    server = "localhost"
    database = "plantdesign"
    connection_pool = plantdesign.ConnectionPool(server, database)  # 连接池
    factory = Factory(connection_pool)

    plant_dao = factory.create_plant_dao()
    category_dao = factory.create_category_dao()
    conservation_dao = factory.create_conservation_dao()
    pest_dao = factory.create_pest_dao()
    pesticide_dao = factory.create_pesticide_dao()
    pest_pesticide_dao = factory.create_pest_pesticide_dao()
    monitoring_data_dao = factory.create_monitoring_data_dao()
    monitoring_personnel_dao = factory.create_personnel_data_dao()
    monitoring_dao = factory.create_monitoring_dao()

    plant_manager = PlantInfo.PlantManager(plant_dao)
    category_manager = CategoryService(category_dao)
    conservation_manager = ConservationService(conservation_dao)
    pest_manager = plantPest.PestManager(pest_dao, pesticide_dao, pest_pesticide_dao)
    monitor_manager = plantMonitor.MonitoringManager(monitoring_dao, monitoring_personnel_dao, monitoring_data_dao)

    user = UserDAO(connection_pool, category_manager, pest_manager,
                   conservation_manager, plant_manager, monitor_manager)
    # user.initialization()
    user.user_run()
