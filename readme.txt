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

CREATE TABLE 植物养护 (
        任务编号 VARCHAR(50) PRIMARY KEY,
        任务名称 VARCHAR(255) NOT NULL,
        执行时间 date,
        执行地点 VARCHAR(255),
        执行人员 VARCHAR(255),
        任务描述 TEXT,
        养护对象 VARCHAR(255)
        );

CREATE TABLE 用户(
        账号 VARCHAR(255) PriMARY KEY,
        密码 VARCHAR(255) NOT NULL,
        类型 VARCHAR(255) NOT NULL
);
