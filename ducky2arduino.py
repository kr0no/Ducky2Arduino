#!/usr/bin/python

import sys

if len(sys.argv) < 2 or len(sys.argv) > 3:
	print('Usage: ds2arduino.py input.file output.file')
	sys.exit()
	
input = sys.argv[1]
output = sys.argv[2]

try:
	input_file = open(input, "r")
except:
	print('File ' +sys.argv[1]+ ' not found')
	sys.exit()	
output_file = open(output, "w")

data = '#include "HID-Project.h"\n\nvoid setup() {\n	Keyboard.begin();\n	delay(500);\n\n	// Payload\n	'

for line in input_file:
	cmd = line.split(' ', 1)
	if cmd[0] == "REM":
		last_cmd = "// " + cmd[1].strip() + "\n	"
		data += last_cmd
	elif cmd[0] == "DELAY":
		last_cmd = "delay(" + cmd[1].strip() + ");\n	"
		data += last_cmd
	elif cmd[0] == "STRING":
		last_cmd = 'Keyboard.print("' + cmd[1].strip().replace('\"', '\\\"') + '");\n	'
		data += last_cmd
	elif cmd[0] == "GUI":
		last_cmd = "Keyboard.press(KEY_LEFT_GUI);\n	Keyboard.press(KEY_" + cmd[1].strip().upper() + ");\n	Keyboard.releaseAll();\n	"
		data += last_cmd
	elif cmd[0] == "MENU" or cmd[0] == "APP":
		last_cmd = "Keyboard.press(KEY_LEFT_SHIFT);\n	Keyboard.press(KEY_F10);\n	Keyboard.releaseAll();\n	"
		data += last_cmd
	elif cmd[0] == "ALT":
		last_cmd = "Keyboard.press(KEY_LEFT_ALT);\n	Keyboard.press(KEY_" + cmd[1].strip().upper() + ");\n	Keyboard.releaseAll();\n	"
		data += last_cmd
	elif cmd[0] == "CONTROL" or cmd[0] == "CTRL":
		last_cmd = "Keyboard.press(KEY_LEFT_CTRL);\n	Keyboard.press(KEY_" + cmd[1].strip().upper() + ");\n		Keyboard.releaseAll();\n	"
		data += last_cmd
	elif cmd[0].strip() == "ENTER":
		last_cmd = "Keyboard.write(KEY_ENTER);\n	"
		data += last_cmd
	elif cmd[0].strip() == "UP" or cmd[0].strip() == "UPARROW":
		last_cmd = "Keyboard.write(KEY_UP); \n	"
		data += last_cmd
	elif cmd[0].strip() == "DOWN" or cmd[0].strip() == "DOWNARROW":
		last_cmd = "Keyboard.write(KEY_DOWN); \n	"
		data += last_cmd
	elif cmd[0].strip() == "LEFT" or cmd[0].strip() == "LEFTARROW":
		last_cmd = "Keyboard.write(KEY_LEFT); \n	"
		data += last_cmd
	elif cmd[0].strip() == "RIGHT" or cmd[0].strip() == "RIGHTARROW":
		last_cmd = "Keyboard.write(KEY_RIGHT); \n	"
		data += last_cmd
	elif cmd[0].strip() == "SPACE":
		last_cmd = "Keyboard.write(KEY_SPACE); \n	"
		data += last_cmd
	elif cmd[0].strip() == "TAB":
		last_cmd = "Keyboard.write(KEY_TAB); \n	"
		data += last_cmd
	elif cmd[0].strip() == "HOME":
		last_cmd = "Keyboard.write(KEY_HOME); \n	"
		data += last_cmd
	elif cmd[0] == "REPEAT" or cmd[0] == "REPLAY":
		last_cmd = "for (int i=0; i<" + cmd[1] + "; i++) {\n		" + last_cmd + "}\n	"
		data += last_cmd
		
data += '}\n\nvoid loop() { }\n'
output_file.write(data)
print('Payload saved to ' + sys.argv[2])

input_file.close()
output_file.close()