# Active Directory section

## Index

- [Active Directory overview](#Active-Directory-overview)

## Active Directory overview

#### What is a Active directory ?

1. Directory service developed by Microsoft to manage Windows domain networks

2. Stores information related to objects, such as Computers, Users, Printers...

3. Authenticates using Kerberos tickets --> Non-Windows devices, such as Linux machines, firewalls... can also authenticate to Active Directory via RADIUS or LDAP

#### Why Active Directory ?

Active Directory is the most commonly used identity management service in the world. 

Can be exploited wihtout ever attacking patchable exploits

#### Physical AD Components

- [Domain Controller](#Domain-Controller)
- [AD DS data store](#AD-DS-data-store)

##### Domain Controller 

It's the domain head honcho. 
A domain controller is a server with the AD DS server role installed that has specifically been promoted to a domain controller.

--> Host a copy of the AD DS directory store<br>
--> Provide authentication and authorization services<br>
--> Replicate updates to other domain controllers in the domain and forest<br>
--> Allow administrative access to manage users accounts and network resources<br>

#### AD DS data store

The AD DS data store contains the database files and processes that store and manage directory information for users, services and applications

--> Store the Ntds.dir file --> this file contains all informations from AD data including password hashes.<br>
--> The file is stored by default in the %SystemRoot%\NTDS folder on all domain controllers<br>
--> The file is accessible only through the domain controller processes and protocols

#### Logical AD Components

- [The AD DS Schema](#The-AD-DS-Schema)
- [Domains](#Domains)
- [Trees](#Trees)
- [Forests](#Forests)
- [Organizational Units](#Organizational-Units)
- [Trusts](#Trusts)
- [Objects](#Objects)

##### The AD DS Schema

It's a **rule book**.<br>

--> It define every type of object that can be stored in the directory.<br>
--> It enforces rules regarding object creation and configuration<br>

##### Domains

Domains are used to group and manage objects in an organization.<br>

--> It's an administrative boundary for applying policies to groups of objects<br>
--> It's a replication boundary for replicating data betwenn domain controllers
--> It's an authentication and authorization boundary that provides a way to limit the scope of access to ressources

##### Trees

A domain tree is a hierarchy of domains in AD DS

All domains in the tree :<br>
--> share a contigous namespace with the parent domain<br>
--> can have additional child domains<br>
--> by default create a two-way transitive trust with other domains<br>

##### Forests

A forest is a collection of one or more domain trees

Forests:<br>
--> share a common schema<br>
--> share a common configuration partition<br>
--> share a common global catalog to enable searching<br>
--> enable trusts between all domains in the forest<br>
--> share the Entreprise Admins and Schema Admins groups<br>

##### Organizational Units

OUs are Active Directory containers that can contain users, groups, computers, and other Ous

OUs are used to:<br>
--> represent your organizatio hierarchically and logically<br>
--> mange a collection of objects in a consitent way<br>
--> delegate permissions to administer groups of objects<br>
--> apply policies<br>

##### Trusts

Trusts provide a mechanism for users to gain access to resources in another domain<br>

Types of trusts :<br>
--> Bidirectional --> The trustdirection flows from trusting domain to the trusted domain<br>
--> Transitive --> The trust relationship is extended beyond a two-domain trust to include other trusted domains<br>

All domains in a forest trust all other domains in the forest<br>
Trusts can extended outside of the forest<br>


#### Objects

A object appears in an OUs.

Differents objects :<br>
User --> Enables network resource access for a user<br>
InetOrgPerson --> Similar to a user account + Used for compatibility with other directory services<br>
Contacts --> Used primarily to assign e-mail addresses to external users + Does not enable network access<br>
Groups --> Used to simpily the administration of access control<br>
Computers --> Enables authentication and auditing of computer access to resources<br>
Printers --> Used to simplify the process of locating and connecting to printers<br>
Shared folders --> Enables users to search for shared folders based on properties<br>






































