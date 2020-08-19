# Reverse engineering for beginners by Dennis Yurichev

Each MIPS instruction is 32 bits<br>

The main difference between x86/ARM and x64/ARM64 is that the pointer to the stack is now 64-bits.<br>

Differences between intel syntax and AT&T syntax :<br>
  - In AT&T source and destination are in opposite order :<br>
      Intel syntax : <instruction> <dest> <source> (a=b)<br>
      AT&T syntax : <instruction>  <source> <dest> (a-->b)<br>
  - In AT&T, a register is preceded by "%" and a number by "$"<br>
  
  #### Chapter 4 : Function prologue and epilogue
  
  A function prologue is a sequence of instructions at the start of the function. It often looks like this
  
  csbqcbujqs
  
