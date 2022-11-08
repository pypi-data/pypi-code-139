#!/usr/bin/env python

from skyway import *
paths = config['paths']

import json

firewalld_cmd = "firewall-cmd --zone=cloud --permanent"



def ip_ranges_gcp():
    
    domains = []
    
    for row in shexec(['nslookup -q=TXT _cloud-netblocks.googleusercontent.com  8.8.8.8']):
        if row.startswith('_cloud-netblocks.googleusercontent.com'):
            segs = row.split(' ')
            for seg in segs:
                if seg.startswith('include:'):
                    domains.append(seg[len('include:'):])
    
    ips = []
    
    for domain in domains:
        for row in shexec(['nslookup -q=TXT ' + domain + '  8.8.8.8']):
            if row.startswith(domain):
                segs = row.split(' ')
                for seg in segs:
                    if seg.startswith('ip4:'):
                        ips.append(seg[len('ip4:'):])
    
    return ips

    

def ip_ranges_aws():
    
    cloud_file = paths["var"] + "/aws-ips.json"
    shexec(["wget 'https://ip-ranges.amazonaws.com/ip-ranges.json'", "-o /dev/null -O", cloud_file])
    data = json.load(open(cloud_file, "r"))
    ips = []
    
    for prefix in data['prefixes']:
        if prefix['service'] == 'EC2' and prefix['region'].startswith('us-east'):
            ips.append(prefix['ip_prefix'])
                
    return ips



def run(args = []):
    
    ip_new = [] #ip_ranges_aws() + ip_ranges_gcp()
    ip_old = shexec([firewalld_cmd, "--list-sources"])[0].split()
    
    for ip in ip_old:
        if ip not in ip_new:
            print("Remove " + ip)
            print(shexec([firewalld_cmd, "--remove-source=" + ip])[0])
    
    for ip in ip_new:
        if ip not in ip_old:
            print("Add " + ip)
            print(shexec([firewalld_cmd, "--add-source=" + ip])[0])
    
    shexec(["firewall-cmd --reload"])




