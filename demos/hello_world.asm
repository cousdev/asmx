; hello_world.asm
; This file shows you how to write Hello World onto the screen.
; This file uses the IOKit package, which comes pre-installed (you can find it at packages/io.py).
; The IOKit package contains a bunch of macros, which makes it easy to output text, or collect input.
; I highly recommend reading and playing around with this file before reading the hello_world_no_iokit.asm file.

; To assemble this file and run it:
; Move this file out of the demos folder and into the asmx folder (parent folder)
; Run (in the parent folder), python asmx.py hello_world.asm hello_world.txt
; If everything worked, you should see a hello_world.txt file generated.
; Open up your Scratch ASMX VM (download it at the Releases page on the GitHub)
; Open the ROM List, right-click, press "import", and then click on hello_world.txt
; Press the green flag button!

IO CONFIG #-221 #150 #100 #10   ; This command sets a couple of default values for Scratch.
                                ; #-221: Sets the X position to -221
                                ; #150 : Sets the Y position to 150
                                ; #100 : Sets the size to 100% (default size)
                                ; #10 : Sets the spacing between each letter to 10. 

IO TEXT #50 "Hello World!"      ; This command:
                                ; 1. Converts the text "Hello World!" into numbers (computers do not understand text, so we must encode it).
                                ; 2. Writes those numbers into RAM (memory), starting at address #50.
                                ; 3. Tells Scratch to read the text, starting at RAM address #50, and render the text on the screen.

HALT                            ; Halt is the equivalent to the "stop all" block.