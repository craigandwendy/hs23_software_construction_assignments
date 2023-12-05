# this program only works for arrays with odd number of elements

ldc R0 0
ldc R1 3
ldc R2 @array
loop1:
str R0 R2
ldc R3 1
add R0 R3
add R2 R3
cpy R3 R1
sub R3 R0
bne R3 @loop1

# first element
ldc R1 @array
# last element
dec R2

loop2:
ldr R0 R1
ldr R3 R2
swp R0 R3
str R0 R1
str R3 R2
inc R1
dec R2
cpy R3 R2
sub R3 R1
bge R3 @loop2

hlt
.data
array: 10