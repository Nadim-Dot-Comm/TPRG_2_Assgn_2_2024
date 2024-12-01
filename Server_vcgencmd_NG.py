#TPRG-2131-01
#Nadim Gutto -- 100665657
#A part of the code was supplied by the teacher which I revised and made changes to make it my own work
#with the help of in-class and online materials.

#https://elinux.org/RPI_vcgencmd_usage
#https://www.nicm.dev/vcgencmd/
#https://www.tomshardware.com/how-to/raspberry-pi-benchmark-vcgencmd

#I couldn't fix the "server already in use" error after the first attempt, so do you mind waiting
#10 seconds before you try a second or third attempt or you can change ports.

'''This is the server portion and should run on the pi, this runs first'''

#Import library's
import socket
import os
import json

#Function to get the core temperature of the Raspberry Pi
def get_temperature():
    temp = os.popen('vcgencmd measure_temp').readline() #Executes vcgencmd command to get Temperature
    return round(float(temp.replace("temp=", "").replace("'C\n", "")), 1) #Examines and returns the temperature as a float, rounds to 1 decimal place.

#Function to get the voltage core on the Raspberry Pi
def get_voltage():
    voltage = os.popen('vcgencmd measure_volts core').readline() #Executes vcgencmd command to get Voltage
    return round(float(voltage.replace("volt=", "").replace("V\n", "")), 1) #Examines and returns the voltage as a float, rounds to 1 decimal place.

#Function to get the GPU memory usage on the Raspberry Pi
def get_gpu_memory():
    gpu_memory = os.popen('vcgencmd get_mem gpu').readline() #Executes vcgencmd command to get GPU memory
    return round(float(gpu_memory.replace("gpu=", "").replace("M\n", "")), 1) #Examines and returns GPU memory in MB as a float, rounds to 1 decimal place.

#Function to get core clock speed on the Raspberry Pi
def get_core_clock():
    core_clock = os.popen('vcgencmd measure_clock core').readline() #Executes vcgencmd command to get core clock speed
    return round(int(core_clock.split("=")[1]) // 1000000, 1) #converts Hz to MHz,rounded to 1 decimal place

#Function to get the arm processor clock speed on the Raspberry Pi
def get_arm_clock():
    arm_clock = os.popen('vcgencmd measure_clock arm').readline() #Executes vcgencmd command to get ARM clock speed
    return round(int(arm_clock.split("=")[1]) // 1000000, 1) #converts Hz to MHz,rounded to 1 decimal place

#Initializes the socket
s = socket.socket()
print("Socket created... ")

host = ''                       #Localhost
port = 5000                     #Port for communication
s.bind((host, port))            #Binds the server to the host and port
s.listen(5)                     #Listens up to 5 incomming connections
print('Socket is listening')

#Accepts connection from client
c, addr = s.accept()
print('Got connection from', addr)

#Function to send data to the client
def Deliver_data():

    #Collect data from the functions
    temperature = get_temperature()
    voltage = get_voltage()
    gpu_memory = get_gpu_memory()
    core_clock = get_core_clock()
    arm_clock = get_arm_clock()

    #Create a dictionary with the data
    data = {
        "Temperature": temperature,
        "Voltage": voltage,
        "GPUMemory": gpu_memory,
        "CoreClock": core_clock,
        "ARMClock": arm_clock
                            }

    #Convert dictionary to JSON and send it
    json_data = json.dumps(data)
    res = bytes(json_data, 'utf-8') #Converts the JSON strings to bytes
    
    #Handles errors if data is not sent
    try:
        c.send(res)  #Send the data as bytes
        print("Data sent successfully")
    except OSError as e:
        print(f"Error sending data: {e}")
#         break #Exit the loop if sending fails

#Main function to run the server
def main():
    Deliver_data() #Sends the data
    c.close() #Closes the connection after sending data


if __name__== '__main__':
    try:
        main() #Calls up the main funtion
    
    except KeyboardInterrupt:
        print("Bye...") #Graceful exit (Ctrl+C)
    
    finally:
        s.close() #Closes the server socket