# cleversafe
- get_events.py is a simple plugin using cleversafe's API to get messages from the GUI console. 

- setup_new_rack.sh and setup_new_rack_expect work together to configure new hosts in a cleversafe cluster. The cli interface uses nut which is not configureable remotely. using expect, i can keep the ssh connection open and send commands like i was standing in front of the server.. The bash script simply loops values through the expect script. 

- ipmi_setup is the last script ran and it uses expect to connect and configure ipmi. 
