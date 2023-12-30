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
CREATE TABLE 植物基本信息 (
    植物编号 VARCHAR(50) PRIMARY KEY,
    植物名称 VARCHAR(255) NOT NULL,
    别名 VARCHAR(255),
    科名 VARCHAR(255),
    种名 VARCHAR(255),
    形态特征 TEXT,
    栽培技术要点 TEXT,
    病虫害防治措施 TEXT,
    应用价值 TEXT
);

CREATE TABLE 植物分类信息 (
	植物编号 VARCHAR(50) PRIMARY KEY,
	科名 VARCHAR(255),
	属名 VARCHAR(255),
	种名 VARCHAR(255),
	别名 VARCHAR(255),
	分布区域 VARCHAR(255),
	生长环境 VARCHAR(255),
	FOREIGN KEY (植物编号) REFERENCES 植物基本信息(植物编号)
);

CREATE TABLE 养护 (
        任务编号 VARCHAR(50) PRIMARY KEY,
        任务名称 VARCHAR(255) NOT NULL,
        执行时间 date,
        执行地点 VARCHAR(255),
        执行人员 VARCHAR(255),
        任务描述 TEXT,
        养护对象 VARCHAR(255)
        );

CREATE TABLE 病虫害 (
    病虫害名称 NVARCHAR(255) PRIMARY KEY,
    防治方法 NVARCHAR(255) NOT NULL
);

CREATE TABLE 防治 (
    病虫害名称 NVARCHAR(255) PRIMARY KEY,
    药剂名称 NVARCHAR(255) NOT NULL
);

CREATE TABLE 药剂 (
    药剂名称 NVARCHAR(255) PRIMARY KEY,
作用期限 NVARCHAR(255) NOT NULL
药剂范围 NVARCHAR(255) NOT NULL
);

CREATE TABLE  检测数据表(
    监测数据编号 INT PRIMARY KEY,
    植物编号 VARCHAR(50),
    异常情况 NVARCHAR(255),
    创建人员 NVARCHAR(255),
    创建时间 DATETIME,
    更新时间 DATETIME,
    光照 FLOAT,
    温度 FLOAT,
   
    CONSTRAINT FK_检测数据表_植物基本信息 FOREIGN KEY (植物编号) REFERENCES 植物基本信息 (植物编号)
);


CREATE TABLE 监测人员 (
    工号 INT PRIMARY KEY,
    姓名 NVARCHAR(255)
);

CREATE TABLE 监测表 (
    检测记录编号 INT PRIMARY KEY,
    监测数据编号 INT,
    监测时间 DATETIME,
    监测地点 NVARCHAR(255),
    检测设备 NVARCHAR(255),
    CONSTRAINT FK_监测记录_监测人员 FOREIGN KEY (监测数据编号) REFERENCES 监测人员 (工号)
);

CREATE TABLE 用户(
        账号 VARCHAR(255) PriMARY KEY,
        密码 VARCHAR(255) NOT NULL,
        类型 VARCHAR(255) NOT NULL
);
