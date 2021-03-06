# Reverse engineering for beginners by Dennis Yurichev

## Index

- [Chapter 4 : Function prologue and epilogue](#chapter-4--function-prologue-and-epilogue)
- [Chapter 5 : Stack](#chapter-5--stack)
- [Chapter 6 : printf() with several arguments](#chapter-6--printf-with-several-arguments)
- [Chapter 7 : scanf()](#chapter-7--scanf)
- [Chapter 8 : accessing passed arguments](#chapter-8--accessing-passed-arguments)
- [Chapter 12 : conditionnal jumps](#chapter-12--conditionnal-jumps)
- [Chapter 15 : simple C-strings processing](#chapter-15--simple-c-strings-processing)
- [Chapter 17 : Floating Point Unit](#chapter-17--floating-point-unit)

Each MIPS instruction is 32 bits<br>

The main difference between x86/ARM and x64/ARM64 is that the pointer to the stack is now 64-bits.<br>

Differences between intel syntax and AT&T syntax :<br>
  - In AT&T source and destination are in opposite order :<br>
      Intel syntax : <instruction> <dest> <source> (a=b)<br>
      AT&T syntax : <instruction>  <source> <dest> (a-->b)<br>
  - In AT&T, a register is preceded by "%" and a number by "$"<br>
  
  ### Chapter 4 : Function prologue and epilogue
  
  A function prologue is a sequence of instructions at the start of the function. It often looks like this :
  ```assembly
  push  ebp
  mov   ebp, esp
  sub   esp, X
  ```
  What these instruction do : save the value in the EBP register, set the value of the EBP register to the value of the ESP and then allocate space on the stack for local variables.  
  The function epilogue frees the allocated space in the stack, returns the value in the EBP register back to its initial state and returns the control flow to te callee (a function called by an other) :
  ```assembly
  mov   esp, ebp
  pop   ebp
  ret   0
  ```
  
### Chapter 5 : Stack

It is one of the most fundamental data structure in computer science.  
Technically it is just a block of memory in process memory along with ESP or RSP register in x86 or x64, or the SP (Stack Pointer, a register pointing to a place in the stack) register in ARM, as a pointer within that block.  

The most frequently used stack access instructions are PUSH and POP (in both x86 and ARM Thumb-mode).  
PUSH substracts from ESP/RSP/SP 4 in 32-bit mode (or 8 in 64-bit mode) and then writes the contents of its sole operand to the memory address pointed by ESP/RSP/SP.  

POP is the reverse operation: it retreives the data from the memory where that SP points to, load it into instruction operand (often a register) and then add 4 (or 8) to the stack pointer.  

After stack allocation, the stack pointerpoints at the bottom of the stack. PUSH decreases the stack pointer and POP increases it. **The bottom of the stack is actually the beginning of the memory allocatedfor the stack block.**  

ARM supports both descending and acending stacks.  
For example, the STMFD (Store Multiple Full Descending)/LDMFD (Load Multiple Full Descending), STMED Store Multiple Empty Descending)/LDMED(Load Multiple Empty Descending) instructions are intended to deal with a descending stack (grows downwards, starting with a high address and progressing to a lower one).  
The STMFA/LDMFA, STMEA/LDMEA (A=Ascending) is the opposite process (grows upwards, starting with a low address to a higher one).  

##### What is the stack used for?

- Save the function's return address
    - x86 : the CALL instruction is equivalent to : PUSH <address_after_call> / JMP <operand> instruction pair.  
      RET fetches a value from the stack and jumps to it, equivalent to : POP <tmp> / JMP <tmp> instruction pair.  

    - ARM : the RA (Return Address) is saved ot the LR (Link Register). If one needs to call another function and use the LR register one more time, its value has to be saved. Usually it is saved in the function prologue. Often, we see instructions like `PUSH  R4-R7, LR` along with this instruction in epilogue `POP  R4-R7, PC`, thus register values to be used in the function are saved in the stack including LR.  

    If a function never calls another function, in RISC it is called a *leaf function*. So, leaf functions do not save the LR register. If such function is small and uses a small number of registers, it may not use the stack at all.

- Passing function arguments
    - the most popular way to pass parmeters in x86 is called `cdecl` :
    ```assembly
    push  arg3
    push  arg2
    push  arg1
    call  f
    add   esp, 12 ; 4*3=12
    ```  
    Callee functions get their arguments via the stack pointer.  

    This is how the argument values are located in the stack before the execution of the f() function's very first instruction :  
    ESP --> return address  
    ESP+4 --> argument#1, marked in IDA as arg_0  
    ESP+8 --> argument#2, marked in IDA as arg_4  
    ESP+0xC --> argument#3, marrket in IDA as arg_8  
   
- Local variable storage  
  A function could allocate space in the stack for its local variable just by decreasing the stack pointer towards the stack bottom
  
- x86 : alloca() function  
    This function works like malloc(), but allocates memory directly on the stack.  
    The allocated memory chunk does not need to be freed via a free() function call, since the function epilogue returns ESP back toits initial state and the allocated memory is just dropped.  
    
- (Windows) SEH (Structured Exception Handling)  
    SEH records are also stored on the stack (if they are present).  
    
- Buffer overflow protection

- Automatic deallocation of data in stack  
    Perhaps, the reason for storing local variables and SEH records in the stack is that they are freed automatically upon function exit, using just one instruction to correct the stack pointer (it is often ADD). Function arguments, as we could say, are also deallocated automatically at the end of the function. In contrast, everything stored in heap (usually, a big chunk of memory provided by the OS so that aplications can divide it by themselves as they wish | malloc()/free() work with the heap) must be deallocated manually.  
    
##### A typical stack layout

A typical stack layout in a 32-bit environment at the start of a function, before the first instruction execution looks like this :  
| ...     | ...                                       |
|---------|-------------------------------------------|
| ESP-0xC | local variable #2, marked in IDA as var_8 |
| ESP-8   | local variable #1, marked in IDA as var_4 |
| ESP-4   | saved value of EBP                        |
| ESP     | return address                            |
| ESP+4   | argument#1, marked in IDA as arg_0        |
| ESP+8   | argument#2, marked in IDA as arg_4        |
| ESP+0xC | argument#3, marked in IDA as arg_8        |
| ...     | ...                                       |

##### Noise in stack

Noise valueds in the stack refers to what was left in there after other function's executions. For example :  
```C
#include <stdio.h>

void f1(){
    int a=1, b=2, c=3;
};

void f2(){
    int a, b, c;
    printf("%d, %d, %d\n", a, b, c);
};

int main(){
    f1();
    f2();
};
```
When we execute this the result in the screen will be `1, 2, 3` but we did not set any variables in f2().  
These are "ghosts" values, which are still in the stack.  

##### Exercises :

- challenge #52 :  
    What does this code do?
```assembly
$SG3103    DB    '%d', 0aH, 00H

_main      PROC  
           push  0
           call  DWORD PTR __imp__time64
           push  edx
           push  eax
           push  OFFSET $SG3103 ; '%d'
           call  DWORD PTR __imp__printf
           add   esp, 16
           xor   eax, eax
           ret   0
_main      ENDP
```
Additional question: why MSVC replaced time() with time64()? Is it correct? Dangerous? What printf() will print after year 2038?  

*This prints the number of seconds elapsed since midnight, January 1, 1970 (UTC).  
time() is the old 32-bit time --> this is not recommended as the end in size of 32-bit time is January 18, 2038. The use of 32-bit time is not allowed on 64-bit platforms.*  

### Chapter 6 : printf() with several arguments

- In MSVC the first 4 arguments has to be passed through the RCX, RDX, R8, R9 registers in Win64, while all the rest via the stack.  

- In GCC, the first 6 arguments are passed through RDI(EDI), RSI, RDX, RCX, R8, R9 registers and all the rest via the stack.  

- In ARM, the first 4 arguments are passed through R0-R3 registers and all the rest via the stack.  

Typical behavior of printf() with several arguments :  

- x86 :
```assembly
...
PUSH  3rd argument
PUSH  2nd argument
PUSH  1st argument
CALL  function
; modify stack pointer (if needed)
```

- x64 (MSVC) :
```assembly
MOV RCX, 1st argument
MOV RDX, 2nd argument
MOV R8, 3rd argument
MOV R9, 4th argument
...
PUSH 5th, 6th argument, etc (if needed)
CALL function
; modify stack pointer (if needed)
```

- x64 (GCC) :
```assembly
MOV RDI, 1st argument
MOV RSI, 2nd argument
MOV RDX, 3rd argument
MOV RCX, 4th argument
MOV R8, 5th argument
MOV R9, 6th argument
...
PUSH 7th, 8th argument, etc (if needed)
CALL function
; modify stack pointer (if needed)
```

- ARM :
```assembly
MOV R0, 1st argument
MOV R1, 2nd argument
MOV R2, 3rd argument
MOV R3, 4th argument
; pass 5th, 6th argument, etc, in stack (if needed)
BL function
; modify stack pointer (if needed)
```

- ARM64 :
```assembly
MOV X0, 1st argument
MOV X1, 2nd argument
MOV X2, 3rd argument
MOV X3, 4th argument
MOV X4, 5th argument
MOV X5, 6th argument
MOV X6, 7th argument
MOV X7, 8th argument
; pass 9th, 10th argument, etc, in stack (if needed)
BL CALL function
; modify stack pointer (if needed)
```

- MIPS (O32 calling convention) :
```assembly
LI $4, 1st argument ; AKA $A0
LI $5, 2nd argument ; AKA $A1
LI $6, 3rd argument ; AKA $A2
LI $7, 4th argument ; AKA $A3
; pass 5th, 6th argument, etc, in stack (if needed)
LW temp_reg, address of function ; LW=Load Word(32-bit)
JALR temp_reg ; JALR=Jump And Link Register
```

### Chapter 7 : scanf()

In x86, the address is represented as a 32-bit number (4 bytes), while in x86-64 it is a 64-bit number (8 bytes).  
Internally in the compiled code, there is no information about pointer types at all.  

##### Exercises

challenge #53 :
This code, compiled in Linux x86-64 using GCC is crashing while execution(segmentation fault). It's also crashed if compiled by MinGW for win32. However, it works in Windows environment if compiled by MSVC 2010 x86. Why?  
```C
#include <string.h>
#include <stdio.h>

void alter_string(char *s)
{
        strcpy (s, "Goodbye!");
        printf ("Result: %s\n", s);
};

int main()
{
        alter_string ("Hello, world!\n");
};
```

*The code is modifying a string constant, which GCC tends to put in a read-only memory seglent (.rodata) in the resultant executable. Writing a read-only memory segment will cause a segmentation fault. MSVC puts string constants in a writable segment, so this would work just fine.*  

### Chapter 8 : accessing passed arguments

We figured out that the caller function is passing arguments to the callee via the stack. But how does the callee access them?  
For example in C :
```C
#include <stdio.h>

int f (int a, int b, int c){
  return a*b+c;
};

int main(){
  printf("%d\n", f(1, 2, 3));
  return 0;
};
```  

We get this after compilation with MSVC 2010 Express :
```assembly
_TEXT SEGMENT
_a$ = 8 ; size = 4
_b$ = 12 ; size = 4
_c$ = 16 ; size = 4
_f  PROC
    push ebp
    mov ebp, esp
    mov eax, DWORD PTR _a$[ebp]
    imul eax, DWORD PTR _b$[ebp]
    add eax, DWORD PTR _c$[ebp]
    pop ebp
    ret 0
_f  ENDP

_main PROC
      push ebp
      mov ebp, esp
      push 3 ; 3rd argument
      push 2 ; 2nd argument
      push 1 ; 1st argument
      call _f
      add esp, 12
      push eax
      push OFFSET $SG2463 ; '%d', 0aH, 00H
      call _printf
      add esp, 8
      ; return 0
      xor eax, eax
      pop ebp
      ret 0
_main ENDP
```  

### Chapter 12 : conditionnal jumps

Typical behavior :  

- x86 :
```assembly
CMP register, register/value
Jcc true ; cc=condition code
false:
... some code to be executed if comparison result is false ...
JMP exit
true:
... some code to be executed if comparison result is true ...
exit:
```

- ARM :
```assembly
CMP register, register/value
Bcc true ; cc=condition code
false:
... some code to be executed if comparison result is false ...
JMP exit
true:
... some code to be executed if comparison result is true ...
exit:
```

### Chapter 15 : simple C-strings processing

Example strlen() :
```C
int my_strlen (const char * str){
  const char *eos = str;
  while( *eos++ ) ;
  return( eos - str - 1 );
};
int main(){
// test
  return my_strlen("hello!");
};
```
Compiling in x86 :
```assembly
_eos$ = -4 ; size = 4
_str$ = 8 ; size = 4
_strlen PROC
  push ebp
  mov ebp, esp
  push ecx
  mov eax, DWORD PTR _str$[ebp] ; place pointer to string from "str"
  mov DWORD PTR _eos$[ebp], eax ; place it to local variable "eos"
$LN2@strlen_:
  mov ecx, DWORD PTR _eos$[ebp] ; ECX=eos

  ; take 8-bit byte from address in ECX and place it as 32-bit value to EDX with sign extension

  movsx edx, BYTE PTR [ecx] ; movsx stand for mov with sign-extend
  mov eax, DWORD PTR _eos$[ebp] ; EAX=eos
  add eax, 1 ; increment EAX
  mov DWORD PTR _eos$[ebp], eax ; place EAX back to "eos"
  test edx, edx ; EDX is zero?
  je SHORT $LN1@strlen_ ; yes, then finish loop
  jmp SHORT $LN2@strlen_ ; continue loop
$LN1@strlen_:
  
  ; here we calculate the difference between two pointers

  mov eax, DWORD PTR _eos$[ebp]
  sub eax, DWORD PTR _str$[ebp]
  sub eax, 1 ; subtract 1 and return result
  mov esp, ebp
  pop ebp
  ret 0
_strlen_ ENDP
```
We get two new instructions here: MOVSX and TEST.  

MOVSX takes a byte from an address in memory ans stores the value in a 32-bit register. MOVSX stands for MOV with Sign-Extend. MOVSX sets the rest of the bits, from the 8th to the 32st, to 1 if the source bytes is negative or to 0 if it is positive.  

By default, the char type is signed in MSVC and GCC. If we have two values of which one is char and the other is int, and if the first value contain -2 (coded as 0xFE) and we just copy this byte into the int container, it makes 0x000000FE, and this from the point of signed int view is 254, but not -2. In signed int, -2 is coded as 0xFFFFFFFE. So if we need to transfer 0xFE from a variable of char type to int, we need to identify its sign and extend it. That is what MOVSX does.  

Then we see TEST EDX, EDX. Here this instruction just checks if the value in EDX equals to 0.  

### Chapter 17 : Floating Point Unit

The FPU is a device within the main CPU (Central Porcessing Unit), specially designed to deal with floating point numbers. It was called "coprocessor" in the past and it stays somewhat aside of the main CPU.  

A number in the IEEE 754 format consists of a *sign*, *significand* (also called *fraction*) and an *exponent*.  

- x86 :  
It is worth looking into [stack machines](https://en.wikipedia.org/wiki/Stack_machine) or learning the basics of the [Forth language](https://en.wikipedia.org/wiki/Forth_(programming_language)), before studying the FPU in x86.  

In the past (before the 80486 CPU) the coprocessor was a separate chip and it was not always pre-installed on the motherboard. It was possible to buy it separately and install it. Starting with the 80486 DX CPU, the FPU is integrated in the CPU.  

The FWAIT instruction reminds us that it switches the CPU to a waiting state, so it can wait until the FPU is done with its work. Another rudiment is the fact that the FPU instruction opcodes start with the so called "escape"-opcodes (D8..DF), opcodes passed to a separate coprocessor.  

The FPU has a stack capable of holding 8 80-bit registers, and each register can hold a number in the [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754-2008_revision) format. They are ST(0)..ST(7). For brievity, IDA and OllyDbg show ST(0) as ST, which is reprented in some textbooks and manuals as "*Stack Top*".  

- ARM, MIPS, x86/x64 SIMD  
In ARM and MIPS the FPU is not a stack, but a set of registers. The same ideology is used in the SIMD extensions of x86/x64 CPUs.  

- C/C++  
The standard C/C++ languages offer at least two floating number types, *float* ([single-precision](https://en.wikipedia.org/wiki/Single-precision_floating-point_format), 32 bits) and *double* ([double-precision](https://en.wikipedia.org/wiki/Double-precision_floating-point_format), 64 bits).  
GCC also supports the *long double* type ([extended precision](https://en.wikipedia.org/wiki/Extended_precision), 80 bits), which MSVC doesn't.  

The *float* type requires the same number of bits as the *int* type in 32-bit environments, but the number representation is completely different.  

Example :  
```C
#include <stdio.h>
double f (double a, double b){
    return a/3.14 + b*4.1;
};
int main(){
    printf ("%f\n", f(1.2, 3.4));
};
```
Let's compile it in MSVC 2010 :
```assembly
CONST SEGMENT
__real@4010666666666666 DQ 04010666666666666r ; 4.1
CONST ENDS
CONST SEGMENT
__real@40091eb851eb851f DQ 040091eb851eb851fr ; 3.14
CONST ENDS
_TEXT SEGMENT
_a$ = 8 ; size = 8
_b$ = 16 ; size = 8
_f PROC
    push ebp
    mov ebp, esp
    fld QWORD PTR _a$[ebp]

; current stack state: ST(0) = _a

    fdiv QWORD PTR __real@40091eb851eb851f

; current stack state: ST(0) = result of _a divided by 3.14

    fld QWORD PTR _b$[ebp]
 
; current stack state: ST(0) = _b; ST(1) = result of _a divided by 3.14

    fmul QWORD PTR __real@4010666666666666

; current stack state:
; ST(0) = result of _b * 4.1;
; ST(1) = result of _a divided by 3.14
    
    faddp ST(1), ST(0)

; current stack state: ST(0) = result of addition

    pop ebp
    ret 0
_f ENDP
```
FLD takes 8 bytes from stack and loads the number into the ST(0) register, automatically converting it into the internal 80-bit format (extended precision).  

FDIV divides the value in ST(0) by the number stored at address __real@40091eb851eb851f (the value 3.14 is encoded here. Thes assembly syntax does not support floating point numbers, so what we see here is the hexadecimal representation of 3.14 in 64-bit IEEE 754 format.  

After the execution of FDIV, ST(0) hold the quotient.  

There is also the FDIVP instruction, which divides ST(1) by ST(0), popping both these values from stack and then pushing the result.  

Then the FLD instruction pushes the value of b into the stack.  

After that, the quotient is placed in ST(1), and ST(0) hold the value of b.  

The next FMUL instruction does multiplication: b from St(0) is multiplied by the value at __real@4010666666666666 (the number 4.1 is there) and leaves the result in the ST(0) register.  

The last FADDP instruction adds the two values at top of stack, storing the result in ST(1) and then popping the value of ST(0), thereby leaving the result at the top of the stack, in ST(0).  

The function must return its result in the St(0) register, so there are no any other instructions except the function epilogue after FADDP.  

### Chapter 18 : arrays

Example :
```C
#include <stdio.h>

int main(){
  int a[20];
  int i;
  
  for (i=0; i<20; i++){
      a[i]=i*2;
  }
  
  for (i=0; i<20; i++){
      printf("a[%d]=%d\n", i, a[i]);
  }
  
  return 0;
};
```
Lets' compile in MSVC x86 :
```assembly
_TEXT SEGMENT
_i$ = -84 ; size = 4
_a$ = -80 ; size = 80
_main PROC                          |
    push ebp                        |
    mov ebp, esp                    |
    sub esp, 84 ; 00000054H         |--> initalization i=0
    mov DWORD PTR _i$[ebp], 0       |
    jmp SHORT $LN6@main             |
$LN5@main:
    mov eax, DWORD PTR _i$[ebp]
    add eax, 1
    mov DWORD PTR _i$[ebp], eax
$LN6@main:
    cmp DWORD PTR _i$[ebp], 20 ; 00000014H    --> i, 20?
    jge SHORT $LN4@main                       --> if i>=20 jump to LN4
    mov ecx, DWORD PTR _i$[ebp]               --> else
    shl ecx, 1                                --> shift left 1 = multiplication by 2
    mov edx, DWORD PTR _i$[ebp]
    mov DWORD PTR _a$[ebp+edx*4], ecx
    jmp SHORT $LN5@main
$LN4@main:
    mov DWORD PTR _i$[ebp], 0    --> reinitialization of i to 0 for the second loop
    jmp SHORT $LN3@main
$LN2@main:
    mov eax, DWORD PTR _i$[ebp]
    add eax, 1
    mov DWORD PTR _i$[ebp], eax
$LN3@main:
    cmp DWORD PTR _i$[ebp], 20 ; 00000014H
    jge SHORT $LN1@main
    mov ecx, DWORD PTR _i$[ebp]
    mov edx, DWORD PTR _a$[ebp+ecx*4]
    push edx
    mov eax, DWORD PTR _i$[ebp]
    push eax
    push OFFSET $SG2463
    call _printf
    add esp, 12 ; 0000000cH
    jmp SHORT $LN2@main
$LN1@main:
    xor eax, eax
    mov esp, ebp
    pop ebp
    ret 0
_main ENDP
```

##### Buffer overflow

So, array indexing is just *array[index]*. If we study the generated code closely, we can note the missing index bounds checking, which could check if it is less than 20. What if the index is 20 or greater? That's the one C/C++ feature is often blamed for.  

Here is a code that succesfully compiles and works :
```C
#include <stdio.h>

int main(){
    int a[20];
    int i;
    
    for (i=0; i<20; i++){
        a[i]=i*2;
    }
    
    printf("a[20]=%d\n", a[20]);
    
    return 0;
};
```
Let's comile it :
```assembly
$SG2474 DB 'a[20]=%d', 0aH, 00H
_i$ = -84 ; size = 4
_a$ = -80 ; size = 80
_main PROC
    push ebp
    mov ebp, esp
    sub esp, 84
    mov DWORD PTR _i$[ebp], 0
    jmp SHORT $LN3@main
$LN2@main:
    mov eax, DWORD PTR _i$[ebp]
    add eax, 1
    mov DWORD PTR _i$[ebp], eax
$LN3@main:
    cmp DWORD PTR _i$[ebp], 20
    jge SHORT $LN1@main
    mov ecx, DWORD PTR _i$[ebp]
    shl ecx, 1
    mov edx, DWORD PTR _i$[ebp]
    mov DWORD PTR _a$[ebp+edx*4], ecx
    jmp SHORT $LN2@main
$LN1@main:
    mov eax, DWORD PTR _a$[ebp+80]
    push eax
    push OFFSET $SG2474 ; 'a[20]=%d'
    call DWORD PTR __imp__printf
    add esp, 8
    xor eax, eax
    mov esp, ebp
    pop ebp
    ret 0
_main ENDP
_TEXT ENDS
END
```
The code prints this result : *a[20]=1638280*  
It is just something that was lying in the stack near to the array, 80 bytes away from its first element.  

Let's try to find out where did this value come from, using OllyDbg. Let's load and find the value located right after the last array element :  
<img src="https://github.com/sirbrowser/astroworld/blob/master/images/olly1.PNG">  
Judging by the stack layout, this is the saved value of the EBP register.  

Let's trace further and see how it gets resolved:  
<img src="https://github.com/sirbrowser/astroworld/blob/master/images/olly2.PNG">  
Indeed, how it could be different? The compiler may generate some additionnal code to check the index value to be always in the array's bounds (like in higher-level programming languages) but this makes the code slower.  

##### Writing beyond array bounds

We succesfully read some values from the stack illegaly, but what if we could write something to it?  
Here is what we got in C:  
```C
#include <stdio.h>

int main(){
  int a[20];
  int i;
  
  for(i=0; i<30; i++){
    a[i]=i;
  }
  
  return 0;
};
```
 And what we get in MSVC :
 ```assembly
 _TEXT SEGMENT
_i$ = -84 ; size = 4
_a$ = -80 ; size = 80
_main PROC
  push ebp
  mov ebp, esp
  sub esp, 84
  mov DWORD PTR _i$[ebp], 0
  jmp SHORT $LN3@main
$LN2@main:
  mov eax, DWORD PTR _i$[ebp]
  add eax, 1
  mov DWORD PTR _i$[ebp], eax
$LN3@main:
  cmp DWORD PTR _i$[ebp], 30 ; 0000001eH
  jge SHORT $LN1@main
  mov ecx, DWORD PTR _i$[ebp]
  mov edx, DWORD PTR _i$[ebp] ; that instruction is obviously redundant
  mov DWORD PTR _a$[ebp+ecx*4], edx ; ECX could be used as second operand here instead
  jmp SHORT $LN2@main
$LN1@main:
  xor eax, eax
  mov esp, ebp
  pop ebp
  ret 0
_main ENDP
 ```
 The compiled program crashes after running. No wonder. Let's see where exactly does it crash.  
 Let's load it into OllyDbg, and trace until all 30 elements are written:  
 <img src="https://github.com/sirbrowser/astroworld/blob/master/images/olly3.PNG">  

Trace until the function end:  
<img src="https://github.com/sirbrowser/astroworld/blob/master/images/olly4.PNG">  

Now keep our eyes on the registers.  

EIP is 0x15 now. It is not a legal address for code (at least for win32 code). We got there somehow against our will. It is also interesting that the EBP register contain 0x14, ECX and EDX 0x1D.  

After the control flow was passed to main(), the value in the EBP register was saved on the stack. Then, 94 bytes were allocated for the array and the i variable. That's (20+1)*sizeof(int). ESP now points to the _i variable in the local stack and after the execution of the next PUSH something, something is appearing next to _i.  

That's the stack layout while the control is in main():  
|ESP    |4 bytes allocated for i variable   |
|-------|-----------------------------------|
|ESP+4  |80 bytes allocated for a [20] array|
|ESP+84 |saved EBP value                    |
|ESP+88 |return address                     |

*a[19]=something* statement writes the last *int* in the bounds of the array.  
*a[20]=something* statement writes *something* to the place where the value of EBP is saved.  

Let's take a look at the register state at the moment of the crash. In our case, 20 was written in the 20th element. At the function end, the function epilogue restores the original EBP value. (20 in decimal is 0x14 in hexadecimal). Then RET gets executed, which is effectively equivalent to POP EIP instruction.  

The RET instruction takes the return address from the stack (that is the address in CRT (C Runtime Library), which was called main()), and 21 is stored there (0x15 in hexa). The CPU traps at address 0x15, but there is no executable code there, so exception gets raised.  

Welcome! It is called a buffer overflow!  

Replace the *int* array with a string (char array), create a long string deliberately and pass it to the program, to the function, which does not check the length of the string and copies it in a short buffer, and you'll able to point the program to an address to which it must jump. It is not that simple in reality, but that is how it emerged.  

##### Multidimensional arrays





















