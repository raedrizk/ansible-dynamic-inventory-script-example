#!/usr/bin/env python
# -*- coding:utf-8 -*-
# https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html#developing-inventory-scripts
#from __future__ import (absolute_import, division, print_function, unicode_literals)
import mysql.connector # pip3 install mysql-connector in virtual environment
import json
import sys
import os

#Read env variables for db credentials
mysql_host = os.environ['CMDB_HOST']
mysql_user = os.environ['CMDB_USER']
mysql_password = os.environ['CMDB_PASSWORD']
mysql_database = os.environ['CMDB_DB']

def get_host(host):
    returned = {}
    mydqldb = mysql.connector.connect(
      host=mysql_host,
      user=mysql_user,
      password=mysql_password,
      database=mysql_database
    )
    dbcursor = mydqldb.cursor()
    dbcursor.execute("SELECT hostname, ip_address, os, os_version, deployed_on, system_use FROM hosts where hostname='"+host+"'")
    dbresult = dbcursor.fetchall()
    for row in dbresult:
        returned["ansible_host"] = row[1]
        returned["os"] = row[2]
        returned["os_version"] = row[3]
        returned["location"] = row[4]
        returned["system_use"] = row[5]
     
    return returned
    
def get_all():
    returned = {}
    mydqldb = mysql.connector.connect(
      host=mysql_host,
      user=mysql_user,
      password=mysql_password,
      database=mysql_database
    )
    dbcursor = mydqldb.cursor()
    # Create group for os
    dbcursor.execute("SELECT distinct(os) FROM hosts")
    dbresult = dbcursor.fetchall()
    for row in dbresult:
        returned[row[0]]={}
        if row[0] == 'win':
            returned[row[0]]["vars"]={"ansible_connection":"winrm", "ansible_winrm_server_cert_validation":"ignore"}
        else:
            returned[row[0]]["vars"]={}
           
        returned[row[0]]["hosts"]=[]
        groupcursor = mydqldb.cursor()
        groupcursor.execute("SELECT hostname FROM hosts where os='"+row[0]+"'")
        groupresult = groupcursor.fetchall()
        for group in groupresult:
            returned[row[0]]["hosts"].append(group[0])   
        
    #Create group for location
    dbcursor.execute("SELECT distinct(deployed_on) FROM hosts")
    dbresult = dbcursor.fetchall()
    for row in dbresult:
        returned[row[0]]={}
        returned[row[0]]["vars"]={}   
        returned[row[0]]["hosts"]=[]
        groupcursor = mydqldb.cursor()
        groupcursor.execute("SELECT hostname FROM hosts where deployed_on='"+row[0]+"'")
        groupresult = groupcursor.fetchall()
        for group in groupresult:
            returned[row[0]]["hosts"].append(group[0])   
                
    #create group for system use
    dbcursor.execute("SELECT distinct(system_use) FROM hosts")
    dbresult = dbcursor.fetchall()
    for row in dbresult:
        returned[row[0]]={}
        returned[row[0]]["vars"]={}   
        returned[row[0]]["hosts"]=[]
        groupcursor = mydqldb.cursor()
        groupcursor.execute("SELECT hostname FROM hosts where system_use='"+row[0]+"'")
        groupresult = groupcursor.fetchall()
        for group in groupresult:
            returned[row[0]]["hosts"].append(group[0])       
    
    #set _meta
    dbcursor.execute("SELECT hostname, ip_address, os, os_version, deployed_on, system_use, hostname FROM hosts")
    dbresult = dbcursor.fetchall()
    meta = {}
    meta_hostvars = {}
    
    for row in dbresult:
        meta_hostvars[row[0]] = {}
        meta_hostvars[row[0]]["ansible_host"] = row[1]
        meta_hostvars[row[0]]["os"] = row[2]
        meta_hostvars[row[0]]["os_version"] = row[3]
        meta_hostvars[row[0]]["location"] = row[4]
        meta_hostvars[row[0]]["system_use"] = row[5]
    
    meta["hostvars"] = meta_hostvars 
    returned["_meta"] = meta
    
    return returned
  
if __name__ == '__main__':
    # inventory dictionary should have the structure of: { "group": { "hosts": [], "vars": {} }, "_meta": {} } }
    inventory = {}
    #variable to hold value of command line option if passed
    hostname = None

    if len(sys.argv) > 1:
        if sys.argv[1] == "--host":
            hostname = sys.argv[2]
            inventory = get_host(hostname)
        elif sys.argv[1] == "--list":
            inventory = get_all()

    sys.stdout.write(json.dumps(inventory, indent=2))
