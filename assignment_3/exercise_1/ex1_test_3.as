ldc R0 1
ldc R1 0
loop:
ldc R2 1
sub R0 R1
add R1 R2
beq R0 @loop
hlt