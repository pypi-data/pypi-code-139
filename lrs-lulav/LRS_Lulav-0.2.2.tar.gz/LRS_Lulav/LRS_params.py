import argparse
from this import d

from pkg_resources import Distribution
from soupsieve import match
from bson.objectid import ObjectId
import pymongo
import redis
import yaml
import json
from pathlib import Path
from ament_index_python.packages import get_package_share_directory

#
# MONGO
# 
MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"

class LRS_params():
    def __init__(self, user_id, project_id, test_id, test_run_id, simulation_run_id):
        #
        # MONGO
        # 
        self.mymongo = pymongo.MongoClient(MONGO_CONNECTION_STRING)        
        
        self.col_users = self.mymongo['LRS']['users']
        self.col_projects = self.mymongo['LRS']['projects']                
        self.col_tests = self.mymongo['tests']['tests']
        
        # get data
        self.user_id = user_id
        self.project_id = project_id   
        self.test_id = test_id    
        self.test_run_id = test_run_id
        self.simulation_run_id = simulation_run_id
        self.user = self._get_user()
        self.project = self._get_project()    
        self.test = self._get_test()

    def _get_user(self):        
        user = self.col_users.find_one({"_id": ObjectId(self.user_id)})                
        return user
    
    def _get_project(self):        
        project = self.col_projects.find_one({ 
            "user_id": ObjectId(self.user_id), 
            "_id": ObjectId(self.project_id)
        })        
        return project
    
    def _get_test(self):        
        test = self.col_tests.find_one({"_id": ObjectId(self.test_id)})                
        return test
        
    def _coersion(self, value, type):        
        if type == "float":
            return float(value)                                                
        return value
        
    def _eval_distribution(self, dist: Distribution):    
        import numpy as np
        
        if dist["type"] == "normal":                            
            return np.random.normal(dist["params"][0]["value"], dist["params"][1]["value"])
        
        if dist["type"] == "normal":                            
            return np.random.exponential(dist["params"][0]["value"])
        
        if dist["type"] == "laplace":                 
            return np.random.laplace(dist["params"][0]["value"], dist["params"][1]["value"])
        
        if dist["type"] == "poisson":                            
            return np.random.poisson(dist["params"][0]["value"])
        
        if dist["type"] == "power":                            
            return np.random.power(dist["params"][0]["value"])
                
        if dist["type"] == "laplace":                 
            return np.random.uniform(dist["params"][0]["value"], dist["params"][1]["value"])
           
        if dist["type"] == "zipf":                            
            return np.random.zipf(dist["params"][0]["value"])   
        
        if dist["type"] == "vonmises":                 
            return np.random.vonmises(dist["params"][0]["value"], dist["params"][1]["value"])
          
        if dist["type"] == "rayleigh":                            
            return np.random.rayleigh(dist["params"][0]["value"])   
        
        if dist["type"] == "const":
            value = self._coersion(dist["params"][0]["value"], dist["params"][0]["type"])
            return value
        
        if dist["type"] == "string":                            
            return dist["params"][0]["value"]
                                    
        raise f"Error: {dist['type']} is not supported."        
        
    def init_params(self):
        config = {}        
        initFile = [ini for ini in self.project["projectInitFiles"] if ini["_id"] == self.test["simulationSettings"]["init_file_id"]][0]                
        paramSettings = {} 
        for ps in initFile["parameterSettings"]:            
            ps["value"] = self._eval_distribution(ps["distribution"])            
            paramSettings[str(ps["param_id"])] = ps                   
        
        for package in self.project["packages"]:            
            config[package["name"]] = {}
            for node in package["nodes"]:                
                config[package["name"]][node["name"]] = {
                    "ros__parameters": {}
                }
                for parameter in node["parameters"]:                    
                    value = self._coersion(parameter['value'], parameter['parameterType'])
                    paramSetting = paramSettings.get(str(parameter["_id"]))
                    if paramSetting:
                        value = paramSetting["value"]
                    config[package["name"]][node["name"]]["ros__parameters"][parameter['name']] = value                                    
                
        for package_name, val in config.items():
            # params.yaml
            # Path("vova").mkdir(parents=True, exist_ok=True)
            path_to_package = get_package_share_directory(package_name) # get the path to the package install direcotry
            path = f"{path_to_package}/config/"
            # path = f"install/{package_name}/share/{package_name}/config/"
            Path(path).mkdir(parents=True, exist_ok=True)
            path = path + "params.yaml"
            
            with open(path, 'w') as file:                                     
                yaml.dump(val, file)           
        
        print(f" ----- uploading to {self.test_run_id} metadata")
        
        db = self.mymongo["test_data"]
        col = db[f"{self.test_run_id}"] # TODO: modify. add publick LRS util connections for all collections. 
        
        col.update_one({
                "type": "metadata",
                "test_id": ObjectId(self.test_id),
                "test_run_id": ObjectId(self.test_run_id),
                "simulation_run_id": ObjectId(self.simulation_run_id),
            },
            { 
                "$set":{
                    "type": "metadata",
                    "test_id": ObjectId(self.test_id),
                    "test_run_id": ObjectId(self.test_run_id),
                    "simulation_run_id": ObjectId(self.simulation_run_id),
                    "paramSettings": paramSettings,
                    "config": config,              # for full state - Evaluated config file
                    "test": self.test, # for full state
                    "project": self.project        # for full state
                }
            },
            upsert=True
        )    
       