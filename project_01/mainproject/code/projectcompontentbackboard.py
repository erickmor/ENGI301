"""
--------------------------------------------------------------------------
Bop It Interactive Grade
--------------------------------------------------------------------------
License:   
Copyright 2021 Erick Morales

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------


"""

import time
import busio
import board
import digitalio

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM



import spi_screen as SPI

class Project():
    image = None
    clk_pin = None
    miso_pin = None
    mosi_pin = None
    cs_pin = None
    dc_pin = None
    reset_pin = None
    baudrate = None
    rotation = None
    display = None
    button = None
    limitswitch = None
    potentiometer = None
    joystickx = None
    joysticky = None
    buzzer = None
    
    
    def __init__(self, image="blinka.jpg",clk_pin=board.SCLK, miso_pin=board.MISO, mosi_pin=board.MOSI,
                       cs_pin=board.P1_6, dc_pin=board.P1_4, reset_pin=board.P1_2,
                       baudrate=24000000, rotation=90, button="P2_2", limitswitch="P2_4",
                       potentiometer="P1_19", joystickx="P1_21", joysticky="P1_23", buzzer="P2_1"):
    
        self.image = image
        self.display = SPI.SPI_Display(clk_pin, miso_pin, mosi_pin, cs_pin, dc_pin, reset_pin, baudrate, rotation)
        self.button = button
        self.limitswitch = limitswitch
        self.potentiometer = potentiometer
        self.joystickx = joystickx
        self.joysticky = joysticky
        self.buzzer = buzzer
        self._setup()
    
    # End def
    
    def _setup(self):
        self.display.fill((0, 0, 255)) 
        
        # Initialize Button
        GPIO.setup(self.button, GPIO.IN)
        
        # Initialize Limit Switch
        GPIO.setup(self.limitswitch, GPIO.IN)
        
        # Initialize Analog Inputs Potentiometer and Joystick
        ADC.setup()
        
        time.sleep(1)
    
    def run(self):
        while(1):
            
            self.display.image(self.image)
            time.sleep(0.5)
            self.display.fill((0, 255, 0))
            time.sleep(0.5)
            self.display.blank()
            time.sleep(0.5)
            
            if (GPIO.input(self.button) == 1):
                self.display.fill((255, 0, 0))
                time.sleep(0.5)
            else:
                self.display.fill((0, 0, 255))
                time.sleep(0.5)
                
            if (GPIO.input(self.limitswitch) == 0):
                self.display.text("Limit Switch Click")
                time.sleep(0.5)
            else:
                self.display.text("Limit Switch Free")
                time.sleep(0.5)
            
            potentiometervalue = ADC.read_raw(self.potentiometer)
            
            if potentiometervalue < 2046:
                self.display.text("Potentiometer at Low")
                time.sleep(0.5)
            else:
                self.display.text("Potentiometer at High")
                time.sleep(0.5)
                
            valueofjoystickx = ADC.read_raw(self.joystickx)
            self.display.text(str(valueofjoystickx))
            time.sleep(0.5)
            
            valueofjoysticky = ADC.read_raw(self.joysticky)
            self.display.text(str(valueofjoysticky))
            time.sleep(0.5)
            
            PWM.start(self.buzzer, 20, 440)
            time.sleep(2)
            PWM.stop(self.buzzer)
            PWM.cleanup()
            

    # End def
    
    def cleanup(self):
        self.display.text(["Goodbye!", "Thanks for Playing :)"])    
    # End def
    
if __name__ == '__main__':
    
    print("Start")
    
    project = Project()
    
    try:
        project.run()
        
    except KeyboardInterrupt:
        project.cleanup()
        
    print("End of Game")
    
    

    


