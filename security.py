#pip install python-dotenv
from itertools import count
import subprocess as sp
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env') #Please, Check the route for .env file.
load_dotenv(dotenv_path)

# Set the limits for CPU and RAM
CPU_USE_LIMIT=os.environ.get("CPU_USE_LIMIT") #Specific the percent limit use for CPU
CPU_TEMP_LIMIT=os.environ.get("CPU_TEMP_LIMIT") #Specific the TEMP Limit in °C
RAM_USE_LIMIT=os.environ.get("RAM_USE_LIMIT") #Specific the RAM percent limit

#Savig System info in variables...
#CPU USE
cmd_CPU_USE = "top -bn1 | awk '/Cpu/ { cpu =  100 - $8  }; END { print cpu }'"
CPU_USE = sp.getoutput(cmd_CPU_USE)

#CPU TEMPERATURE
cmd_CPU_TEMP='vcgencmd measure_temp|cut -c 6-7'
CPU_TEMP = sp.getoutput(cmd_CPU_TEMP)
cmd_CPU_TEMP_COMPLETA='vcgencmd measure_temp|cut -c 6-11'
CPU_TEMP_COMPLETA = sp.getoutput(cmd_CPU_TEMP_COMPLETA)

#RAM INFO
cmd_RAM_USE = "free | grep Mem | awk '{print $3/$2 * 100.0}'"
RAM_USE = sp.getoutput(cmd_RAM_USE)

#SSH CONNECTIONS
cmd_SSH_IP_CONNECTION = "pinky | sed -e 's/\s/#/g' | grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'"
SSH_IP_CONNECTION = sp.getoutput(cmd_SSH_IP_CONNECTION)

MESSAGE = ""
count = 0 #If the count is switch to 1 , dont andd first message

# Step 1 - Cheking CPU Temperature
if int(CPU_TEMP) > int(CPU_TEMP_LIMIT):
    MESSAGE+="RASPBERRY NOTIFICATION!!: \n\n"
    count = 1 
    MESSAGE+="- CPU temperature: "+CPU_TEMP_COMPLETA+" \n"

#Step 2 - Cheking CPU USED
if int(float(CPU_USE)) > int(CPU_USE_LIMIT): 
    if count == 0:
        MESSAGE+="RASPBERRY NOTIFICATION!!: \n\n"
        count = 1
    MESSAGE+="- CPU usage: "+CPU_USE+"% \n"

#Step 3 - Cheking RAM PERCENT USED
if int(float(RAM_USE)) > int(RAM_USE_LIMIT): 
    if count == 0:
        MESSAGE+="RASPBERRY NOTIFICATION!!: \n\n"
        count = 1
    MESSAGE+="- RAM usage: "+RAM_USE+"% \n"

#Step 4 - Cheking IPS in network
if len(SSH_IP_CONNECTION) > 5: #One IP has more than 5 chars
    if count == 0:
        MESSAGE+="RASPBERRY NOTIFICATION!!: \n\n"
        count = 1

    MESSAGE+="- SSH connections: \n"
    IPS = SSH_IP_CONNECTION.splitlines()

    for IP in IPS:
	    MESSAGE+="    "+IP+" \n" 

#Sending alarm
if count == 1:
    #Getting main variables from .env
    TOKEN = os.environ.get("TOKEN")
    ID = os.environ.get("ID")
    
    url_req = "https://api.telegram.org/bot" + TOKEN + "/sendMessage" + "?chat_id=" + ID + "&text=" + MESSAGE 
    requests.get(url_req)