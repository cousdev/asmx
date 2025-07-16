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
SUB u3 u2  ; Test for equality
JEQ u3 @played_rock

SET u3 #48 ; 48 is P for Paper
SUB u3 u2 ; Test for equality
JEQ u3 @played_paper

SET u3 #51 ; 51 is S for Scissors
SUB u3 u2  ; Test for equality
JEQ u3 @played_scissors

; At this point, we don't know what the user played.
IO CONFIG #-221 #110 #100 #10
IO TEXT #10 "I didn't understand"
HALT

@played_rock
IO CONFIG #-221 #110 #100 #10
IO TEXT #10 "You played rock"
SET u2 #1


@played_paper
IO CONFIG #-221 #110 #100 #10
IO TEXT #10 "You played paper"
SET u2 #2


@played_scissors
IO CONFIG #-221 #110 #100 #10
IO TEXT #10 "You played scissors."
SET u2 #3



@compare
; Compare player (u2) vs machine (u1)
; tie if u2 == u1
SUB u2 u1
JEQ u2 @draw

MOV u3 u2

; win if difference is 1 (e.g. 2 beats 1, 3 beats 2)
CMP u3 #1
JEQ u3 @win

; win if difference is -2 (e.g. 1 beats 3)
CMP u3 #-2
JEQ u3 @win

; otherwise loss
JMP @lose


@draw
IO CONFIG #-221 #90 #100 #10
IO TEXT #10 "You tied."
HALT

@win
IO CONFIG #-221 #90 #100 #10
IO TEXT #10 "You won!"
HALT

@lose
IO CONFIG #-221 #90 #100 #10
IO TEXT #10 "You lost."
HALT