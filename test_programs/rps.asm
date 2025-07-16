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
JEQ u1 #1 @computer_rock
JEQ u1 #2 @computer_paper
JMP @computer_scissors



@computer_rock
IO CONFIG #-221 #110 #100 #10
IO TEXT #10 "CPU played Rock."
JMP @load_user_choice

@computer_paper
IO CONFIG #-221 #110 #100 #10
IO TEXT #10 "CPU played Paper."
JMP @load_user_choice

@computer_scissors
IO CONFIG #-221 #110 #100 #10
IO TEXT #10 "CPU played Scissors."
JMP @load_user_choice


; Lets load the user's choice from address #50
@load_user_choice
LOAD u2 #50

; Next, we determine which choice the user made.
JEQ u2 #50 @played_rock ; 50 is R for Rock

JEQ u2 #48 @played_paper ; 48 is P for Paper

JEQ u2 #51 @played_scissors ; 51 is S for Scissors

; At this point, we don't know what the user played.
IO CONFIG #-221 #90 #100 #10
IO TEXT #10 "I didn't understand."
HALT

@played_rock
IO CONFIG #-221 #90 #100 #10
IO TEXT #10 "You played rock."
SET u2 #1
JMP @compare


@played_paper
IO CONFIG #-221 #90 #100 #10
IO TEXT #10 "You played paper."
SET u2 #2
JMP @compare


@played_scissors
IO CONFIG #-221 #90 #100 #10
IO TEXT #10 "You played scissors."
SET u2 #3
JMP @compare



@compare
; Compare player (u2) vs machine (u1)
; tie if u2 == u1

JEQ u2 u1 @draw

SUB u2 u1
JEQ u2 #1 @win
JEQ u2 #-2 @win
JMP @lose


@draw
IO CONFIG #-221 #70 #100 #10
IO TEXT #10 "You tied."
HALT

@win
IO CONFIG #-221 #70 #100 #10
IO TEXT #10 "You won!"
HALT

@lose
IO CONFIG #-221 #70 #100 #10
IO TEXT #10 "You lost."
HALT