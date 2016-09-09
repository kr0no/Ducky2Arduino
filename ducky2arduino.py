#!/usr/bin/python

import sys

if len(sys.argv) < 2 or len(sys.argv) > 3:
	print('Usage: ds2arduino.py input.file output.file')
	sys.exit()
	
input = sys.argv[1]
output = sys.argv[2]

data = '#include "HID-Project.h"\n\nvoid setup(){\n	Keyboard.begin();\n	delay(500);\n	'

try:
	input_file = open(input, "r")
except:
	print('File ' +sys.argv[1]+ ' not found')
	sys.exit()
	
output_file = open(output, "w")

for line in input_file:
	cmd = line.split(' ', 1)
	if cmd[0] == "REM":
		data += ("// " + cmd[1].strip() + "\n	") 
	elif cmd[0] == "DELAY":
		data += ("delay(" + cmd[1].strip() + ");\n	")
	elif cmd[0] == "STRING":
		data += ("Keyboard.print('" + cmd[1].strip().replace('\'', '\\\'') + "');\n	")
	elif cmd[0] == "GUI":
		data += ("Keyboard.press(KEY_LEFT_GUI);\n	Keyboard.press(KEY_" + cmd[1].strip().upper() + ");\n	Keyboard.releaseAll();\n	")
	elif cmd[0] == "MENU" or cmd[0] == "APP":
		data += ("Keyboard.press(KEY_LEFT_SHIFT);\n	Keyboard.press(KEY_F10);\n	Keyboard.releaseAll();\n	")
	elif cmd[0] == "ALT":
		data += ("Keyboard.press(KEY_LEFT_ALT);\n	Keyboard.press(KEY_" + cmd[1].strip().upper() + ");\n	Keyboard.releaseAll();\n	")
	elif cmd[0] == "CONTROL" or cmd[0] == "CTRL":
		data += ("Keyboard.press(KEY_LEFT_CTRL);\n	Keyboard.press(KEY_" + cmd[1].strip().upper() + ");\n		Keyboard.releaseAll();\n	")
	elif cmd[0].strip() == "ENTER":
		data += ("Keyboard.write(KEY_ENTER);\n	")

data += '}\n\nvoid loop() {}\n'
output_file.write(data)
print('Payload saved to ' + sys.argv[2])

input_file.close()
output_file.close()