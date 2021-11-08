"""
--------------------------------------------------------------------------
Bop It Interactive Game
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

Use the following hardware components to make a homemade Bop It:
 - Arcade Button
 - Limit Switch
 - Joystick
 - Potentiometer
 - SPI Display
 - Buzzer
 
Requirements
    - Hardware: 
        - At beginning of game: display start screen on SPI Display, beep buzzer 3x
        - Button
            - Wait for button press to initialize game
        - Once game starts: SPI Display countdown "3,2,1, GO", Display First Level along
            with time given to receive response
        - During each level: Randomize input needed, record current values of selected
            input and current time, wait until input values change, record time when 
            input values change, compare time difference to time given to respond,
            when time given is less than time difference - do not advance to next level,
            when time given is greater than time difference - advance to next level
        - If input is in time, display green screen on SPI Display while buzzer beeps 1x 
            and then Next Level Screen with new adjusted time given. Add one point to 
            score.  
        - If input is delayed, display red screen on SPI Display while buzzer beeps 2x
            and then display last score. 
        - When last score is displayed: Display screen offering option to return to start
        - Ability to return to start and start game over again like new.
        - User Interaction
            - Needs to be able to start game by pressing button
            - Needs to be able to interact with all inputs
            

"""

import time
import busio
import board
import digitalio
import random

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM

import spi_screen as SPI

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------




class Project():
    """ Project """
    startupimage       = None
    clk_pin            = None
    miso_pin           = None
    mosi_pin           = None
    cs_pin             = None
    dc_pin             = None
    reset_pin          = None
    baudrate           = None
    rotation           = None
    display            = None
    button             = None
    limitswitch        = None
    potentiometer      = None
    joystickx          = None
    joysticky          = None
    buzzer             = None
    buttonimage        = None
    limitswitchimage   = None
    potentiometerimage = None
    joystickimage      = None
    
    
    def __init__(self, startupimage="intro.jpg", 
                        buttonimage="button.jpg", 
                        limitswitchimage="limitswitch.jpg", 
                        potentiometerimage="potentiometer.jpg",
                        joystickimage="joystick.jpg", 
                        clk_pin=board.SCLK, miso_pin=board.MISO, 
                        mosi_pin=board.MOSI,cs_pin=board.P1_6, 
                        dc_pin=board.P1_4, reset_pin=board.P1_2,
                        baudrate=24000000, rotation=90, button="P2_2", 
                        limitswitch="P2_4", potentiometer="P1_19", 
                        joystickx="P1_21", joysticky="P1_23", buzzer="P2_1"):
        
        """Initialize variables and set up display"""
        self.display = SPI.SPI_Display(clk_pin, miso_pin, mosi_pin, cs_pin, 
                                            dc_pin, reset_pin, baudrate, 
                                            rotation)
        self.button             = button
        self.limitswitch        = limitswitch
        self.potentiometer      = potentiometer
        self.joystickx          = joystickx
        self.joysticky          = joysticky
        self.buzzer             = buzzer
        self.startupimage       = startupimage
        self.buttonimage        = buttonimage
        self.limitswitchimage   = limitswitchimage
        self.potentiometerimage = potentiometerimage
        self.joystickimage      = joystickimage
        
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """Setup the hardware components."""
        
        # Initialize Display
        self.display.image(self.startupimage)
        self.singlebuzzer()      
        self.singlebuzzer()
        self.singlebuzzer()
        # Initialize Button
        GPIO.setup(self.button, GPIO.IN)
        
        # Initialize Limit Switch
        GPIO.setup(self.limitswitch, GPIO.IN)
        
        # Initialize Analog Inputs Potentiometer and Joystick
        ADC.setup()
        
        time.sleep(0.1)
        
    # End def
    
    
    def singlebuzzer(self):
        """Code for Single Buzzer Noise."""
        PWM.start(self.buzzer, 20, 440)
        time.sleep(0.5)
        PWM.stop(self.buzzer)
        PWM.cleanup()
    # End def
    
    
    def goodbuzzer(self):
        """Code for whenever entry is successful."""
        PWM.start(self.buzzer, 20, 380)
        time.sleep(1)
        PWM.stop(self.buzzer)
        PWM.cleanup()
    # End def
        
        
    def badbuzzer(self):
        """Code for whenever entry is unsuccessful"""
        PWM.start(self.buzzer, 80, 600)
        time.sleep(0.5)
        PWM.stop(self.buzzer)
        PWM.start(self.buzzer, 80, 600)
        time.sleep(0.5)
        PWM.stop(self.buzzer)
        PWM.cleanup()   
    # End def
    
    
    def countdown(self):
        """Code for initial countdown at start of game."""
        self.display.text("3")
        self.singlebuzzer()
        self.display.text("2")
        self.singlebuzzer()
        self.display.text("1")
        self.singlebuzzer()
        self.display.text("GO")
        time.sleep(1)
    # End def
    
        
    def buttonlevel(self, TimetoScore):
        """Code for whenever button input is necessary."""
        self.display.image(self.buttonimage)
        TimeInitial = time.time()
        while (GPIO.input(self.button) == 1):
            time.sleep(0.1)
            
        TimeFinal = time.time()
        
        if (TimeFinal-TimeInitial) < TimetoScore:
            LevelUp = 1
        else:
            LevelUp = 0
            
        return LevelUp
    # End def
    
        
    def potentiometerlevel(self, TimetoScore):
        """Code for whenver potentiometer input is necessary."""
        self.display.image(self.potentiometerimage)
        TimeInitial = time.time()
        potentiometerstale = ADC.read_raw(self.potentiometer)
        potentiometercurrent = ADC.read_raw(self.potentiometer)
        potentiometerstale = int(potentiometerstale // 32)
        potentiometercurrent = int(potentiometercurrent // 32)
        while potentiometercurrent == potentiometerstale:
            potentiometercurrent = ADC.read_raw(self.potentiometer)
            potentiometercurrent = int(potentiometercurrent // 32)
            time.sleep(0.4)
            
        TimeFinal = time.time()
        
        if (TimeFinal-TimeInitial) < TimetoScore:
            LevelUp = 1
        else:
            LevelUp = 0
            
        return LevelUp
    #End def
    
        
    def joysticklevel(self, TimetoScore):
        """Code for whenever joystick input is necessary."""
        self.display.image(self.joystickimage)
        TimeInitial = time.time()
        joystickxstale = ADC.read_raw(self.joystickx)
        joystickystale = ADC.read_raw(self.joysticky)
        joystickxcurrent = ADC.read_raw(self.joystickx)
        joystickycurrent = ADC.read_raw(self.joysticky)
        while (joystickxcurrent - joystickxstale) < 30 and (joystickycurrent - joystickystale) < 30:
            joystickxcurrent = ADC.read_raw(self.joystickx)
            joystickycurrent = ADC.read_raw(self.joysticky)            
            time.sleep(0.1)
            
        TimeFinal = time.time()
        
        if (TimeFinal-TimeInitial) < TimetoScore:
            LevelUp = 1
        else:
            LevelUp = 0
            
        return LevelUp 
    # End def
        
    def limitswitchlevel(self, TimetoScore):
        """Code for whenever limit switch input is necessary."""
        self.display.image(self.limitswitchimage)
        TimeInitial = time.time()
        while (GPIO.input(self.limitswitch) == 1):
            time.sleep(0.1)
            
        TimeFinal = time.time()
        
        if (TimeFinal-TimeInitial) < TimetoScore:
            LevelUp = 1
        else:
            LevelUp = 0
            
        return LevelUp  
    # End def    
    
    
    def levelone(self):
        """Code for first level display"""
        self.display.text(["Level 1","Respond in:","","10","seconds"])
        time.sleep(2)
    # End def
    
        
    def leveldisplayupdate(self,CurrentLevel,TruncatedTimetoScore):
        """"Code for updating the display with next level information"""
        str1 = "Level "
        str2 = str(CurrentLevel)
        Line1 = str1 + str2
        
        self.display.text([Line1,"Respond in:","",TruncatedTimetoScore,"seconds"])
        time.sleep(1)
    # End def
    
    
    def run(self):
        """Execute the main program."""
        while(1):
        # Wait until button is pressed to start game
            while (GPIO.input(self.button) == 1):
                time.sleep(0.1)
        
            self.countdown()
            
            Score = 0
            TimetoScore = 10
            CurrentLevel = 1
            
            self.levelone()
            
            while(2):
                choice = random.randint(1,4)
                LevelUp = 0
                
                if choice == 1:
                    LevelUp = self.buttonlevel(TimetoScore)
                elif choice == 2:
                    LevelUp = self.potentiometerlevel(TimetoScore)
                elif choice == 3:
                    LevelUp = self.joysticklevel(TimetoScore)
                elif choice == 4:
                    LevelUp = self.limitswitchlevel(TimetoScore)
                    
                if LevelUp == 1:
                    self.display.fill((0,255,0))
                    self.goodbuzzer()
                    TimetoScore = 0.9*TimetoScore
                    Score = Score + 1
                    TimetoScoreString = str(TimetoScore)
                    TruncatedTimetoScore = TimetoScoreString[:4]
                    CurrentLevel = CurrentLevel + 1
                    
                    self.leveldisplayupdate(CurrentLevel,TruncatedTimetoScore)
                    self.display.blank()
                else:
                    self.display.fill((255,0,0))
                    self.badbuzzer()
                    time.sleep(1)
                    self.display.text(["Final Score: ", "" , str(Score)])
                    time.sleep(4)
                    break
                
            self.display.text(["Press button to return", "to start screen"])
                
            while (GPIO.input(self.button) == 1):
                time.sleep(0.1)
                
            self._setup()        
            
    # End def


    
    def cleanup(self):
        """Execute exit message for game end."""
        self.display.text(["Goodbye!", "Thanks for Playing :)"])    
    # End def
    
# End class    


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    
    print("Start")
    
    #Create instantation of the project
    project = Project()
    
    try:
        #run project
        project.run()
        
    except KeyboardInterrupt:
        #Display exit message
        project.cleanup()
        
    print("End of Game")
    
    

    


