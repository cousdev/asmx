; This is Rock, Paper, Scissors. It will be the first game written for the ASMX platform.

; Show the decision screen
IO CONFIG #-221 #150 #100 #10
IO TEXT #10 "Choose R, P, or S:"

; Record user input
IO CONFIG #-221 #130 #100 #10
IO INPUT #50

; Generate a random choice
RAND u1 #1 #3   ; Choose a choice from 1 - 3
                ; 1 is rock
                ; 2 is paper
                ; 3 is scissors

; Lets load the user's choice from address #50
LOAD u2 #50

; Next, we determine which choice the user made.
SET u3 #50 ; 50 is R for rock.
CMP u2 u3  ; Test for equality
JEQ @played_rock

SET u3 #48 ; 48 is P for Paper
CMP u2 u3  ; Test for equality
JEQ @played_paper

SET u3 #51 ; 51 is S for Scissors
CMP u2 u3  ; Test for equality
JEQ @played_scissors

; At this point, we don't know what the user played.
IO CONFIG #-221 #110 #100 #10
IO TEXT #10 "I didn't understand"
HALT

@played_rock
IO CONFIG #-221 #110 #100 #10
IO TEXT #10 "You played rock"
HALT

@played_paper
IO CONFIG #-221 #110 #100 #10
IO TEXT #10 "You played paper"
HALT

@played_scissors
IO CONFIG #-221 #130 #100 #10
IO TEXT #10 "You played scissors."
HALT