# Introduction to splunk Entreprise Security

## Index :
- [Splunk terminology](#splunk-terminology)
- [Splunk infrastructure](#splunk-infrastructure)
- [Splunk roles](#splunk-roles)
- [Some useful search commands](#some-useful-search-commands)

#### Splunk terminology

All splunk terminology is available on splunk website (it is callled "splexicon") --> https://docs.splunk.com/Splexicon

- Event : single piece of data in Splunk, similar to a record in a log file. When datat is indexed, it is divided into individual events.<br>
  --> each event is given a timestamp, host, source and sourcetype.<br>
  --> similar events can be categorized together with event types.<br>
 
- Dashboard<br>
  --> are written in XML.<br>
  --> can be converted into HTML to be displayed on websites for example.<br>
  
- SPL (Search Processing Language)<br>
  --> Splunk search language.<br>
  --> syntax is based on Unix pipeline and SQL.<br>
  
- Index<br>
  --> container of data.<br>
  --> permit access control and permissions.<br>
  
- Lookup<br>
  --> product csv human redabled.<br>
  --> for example in a log we can have a code 404 and transform it to display "error" for reports to non-technical people.<br>
  
- Onboarding<br>
  --> collect, parsing and sending logs to indexers.
  
- Transforming command<br>
  --> commands that create statistics and visualizations.<br>
  
-------------------------------------------------

https://splunkbase.splunk.com/ --> splunk marketplace for add-ons to integrate into splunk.<br>

-------------------------------------------------

Before configuring splunk you need to ask the following questions :<br>
- What index should store this data?<br>
- What is the desired retention period?<br>
- Who should have access to that data?<br>
- Is there a sample log to review? == to test before prod.<br>

'/opt/splunk/bin/splunk btool inputs list --debug' --> find conf file to edit or troubleshoot.<br>

#### Splunk infrastructure

- Indexer : database server for splunk, it porcess machine data and transforms them into splunk indexes as events.<br>

- Search Head : this is where users interact with splunk, it indexes data in indexers.<br>
  --> this is where dashboards/visualizations/reports live and run.<br>

- Forwarder : forward data to another instance, it consumes data and forward to indexers (for example forwarder is configured on a web server and will send log to indexers).<br>
  
  --> universal forwarder : A type of forwarder, which is a Splunk Enterprise instance that sends data to another Splunk Enterprise instance or to a third-party system. The universal forwarder is a dedicated, streamlined version of Splunk Enterprise that contains only the essential components needed to forward data. The universal forwarder does not support python and does not expose a UI. In most situations, the universal forwarder is the best way to forward data to indexers. Its main limitation is that it forwards unparsed data, except in certain cases, such as structured data. You must use a heavy forwarder to route event-based data.<br>
 
  --> heavy forwarder : A type of forwarder, which is a Splunk Enterprise instance that sends data to another Splunk Enterprise instance or to a third-party system. A heavy forwarder has a smaller footprint than a Splunk Enterprise indexer but retains most of the capabilities of an indexer. An exception is that it cannot perform distributed searches. You can disable some services, such as Splunk Web, to further reduce its footprint size. Unlike other forwarder types, a heavy forwarder parses data before forwarding it and can route data based on criteria such as source or type of event. It can also index data locally while forwarding the data to another indexer.<br>
  
- Syslog receiver<br>
  --> !! do not send syslog over TCP or UDP inputs because data can be lost.<br>
  --> it is better to have a dedicated product, using syslog-ng on a forwarder.<br>

- Deployment server<br>
  --> centralized configuration manager, grouping different splunk instances.<br>
  
- Splunk clustering (2 types)<br>
  --> indexer replication cluster.<br>
  --> search head cluster.<br>
  
- CIM (Common Information Model)<br>
  --> allows for common fields to be used regardless of data type.<br>
  --> makes corrrelation of possible and practical sources.<br>
  --> for example a source field can be named differently (SRC, source, ip_source, ...).<br>
  
- splunkd<br>
  --> manage indexers, search heads forwarders and browser interface.<br>
  
- Ports<br>
  --> 8089 : splunkd (search commands, communication with license and deployment servers, REST API, CLI.<br>
  --> 8000 : splunk web<br>
  --> 8065 : application server<br>
  --> 8191 : KVStore<br>
  
#### Splunk roles

- Admin : can install apps and create knowledge objects for all users.<br>
- Power : can create and store knowledge objects for users of an app and do realtime searches.<br>
- User : Will only see their own knowledge objects and those shared with them.<br>
  
#### Some useful search commands

`sourcetype=<source> | top limit=20 <field>` --> show top values of a field.<br>
`sourcetype=<source> | table _time,process,user` --> create a table with 3 fields<br>
`""""""""""""""""""" | chat count by dest-port time chart count (<>) by <>`<br>
`iplocation` and `geostats`  --> data visualization geo ip.<br>
`eval` --> replace values.<br>
`rename` --> rename fields in table.<br>
`dedup` --> remove duplicated values of a field.<br>
  
---------------------------------------------

How does the storage works?<br>

--> hot bucket : newest ones open for writing (readable)<br>
--> warm bucket : recent data, buckets are closed (read-only)<br>
--> cold bucket : oldest data still in the index (read-only)<br>
--> frozen bucket : deletion is the default action, not searchable<br>

