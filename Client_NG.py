#TPRG-2131-01
#Nadim Gutto -- 100665657
#A part of the code was supplied by the teacher which I revised and made changes to make it my own work
#with the help of in-class and online materials.

#I couldn't fix the "server already in use" error after the first attempt, so do you mind waiting
#10 seconds before you try a second or third attempt or you can change ports.

'''This is the client portion and should run on the PC and after the server is running first'''

#Import library's
import socket
import json

#Function to handle errors when connecting to the server
def handle_connection_error(e):
    print(f"Error: {e}")
    #Lets the user know why it's not connecting
    print("Could not connect to the server. Please ensure the server is running or is reachable.")

#Connects to the server
s = socket.socket()

host = '10.102.13.59'  #IP address of the Raspberry Pi
port = 5000            #Port the server is listening

try:
    s.connect((host, port))              #Trys to establish a connection to the server
    print(f"Connected to {host}:{port}") #Lets the user know the connection was a success

    response = s.recv(1024).decode()     #Receive and decode the response

    #Convert the JSON response back to a Python dictionary
    data = json.loads(response)

    #Prints each piece of data on separate lines
    print("Temperature: {} °C".format(data["Temperature"])) #Displays Temperature
    print("Voltage: {} V".format(data["Voltage"]))          #Displays Voltage
    print("GPU Memory: {} MB".format(data["GPUMemory"]))    #Displays GPU memory
    print("Core Clock: {} MHz".format(data["CoreClock"]))   #Displays Core clock speed
    print("ARM Clock: {} MHz".format(data["ARMClock"]))     #Displays ARM clock speed

except socket.error as e:
    handle_connection_error(e)  #Handles socket connection errors

except Exception as e:
    print(f"An unexpected error occurred: {e}") #Catches unexpected errors

finally:
    s.close()  #Closes the socket when done
    print("Connection closed.") #Lets the user know the connection closed
