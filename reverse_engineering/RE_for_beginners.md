# Reverse engineering for beginners by Dennis Yurichev

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

### Chapter 10 : pointers