JMP @jump_1
HALT

@jump_1
SET u1 #1
JEQ u1 #1 @jump_2
HALT

@jump_2
JLT u1 #2 @jump_3
HALT

@jump_3
JGT u1 #0 @jump_4
HALT

@jump_4
SET u2 #2
HALT