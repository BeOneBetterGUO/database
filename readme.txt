此项目为数据库系统课设，
使用sql server及ssms
数据库名字为plantdesign
使用pyodbc

以下是作者：
dafu
grant
chosen
yujie

建表语句：
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
    );

CREATE TABLE PlantConservation (
        conservation_id VARCHAR(50) PRIMARY KEY,
        conservation_name VARCHAR(255) NOT NULL,
        conservation_time date,
        conservation_location VARCHAR(255),
        conservation_stuff VARCHAR(255),
        conservation_description TEXT,
        conservation_object VARCHAR(255)
        );