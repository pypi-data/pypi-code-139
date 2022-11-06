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

#
# MONGO
# 
MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"

class LRS_util():
    def __init__(self):
        #
        # MONGO
        # 
        self.mymongo = pymongo.MongoClient(MONGO_CONNECTION_STRING)        
        
        self.col_users = self.mymongo['LRS']['users']
        self.col_projects = self.mymongo['LRS']['projects']                
        self.col_tests = self.mymongo['tests']['tests']

    def get_user(self, user_id):        
        user = self.col_users.find_one({"_id": ObjectId(user_id)})                
        return user
    
    def get_project(self, user_id, project_id):        
        project = self.col_projects.find_one({ 
            "user_id": ObjectId(user_id), 
            "_id": ObjectId(project_id)
        })        
        return project
    
    def get_test(self, test_id):        
        test = self.col_tests.find_one({"_id": ObjectId(test_id)})                
        return test

    def get_launch_file(self, user_id, project_id, launch_id):     
        # print("user_id, project_id, launch_id", user_id, project_id, launch_id);        
        project = self.get_project( user_id, project_id)
        # print(project)
                        
        for l in project["launches"]:
            if l["_id"] == launch_id:
                # print("found in launches")
                return None, l                  
                
        for p in project["packages"]:
            for l in p["launches"]:
                if l["_id"] == launch_id:
                    # print("found in packages launches")
                    return p, l   
                
        return None, None        
        
   
   