; Alright, it's time for the Hello World program.
; The basic foundations of IOKit have been laid, enough to test at least.

; Configure some registers that we will send to the controller.
SET u1 #1 ; Set IOKit mode to 1, Text Output mode.
SET u2 #-221 ; Set the X position for where we want to draw the text.
SET u3 #150 ; Set the Y position for where we want to draw the text.
SET u4 #100 ; Set the size to 100% (normal size).
SET u5 #20 ; This is the starting point for where our text will be, it should suffice.
SET u6 #10 ; 20 pixels of space apart from each letter.

; Time to push each of these settings to the IOKit Controller.
STORE #1 u1
STORE #2 u2
STORE #3 u3
STORE #4 u4
STORE #5 u5
STORE #6 u6

; Next, write "hello world" into the text buffer.
SET u1 #8 ; h
SET u2 #5 ; e
SET u3 #12 ; l
SET u4 #12 ; l
SET u5 #15 ; o

SET u6 #27 ; space

; Before we start the second world, we're running out of registers, so let's push these onto the RAM.
STORE #20 u1
STORE #21 u2
STORE #22 u3
STORE #23 u4
STORE #24 u5
STORE #25 u6

; Alright, let's write the second word now.
SET u1 #23 ; w
SET u2 #15 ; o
SET u3 #18 ; r
SET u4 #12 ; l
SET u5 #4 ; d

SET u6 #0 ; Null terminator

; Alright, let's store the second word in RAM now.
STORE #26 u1
STORE #27 u2
STORE #28 u3
STORE #29 u4
STORE #30 u5
STORE #31 u6

; Okay, now for the big moment...
HARDCALL #100 ; HARDCALL!!!

; After that, halt.
HALT