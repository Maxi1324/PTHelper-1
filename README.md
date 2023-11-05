## Packet Tracer Helper

Aim of this project was to make it easy to cheat in Packet Tracer Activities
This was a little side project, so the code is not tested very well, and kind of ugly

my code is based on the amazing work of mircodezorzi:
https://github.com/mircodezorzi/pka2xml

he is a hero

###
warning: device switch should always only used alone with no other maipulation results in some errors

### install 

#### windows install
1. download the newest release
2. execute the PacketTracerHelper.exe file
    - keep in mind, that you need also the "internal" folder, so don't delete it

#### platform independet:
1 python 3.9.7 
``` shell
    py -m venv pka_env
    env\Scripts\activate
    pip install pyinstaller PyQt5 docker lxml importlib-metadata matplotlib networkx
    py Gui2.py
```
2. install docker and have the deamon running

### description

This project allows you to cheat in any Packet Tracer activity you need to cheat on. If functionalities are missing, you can implement them yourself, very easily, and hopefully contribute to this project :)

After starting, you will be prompted with the start screen. There, you need to click on the big button in the middle, and then select your start file (the activity file or a colleague's Packet Tracer file).

Next, you'll be on the manipulation screen. On the right, you'll find all the current manipulations, initially none. You can add some by using the "Add Manipulation" button.

Then, you'll be prompted to select one and press "Add."

By clicking on the manipulation in the manipulation screen, you can access the settings of the manipulation.

The last functionality is the "Export" button. This applies all manipulations and creates a new Packet Tracer file with all the changes :)

If you find a bug, pleace report them in an github issue on this repo

### currently implemented maipulations
1.  Reset File Name History

A Packet Tracer File saves always, when it can it's current location or file. This Manipulation allows you to change that. You can remove entries or add them

2. Device Switch

Often Teachers disable the copying of devices form one file to another, or they request you to upload the file at the start of the activity and at the end. They do this, so they can identify if this activity is done by you. This Manipulation allows you to bypass this.

your first selected file is the device source the the second the destination, s the file you select in the settings diialog

3. Change User Informations

Many Cisco Activites are not personaliesd to any extent their only security mechanisms is the packet tracer internal one. When the User Settings are changed the activity is reset. This manipulation bypasses this.

you can change the email, username, and external informations

4. Change Ipv4 Addresses

This allows you to replace ipv4 Addresses actuially is searches in the packet tracer file for anything, that looks like a ip address, so also Broadcast Addresses, Wildcard Masks router ids........

so be careful, this manipulation has a lot of potential

5. Change ipv6 Addresses exact the same like change ipv4 addresses, but with ipv6 addresses. 

these where the good ones the rest works, but really poorly

6. Change DB Grading
sets the persentage to 100% but by removing the criterias, so if the auditor does not check them by one it works, but if he, he will see it

7. Rest File Name History
changes the start date

8. Change OSPFAreas and OSPFProcessIDs
does it best to do it

9. change ACLIpv4
gives it best at renaming or renumbering ipv4 ACLs


10. change ACLIpv6
gives it best at renaming or renumbering ipv6 ACLs

### development

a pka or pkt file are just encrypted xml files, so they are fairly simple to manipulate

1. do the platform independetnd install 
2. implement a Mani(Manipulaton)
    - create a new module this module needs three parts the 
    - define the name of the manipulation
    - define the manipulation function
        - parameter: xml in etree format    
        - returns: manipulated xml
        - called on export
    - define the settings function
        - parameter: xml
        - called after added to manipulation stack
3. build use pyistaller

