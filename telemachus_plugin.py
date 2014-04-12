
# This allows you to more conveniently write scripts that can interface with
# Telemachus
#url = 'http://127.0.0.1:8085/telemachus/datalink?alt='
#url = 'http://192.168.1.3:8085/telemachus/datalink?alt='
    # This is the URL that Telemachus can be found at.
    # Adjust it based on your firewall settings.

import json
from urllib.request import urlopen
import urllib
import time
import os
import math
import configparser as config

import socket

# set time out to 2 second.
socket.setdefaulttimeout(1) 

url = 'http://127.0.0.1:8085/telemachus/datalink?alt='

# Telemachus Definitions
    #The readings are for the active vessel unless otherwise noted
def read_angularvelocity():
    fresh_json = json.loads(urlopen(url + 'v.angularVelocity').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result


def read_asl():
    fresh_json = json.loads(urlopen(url + 'v.altitude').read().decode('utf-8'))
    result = fresh_json['alt']
    return result


def read_apoapsis():
    fresh_json = json.loads(urlopen(url + 'o.ApA').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result


def read_body():
    fresh_json = json.loads(urlopen(url + 'v.body').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result


def read_eccentricity():
    fresh_json = json.loads(urlopen(url + 'o.eccentricity').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result


def read_facing(dimension):
    if dimension in ['pitch']:
        fresh_json = json.loads(urlopen(url + 'n.pitch').read().decode('utf-8'))
        result = math.radians(int(fresh_json["alt"]))
    elif dimension in ['yaw']:
        fresh_json = json.loads(urlopen(url + 'n.heading').read().decode('utf-8'))
        result = math.radians(int(fresh_json["alt"]))
    elif dimension in ['roll']:
        fresh_json = json.loads(urlopen(url + 'n.roll').read().decode('utf-8'))
        result = math.radians(int(fresh_json["alt"]))
    else:
        result = -1
    return result


def read_heading():
    #Note: This returns facing:yaw, not your heading over land
    #Basically what the navball shows, not 'true' heading
    fresh_json = json.loads(urlopen(url + 'n.heading').read().decode('utf-8'))
    result = math.radians(int(fresh_json["alt"]))
    return result


def read_inclination():
    fresh_json = json.loads(urlopen(url + 'o.inclination').read().decode('utf-8'))
    result = math.radians(int(fresh_json["alt"]))
    return result


def read_missiontime():
    fresh_json = json.loads(urlopen(url + 'v.missionTime').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result


def read_orbitalperiod():
    fresh_json = json.loads(urlopen(url + 'o.period').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result


def read_orbitalvelocity():
    fresh_json = json.loads(urlopen(url + 'v.orbitalVelocity').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result


def read_periapsis():
    fresh_json = json.loads(urlopen(url + 'o.PeA').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result


def read_resource(resource):
    reformated_resource = url + 'r.resource' + '[' + resource + ']'
    fresh_json = json.loads(urlopen(reformated_resource).read().decode('utf-8'))
    result = fresh_json["alt"]
    return result


def read_resource_max(resource):
    reformated_resource = url + 'r.resourceMax' + '[' + resource + ']'
    fresh_json = json.loads(urlopen(reformated_resource).read().decode('utf-8'))
    result = fresh_json["alt"]
    return result


def read_surfacespeed():
    fresh_json = json.loads(urlopen(url + 'v.surfaceSpeed').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result


def read_throttle():
    fresh_json = json.loads(urlopen(url + 'f.throttle').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result

def read_time_to_ap():
    fresh_json = json.loads(urlopen(url + 'o.timeToAp').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result

def read_time_to_pe():
    fresh_json = json.loads(urlopen(url + 'o.timeToPe').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result


def read_universaltime():
    fresh_json = json.loads(urlopen(url + 't.universalTime').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result


def read_verticalspeed():
    fresh_json = json.loads(urlopen(url + 'v.verticalSpeed').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result

def read_heightFromTerrain():
    fresh_json = json.loads(urlopen(url + 'v.heightFromTerrain').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result

def read_name():
    fresh_json = json.loads(urlopen(url + 'v.name').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result

def read_bodyGravitationalParameter():
    fresh_json = json.loads(urlopen(url + 'o.gravParameter').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result

def read_longitudeOfAscendingNode():
    fresh_json = json.loads(urlopen(url + 'o.lan').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result

def read_argumentOfPeriapsis():
    fresh_json = json.loads(urlopen(url + 'o.argumentOfPeriapsis').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result
def read_meanAnomalyAtEpoch():
    fresh_json = json.loads(urlopen(url + 'o.maae').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result


def read_trueAnomaly():
    fresh_json = json.loads(urlopen(url + 'o.trueAnomaly').read().decode('utf-8'))
    result = fresh_json["alt"]
    return result    
# Output Definitions


def abort():
    urlopen(url + 'f.abort')


def fly_by_wire(var):
    urlopen(url + 'v.setFbW' + '[' + str(var) + ']')


def brake(var):
    if var == 2:
        fresh_json = json.loads(urlopen(url + 'v.brakeValue').read().decode('utf-8'))
        if fresh_json["alt"] == "True":
            return 1
        elif fresh_json["alt"] == "False":
            return 0
        else:
            return fresh_json["alt"]
    elif var == 1:
        urlopen(url + 'f.brake' + '[' + 'true' + ']')
        #print 'Setting Brake to on'
    elif var == 0:
        urlopen(url + 'f.brake' + '[' + 'false' + ']')
        #print 'Setting Brake to off'
    else:
        return (-1)
        #print 'Brake value was set wrong'


def gear(var):
    if var == 2:
        fresh_json = json.loads(urlopen(url + 'v.gearValue').read().decode('utf-8'))
        if fresh_json["alt"] == "True":
            return 1
        elif fresh_json["alt"] == "False":
            return 0
        else:
            return fresh_json["alt"]
        
    elif var == 1:
        urlopen(url + 'f.gear' + '[' + 'true' + ']')
        #print 'Setting Gear to on'
    elif var == 0:
        urlopen(url + 'f.gear' + '[' + 'false' + ']')
        #print 'Setting Gear to off'
    else:
        return (-1)
        #print 'Gear value was set wrong'


def light(var):
    if var == 2:
        fresh_json = json.loads(urlopen(url + 'v.lightValue').read().decode('utf-8'))
        if fresh_json["alt"] == "True":
            return 1
        elif fresh_json["alt"] == "False":
            return 0
        else:
            return fresh_json["alt"]
    elif var == 1:
        urlopen(url + 'f.light' + '[' + 'true' + ']')
        #print 'Setting Light to TRUE'
    elif var == 0:
        urlopen(url + 'f.light' + '[' + 'false' + ']')
        #print 'Setting Light to False'
    else:
        return (-1)
        #print 'Light value was set wrong'


def rcs(var):
    if var == 2:
        fresh_json = json.loads(urlopen(url + 'v.rcsValue').read().decode('utf-8'))
        if fresh_json["alt"] == "True":
            return 1
        elif fresh_json["alt"] == "False":
            return 0
        else:
            return fresh_json["alt"]
    elif var == 1:
        urlopen(url + 'f.rcs' + '[' + 'true' + ']')
        #print 'Setting RCS to TRUE'
    elif var == 0:
        urlopen(url + 'f.rcs' + '[' + 'false' + ']')
        #print 'Setting RCS to False'
    else:
        return (-1)
        #print 'RCS value was set wrong'


def sas(var):
    if var == 2:
        fresh_json = json.loads(urlopen(url + 'v.sasValue').read().decode('utf-8'))
        if fresh_json["alt"] == "True":
            return 1
        elif fresh_json["alt"] == "False":
            return 0
        else:
            return fresh_json["alt"]
    elif var == 1:
        urlopen(url + 'f.sas' + '[' + 'true' + ']')
        #print 'Setting SAS to TRUE'
    elif var == 0:
        urlopen(url + 'f.sas' + '[' + 'false' + ']')
        #print 'Setting SAS to False'
    else:
        return (-1)
        #print 'SAS value was set wrong'

def stage():
    urlopen(url + 'f.stage')


def set_facing(dimension, angle):
    #This is done by setting relative positions from 0 to 1, as a percent
    #This is based on the three bars in the lower left corner, NOT the Navball
    if dimension in ['pitch']:
        urlopen(url + 'v.setPitch' + '[' + str(angle) + ']')

    elif dimension in ['yaw']:
        urlopen(url + 'v.setYaw' + '[' + str(angle) + ']')

    elif dimension in ['roll']:
        urlopen(url + 'v.setRoll' + '[' + str(angle) + ']')


def set_throttle(throttle):
    urlopen(url + 'f.setThrottle' + '[' + str(throttle) + ']')


def toggle_ag(agn):
    urlopen(url + 'f.ag' + agn)


