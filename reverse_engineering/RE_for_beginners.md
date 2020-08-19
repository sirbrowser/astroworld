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