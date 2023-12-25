import plantdesign

class PlantConservation:
    def __init__(self, conservation_id, conservation_name, conservation_time, conservation_location, conservation_stuff,
                 conservation_description, conservation_object):
        self.conservation_id = conservation_id  #任务编号
        self.conservation_name = conservation_name  #任务名称
        self.conservation_time = conservation_time  #执行时间
        self.conservation_location = conservation_location  #执行地点
        self.conservation_stuff = conservation_stuff    #执行人员
        self.conservation_description = conservation_description    #任务描述
        self.conservation_object = conservation_object  #养护对象

connection_pool = plantdesign.ConnectionPool('127.0.0.1',"plantdesign",'sa','123456')