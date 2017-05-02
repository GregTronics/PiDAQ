#-----------------------------------------------------------------
#Imports
#-----------------------------------------------------------------
import time
import os
import sys
import signal

#-----------------------------------------------------------------
# System import for Raspberry Pi drivers
#-----------------------------------------------------------------
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#-----------------------------------------------------------------
# Adafruit Library for current sense chip
#-----------------------------------------------------------------
#import Adafruit_ADS1x15
#adc = Adafruit_ADS1x15.ADS1015()
#GAIN = 1

#-----------------------------------------------------------------
# Globals
# menuChoice		-	Variable for the main menu
# storagePath		-	Variable to define the subfolder to store data
# fileExt			-	Variable to define the extension of the stored file
# filePath			-	Variable to define the file name 
# sampleRate		-	Variable to define the amount of time to wait between
#					-	current sense samples
# temperatureUnit	-	Variable to define the temperature unit to use	
#-----------------------------------------------------------------
menuChoice = ''
storagePath = "/testing/"
fileExt = ".txt"
filePath = 'DefaultName'
sampleRate = 10;
temperatureUnit = "B"

#-----------------------------------------------------------------
# Dictionary of current labels
#-----------------------------------------------------------------
currentLabels = {}
currentLabels['J6']="1V0"
currentLabels['J10']="1V2"
currentLabels['J8']="3V3"
currentLabels['J3']="1V8"

#-----------------------------------------------------------------
# Dictionary of current status
#-----------------------------------------------------------------
currentStatus = {}
currentStatus['J6']="Enabled"
currentStatus['J10']="Enabled"
currentStatus['J8']="Enabled"
currentStatus['J3']="Enabled"

#-----------------------------------------------------------------
# Dictionary of thermocouple labels
#-----------------------------------------------------------------
thermoLabels = {}
thermoLabels['T0']="Thermocouple 0"
thermoLabels['T1']="Thermocouple 1"
thermoLabels['T2']="Thermocouple 2"
thermoLabels['T3']="Thermocouple 3"
thermoLabels['T4']="Thermocouple 4"
thermoLabels['T5']="Thermocouple 5"
thermoLabels['T6']="Thermocouple 6"
thermoLabels['T7']="Thermocouple 7"

#-----------------------------------------------------------------
# Dictionary of thermocouple addresses
#-----------------------------------------------------------------
thermoAddress = {}
thermoAddress['T0']="3b-0cdc03883a4a"
thermoAddress['T1']="3b-2cdc03883a8c"
thermoAddress['T2']="3b-0cdc03883a65"
thermoAddress['T3']="3b-0cdc03883a6f"
thermoAddress['T4']="3b-0cdc03883a53"
thermoAddress['T5']="3b-2cdc03883a9f"
thermoAddress['T6']="3b-2cdc03883a78"
thermoAddress['T7']="3b-2cdc03883a82"

#-----------------------------------------------------------------
# Dictionary of thermocouple status
#-----------------------------------------------------------------
thermoStatus = {}
thermoStatus['T0']="Enabled"
thermoStatus['T1']="Enabled"
thermoStatus['T2']="Enabled"
thermoStatus['T3']="Enabled"
thermoStatus['T4']="Enabled"
thermoStatus['T5']="Enabled"
thermoStatus['T6']="Enabled"
thermoStatus['T7']="Enabled"

#-----------------------------------------------------------------
# Globals to define the path to get the temperature data
#-----------------------------------------------------------------
tcStart = '/sys/bus/w1/devices/'
tcEnd = '/w1_slave'

#-----------------------------------------------------------------
# Welcome prompt
#-----------------------------------------------------------------
print('---------------------------------------------------\n')
print('Welcome to the Raspberry Pi Data Acquistion System!')
print('---------------------------------------------------\n')

#-----------------------------------------------------------------
# Menu definition dictionary
#-----------------------------------------------------------------
menu = {}
menu['F']="- Set the filename for recording."
menu['R']="- Set the sample rate for recording."
menu['T']="- Set the thermocouple labels."
menu['E']="- Enable/Disable thermocouple channels."
menu['U']="- Set temperature unit."
menu['C']="- Set the current sensor labels."
menu['N']="- Enable/Disable current channels."
menu['M']="- Set ADAS modes and durations."
menu['D']="- Display Settings."
menu['S']="- Start the DAQ."
menu['A']="- Autodetect Sensors."
menu['Q']="- Quit."

#-----------------------------------------------------------------
# Function to handle Ctrl+C exit
#-----------------------------------------------------------------
def signal_handler(signal, frame):
	print('Data Acquistion is complete')
	sys.exit(0)
	
#-----------------------------------------------------------------
# Function to change the current sensor label
#-----------------------------------------------------------------
def currentInput(tempChoice):
	validFlag = False
	#Loop until valid response
	while validFlag == False:
		#Input prompt
		print "Selected " + tempChoice + " to change. Please enter a new label : "
		newLabel = raw_input()
		
		#Check for blank
		if newLabel == '':
			print "Cannot be blank!\n"
		else:
			#Once valid, return the input
			print "Label changed to " + newLabel
			return newLabel

#-----------------------------------------------------------------
# Function to select which current label to change
#-----------------------------------------------------------------			
def setCurrentLabels():
	currentLoop = False
	# Loop until Q
	while currentLoop == False:
		# Get all the current label keys
		currentKeys = currentLabels.keys()
		# Sort the keys alphabetically
		currentKeys.sort()
		# Loop through dictionary and display
		for entry in currentKeys:
			print entry, " - ", currentLabels[entry]
		#Get the label selection
		currentChoice = raw_input("Select label to change (Q to quit): ")
		# Verify selection and prompt the new label and set the label
		if currentChoice == 'J3':
			currentLabels['J3'] = currentInput(currentLabels[currentChoice])
		elif currentChoice == 'J6':
			currentLabels['J6'] = currentInput(currentLabels[currentChoice])
		elif currentChoice == 'J8':
			currentLabels['J8'] = currentInput(currentLabels[currentChoice])
		elif currentChoice == 'J10':
			currentLabels['J10'] = currentInput(currentLabels[currentChoice])
		elif currentChoice.upper() == 'Q':
			currentLoop = True
		else:
			print "Not a valid choice!\n"

#-----------------------------------------------------------------
# Function to toggle the status of the sensor from enable/disabled
#-----------------------------------------------------------------
def toggleSensor(tempName, tempValue):
	#If the state is enabled, toggle it to disabled
	if tempValue == "Enabled":
		print "Sensor " + tempName + " has been disabled.\n"
		return "Disabled"
	#if the state is disabled, toggle it to enabled	
	else:
		print "Sensor " + tempName + " has been enabled.\n"
		return "Enabled"

#-----------------------------------------------------------------
# Function to toggle current sensors between enabled and disabled
#-----------------------------------------------------------------
def currentEnDis():
	currentLoop = False
	#Loop until Q
	while currentLoop == False:
		#Get the current label keys
		currentKeys = currentLabels.keys()
		#Sort the keys and print the keys
		currentKeys.sort()
		for entry in currentKeys:
			print entry + "\t-\t" + currentLabels[entry] + "\t-\t" + currentStatus[entry]
		#Get the users key choice
		currentChoice = raw_input("Select thermocouple to toggle (Q to quit): ")
		#Based on selection, toggle the status of the current sensor	
		if currentChoice == 'J3':
			currentStatus['J3'] = toggleSensor(currentLabels[currentChoice], currentStatus[currentChoice])
		elif currentChoice == 'J6':
			currentStatus['J6'] = toggleSensor(currentLabels[currentChoice], currentStatus[currentChoice]) 	
		elif currentChoice == 'J8':
			currentStatus['J8'] = toggleSensor(currentLabels[currentChoice], currentStatus[currentChoice])
		elif currentChoice == 'J10':
			currentStatus['J10'] = toggleSensor(currentLabels[currentChoice], currentStatus[currentChoice])
		elif currentChoice.upper() == 'Q':
			currentLoop = True
		else:
			print "Not a valid choice!\n"

#-----------------------------------------------------------------
# Function to toggle the thermocouple sensors between enabled and disabled
#-----------------------------------------------------------------
def thermoEnDis():
	thermoLoop = False
	#Loop until Q
	while thermoLoop == False:
		#Get thermocouple keys
		thermoKeys = thermoLabels.keys()
		#Sort the keys
		thermoKeys.sort()
		#Print the dictionary information
		for entry in thermoKeys:
			print entry + "\t-\t" + thermoLabels[entry] + "\t-\t" + thermoStatus[entry]
		
		thermoChoice = raw_input("Select thermocouple to toggle (Q to quit): ")
		
		#Based on the selection, toggle the Thermocouple
		if thermoChoice == 'T0':
			thermoStatus['T0'] = toggleSensor(thermoLabels[thermoChoice], thermoStatus[thermoChoice])
		elif thermoChoice == 'T1':
			thermoStatus['T1'] = toggleSensor(thermoLabels[thermoChoice], thermoStatus[thermoChoice]) 	
		elif thermoChoice == 'T2':
			thermoStatus['T2'] = toggleSensor(thermoLabels[thermoChoice], thermoStatus[thermoChoice])
		elif thermoChoice == 'T3':
			thermoStatus['T3'] = toggleSensor(thermoLabels[thermoChoice], thermoStatus[thermoChoice])
		elif thermoChoice == 'T4':
			thermoStatus['T4'] = toggleSensor(thermoLabels[thermoChoice], thermoStatus[thermoChoice])
		elif thermoChoice == 'T5':
			thermoStatus['T5'] = toggleSensor(thermoLabels[thermoChoice], thermoStatus[thermoChoice])
		elif thermoChoice == 'T6':
			thermoStatus['T6'] = toggleSensor(thermoLabels[thermoChoice], thermoStatus[thermoChoice])
		elif thermoChoice == 'T7':
			thermoStatus['T7'] = toggleSensor(thermoLabels[thermoChoice], thermoStatus[thermoChoice])
		elif thermoChoice.upper() == 'Q':
			thermoLoop = True
		else:
			print "Not a valid choice!\n"	
			
#-----------------------------------------------------------------
# Function to change the thermocouple label
#-----------------------------------------------------------------
def thermoInput(tempChoice):
	validFlag = False
	#Loop until valid
	while validFlag == False:
		#prompt the user and get the input
		print "Selected " + tempChoice + " to change.  Please enter new label : "
		newLabel = raw_input()
		#Check for blank input
		if newLabel == '':
			print "Cannot be blank!\n"
		#Label valid, return the new label
		else:
			print "Label changed to " + newLabel
			return newLabel

#-----------------------------------------------------------------
# function to select the thermocouple labels
#-----------------------------------------------------------------
def setThermocoupleLables():
	thermoLoop = False
	#Loop until Q is chosen
	while thermoLoop == False:
		#Get the thermocouple keys
		thermoKeys = thermoLabels.keys()
		# Sort the thermocouple keys
		thermoKeys.sort()
		#Print the thermocouple dictionary
		for entry in thermoKeys:
			print entry, " - ", thermoLabels[entry]
		#Select the thermocouple label to change
		thermoChoice = raw_input("Select label to change (Q to quit): ")
		
		if thermoChoice == 'T0':
			thermoLabels['T0'] = thermoInput(thermoLabels[thermoChoice])
		elif thermoChoice == 'T1':
			thermoLabels['T1'] = thermoInput(thermoLabels[thermoChoice]) 	
		elif thermoChoice == 'T2':
			thermoLabels['T2'] = thermoInput(thermoLabels[thermoChoice])
		elif thermoChoice == 'T3':
			thermoLabels['T3'] = thermoInput(thermoLabels[thermoChoice])
		elif thermoChoice == 'T4':
			thermoLabels['T4'] = thermoInput(thermoLabels[thermoChoice])
		elif thermoChoice == 'T5':
			thermoLabels['T5'] = thermoInput(thermoLabels[thermoChoice])
		elif thermoChoice == 'T6':
			thermoLabels['T6'] = thermoInput(thermoLabels[thermoChoice])
		elif thermoChoice == 'T7':
			thermoLabels['T7'] = thermoInput(thermoLabels[thermoChoice])
		elif thermoChoice.upper() == 'Q':
			thermoLoop = True
		else:
			print "Not a valid choice!\n"
			
#-----------------------------------------------------------------
# Function to set the sample rate
#-----------------------------------------------------------------
def setSampleRate():
	#Bring in global variable
	global sampleRate
	validFlag = False
	#Loop until selection is valid
	while validFlag == False:
		#Prompt the user and get the user input
		print "Please enter a sample rate in milliseconds (10 is the minimum): "
		tempSample = raw_input()
		#Check to make sure it is a number
		if tempSample.isdigit() == False:
			print "Must be a number.\n"
		#Answer cannot be blank
		elif tempSample == '':
			print "Cannot be a blank input!\n"
		#Valid input	
		else:
			#If the input is less than 10 (min), then set it to minimum
			if tempSample <= 10:
				sampleRate = 10
				print "Sample rate set to 10ms\n"
				validFlag = True
			#If greater then min, set the value
			else:
				sampleRate = tempSample
				print "Sample rate set to " + sampleRate + "ms\n"
				validFlag = True
	
#-----------------------------------------------------------------
# Funtion to set the filename
#-----------------------------------------------------------------
def setFileName():
	#Bring in the global variable
	global filePath
	validFlag = False
	#Loop until the data is valid
	while validFlag == False:
		#Prompt the user and get the input
		print "Please enter a filename to store the data (no extension): "
		fileName = raw_input()
		#can't be blank
		if fileName == '':
			print "Cannot be a blank input!\n"
		#Can only be alphanumeric
		elif fileName.isalnum() == False:
			print "Can only be alphanumeric!\n"
		#Data is valid
		else:
			#Check to see if the file already exist
			tempPath = storagePath + fileName + fileExt
			if os.path.isfile(tempPath):
				print "File Already Exist.  Please use a different name.\n"
			#unique and can be set
			else:
				print "Valid file.  Path set to: " + tempPath + "\n"
				filePath = fileName
				validFlag = True

#-----------------------------------------------------------------
# Function to change the temperature unit
#-----------------------------------------------------------------
def unitChange():
	#Pull in global variables
	global temperatureUnit
	validFlag = False
	#Loop until Q
	while validFlag == False:
		#print the menu and get user response
		print "Please choose a unit for temperature: "
		print "C:\tCelsius"
		print "F:\tFahrenheit"
		print "B:\tBoth"
		print "Q:\tQuit"
		unitChoice = raw_input("Please select the unit: ")
		
		#Cannot be blank
		if unitChoice == '':
			print "Cannot be blank input!\n"
		#Not blank, check valid
		else:
			#Set the units
			if unitChoice.upper() == 'C':
				temperatureUnit = "C"
				print "Changed units to Celsius.\n"
			elif unitChoice.upper() == 'F':
				temperatureUnit = "F"
				print "Changed units to Fahrenheit.\n"
			elif unitChoice.upper() == 'B':
				temperatureUnit = "B"
				print "Changed units to Both.\n"
			elif unitChoice.upper() == 'Q':
				validFlag = True
			else:
				print "Not valid\n"

#-----------------------------------------------------------------
# Function to display all the settings that are being used for the test
#-----------------------------------------------------------------
def displayAllSettings():
	# Print the header
	print "-------------------------------------------------\n"
	print "Current Settings\n"
	print "-------------------------------------------------\n"
	
	#Filename
	print "Filepath: " + os.getcwd() + storagePath + filePath + fileExt + "\n"
	#Sample Rates
	print "Sample Rate: " + str(sampleRate) + "\n"
	#current sensors
	print "Current Sensors:"
	#Label, Net, Enable/Disable
	currentKeys = currentLabels.keys()
	for entry in currentKeys:
		print entry + "\t-\t" + currentLabels[entry] + "\t-\t" + currentStatus[entry]
	
	#thermocouple sensors
	print "\nThermocouple Sensors:"
	#channel, Label, Address, Enable/Disable
	thermoKeys = thermoLabels.keys()
	thermoKeys.sort()
	for entry in thermoKeys:
		print entry + "\t-\t" + thermoLabels[entry] + "\t-\t" + thermoAddress[entry] + "\t-\t" + thermoStatus[entry]
	
	#units
	print "\nTemperature Unit: " + temperatureUnit

#-----------------------------------------------------------------
# Function to return list of all the enabled current sensors
#-----------------------------------------------------------------
def getCurrentEnabled():
	# Get current keys
	currentKeys = currentLabels.keys()
	# Create blank list
	currentList = []
	# If the item is enabled, add it to the list
	for entry in currentKeys:
		if currentStatus[entry] == "Enabled":
			currentList.append(entry)
	# Return the list
	return currentList

#-----------------------------------------------------------------
# Function to return list of all the thermocouple sensors
#-----------------------------------------------------------------
def getThermoEnabled():
	# Get thermocouple keys
	thermoKeys = thermoLabels.keys()
	# Create blank list
	thermoList = []
	# If the item is enabled, add it to the list
	for entry in thermoKeys:
		if thermoStatus[entry] == "Enabled":
			thermoList.append(entry)
	# Return the list	
	return thermoList

#-----------------------------------------------------------------
# Function to return the temperature reading
#-----------------------------------------------------------------
def temp_raw(tempSensor):
	# Open Bus
	f = open(tempSensor, 'r')
	# Read response
	lines = f.readlines()
	# Close
	f.close()
	# Return data
	return lines
		

#-----------------------------------------------------------------
# Function to get data and convert it to a usable format
#-----------------------------------------------------------------		
def runDAQ():
	#Get all the current sensors that are valid
	for items in getCurrentEnabled():
		print items	
	#Get all the thermocouple sensors that are valid
	for items in getThermoEnabled():
		print items
	
	#Time
	print '|{:>16}| {:>5} | {:>5} | {:>5} | {:>5}'.format('Time (ms)', 'CS0', 'CS1', 'CS2', 'CS3')
	#Current Sensor
	#Setup DAQ
	#Setup display
	#0 | 1 | 2 | 3		0 | 1 | 2 | 3 | 4 | 5 | 6 | 7
	return
	
#-----------------------------------------------------------------
# Function to start the DAQ
#-----------------------------------------------------------------	
def startDAQ():
	# Print the header
	print "------------------------------------------------\n"
	print "Data Acquistion\n"
	print "------------------------------------------------\n"
	
	#Display the settings
	print "Settings: "
	displayAllSettings()
	validFlag = False
	#While choice isn't valid
	while validFlag == False:
		# Make sure the user wants to run the test
		print "\n Data acquistion will run until Ctrl+C is pressed. Press R to continue or Q to abort"
		menuInput = raw_input()
		# Check the input
		if menuInput.upper() == "R":
			print "Starting...."
			validFlag = True
		elif menuInput.upper() == "Q":
			print "Aborting..."
			validFlag = True
		else:
			print "Invalid input\n"
	# if R, run the test, or abort
	if menuInput.upper() == "R":		
		runDAQ()
	else:
		return

#-----------------------------------------------------------------
# Function to auto detect what sensors are valid
#-----------------------------------------------------------------		
def autoDetectSensors():
	# try to get values for thermocouples, if above range, set as disabled
	for sensors in getThermoEnabled():
		print tcStart + thermoAddress[sensors] + tcEnd
		lines = temp_raw(tcStart + thermoAddress[sensors] + tcEnd)
		while lines[0].strip()[-3:] != 'YES':
			time.sleep(0.2)
			lines = temp_raw(tcStart + thermoAddress[sensors] + tcEnd)
		temp_output = lines[1].find('t=')
		if temp_output != -1:
			temp_string = lines[1].strip()[temp_output+2]
			temp_c = float(temp_string) / 1000.0
			temp_f = temp_c * 9.0 / 5.0 + 32.0
		print temp_c, temp_f
		
	# try to get current sensor value, if out of range, disabled
	
	return

#-----------------------------------------------------------------
# Function to analyze the menu choice
#-----------------------------------------------------------------
def menuAnalysis(userChoice):
	if userChoice.upper() == 'F':
		setFileName()
	elif userChoice.upper() == 'R':
		setSampleRate()
	elif userChoice.upper() == 'T':
		setThermocoupleLables()
	elif userChoice.upper() == 'C':
		setCurrentLabels()
	elif userChoice.upper() == 'D':
		displayAllSettings()
	elif userChoice.upper() == 'S':
		startDAQ()
	elif userChoice.upper() == 'Q':
		print "Thanks!"
		sys.exit(0)
	elif userChoice.upper() == 'E':
		thermoEnDis()
	elif userChoice.upper() == 'M':
		print "Set modes"
	elif userChoice.upper() == 'N':
		currentEnDis()
	elif userChoice.upper() == 'U':
		unitChange()
	elif userChoice.upper() == 'A':
		autoDetectSensors()
	else:
		print "Not valid"

#handle ctrl+c press
signal.signal(signal.SIGINT, signal_handler)
		
#-----------------------------------------------------------------
# Function for the main menu
#-----------------------------------------------------------------
while (menuChoice.upper() != 'Q'):
		options = menu.keys()
		for entry in options:
			print entry, menu[entry]
			
		menuChoice = raw_input("Please Select: ")
		menuAnalysis(menuChoice)
		print "\n"