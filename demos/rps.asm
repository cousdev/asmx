; rps.asm

; This file shows the code for a Rock, Paper, Scissors game.
; I recommend learning the basics before reading or editing this program.
; This program uses a good collection of features from the assembler and the VM, making it a good example program.

; First, we use some IOKit macros to ask the user to choose an option.
IO CONFIG #-221 #150 #100 #10
IO TEXT #10 "Choose R, P, or S:"

; After that, we move 20 pixels down, and wait for the user to enter in an input.
IO CONFIG #-221 #130 #100 #10
IO INPUT #50

; Next, the computer generates a random number
RAND u1 #1 #3   ; Chooses a choice from 1 - 3
                ; 1 is rock
                ; 2 is paper
                ; 3 is scissors

JEQ u1 #1 @computer_rock ; If the computer chose rock, jump to the @computer_rock label
JEQ u1 #2 @computer_paper ; If the computer chose paper, jump to the @computer_paper label
JMP @computer_scissors ; If it wasn't rock or paper, then jump to scissors.



@computer_rock
IO CONFIG #-221 #110 #100 #10 ; This block of code informs the user that the CPU played Rock.
IO TEXT #10 "CPU played Rock."
JMP @load_user_choice

@computer_paper
IO CONFIG #-221 #110 #100 #10 ; This block of code informs the user that the CPU played Paper.
IO TEXT #10 "CPU played Paper."
JMP @load_user_choice

@computer_scissors
IO CONFIG #-221 #110 #100 #10 ; This block of code informs the user that the CPU played Scissors.
IO TEXT #10 "CPU played Scissors."
JMP @load_user_choice


; We need to get the users choice from the input. We stored the choice at RAM address #50.
@load_user_choice
LOAD u2 #50

; Next, we check which key was pressed, and jump to a corresponding label.
JEQ u2 #50 @played_rock ; 50 is R for Rock

JEQ u2 #48 @played_paper ; 48 is P for Paper

JEQ u2 #51 @played_scissors ; 51 is S for Scissors

; If they didn't play a valid move, tell them that it didn't understand, and stop the program.
IO CONFIG #-221 #90 #100 #10
IO TEXT #10 "I didn't understand."
HALT

; Write on the screen what they chose.
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

; If the player and machine chose the same thing, go to draw
JEQ u2 u1 @draw

; Calculate the difference between the player and machine
SUB u2 u1

; If the difference is 1, or -2, then jump to win.
JEQ u2 #1 @win
JEQ u2 #-2 @win

; Else, you lose.
JMP @lose


; Write on screen what the result was.
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