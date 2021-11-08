# --------------------------------------------------------------------------
# Bop It Project
# --------------------------------------------------------------------------
# License:   
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

Build Instructions

To run this code, you must import the entirety of the mainproject/code folder 
into your device. This is due to the image files associated with the project. 
Once all files are in the same folder, the ./run function should run the code.
To check, these are the files you need to have:
 - project.py
 - spi_screen.py (Library by Erik Welsh) (Necessary to use SPI Display)
 - button.jpg
 - joystick.jpg
 - limitswitch.jpg
 - potentiometer.jpg
 - intro.jpg
 - run

Please reference Hackster.io page (https://www.hackster.io/ejm9/pocketbeagle-bop-it-project-39caf6)
    for more information on this project.

Operation Instructions

1.) Power PocketBeagle up using laptop of 5V USB adapter
2.) Allow device to boot up
3.) To run program, you have two options
    i.) Set up to run automatically
        - implement following code
        - sudo crontab -e
        - @reboot sleep 30 && sh /var/lib/cloud9/ENGI301/project_01/mainproject/code/run > /var/lib/cloud9/ENGI301/project_01/mainproject/code/log/cronlog2>&1
            Note: Directory before run depends on directory where you store files
            Note: Directory before log depends on directory where you store files
                - Need log file from github (Go to hackster)
    
    ii.) Change directory to location of game files and write ./run
