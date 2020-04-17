# Assembly language

## Index

- Introduction [#introduction]



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



