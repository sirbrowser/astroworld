# Practical Cyber Forensics

## Index 
- [Introduction to cyber forensics](#introduction-to-cyber-forensics)

#### Introduction to cyber forensics

###### Forensic investigation process :<br>
- Incident : Occurence of a cybercrime instance where digital devices like computers, mobile, ect, have been used to commit a crime.<br>

- Identification : scope of actions before starting a forensic examination. (who are the prime suspects? what are the best sources of potential digital evidence that will be further investigated?).
                   It prevents that no essential evidence is missed and costs can be estimated in advance and the scope of the case can be adjusted accordingly.<br>

- Seizure : applicable with the law.<br>

- Imaging : after being seized a forensic image of that evidence is created for further analysis. It is an exact bit by bit copy of a physical storage.<br>

- Hashing : every forensic image is hashed to maintain integrity of that data. Any tampering with evidence will result in a different hash value, and the digital evidence will not be admissible in a court of law.<br>

- Analysis : analysis of all digital evidence.<br>

- Reporting : all the relevant findings should be presented in a report. The investigator cannot present their personal views in this report. It should be easily understandable by any non technical person.<br>

- Preservation : once evidence is collected, it is important to protect it from any type of alteration or deletion. For example, it might be necessary to isolate host systems from the rest of the network.<br>

###### Forensic protocol for evidence acquisition :<br>
- Perform Live forensics (RAM Capturing)
- Shut down the system
- Obtain the storage device (HDD or SSD)
- Perform forensic hashing & imaging of the storage device
- Analyse forensic image with various tools

###### Digital forensic standards and guidelines :<br>
- National Institute of Standard Technology (NIST)
- National Institute of Justice (NIJ)
- International Oragnization on Computer Evidence (IOCE)
- American Society of Crime Laboratory Directors (ASCLD)
- Laboratory Accreditation Board (LAB)
- American Society for Testing and Materials (ASTM)
- ISO SC 27 CS1
- Audio Engineering Society (AES)
- Scientific Working Group on Digital Evidence (SWGDE)
- Scientific Working Group on Imaging Technology (SWGIT)
- Association of Chief Police Officers (ACPO)

**Digital evidence** comprises physical devices such as computer systems, mobile phones, flash drives, memory cards, routers, switches, modems, etc., and the electronic information stored in these devices.<br>
There are four characterisics of digital evidence :
- Latent/Hidden
- Crosses jurisdictionnal borders quickly and easily
- Can be altered, damaged, or destroyed easily
- Can be time sensitive

**Write blockers** are devices that are used for acquisition of information on a drive without creating the possibility of accidentally damaging or wiping the drive contents. They only allow read commands to pass and block any write commands.<br>
There are two types of write blockers :
- Native : uses the same interface on for both input and output (IDE to IDE write block for example)
- Tailgate : uses a different interface for each side (Firewire to SATA write block for example)

**Forensic triage** is the process of collecting, assembling, analyzing, and **prioritizing** digital evidence.<br>

**Chain of custody** refers to the documentation of a piece of evidence throughout its life cycle. Maitaining a proper chain of custody is very important. Any break can lead to a piece of evidence being excluded in the court.<br>
The following must be included in a chain of custody form :
- a list of all devices that were secured from the crime scene for further investigation
- accurate information about the devices that has been copied, transferred, and collected
- timestamp of all the collected evidence
- who processed the item?
- who is the owner of the item?
- where was it taken or seized from?
- all electronic evidence that was collected from the crime scene must be properly documented each time that evidence is viewed
- such documentation must be made available, if requested by the client, throughout the pre-trial discovery phase
