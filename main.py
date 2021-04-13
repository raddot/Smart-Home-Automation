#version 1.16
import sys
import ast
import tokenize
import io
import os
import time
import http.client
import httplib2
import xml.etree.ElementTree as ET
from flask import Flask
from flask_ask import Ask,statement

app = Flask(__name__)
ask = Ask(app, '/')
 
gwurl="192.168.43.162:8080"

def set_device_off_xml():
    tree = ET.parse('deviceonoff.xml')
    root = tree.getroot()
    for st in root.findall("device"):
        st.find("active").text = str("OFF")
    tree.write('deviceonoff.xml')
    return 0 

def set_device_on_xml():
    tree = ET.parse('deviceonoff.xml')
    root = tree.getroot()
    for st in root.findall("device"):
        st.find("active").text = str("ON")
    tree.write('deviceonoff.xml')
    return 0 

def set_zone_off_xml():
    tree = ET.parse('zone1.xml')
    root = tree.getroot()
    root.find("active").text =str("0")
    tree.write('zone1.xml')
    return 0 

def set_zone_on_xml():
    tree = ET.parse('zone1.xml')
    root = tree.getroot()
    root.find("active").text =str("1")
    tree.write('zone1.xml')
    return 0 

def scheduleset_device_off_xml():
    tree = ET.parse('schedule.xml')
    root = tree.getroot()
    for st in root.findall("event"):
        st.find("active").text = str("OFF")
    tree.write('schedule.xml')
    return 0 

def scheduleset_device_on_xml():
    tree = ET.parse('schedule.xml')
    root = tree.getroot()
    for st in root.findall("event"):
        st.find("active").text = str("ON")
    tree.write('schedule.xml')
    return 0 

def set_brightness(per):
    tree = ET.parse('deviceonoff.xml')
    root = tree.getroot()
    for st in root.findall("device"):
        for st1 in root.iter("status"):
            st1.find("slight_1").text=str(per)
    tree.write('deviceonoff.xml')
    return 0 

def set_name(name2):
    tree = ET.parse('deviceonoff.xml')
    root = tree.getroot()
    for st in root.findall("device"):
        st.find("dev_name").text=str(name2)
    tree.write('deviceonoff.xml')
    return 0 

def arm():
    tree = ET.parse('security.xml')
    root = tree.getroot()
    for st in root:
        st.text = str("2")
    tree.write('security.xml')
    return 0 

def disarm():
    tree = ET.parse('security.xml')
    root = tree.getroot()
    for st in root:
        st.text = str("0")
    tree.write('security.xml')
    return 0 

def formzonexml(st):
    tree = ET.parse('zone.xml')
    root = tree.getroot()
    for tag in root:
        print("global",st.find('zone_id').text)
        print("local",root.find('zone_id').text)
        root.find('zone_id').text = st.find('zone_id').text
        print("global",st.find('zone_id').text)
        print("local",root.find('zone_id').text)
        root.find('zone_type').text = st.find('zone_type').text
        root.find('active').text = st.find('active').text
        root.find('zone_name').text = st.find('zone_name').text
        root.find('valid').text = st.find('valid').text    
        root.find('devices_inzone').text = st.find('devices_inzone').text
        root.find('parent_index').text = st.find('parent_index').text
        root.find('icon_name').text = st.find('icon_name').text
        root.find('ex_dev_id').text = st.find('ex_dev_id').text
        root.find('ex_zone_id').text = st.find('ex_zone_id').text
        root.find('child_zone_id').text = st.find('child_zone_id').text
        root.find('sec_mode').text = st.find('sec_mode').text    
        root.find('es_timeout').text = st.find('es_timeout').text
        root.find('es_status').text = st.find('es_status').text
        root.find('operation').text = st.find('operation').text
        root.find('dim').text = st.find('dim').text
    tree.write('zone.xml')
    tree1 = ET.parse('zone1.xml')
    root1 = tree1.getroot()
    root1.find('zoneid').text = st.find('zone_id').text
    root1.find('active').text = st.find('active').text
    tree1.write('zone1.xml')
    return 0

def formdevicexml(st):
    tree = ET.parse('deviceonoff.xml')
    root = tree.getroot()
    print(root)
    for tag in root:
        print(tag)
        tag.find('dev_id').text = st.find('dev_id').text
        tag.find('reachable').text = st.find('reachable').text
        tag.find('active').text = st.find('active').text
        tag.find('mac').text = st.find('mac').text
        tag.find('dev_type').text = st.find('dev_type').text    
        tag.find('sub_dev_type').text = st.find('sub_dev_type').text
        #tag.find('appliance_type').text = st.find('appliance_type').text
        tag.find('dev_name').text = st.find('dev_name').text
        tag.find('zoneid').text = st.find('zoneid').text
        tag.find('status').text = st.find('status').text
    tree.write('deviceonoff.xml')
    return 0

def formsecxml(st):
    print(st)
    tree = ET.parse('security.xml')
    root = tree.getroot()
    print(" Tree ")
    for tag in root:
        root=st
    print(tag in root)
    tree.write('security.xml')
    return 0

def scheduleformdevicexml(st,tm):
    tree = ET.parse('schedule.xml')
    root = tree.getroot()
    for tag in root:
        tag.find('dev_id').text = st.find('dev_id').text
        tag.find('active').text = st.find('active').text
        tag.find('dev_type').text = st.find('dev_type').text    
        tag.find('sub_dev_type').text = st.find('sub_dev_type').text
        #tag.find('appliance_type').text = st.find('appliance_type').text
        tag.find('userSetTimeout').text=tm
    tree.write('schedule.xml')
    return 0

def deviceonoff(ourl,dev,status,per):
	conn = http.client.HTTPConnection(ourl)
	conn.request("GET","/dev")
	res = conn.getresponse()
	getrsp = (res.read())
	root = ET.fromstring(getrsp)
	print(ourl)
	for st in root.iter("device"):
		if isequal(str(st.find('dev_name').text),dev) is (1):
			url = '/dev/' + str(st.find('dev_id').text)
			formdevicexml(st)
			if per:
				per=int(per)
				per=int((per/100)*255)
				set_brightness(per)
				if isequal(str(st.find('active').text),"OFF") is (1):
					set_device_on_xml()							
			if isequal(status, "ON") is (1):
				set_device_on_xml()
			elif isequal(status, "OFF") is (1):
				set_device_off_xml()
			else:
				print("Done")
				#set_device_off_xml()	
			sendputcmd (ourl, 'deviceonoff.xml',  url)			
	conn.close() 
	return 0

def renamedevice(ourl,dev,name2):
	conn = http.client.HTTPConnection(ourl)
	conn.request("GET","/dev")
	res = conn.getresponse()
	getrsp = (res.read())
	root = ET.fromstring(getrsp)
	print(ourl)
	for st in root.iter("device"):
		if isequal(str(st.find('dev_name').text),dev) is (1):
			url = '/dev/' + str(st.find('dev_id').text)
			formdevicexml(st)
			set_name(name2)	
			sendputcmd (ourl, 'deviceonoff.xml',  url)			
	conn.close() 
	return 0

def zoneonoff(ourl,zone,status):
	conn = http.client.HTTPConnection(ourl)
	conn.request("GET","/zone")
	res = conn.getresponse()
	getrsp = (res.read())
	root = ET.fromstring(getrsp)
	print(ourl)
	for st in root.iter("zoneop"):
		if isequal(str(st.find('zone_name').text),zone) is (1):
			url = '/zone/active'
			print("ghuss raha hai")
			formzonexml(st)
			if isequal(status, "ON") is (1):
				set_zone_on_xml()
				sendputcmd (ourl, 'zone1.xml',  url)
			else:
				set_zone_off_xml()
				sendputcmd (ourl, 'zone1.xml',  url)
	conn.close()   
	return 0

def secureit(ourl,secure):
	conn = http.client.HTTPConnection(ourl)
	conn.request("GET","/gateway/homesecmode")
	res = conn.getresponse()
	url = '/gateway/homesecmode/'
	getrsp = (res.read())
	root = ET.fromstring(getrsp)
	print(ourl)
	for st in root.iter("home_sec_mode"):
		formsecxml(st)
	if(isequal(str(secure),"arm")) is (1):
		arm()
	else:
		disarm()
	sendputcmd (ourl, 'security.xml',  url)
	conn.close()
	return 0

def scheduledeviceonoff(ourl,dev,status,tm):
    conn = http.client.HTTPConnection(ourl)
    conn.request("GET","/dev")
    res = conn.getresponse()
    getrsp = (res.read())
    root = ET.fromstring(getrsp)
    print(tm)
    print(ourl)
    for st in root.iter("device"):
        if isequal(str(st.find('dev_name').text),dev) is (1):
            url= '/schedule/dev/create'
            scheduleformdevicexml(st,tm)
            #if per:
             #   per=int(per)
              #  per=int((per/100)*255)
               # set_brightness(per)
                #if isequal(str(st.find('active').text),"OFF") is (1):
                 #   scheduleset_device_on_xml()                         
            if isequal(status, "ON") is (1):
                scheduleset_device_on_xml()
            elif isequal(status, "OFF") is (1):
                scheduleset_device_off_xml()
            else:
                scheduleset_device_off_xml()    
            sendputcmd (ourl, 'schedule.xml',  url)         
    conn.close() 
    return 0

def which_zone(dev):
	conn = http.client.HTTPConnection(gwurl)
	conn.request("GET","/dev")
	res = conn.getresponse()
	getrsp = (res.read())
	root = ET.fromstring(getrsp)
	print(gwurl)
	for st in root.iter("device"):
		if isequal(str(st.find('dev_name').text),dev) is (1):
			zoneid=str(st.find('zoneid').text)						
	conn.close()
	if zoneid==0:
		return "none"
	conn = http.client.HTTPConnection(gwurl)
	conn.request("GET","/zone")
	res = conn.getresponse()
	getrsp = (res.read())
	root = ET.fromstring(getrsp)
	print(gwurl)
	for st in root.iter("zoneop"):
		if isequal(str(st.find('zone_id').text),zoneid) is (1):
			print ("Zone Name",st.find('zone_name').text)
			print(str(st.find('zone_id').text))
			zone_name=str(st.find('zone_name').text)
	conn.close()
	return zone_name


def sendputcmd(ourl, xml, url):
    fp = open(xml, "r")
    print ()
    conn = http.client.HTTPConnection(ourl)
    conn.request("PUT", url, fp.read())
    response = conn.getresponse()
    print(response.status, response.reason)
    
def isequal(a, b):
	try:
		if a.upper() == b.upper():
			return 1
		else:
			return 0 
	except AttributeError:
		return 0

@ask.intent('DeviceIntent', mapping={'dev': 'device','status':'control','per':'percentage'})
def devop(dev,status,per):
    deviceonoff(gwurl,dev,status,per)
    if status and per:
        speech_text = "%s is %s at %s percent" % (dev,status,per)
    elif status:
        speech_text = "%s is %s " % (dev,status)
    elif per:
        speech_text = "%s is on at %s percent" % (dev,per)
    return statement(speech_text).simple_card(speech_text)

@ask.intent('RenameIntent', mapping={'dev': 'device','name':'new_name'})
def renamedevop(dev,name):
    renamedevice(gwurl,dev,name)
    speech_text = "%s is renamed to %s" % (dev,name)
    print(dev,name)
    return statement(speech_text).simple_card(speech_text)
    
@ask.intent('ZoneIntent', mapping={'zone': 'zone','status':'control'})
def zoneop(zone,status):
    status=status.upper()
    zoneonoff(gwurl,zone,status)
    speech_text = "%s is %s" % (zone,status) 
    return statement(speech_text).simple_card('Hello', speech_text)

@ask.intent('ArmIntent', mapping={'secure': 'security'})
def securityop(secure):
    secureit(gwurl,secure)
    speech_text = "Home is %s" % secure
    return statement(speech_text).simple_card(speech_text)

@ask.intent('ScheduleIntent', mapping={'dev': 'device','status':'control','tm':'time','unit':'unit'})
def scheduledevop(dev,status,tm,unit):
    tm=int(tm)
    speech_text = "%s will be %s in %s %s" % (dev,status,tm,unit)
    if isequal(unit,"minutes"):
        tm=str(int(time.time()+tm*60))
    elif isequal(unit,"hours"):
        tm=str(int(time.time()+tm*3600))
    else:
        tm=str(int(time.time()+tm))
    scheduledeviceonoff(gwurl,dev,status,tm)
    return statement(speech_text).simple_card(speech_text)
    
@ask.intent('WhichZoneIntent', mapping={'device':'device'})
def whichzone(device):
    print(" GW response")
    speech_text ="Zone of %s is"%device
    speech_text += which_zone(device)
    return statement(speech_text).simple_card('Hello', speech_text)
if __name__=='__main__':
     app.run()
