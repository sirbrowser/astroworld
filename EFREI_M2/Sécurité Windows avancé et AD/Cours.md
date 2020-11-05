# Sécurité Windows avancée & AD

### Module 1 : Windows Architecture & Security Mechanisms

##### Section 1 : Core OS components

All modern releases of Windows are based on the NT kernel.  
Le user mode ne communique jamais directement avec la mémoire.  

<img src=https://github.com/sirbrowser/astroworld/blob/master/images/couches.PNG >  

- debugger utility : allow inspection of internal memory structure / stope execution of OS under conditions.
- debugger mode : live debugging / memory dumps (copy of memory)

- complet memory dump : big files, several hundred of Gb
- kernel memory dump : only kernel memory data
- small memory dump : only crash memory data

`.sympath` --> précise les symboles au debugger.  

- multitasking n'est pas vrmt du multitasking, le processeur execute un petit content d'une tache et aisni de suite ce quii peut faire croire a l'user a du multitasking.  

- preemption : permet le controle de priorité / task switching in windows / only NT family / tasks can be interrupted  

- interruptions :
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/interruption.PNG >  

- virtual memory :
memory management consists in a strong collaboration between hardware (modern CPU provides a unit called MMU : translation between virtual and physical address) and software.  



#### Section 2 : Windows boot sequence

#### Section 3 : Windows debugger
