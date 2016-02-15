# The MIT License (MIT)

# Copyright (c) 2016 Bill Jones

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# dns.py
# by Bill Jones
# billsridepics@gmail.com
# 
# A Python program to be run on a Raspberry Pi
# Fetches details of DNS requests made to dnsmasq
# and displays them on an lcd shield

import os
import subprocess
import Adafruit_CharLCDPlate 
import time

history = []
sorted_time = []
sorted_address = []
sorted_client = []

def log_load():
    global history
    global sorted_time
    global sorted_address
    global sorted_client


    history = []
    time_count = {}
    address_count = {}
    client_count = {}

    cat_proc = subprocess.Popen(["cat", "/var/log/dnsmasq.log.1", "/var/log/dnsmasq.log"], stdout=subprocess.PIPE)
    grep_proc = subprocess.Popen(["grep", "query\[A"], stdin=cat_proc.stdout, stdout=subprocess.PIPE)  
    awk_proc = subprocess.Popen(["awk", " {print $1, $2, $3, $6, $8;}"], stdin=grep_proc.stdout, stdout=subprocess.PIPE)
    infile = awk_proc.stdout


    for line in infile:
        fields = line.split()
        time = fields[2].split(':')
        minute = int(time[1])
        newtime = fields[0] + ' ' + fields[1] + ' ' + time[0] + ':' + str((minute/15)*15).zfill(2)
        address = fields[3]
	addr_parts  = address.split(".")
	part_count =  len(addr_parts)
	if part_count <= 2:
    		op =  address
	else:
    		if addr_parts[part_count -2] == "co":
        		op =  ''.join([addr_parts[part_count - 3],".",addr_parts[part_count - 2], ".",addr_parts[part_count -1]])
    		else:
        		op =  ''.join([addr_parts[part_count - 2], ".",addr_parts[part_count -1]])
	address = op
        client = fields[4]
        event = []
        event.append(newtime)
        event.append(address)
        event.append(client)
        history.append(event)
        try:
            time_count[newtime] = time_count[newtime] + 1
        except:
            time_count[newtime] = 1
        try:
            address_count[address] = address_count[address] + 1
        except:
            address_count[address] = 1
        try:
            client_count[client] = client_count[client] + 1
        except:
            client_count[client] = 1       
    infile.close()
    sorted_time = sorted(time_count, key=time_count.get, reverse=True)
    sorted_address = sorted(address_count, key=address_count.get, reverse=True)
    sorted_client = sorted(client_count, key=client_count.get, reverse=True)



def mid_levels(history, top_type, top_name, result_type):
    thing_count = {}
    if top_type == 'ADDRESS':
        top_index = 1
    if top_type == 'TIME':
        top_index = 0
    if top_type == 'CLIENT':
        top_index = 2
    if result_type == 'ADDRESS':
        result_index = 1
    if result_type == 'TIME':
        result_index = 0
    if result_type == 'CLIENT':
        result_index = 2
    for item in history:
        if item[top_index] == top_name:
            try:
                thing_count[item[result_index]] = thing_count[item[result_index]] + 1
            except:
                thing_count[item[result_index]] = 1
    sorted_thing = sorted(thing_count, key=thing_count.get, reverse=True)
    return sorted_thing

def bottom_levels(history, top_type, top_name, mid_type, mid_name):
    thing_count = {}
    if top_type == 'ADDRESS':
        top_index = 1
    if top_type == 'TIME':
        top_index = 0
    if top_type == 'CLIENT':
        top_index = 2
    if mid_type == 'ADDRESS':
        mid_index = 1
    if mid_type == 'TIME':
        mid_index = 0
    if mid_type == 'CLIENT':
        mid_index = 2
    result_index = 3 - mid_index - top_index        
    for item in history:
        if item[top_index] == top_name and item[mid_index] == mid_name:
            try:
                thing_count[item[result_index]] = thing_count[item[result_index]] + 1
            except:
                thing_count[item[result_index]] = 1
    sorted_thing = sorted(thing_count, key=thing_count.get, reverse=True)
    return sorted_thing


def reload_plate():
    global lcd    
    lcd.clear()    
    lcd.message('Loading...')
    trivia = log_load()

def plate_scene(level, top_type = 'ADDRESS', top_name = 'www.google.com', mid_type = 'ADDRESS', mid_name = 'www.google.com', bottom_name = 'ADDRESS'):
    global lcd    
    if level == 0:
        lcd.clear()
        lcd.message(' DNS LOG BROWSE\n' + '{:^16}'.format(top_type))
    if level == 1:
        lcd.clear()
        lcd.message('{:^16}'.format(top_type) + '\n' + '{:^16}'.format(top_name))
    if level == 2:
        lcd.clear()
        lcd.message('{:^16}'.format(top_name) + '\n' + '{:^16}'.format(mid_type))
    if level == 3:
        lcd.clear()
        lcd.message('{:^16}'.format(top_name) + '\n' + '{:^16}'.format(mid_name))
    if level == 4:
        lcd.clear()
        lcd.message('{:^16}'.format(mid_name) + '\n' + '{:^16}'.format(bottom_name))


        
def plate_sideways(direction, level, top_type = 'ADDRESS', top_name = 'www.google.com', mid_type = 'ADDRESS', mid_name = 'www.google.com'):
    global lcd
    global current_top_type   
    global top_item 
    global current_top_name
    global current_mid_type
    global mid_item
    global current_mid_collection
    global current_mid_name
    global bottom_item
    global current_bottom_name
    global current_bottom_collection
    global current_bottom_type
    if level == 0:
        if top_type == 'ADDRESS':
            if direction == 'RIGHT':
                current_top_type = 'CLIENT'
            else:
                current_top_type = 'TIME'
        if top_type == 'CLIENT':
            if direction == 'RIGHT':
                current_top_type = 'TIME'
            else:
                current_top_type = 'ADDRESS'
        if top_type == 'TIME':
            if direction == 'RIGHT':
                current_top_type = 'ADDRESS'
            else:
                current_top_type = 'CLIENT'
        plate_scene(level, current_top_type)
    if level == 1:
        if top_type == 'ADDRESS':
            if direction == 'RIGHT':
                if top_item < len(sorted_address)-1:
                    top_item = top_item + 1
            else:
                if top_item > 0:
                    top_item = top_item -1
            top_name = sorted_address[top_item]
        if top_type == 'CLIENT':
            if direction == 'RIGHT':
                if top_item < len(sorted_client)-1:
                    top_item = top_item + 1
            else:
                if top_item > 0:
                    top_item = top_item -1
            top_name = sorted_client[top_item]
        if top_type == 'TIME':
            if direction == 'RIGHT':
                if top_item < len(sorted_time)-1:
                    top_item = top_item + 1
            else:
                if top_item > 0:
                    top_item = top_item -1
            top_name = sorted_time[top_item]
        current_top_name = top_name        
        plate_scene(level, current_top_type, top_name)
    if level == 2:
        if top_type == 'ADDRESS':
            if mid_type == 'CLIENT':
                current_mid_type = 'TIME'
            else:
                current_mid_type = 'CLIENT'
        if top_type == 'CLIENT':
            if mid_type == 'ADDRESS':
                current_mid_type = 'TIME'
            else:
                current_mid_type = 'ADDRESS'
        if top_type == 'TIME':
            if mid_type == 'CLIENT':
                current_mid_type = 'ADDRESS'
            else:
                current_mid_type = 'CLIENT'
        plate_scene(level, top_type, top_name, current_mid_type)
    if level == 3:
        if direction == 'RIGHT':
            if mid_item < len(current_mid_collection) - 1:
                mid_item = mid_item + 1
        else:
            if mid_item > 0:
                mid_item = mid_item -1
        mid_name = current_mid_collection[mid_item]
        current_mid_name =  mid_name
        plate_scene(level, top_type, top_name, mid_type, mid_name) 
    if level == 4:
        if direction == 'RIGHT':
            if bottom_item < len(current_bottom_collection) - 1:
                bottom_item = bottom_item + 1
        else:
            if bottom_item > 0:
                bottom_item = bottom_item -1
        bottom_name = current_bottom_collection[bottom_item]
        current_bottom_name =  bottom_name
        plate_scene(level, top_type, top_name, mid_type, mid_name, bottom_name) 
           

def plate_down(level, top_type = 'ADDRESS', top_name = 'www.google.com', mid_type = 'ADDRESS', mid_name = 'www.google.com'):
    global lcd
    global current_top_type
    global sorted_address
    global scene
    global top_item
    global current_mid_type
    global current_mid_name
    global current_top_name
    global mid_item
    global current_mid_collection
    global bottom_item
    global current_bottom_collection
    if level == 0:
        if top_type == 'ADDRESS':
            top_name = sorted_address[0]
        if top_type == 'CLIENT':
            top_name = sorted_client[0]
        if top_type == 'TIME':
            top_name = sorted_time[0]
        scene = 1
        top_item = 0
        current_top_name = top_name 
        current_top_type = top_type       
        plate_scene(scene, top_type, top_name)
    if level == 1:
        if top_type == 'ADDRESS':
            current_mid_type = 'CLIENT'
        if top_type == 'CLIENT':
           current_mid_type = 'TIME'
        if top_type == 'TIME':
           current_mid_type = 'ADDRESS'
        scene = 2
        plate_scene(scene, top_type, top_name, current_mid_type) 
    if level == 2:
        scene = 3
        mid_item = 0
        current_mid_collection = mid_levels(history, top_type, top_name, mid_type)
        mid_name = current_mid_collection[mid_item]
        current_mid_name = mid_name
        plate_scene(scene, top_type, top_name, mid_type, mid_name)
    if level == 3:
        scene = 4
        bottom_item = 0
        current_bottom_collection = bottom_levels(history, top_type, top_name, mid_type, mid_name)
        bottom_name = current_bottom_collection[bottom_item]
        current_bottom_name = bottom_name
        plate_scene(scene, top_type, top_name, mid_type, mid_name, bottom_name)
        
            

def plate_up(level, top_type = 'ADDRESS', top_name = 'www.google.com', mid_type = 'ADDRESS', mid_name = 'www.google.com'):
    global lcd
    global current_top_type
    global sorted_address
    global scene
    global top_item
    if level == 1:
        scene = 0
        plate_scene(scene, top_type)
    if level == 2:
        scene = 1
        plate_scene(scene, top_type, top_name)
    if level == 3:
        scene = 2
        plate_scene(scene, top_type, top_name, mid_type)
    if level == 4:
        scene = 3
        plate_scene(scene, top_type, top_name, mid_type, mid_name)

# Establish constants and variables for keeping track of how long to wait before changing behaviors
indicator_mode_wait = 15.0   # How many seconds to wait since last button push before turning off the LCD
last_button_input_time = time.time() # Make it appear that buttons have been pressed as soon as we start

# Establish boolean variables to keep track of what's going on with buttons
in_indicator_mode = True

lcd = Adafruit_CharLCDPlate.Adafruit_CharLCDPlate()
lcd.begin(16, 2)
lcd.clear()
lcd.backlight(lcd.ON)
reload_plate()
scene = 0
current_top_type = 'ADDRESS'
current_top_name = ''
current_mid_type = ''
current_mid_name = ''
top_item = 0
mid_item = 0
current_mid_collection = []
current_bottom_collection = []
bottom_item = 0
current_bottom_type = ''
current_bott0m_name = ''
plate_scene(scene, current_top_type)

btn = (lcd.SELECT, lcd.LEFT, lcd.UP, lcd.DOWN, lcd.RIGHT)
while True:
    try:
        for b in btn:
            if lcd.buttonPressed(b):
                if in_indicator_mode == False:
                    lcd.backlight(lcd.ON)
                    in_indicator_mode = True
                last_button_input_time = time.time()                
                if b==lcd.SELECT:
                    reload_plate()
                    scene = 0
                    current_top_type = 'ADDRESS'
                    plate_scene(scene, current_top_type)
                if b==lcd.RIGHT:
                    plate_sideways('RIGHT', scene, current_top_type, current_top_name, current_mid_type, current_mid_name)
                if b==lcd.LEFT:
                    plate_sideways('LEFT', scene, current_top_type, current_top_name, current_mid_type, current_mid_name)
                if b==lcd.DOWN:
                    plate_down(scene, current_top_type, current_top_name, current_mid_type, current_mid_name)
                if b==lcd.UP:
                    plate_up(scene, current_top_type, current_top_name, current_mid_type, current_mid_name)
                time.sleep(.2)                
                break
        if in_indicator_mode == True:
            if time.time() - last_button_input_time > indicator_mode_wait:
                in_indicator_mode = False
                lcd.backlight(lcd.OFF)                         
        time.sleep(.03)

    except KeyboardInterrupt:
        time.sleep(1)
        lcd.clear()
        lcd.backlight(lcd.OFF)
        exit()



