# Reverse engineering for beginners by Dennis Yurichev

Each MIPS instruction is 32 bits<br>

The main difference between x86/ARM and x64/ARM64 is that the pointer to the stack is now 64-bits.<br>

Differences between intel syntax and AT&T syntax :<br>
  - In AT&T source and destination are in opposite order :<br>
      Intel syntax : <instruction> <dest> <source> (a=b)<br>
      AT&T syntax : <instruction>  <source> <dest> (a-->b)<br>
  - In AT&T, a register is preceded by "%" and a number by "$"<br>
  
  #### Chapter 4 : Function prologue and epilogue
  
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
  
