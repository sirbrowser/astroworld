# Assembly language

## Index

- [Introduction](#introduction)
- [The flags register](#the-flags-register)
- [The branching & flow control instructions](#the-branching--flow-control-instructions)
- [Data types chars](#data-types-chars)


#### Introduction

A program looks like :

```assembly
Name: test
.model small

.data

.code

main proc

	main endp
end
```



A register is 16 bits.

If all register are occupied the data is stored in the central memory.

we store our variables in `.data` <br>

`variablename db 12` --> db means one byte, we can put ? as initial value if we do not know it<br>

```assembly
.data
var1 db 15 // one byte/8 bits
var2 dw 151 // two bytes/16 bits
var3 dd 115 // 4 bytes/32bits
var4 dq ? // 8 bytes/64bits
var5 dt 5 // 10 bytes/80bits
```

We also define constants in `.data`  before the variables :

`Pi EQU 3.14`  --> defines a Pi constant<br>

- mov instruction

`mov des,src` --> des takes the value of src, des is only use with registers and variables NOT constants.<br>

We can't mov a variable into an other variable, des and src should have the same size

When dealing with variables we need to put these instructions at the beginnning of the main :

```assembly
mov ax,@data
mov ds,ax
```

The program to invert values of variables :

```assembly
main proc
	mov ax,@data
	mov ds,ax
	
	mov var2,C
	mov al,var1  --> not ax because it is 16bit and
	mov ah,var2  -->var are 8 bits
	
	mov var2,al
	mov var1,ah
```

- xchg instruction

xchg can permute two registers or one register with a variable (NOT constants and NOT two variables) and size should be equals.

- add & subb instruction

`add des,src` --> add src to des and save the value in des.

destination should not be a constant, we can't add two variables, size should be equals.

```assembly
.data
	num1 db 6
	num2 db 3
.code
main proc
	mov ax,@data
	mov ds,ax
	
	mov al,num1
	mov ah,num2
	
	mov sum,al
	add sum,ah
	
	mov def,al
	sub def,ah
```

- inc, dec, neg instructions

Does not accept constants, only variable and register and the size does not matter.

neg instruction multiply the destination by -1.

#### The flags register

6 status flags

3 control flags

To detect overflow in unsigned numbers we use the Carry Flag (CF), for signed numbers we use Overflow Flag (OF).

`mov/xcg` --> No flag will be affected<br>

`add/sub` --> All flags<br>

`inc/dec` --> All except CF<br>

`neg -(2)^n-1` --> overflow<br>

ZF (Zero Flag) is raised when the value is 0.

SF (Signed Flag) is raised when the value is negative.

mov and xch instructions are not affected by the flags.

inc and dec are not affected by OF and CF.

PF (Parity Flag) is the number of 1 in binary in the lower part of a register. 

#### The branching & flow control instructions

The branching :
There are 2 types of branching : conditionnal and unconditionnal.<br>
Conditionnal :
`j<first letter of the flag> <name of label>` --> "jump if" the condition is verified<br>
Unconditionnal:
`jn<first letter of the flag> <name of label>` --> "jump if not" --> jump if the flag is not raised<br>

```assembly
.code

main proc
    
    mov al,5
    mov bl,5
    sub al,bl
    
    jz label 	--> here if the zero flag is raised we jump to the instruction label
    
    mov cl,12	|
    		| --> this is not executed by the program!!!
    add cl,bl	|
    
    label: inc al --> we jumped here
    
    
    main endp
end
```

We can jump without verifying any condition --> `jmp <label_name>`<br>

For unsigned numbers :
```assembly
ja	 	--> jump if >0 / "a" stands for above
jae		--> jump if >=0 /"ae"-----------above or equal
jb		--> jump if <0 / "b" -----------below
jbe		--> jump if <=0 / "be"----------below or equal
je		--> jump if =0 / "e" -----------equal
```

Example:
```assembly
.data 

var1 db ?

.code

main proc
    
        mov ax,@data
        mov ds,ax
    
        mov al,5
        mov ah,6
        
        cmp al,ah  --> compare al to ah
        
        ja above   --> if comparison is positive we jump to above      
        
        mov var1,0
        jmp endf
        
        above: mov var1,1
       
      endf:ret  
    
    main endp
end
```

For signed numbers and unsigned numbers too:
```assembly
jg 		--> jump if greater(g)
jge		--> greater or equal
jl		--> lesser
jle		--> lesser or equal
je=jz		--> equal
```

#### Data types chars

```assembly
.data 

<variable_name> db '<our character>' --> always db for characters!!! --> only one charcater not strings!!!!
```

To print in DOS screen a character :
```assembly
.code
main proc

mov ah,2 --> service code for interruption, needs to be in ah register
mov dl,'1' --> the char that we want to print needs to be in dl register
int 21h --> code instruction to interrupt the program and print out in DOS screen
```

To read a char from the keyboard :
```assembly
.code
main proc

mov ah,1 --> service code for reading keyboard entry
int 21h
```
The result is in al register!

Ask for an input and print in in DOS :
```assembly
.code 

main proc

    mov ah,1
    int 21h	--> ask for keyboard input 
    
    mov ah,2
    mov dl,al
    int 21h	--> print the input in the DOS
    
    mov ah,4ch
    int 21h	--> instruction to close DOS screen and go back to the system
          
    
    main endp
end   
```

Operations on the chars :

We can use same instructions as unsigned numbers (inc, add, je ...)

Print a message in DOS screen:
```assembly
.model small
.data

msg db 'Hello world !!!$' --> dollar always in the end of a string, we can add 'Hello',10,13,'world$': print hello\nworld

.code

main proc
    
    mov ax,@data
    mov ds,ax
    
    mov ah,9 --> status code to print a string
    lea dx,msg --> lea (load effective address), put the address of the variable in dx
    int 21h
    
    mov ah,4ch --> close DOS screen
    int 21h
    ret
    
    main endp
end
```

