import plantdesign


def init():
    connectionPool = plantdesign.ConnectionPool('127.0.0.1',"plantdesign",'sa','123456')
    createTablePlantInfo = """
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
    connectionPool.exec_sql_with_commit(createTablePlantInfo)
