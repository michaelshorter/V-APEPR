import os
import time
import subprocess

subprocess.Popen(['firefox'])
time.sleep (30)

while True:
	os.system("xdotool key F5")
	time.sleep(60)
	print("Refresh complete")
