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
| ESP | return address |
| ESP+4 | arguments#1, marked in IDA as arg_0 |

