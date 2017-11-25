import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject
import os
import time
import RPi.GPIO as GPIO

global temp_sensor_1
global temp_sensor_2
temp_sensor_1='/sys/bus/w1/devices/28-0000085b5166/w1_slave'
temp_sensor_2='/sys/bus/w1/devices/28-0000085a4bc5/w1_slave'

def temp_raw(sensor):
    if sensor=='S1':
        f=open(temp_sensor_1, 'r')        
    else:
        f=open(temp_sensor_2, 'r')
        
    lines=f.readlines()
    f.close
    return lines
        
def read_temp(sensor):
    lines=temp_raw(sensor)
    while lines[0].strip()[-3:]!='YES':
        time.sleep(0.2)
        lines=temp_raw(sensor)
    temp_output=lines[1].find('t=')
    if temp_output!=-1:
        temp_string=lines[1].strip()[temp_output+2:]
        temp_c=float(temp_string)/1000
        return temp_c
        
def StarteLuefter():
    GPIO.output(18,  GPIO.HIGH)
    
def StoppeLuefter():
    GPIO.output(18,  GPIO.LOW)

class MyApp (object):

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("GUI.glade")
        self.builder.connect_signals(self)

    def run(self):
        self.builder.get_object("window1").show_all()
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        #Init GPIO Pins
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(18,  GPIO.OUT)
        self.start_temp_request()
        Gtk.main()

    def on_window1_destroy(self, *args):
        Gtk.main_quit()
    
    #================
    #Handle   
    #================
    def on_start_click(self,  button):
        StarteLuefter()
        
    def on_stop_click(self,  button):
        StoppeLuefter()
     
    #================
    #Temp Sensor Functions
    #================
    def temp_request_1(self):
        Temp_Field_1=self.builder.get_object('Temp1')
        Temp_Field_1.set_property('text', str(read_temp('S1')))
        return True
        
    def temp_request_2(self):
        Temp_Field_2=self.builder.get_object('Temp2')
        Temp_Field_2.set_property('text', str(read_temp('S2')))
        return True
        
    def start_temp_request(self):
        GObject.timeout_add_seconds(5, self.temp_request_1)
        GObject.timeout_add_seconds(5, self.temp_request_2)

MyApp().run()
