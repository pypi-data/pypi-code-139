#!/usr/bin/env python

from . import *
import logging

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

import os,time



class GCP(Cloud):
    
    def __init__(self, vendor_cfg, kwargs):
        super().__init__(vendor_cfg, kwargs)
        keyfile = cfg['paths']['etc'] + '/accounts/' + self.key_file + '.json'
        
        if not os.path.isfile(keyfile):
            raise Exception("PEM key [%s] is not found." % (keyfile))
                
        ComputeEngine = get_driver(Provider.GCE)
        self.driver = False
        error = 0
        
        while self.driver == False and error<10:
            try:
                self.driver = ComputeEngine(self.service_account, keyfile, project = self.project_id)
            except:
                time.sleep(3)
        
        assert(self.driver != False)
        return
    
    
    def get_host_ip(self, hostname):
        return self.driver.ex_get_node(hostname).public_ips[0]
    
    
    def running_nodes(self):
        data = []
        
        for node in self.driver.list_nodes():
            if node.state == "running":
                data.append(node.name)
        
        return data
    
    
    def list_nodes(self):
        data = []
        
        for node in self.driver.list_nodes():
            data.append([node.name, node.state, node.size, node.id])
        
        return data
    
    
    def destroy_nodes(self, names):
        if isinstance(names, str): names = [names]
        
        for name in names:
            try:
                node = self.driver.ex_get_node(name)
                self.driver.destroy_node(node)
            except:
                continue
        
        return
    
    def create_nodes(self, node_type, names = []):
        c = self.vendor
        if isinstance(names, str): names = [names]
        
        nodes = {}
        cfg = c['node-types'][node_type]
        preemptible = cfg['preemptible'] if 'preemptible' in cfg else False

        for name in names:
            
            gpu_type = None
            gpu_count = None
            location = c['location'] + '-b'
            
            if 'gpu' in cfg:
                gpu_type = cfg['gpu-type']
                gpu_count = cfg['gpu']
                location = c['location'] + '-c'
            
            try:
                node = self.driver.create_node(name, 
                            size = cfg['name'], 
                            image = c['image-name'], 
                            location = location,
                            ex_preemptible = preemptible,
                            ex_accelerator_type = gpu_type,
                            ex_accelerator_count = gpu_count,
                            ex_on_host_maintenance = 'TERMINATE')

                nodes[name] = [name, node.public_ips[0]]
                
            except Exception as ex:
                logging.info("Failed to create %s. Reason: %s" % (name, str(ex)))
                self.destroy_nodes([name])
        
        return nodes
    
'''    
    # COMMON API
    
    
    
    
    # COMMON API
    def is_excluded_node(self, node_key):
        return node_key in self.cfg['excluded-nodes']
        
        
        
    # COMMON API
    
    
    
    
    
    
    # COMMON API
    
    
    
    
    # COMMPON API
    def connect_node(self, name):
        
        node = self.driver.ex_get_node(name)
        host = node.public_ips[0]
        print("Connect IP: " + host)
        cmd = 'ssh -i /root/rcc-aws.pem ' + self.cfg['username'] + '@' + host
        os.system(cmd)
        return
'''

