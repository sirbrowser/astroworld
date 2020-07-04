# Reconnaissance

## Index

- [Lab 01](#lab-01)
- [Lab 02](#lab-02)
- [Lab 03](#lab-03)
- [Lab 04](#lab-04)
- [Lab 05](#lab-05)

#### Lab 01

To find the maximum frame size on the network :

`ping <url> -f -l <packet_size>` --> modify the packet size until you find the last value before it says "Packet needs to be fragmented but DF set".<br>

`ping <host> -i <value>` --> -i set a TTL value, it is another mean than `tracert` to find the number of hopes to reach the target.<br>

Use of nslookup :<br>
When you do a nslookup and you get a "non-authoritative answer" you need to obtain the domain's authoritative name server :<br>

```
nslookup    |--> to open nslookup interactive session
set type=cname
<domaine_name>
```<br>
This returns the domain’s authoritative name server, along with the mail server address.<br>

Then you want to obtain the ip address of that server :
```
set type=a
<server_name>
```

#### Lab 02
Finding company's sub-domains using Sublist3r

