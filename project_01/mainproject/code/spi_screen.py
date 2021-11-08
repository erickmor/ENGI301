# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
SPI Display Library
--------------------------------------------------------------------------
License:   
Copyright 2021 Erik Welsh

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
Software API:

  SPI_DISPLAY()
    - Provide i2c bus that dispaly is on
    - Provide i2c address for the display
    
    blank()
      - Fill the display with black (i.e. color (0,0,0))
    
    fill(color)
      - Fills the display with the given (R, G, B) color tuple
    
    image(filename, rotation=90)
      - Erases display and shows image from filename
    
    text(value, fontsize=24, fontcolor=(255,255,255), backgroundcolor=(0,0,0), 
                justify=LEFT, align=TOP, rotation=90):
      - Erases display and shows text value on display
      - Value can either be a string or list of strings for multiple lines of text

--------------------------------------------------------------------------
Background Information: 

Links:
  - https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/overview
  - https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/spi-wiring-and-test
  - https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/python-wiring-and-setup
  - https://learn.adafruit.com/adafruit-2-8-and-3-2-color-tft-touchscreen-breakout-v2/python-usage

  - https://circuitpython.readthedocs.io/projects/rgb_display/en/latest/api.html#module-adafruit_rgb_display.rgb
  - https://circuitpython.readthedocs.io/projects/rgb_display/en/latest/_modules/adafruit_rgb_display/rgb.html
  
Software Setup:
  - sudo apt-get update
  - sudo pip3 install --upgrade Pillow
  - sudo pip3 install adafruit-circuitpython-busdevice
  - sudo pip3 install adafruit-circuitpython-rgb-display
  - sudo apt-get install ttf-dejavu -y

"""
import time
import busio
import board
import digitalio

from PIL import Image, ImageDraw, ImageFont

from   adafruit_rgb_display import color565
import adafruit_rgb_display.ili9341 as ili9341

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------
LEFT               = 0
RIGHT              = 1
TOP                = 2
BOTTOM             = 3
CENTER             = 4

PADDING            = -5                # May need to adjust based on font

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------
class SPI_Display():
    """ Class to manage an SPI display """
    reset_pin = None
    dc_pin    = None
    cs_pin    = None
    spi_bus   = None
    display   = None
    
    def __init__(self, clk_pin=board.SCLK, miso_pin=board.MISO, mosi_pin=board.MOSI,
                       cs_pin=board.P1_6, dc_pin=board.P1_4, reset_pin=board.P1_2,
                       baudrate=24000000, rotation=90):
        """ SPI Display Constructor
        
        :param clk_pin   : Value must be a pin from adafruit board library
        :param miso_pin  : Value must be a pin from adafruit board library
        :param mosi_pin  : Value must be a pin from adafruit board library
        :param cs_pin    : Value must be a pin from adafruit board library
        :param dc_pin    : Value must be a pin from adafruit board library
        :param reset_pin : Value must be a pin from adafruit board library
        :param baudrate  : SPI communication rate; default 24MHz
        :param rotation  : Rotation of display; default 90 degrees (landscape)
        
        """
        # Configuration for CS and DC pins:
        self.reset_pin = digitalio.DigitalInOut(reset_pin)
        self.dc_pin    = digitalio.DigitalInOut(dc_pin)
        self.cs_pin    = digitalio.DigitalInOut(cs_pin)

        # Setup SPI bus using hardware SPI
        self.spi_bus   = busio.SPI(clock=clk_pin, MISO=miso_pin, MOSI=mosi_pin)

        # Create the ILI9341 display:
        self.display   = ili9341.ILI9341(self.spi_bus, cs=self.cs_pin, dc=self.dc_pin,
                                         baudrate=baudrate, rotation=rotation)
        
        # Initialize Hardware
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """Initialize the display itself"""
        # Clear the display
        self.blank()

    # End def    


    def blank(self):
        """Clear the display a black screen"""
        self.fill((0,0,0))

    # End def


    def fill(self, color):
        """Fill the display with the given color"""
        if ((color[0] < 0) or (color[0] > 255) or 
            (color[1] < 0) or (color[1] > 255) or
            (color[2] < 0) or (color[2] > 255)):
            raise ValueError("(R,G,B) must be between 0 and 255: ({0}, {1}, {2})".format(color[0], color[1], color[2]))

        self.display.fill(color565(color[0], color[1], color[2]))

    # End def


    def _get_dimensions(self, rotation):
        """Get display dimensions"""
        # Check image rotation
        if rotation % 180 == 90:
            height = self.display.width  # Swap height/width to rotate it to landscape!
            width  = self.display.height
        else:
            width  = self.display.width
            height = self.display.height
        
        return (width, height)

    # End def


    def image(self, filename, rotation=90):
        """Display the image on the screen"""
        # Fill display with black pixels to clear the image
        self.blank()

        # Create image with file name
        image = Image.open(filename)

        # Get screen dimensions
        width, height = self._get_dimensions(rotation)

        # Scale the image to the smaller screen dimension
        image_ratio  = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width  = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width  = width
            scaled_height = image.height * width // image.width
        
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

        # Crop and center the image
        x = scaled_width  // 2 - width  // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))

        # Display image
        self.display.image(image)
        
    # End def
    

    def text(self, value, fontsize=24, fontcolor=(255,255,255), 
                   backgroundcolor=(0,0,0), justify=CENTER, align=CENTER, 
                   rotation=90):
        """ Update the display with text
        
        :param value           : Value can be a string or list of string
        :param fontsize        : Size of font
        :param fontcolor       : (R, G, B) tuple for the color of the text
        :param backgroundcolor : (R, G, B) tuple for the color of the background
        :param justify         : Value in [LEFT, CENTER, RIGHT]
        :param align           : Value in [TOP, CENTER, BOTTOM]
        :param rotation        : Orientation of the display
        
        Will throw a ValueError 
        """
        # Debug variable
        debug = False
        
        # Check inputs:
        if justify not in [LEFT, CENTER, RIGHT]:
            raise ValueError("Input justify must be in [LEFT, CENTER, RIGHT]")
        if align not in [TOP, CENTER, BOTTOM]:
            raise ValueError("Input align must be in [TOP, CENTER, BOTTOM]")

        # Determine if text value is string or list
        #   - Rest of function assumes value is a list of strings
        if (type(value) is not list):
            value = [value]

        # Clear screen
        self.fill(backgroundcolor)
        
        # Get display dimensions
        width, height = self._get_dimensions(rotation)

        # Create a canvas for drawing
        canvas = Image.new("RGB", (width, height))

        # Get drawing object to draw on canvas
        draw   = ImageDraw.Draw(canvas)

        # Load a TTF Font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)

        # Get height of a character
        font_height = font.getsize(" ")[1]

        if (debug):
            print("Canvas h = {0}".format(height))
            print("Font   h = {0}".format(font_height))

        # Calculate number of lines supported on screen w/ font choice        
        num_line = height // font_height
        
        if (debug):
            print("Num Lines      = {0}".format(num_line))

        # Issue warning if too many lines        
        if (len(value) > num_line):
            print("WARNING:  Too many lines for font size.  Truncating.")
            print("    Required lines : {0}".format(len(value)))
            print("    Available lines: {0}".format(num_line))
            # Truncate list
            del value[num_line:]
            
        # Create list of positions for each line
        text_height = len(value) * font_height   # Number of lines * font height

        # Get initial y position
        if align == TOP:
            y = 0
        if align == BOTTOM:
            y = height - text_height
        if align == CENTER:
            y = (height // 2) - (text_height // 2) 
        
        # Adjust y position by padding
        y = y + PADDING
        
        # Only print lines there is space for
        for i, line in enumerate(value):
            # Get width of line
            line_width = font.getsize(line)[0]
            
            # Issue warning if too many characters
            if (line_width > width):
                print("WARNING:  Too many characters for the line.  Truncating.")
                print("    Required width : {0}".format(line_width))
                print("    Available width: {0}".format(width))
                # Truncate line
                for i in range(len(line)):
                    line_width = font.getsize(line[:-(i+1)])[0]
                    if (line_width <= width):
                        line = line[:-(i+1)]
                        break

            # Get x position
            if justify == LEFT:
                x = 0
            if justify == RIGHT:
                x = width - line_width
            if align == CENTER:
                x = (width // 2) - (line_width // 2) 

            # Draw the text
            draw.text((x, y), line, font=font, fill=fontcolor)
            y += font_height
        
        # Display image
        self.display.image(canvas)

    # End def
    
# End class


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    import time

    delay = 2
    
    print("Test SPI Display:")
    
    print("Create Display")
    display = SPI_Display()
    time.sleep(delay)

    # Test Functions
    print("Fill Red")
    display.fill((255, 0, 0))   
    time.sleep(delay)

    print("Fill Green")
    display.fill((0, 255, 0))   
    time.sleep(delay)
    
    print("Fill Blue")
    display.fill((0, 0, 255))   
    time.sleep(delay)
    
    print("Display blinka.jpg")
    display.image("blinka.jpg")
    time.sleep(delay)

    print("Display Text")
    display.text("This is some text!!")
    time.sleep(delay)
    
    print("Display Multi-line Text")
    display.text(["This is some text", "on multiple lines!!"])
    time.sleep(delay)
    
    print("Display Multi-line Text, centered")
    display.text(["This is some text", "on multiple lines!!"], justify=CENTER, align=CENTER)
    time.sleep(delay)
    
    print("Display Multi-line Text, right justify, align bottom, fontsize 30")
    display.text(["This is some text", "on multiple lines!!", "asdf", "asdf", "asdf", "abcdefghijklmnopqrstuvwxyz"], 
                 fontsize=30, justify=RIGHT, align=BOTTOM)
    time.sleep(delay)
    
    print("Test Finished.")



